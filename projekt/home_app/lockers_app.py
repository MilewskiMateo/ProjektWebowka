import logging
import os
import json

import redis

from model.waybill import *
from const import *
from flask import Flask,abort, request, session, render_template, render_template, make_response, jsonify, redirect, url_for, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import hashlib


FILES_PATH = "waybill_files/"
SHIP_TIME = 'time_of_creation'
FILENAMES = "filenames"

SHIP_STATUS="ship_status"
STATUS_NEW = "new"
STATUS_WAITING = "waiting"
STATUS_PICKED_UP = "picked up"
STATUS_COURIER = "courier"



app = Flask(__name__, static_url_path="")
log = app.logger
db = redis.Redis(host="redis-db", port=6379, decode_responses=True)

app.secret_key =  os.environ.get(SESSION_SECRET_KEY)

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config["JWT_SECRET_KEY"] = os.environ.get(SECRET_KEY)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = TOKEN_EXPIRES_IN_SECONDS
app.config["PERMANENT_SESSION_LIFETIME"] = 300

jwt = JWTManager(app)

def noJWTPage(error):
    return render_template("/errors/401.html")

jwt.unauthorized_loader(noJWTPage)

def setup():
    log.setLevel(logging.DEBUG)




@app.route('/',methods=[GET])
def home():
    return render_template('/lockers/index.html')

@app.route('/pick-up',methods=[GET])
def pick():
    return render_template('/lockers/pick-up.html')

@app.route('/post-it',methods=[GET])
def post():
    if(request.args.get('wrong')=='1'):
        return render_template('/lockers/post-it.html',wrong=True)
    elif(request.args.get('status_wrong')=='1'):
        return render_template('/lockers/post-it.html',status_wrong=True)
    else:    
        return render_template('/lockers/post-it.html')

@app.route('/post-it/send',methods=[POST])
def sendPost():
    lockerId = request.form.get('lockerId')
    shipId = request.form.get('shipId')
    if db.exists(shipId) and db.exists(lockerId):
        ship = json.loads(db.get(shipId))
        if ship[SHIP_STATUS] == STATUS_NEW:
            ship[SHIP_STATUS] = STATUS_WAITING
            db.set(shipId,json.dumps(ship))
            db.lpush(db.hget(lockerId,'Nadane'),shipId) 
            return redirect(url_for('home'))
        else:
            return redirect(url_for('post',status_wrong=1))
    else:
        return redirect(url_for('post',wrong=1))


@app.route('/storage',methods=[GET])
def storage():
    if(request.args.get('wrong')=='1'):
        return render_template('/lockers/storage.html',wrong=True)
    else:    
        return render_template('/lockers/storage.html')

@app.route('/storage/list',methods=[GET])
def storageList():
    timeToken = request.args.get('timeToken')
    lockerId = request.args.get('lockerId')
    if db.exists(lockerId) and db.exists(lockerId+'TimeToken'):
        timeToken_dict = json.loads(str(db.get(lockerId + 'TimeToken')))
        if (timeToken_dict['TimeToken'] == timeToken):

            courier_Id = timeToken_dict['UserId']
            first_index = request.args.get('from', default = 0, type = int)
            last_index = request.args.get('to', default = 2, type = int)
            waiting_list = db.hget(lockerId,'Nadane')
            full_lenght = db.llen(waiting_list)
            files = db.lrange(waiting_list, first_index, last_index)
            next_page=''
            prev_page=''
            if(last_index<full_lenght-1):
                next_page = request.path +'?timeToken='+timeToken+'&lockerId='+lockerId+ "&from="+ str(last_index + 1) + "&to=" + str(last_index + 3)
            if(first_index>0):
                prev_page = request.path +'?timeToken='+timeToken+'&lockerId='+lockerId+ "&from="+ str(first_index - 3)+ "&to=" + str(first_index -1)

            my_ships = []
            for r in files:
                new_row = json.loads(db.get(r))
                my_ships.append(new_row)

            response = make_response(render_template("/lockers/storage-list.html",  my_ships=my_ships, numberOfShips=full_lenght,  nextPage = next_page , prevPage = prev_page,courier_Id = courier_Id,locker_Id= lockerId))
            return response
        return redirect(url_for('storage',wrong=1))
    else:
        return redirect(url_for('storage',wrong=1))

@app.route('/storage/pick',methods=[POST])
def storagePickUp():
    
    picked_list = request.form.getlist('checkboxes')
    courier_id = request.form.get("courier_id")
    locker_Id = request.form.get("locker_id")
    log.error(picked_list)
    for shipId in picked_list:
        ship = json.loads(db.get(shipId))
        log.error(ship)
        ship[SHIP_STATUS] = STATUS_PICKED_UP
        db.set(shipId,json.dumps(ship))
        db.lpush(courier_id+"CourierShips",shipId)
        db.lrem(db.hget(locker_Id,'Nadane'),0,shipId) 

    return redirect(url_for('home')) 


############## pomocnicze ##########################


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
