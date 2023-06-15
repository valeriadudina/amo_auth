import json
import requests
from DataBase import db_config
def initial_auth(domain, client_id,client_secret, code, redirect_uri):
    url = f"https://{domain}/oauth2/access_token"
    print(url)
    data =json.dumps({
      "client_id": client_id,
      "client_secret": client_secret,
      "grant_type": "authorization_code",
      "code": code,
      "redirect_uri": redirect_uri
    })
    print(data)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=data)
    print(response)
    if response.status_code==200:
        resp_json = json.loads(response.text)
        print(resp_json)
        return resp_json.get('expires_in'), resp_json.get('access_token'), resp_json.get('refresh_token')
    else:
        return response.status_code,response.text , response


def refresh(db):
    url = f"https://{db.domain}/oauth2/access_token"
    print(url)
    data = json.dumps({
  "client_id": db.client_id,
  "client_secret": db.client_secret,
  "grant_type": "refresh_token",
  "refresh_token":db.refresh_token,
  "redirect_uri": db.redirect_uri
})
    print(data)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=data)
    print(response.text)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        return "400"