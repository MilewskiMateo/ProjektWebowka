import logging
import os
import uuid
import glob

import redis
import json


from datetime import datetime, timedelta
from const import *
from flask import Flask, session, request, render_template, render_template, make_response, jsonify, redirect, url_for, send_file,abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,set_access_cookies,unset_jwt_cookies

import hashlib

app = Flask(__name__, static_url_path="")
log = app.logger
db = redis.Redis(host="redis-db", port=6379, decode_responses=True)

app.secret_key = "any random string"

FILES_PATH = "waybill_files/"
SHIP_TIME = 'time_of_creation'
FILENAMES = "filenames"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
SHIP_PATH_AND_FILENAME = "path_and_filename"

SHIP_STATUS="ship_status"
STATUS_NEW = "new"
STATUS_WAITING = "waiting"
STATUS_PICKED_UP = "picked up"
STATUS_COURIER = "courier"


app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config["JWT_SECRET_KEY"] = os.environ.get(SECRET_KEY)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES_IN_SECONDS
app.config["PERMANENT_SESSION_LIFETIME"] = TOKEN_EXPIRES_IN_SECONDS
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)



def setup():
    log.setLevel(logging.DEBUG)


@app.route("/", methods=["GET"])
def home():
    isLoggedIn = 'login' in session
    if(isLoggedIn):
        refresh_session_timer(session['login'])
    response = make_response( render_template("/main/home.html", isLoggedIn=isLoggedIn))
    responseWithCoockie = my_refresh_coockie(response,request)
    return responseWithCoockie

@app.route("/init-db", methods=["GET"])
def init_db():
    if not db.exists('paczkomaty'):
        db.rpush('paczkomaty','paczkomat1')
        db.hmset('paczkomat1', {'Nadane':'H7fJYnvuKD','Oczekujace':'24W37G2hqj'})

        db.rpush('paczkomaty','paczkomat2')
        db.hmset('paczkomat2', {'Nadane':'UqrEm9vYhl','Oczekujace':'tJEpFY3uo6'})

        db.rpush('paczkomaty','paczkomat3')
        db.hmset('paczkomat3', {'Nadane':'cgUTcAqIn0','Oczekujace':'VyCOZB6SSY'})
        # Admin1
        # slomianykapelusz25!
        db.hmset('43192475f95e3820fe441daaff7c84d9b73ca3a5afc7309ae03f783151b6b0976e4d68cd990f97ad0d65ca640d35a407199d6d7510f1dff5477b8cfce1531475', {'login' : 'Admin1','password':'6d5979138541e0dc037223cd76c27486123bb60f3a4c60fc775d693eb7ab7a878f917d7a80a3fa465e985d5301311a3ada17490229195b1e864697937404f9de','isAdmin': 'True'})
        # Admin2
        # NieodpowiedzialneHaslo123
        db.hmset('f08bf04ffe5c88a8961792dd8de4442c6b9bcee2bd89a41d54bdd6eae0e9d201af5c12921f72a147636f9493ef4b6448608316b3a9a962b1b8df2fb06f1f6743', {'login' : 'Admin2','password':'66057699b2511dcb53a881952cd804272dac7d7fdbef07e0b76724e9a8fc5e8401f0d166e0bd9d9f795d500f9da278bc893c99a4062ae740ba23a4262a48b234','isAdmin': 'True'})
        # Admin3
        # MojPiesJestSuper
        db.hmset('2dc8bb50a33631f46a9ac411cc45c650b925f1f0d1181740b79446d00058290c6b4dd8fee7d05a518975eb57781b7cac657d279353314da1cdee4528a5904305', {'login' : 'Admin3','password':'6f6520888a159fc92d4b3cc475bca5ccd63232dff89dcdd70a1927f8cfa91e65fa1fc60ed5d712cb504d51c056c24da65b4344577a2f3f93138ae61fdbc2f7ca','isAdmin': 'True'})

        return ('', 204)
    return('',204)


@app.route("/registration", methods=["GET"])
def register():
    isLoggedIn = 'login' in session
    if(isLoggedIn):
        refresh_session_timer(session['login'])
    response = make_response( render_template("/main/registration.html", isLoggedIn=isLoggedIn))
    responseWithCoockie = my_refresh_coockie(response,request)
    return responseWithCoockie


@app.route("/registration/register", methods=["POST"])
def addUser():
    login = request.form['login']
    login_hash = hashlib.sha512(login.encode("utf-8")).hexdigest()
    if(db.exists(login_hash)):
        return jsonify({"responseMessage": "Użytkownik o takim loginie już istnieje"}), 201
    else:
        myDict = request.form.to_dict()
        myDict['password'] = hashlib.sha512(
            myDict['password'].encode("utf-8")).hexdigest()
        del myDict['second_password']

        db.hmset(login_hash, myDict)
        return redirect(url_for("home"))


@app.route("/login", methods=["GET"])
def login():
    return render_template("/main/login.html")


