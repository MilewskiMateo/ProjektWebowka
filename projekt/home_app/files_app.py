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


@app.route("/waybill/<string:waybill_hash>", methods=[GET])
@jwt_required
def download_waybill(waybill_hash):

    filename = waybill_hash + ".pdf"
    if not (db.exists(waybill_hash)):
        abort(400)
    my_dict = json.loads(db.get(waybill_hash))
    fullname = "{}{}.pdf".format(FILES_PATH, waybill_hash)

    if not os.path.isfile(fullname):
        waybill = to_waybill(my_dict)

        if os.path.isfile(FILES_PATH + waybill_hash + ".png"):
            waybill.generate_and_save(
                fullname, photo_path=FILES_PATH + waybill_hash + ".png")
        elif os.path.isfile(FILES_PATH + waybill_hash + ".jpg"):
            waybill.generate_and_save(
                fullname, photo_path=FILES_PATH + waybill_hash + ".jpg")
        elif os.path.isfile(FILES_PATH + waybill_hash + ".jpeg"):
            waybill.generate_and_save(
                fullname, photo_path=FILES_PATH + waybill_hash + ".jpeg")
        else:
            waybill.generate_and_save(fullname)

    if fullname is not None:
        try:
            return send_file(fullname, attachment_filename=filename)
        except Exception as e:
            log.error(e)

    return filename, 200


############## pomocnicze ##########################

def to_waybill(dict):
    sender_dict = {}
    recipient_dict = {}

    for key in dict:
        if("sender" in key):
            sender_dict[key] = dict[key]
        else:
            recipient_dict[key] = dict[key]

    sender = to_sender(sender_dict)
    recipient = to_recipient(recipient_dict)

    return Waybill(sender, recipient)


def to_sender(form):
    name = form['sender_name']
    surname = form['sender_surname']
    telephone = form['sender_telephone']
    address = Address(form['sender_street'], form['sender_nr'],
                      form['sender_postal'], form['sender_country'])

    return Person(name, surname, telephone, address)


def to_recipient(form):
    name = form['name']
    surname = form['surname']
    telephone = form['telephone']
    address = Address(form['street'], form['nr'],
                      form['postal'], form['country'])

    return Person(name, surname, telephone, address)


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
