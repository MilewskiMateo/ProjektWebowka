import logging
import os
import json
import uuid
import hashlib
import redis

from const import *
from flask import Flask,abort, request, session, render_template, render_template, make_response, jsonify, redirect, url_for, send_file

app = Flask(__name__, static_url_path="")
log = app.logger
db = redis.Redis(host="redis-db", port=6379, decode_responses=True)

app.secret_key =  os.environ.get(SESSION_SECRET_KEY)
app.config["PERMANENT_SESSION_LIFETIME"] = 300

SHIP_STATUS="ship_status"
STATUS_NEW = "new"
STATUS_WAITING = "waiting"
STATUS_PICKED_UP = "picked up"
STATUS_COURIER = "courier"


def setup():
    log.setLevel(logging.DEBUG)


@app.route('/',methods=[GET])
def home():
    return render_template('/couriers/index.html')



@app.route('/token',methods=[GET])
def token():
    if 'Courierlogin' in session:
        login_hash = session['Courierlogin']

        if not (refresh_session_timer(login_hash)):
            return redirect(url_for('login'))

        if(request.args.get('wrong')== '1'):
            return render_template('/couriers/token.html',wrong=True)
        elif(request.args.get('timeToken')):
            return render_template('/couriers/token.html',timeToken=request.args.get('timeToken'))
        else:    
            return render_template('/couriers/token.html')
    else:
        return redirect(url_for('login'))


@app.route('/token/generate',methods=[POST])
def generate():
    if 'Courierlogin' in session:
        login_hash = session['Courierlogin']

        if not (refresh_session_timer(login_hash)):
            return redirect(url_for('login'))

        lockerId=request.form.get('lockerId')

        if(db.exists(lockerId)):
            time_token = uuid.uuid4().hex[0:10]

            my_dict = {'UserId' : login_hash, 'TimeToken': time_token}
            my_json = json.dumps(my_dict)
            db.set(lockerId+"TimeToken",my_json)
            db.expire(lockerId+"TimeToken",60)

            return redirect(url_for('token',timeToken=time_token))

        return redirect(url_for('token',wrong=1))
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=["GET"])
def login():
    return render_template("/couriers/login.html")


@app.route("/login/log", methods=["POST"])
def loginRequest():
    login_hash = hashlib.sha512(request.form['login'].encode("utf-8")).hexdigest()
    password_hash = hashlib.sha512( request.form['password'].encode("utf-8")).hexdigest()
    if(db.exists(login_hash)):
        if(db.hget(login_hash, 'password') == password_hash and db.hget(login_hash, 'isAdmin')== 'True'):
            response = make_response(redirect(url_for('home')))
            session['Courierlogin'] = login_hash
            session.permanent = True

            db.set(login_hash + "Session","true")
            db.expire(login_hash + "Session",TOKEN_EXPIRES_IN_SECONDS)

            return response
        else:
            return jsonify({"responseMessage": "Dane logowania niepoprawne"}), 201

    else:
        return jsonify({"responseMessage": "Dane logowania niepoprawne"}), 201


@app.route("/logout", methods=["GET"])
def logout():
    db.expire(session['Courierlogin'] + "Session",1)
    session.clear()
    return redirect(url_for('login'))



@app.route('/pick-up',methods=[GET])
def pickUp():
    if 'Courierlogin' in session:
        login_hash = session['Courierlogin']

        if not (refresh_session_timer(login_hash)):
            return redirect(url_for('login'))

        if(request.args.get('wrong')=='1'):
            return render_template('/couriers/pick-up.html',wrong=True)
        elif(request.args.get('status_wrong')=='1'):
            return render_template('/couriers/pick-up.html',status_wrong=True)
        else:    
            return render_template('/couriers/pick-up.html')
    else:
        return redirect(url_for('login'))


@app.route('/pick-up/pick', methods=[POST])
def pick():
    if 'Courierlogin' in session:
        login_hash = session['Courierlogin']

        if not (refresh_session_timer(login_hash)):
            return redirect(url_for('login'))    

        shipId = request.form.get('shipId')
        if db.exists(shipId):
            ship = json.loads(db.get(shipId))
            if ship[SHIP_STATUS] == STATUS_NEW:
                ship[SHIP_STATUS] = STATUS_COURIER
                db.set(shipId,json.dumps(ship))
                db.lpush(login_hash + 'CourierShips',shipId) 
                return redirect(url_for('home'))
            else:
                return redirect(url_for('pickUp',status_wrong=1))
        else:
            return redirect(url_for('pickUp',wrong=1))
    else:
        return redirect(url_for('login'))

@app.route('/my-ships',methods=[GET])
def myShips():
    if 'Courierlogin' in session:
        login_hash = session['Courierlogin']

        if not (refresh_session_timer(login_hash)):
            return redirect(url_for('login'))

        if db.exists(login_hash):

            first_index = request.args.get('from', default = 0, type = int)
            last_index = request.args.get('to', default = 2, type = int)
            courier_ships_id = login_hash+'CourierShips'
            full_lenght = db.llen(courier_ships_id)
            files = db.lrange(courier_ships_id, first_index, last_index)
            next_page=''
            prev_page=''
            if(last_index<full_lenght-1):
                next_page = request.path + "?from="+ str(last_index + 1) + "&to=" + str(last_index + 3)
            if(first_index>0):
                prev_page = request.path + "?from="+ str(first_index - 3)+ "&to=" + str(first_index -1)

            my_ships = []
            for r in files:
                new_row = json.loads(db.get(r))
                my_ships.append(new_row)

            response = make_response(render_template("/couriers/my-ships.html",  my_ships=my_ships, numberOfShips=full_lenght,  nextPage = next_page , prevPage = prev_page))
            return response

        else:
            abort(403)

    else:
        return redirect(url_for('login'))


@app.route("/offline")
def offline():
    return render_template("couriers/offline.html")


@app.route("/error")
def error():
    return render_template("couriers/error.html")


@app.route("/service-worker.js")
def service_worker():
    return app.send_static_file("service-worker.js")




############## pomocnicze ##########################

def refresh_session_timer(login_hash):
    if(db.exists(login_hash+"Session")):
        db.expire(login_hash + "Session",TOKEN_EXPIRES_IN_SECONDS)
        return True
    else:
        return False


@app.errorhandler(400)
def page_bad_request(error):
    return render_template("errors/400.html", error=error)
    
@app.errorhandler(401)
def page_unauthorized(error):
    return render_template("errors/401.html", error=error)

@app.errorhandler(403)
def page_forbidden(error):
    return render_template("errors/403.html", error=error)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html", error=error)


@app.errorhandler(500)
def page_server_err(error):
    return render_template("errors/500.html", error=error)