@app.route("/login/log", methods=["POST"])
def loginRequest():
    login = request.form['login']
    password_hash = hashlib.sha512(
        request.form['password'].encode("utf-8")).hexdigest()
    login_hash = hashlib.sha512(login.encode("utf-8")).hexdigest()
    if(db.exists(login_hash)):
        if(db.hget(login_hash, 'password') == password_hash):
            response = make_response(redirect(url_for('home')))
            session['login'] = login_hash
            session.permanent = True

            access_token = create_access_token(identity=login_hash)
            
          
            set_access_cookies(response, access_token,TOKEN_EXPIRES_IN_SECONDS)

            db.set(login_hash + "Session","true")
            db.expire(login_hash + "Session",TOKEN_EXPIRES_IN_SECONDS)


            return response
        else:
            return jsonify({"responseMessage": "Dane logowania niepoprawne"}), 201

    else:
        return jsonify({"responseMessage": "Dane logowania niepoprawne"}), 201




@app.route("/logout", methods=["GET"])
def logout():
    db.expire(session['login'] + "Session",1)
    session.clear()
    response = make_response(render_template("/main/home.html"))
    unset_jwt_cookies(response)
    return response


@app.route("/checkLogin/<login>", methods=["GET"])
def download_waybill(login):
    login_hash = hashlib.sha512(login.encode("utf-8")).hexdigest()
    if(db.exists(login_hash)):
        return make_response('available' + login_hash, 200)
    else:
        return make_response('not available ', 404)


@app.route("/new_ship/add", methods=["POST"])
def new_ship_add():
    if 'login' in session:
        login_hash = session['login']

        if not (refresh_session_timer(login_hash)):
            return redirect("https://localhost:8080/login")

        if(db.exists(login_hash)):
            unique_filename = uuid.uuid4().hex
            ship_photo = request.files['file-input']

            if ship_photo and allowed_file(ship_photo.filename):
                ship_photo.save(FILES_PATH + unique_filename + '.' +
                                ship_photo.filename.rsplit('.', 1)[1].lower())

            myDict = request.form.to_dict()
            now_time = str(datetime.now() + timedelta(hours=1))[:-7]
            myDict[SHIP_TIME] = now_time
            myDict[SHIP_STATUS] = STATUS_NEW
            myDict[SHIP_PATH_AND_FILENAME] = unique_filename

            db.rpush(login_hash + "Ships", unique_filename)

            db.set(unique_filename, json.dumps(myDict))

            return jsonify({"responseMessage": "Udalo sie"})
        else:
            return redirect("https://localhost:8080/login")
    else:
        return redirect("https://localhost:8080/login")
        

@app.route("/ships", methods=["GET"])
def ships():
    if 'login' in session:
        login_hash = session['login']

        if not (refresh_session_timer(login_hash)):
            return redirect("https://localhost:8080/login")

        first_index = request.args.get('from', default = 0, type = int)
        last_index = request.args.get('to', default = 2, type = int)
        full_lenght = db.llen(login_hash+"Ships")
        files = db.lrange(login_hash+"Ships", first_index, last_index)
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

        response = make_response(render_template("/main/ships.html", isLoggedIn=True, my_ships=my_ships, numberOfShips=full_lenght,  nextPage = next_page , prevPage = prev_page))
        responseWithCoockie= my_refresh_coockie(response,request)
        return responseWithCoockie
    else:
        return redirect("https://localhost:8080/login")



@app.route("/ships/delete", methods=["DELETE"])
def delete_ship():
    if 'login' in session:
        login_hash = session['login']

        if not (refresh_session_timer(login_hash)):
            return redirect("https://localhost:8080/login")
        
        waybill_hash = request.args.get('id',type = str)
        remove_file(waybill_hash)
        db.delete(waybill_hash)
        db.lrem(login_hash+"Ships",0,waybill_hash)

        return redirect(url_for("ships"))
    else:
        return redirect("https://localhost:8080/login")


@app.route("/new_ship", methods=["GET"])
def new_ship():
    if 'login' in session:
        login_hash = session['login']

        if not (refresh_session_timer(login_hash)):
            return redirect("https://localhost:8080/login")

        if(db.exists(login_hash)):
            response = make_response(render_template("/main/new_ship.html", isLoggedIn=True))
            responseWithCoockie = my_refresh_coockie(response,request)
            return responseWithCoockie
    else:
        return redirect("https://localhost:8080/login")


################### pomocnicze #############################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def refresh_session_timer(login_hash):
    if(db.exists(login_hash+"Session")):
        db.expire(login_hash + "Session",TOKEN_EXPIRES_IN_SECONDS)
        return True
    else:
        return False


def my_refresh_coockie(response,request):
    if(request.cookies.get('access_token_cookie')):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        set_access_cookies(response, access_token,TOKEN_EXPIRES_IN_SECONDS)
        return response
    else:
        return response
        
def remove_file(waybill_hash):
    files =  glob.glob('waybill_files/'+waybill_hash+'*')
    for f in files:
        try:
            os.remove(f)
        except FileNotFoundError as e:
            print("Error: %s : %s" % (f, e.strerror))


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