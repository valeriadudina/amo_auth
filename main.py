import requests
from flask import Flask, request
import json
import random
from DataBase import db_config
from AmoHandler import initial_auth, refresh
from datetime import datetime, timedelta
app = Flask(__name__)

@app.route('/add_new_company', methods=['POST'])
def add_new_company():
    data = request.get_json()
    print(data)
    db = db_config(data.get('domain'))
    if db.client_id and db.client_secret and db.access_token:
        if db.timestamp + timedelta(seconds=db.expires_in) < datetime.now():
            refresh_response = refresh(db)
            if refresh_response != "400":
                db.access_token = refresh_response.get('access_token')
                db.expires_in = refresh_response.get('expires_in')
                db.refresh_token = refresh_response.get('refresh_token')
                db.timestamp = datetime.now()
                db.update_db()
                return json.dumps({"token": db.access_token, "note":"This company has token"})
            else:
                return json.dumps({ "note":"This company has token", "success":False, "reason":"smth went wrong"})
        else:
            return json.dumps({"token": db.access_token, "note": "This company has token"})
    else:
        expires_in, access_token, refresh_token = initial_auth(data.get('domain'), data.get('client_id'), data.get('client_secret'), data.get('code'), data.get('redirect_uri'))
        print("refresh = ", refresh_token)
        print('access = ', access_token)

        db.add_account(data.get('domain'), data.get("client_id"), data.get('client_secret'), data.get('redirect_uri'), refresh_token,access_token, expires_in)
        print(db)

        return json.dumps({"token":db.access_token})

@app.route('/get_token', methods=['GET'])
def get_token():
    args = request.args
    print(args.get('domain'))
    db = db_config(args.get('domain'))
    print(db.access_token)
    print(vars(db))
    print(type(db.timestamp))

    if db.timestamp + timedelta(seconds=db.expires_in) > datetime.now():
        refresh_response = refresh(db)
        if refresh_response!="400":
            db.access_token = refresh_response.get('access_token')
            db.expires_in = refresh_response.get('expires_in')
            db.refresh_token = refresh_response.get('refresh_token')
            db.timestamp = datetime.now()
            db.update_db()
            return json.dumps({"token":db.access_token})
        else:
           return "smth went wrong"


    else:
        print('return only')
        return json.dumps({'token':db.access_token})

if __name__=="__main__":
    app.run(port=3000)