import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error
from datetime import datetime

def get_config(domain):
    db = mysql.connector.connect(
        host="host",
        user="user",
        password="password",
        database="db_name"
    )

    curs = db.cursor()

    sql = "SELECT * FROM token.amo_auth_service WHERE domain = %s"
    param = (domain, )
    curs.execute(sql, param)
    result = curs.fetchall()

    for x in result:
      print(x)
    print("len = ", len(result))
    if result != []:
        return result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], result[0][7], result[0][8]
    else:
        return  None,None,None,None,None, None, None

class db_config:
    def __init__(self, domain):
        self.domain = domain
        client_id, client_secret,redirect_uri, refresh_token, access_token, expires_in, timestamp = get_config(domain)
        self.client_id = client_id
        self.client_secret=client_secret
        self.redirect_uri=redirect_uri
        self.refresh_token=refresh_token
        self.access_token=access_token
        self.expires_in=expires_in
        self.timestamp=timestamp

    def add_account(self, domain, client_id, client_secret, redirect_uri, refresh_token, access_token, expires_in):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.expires_in = expires_in
        db = mysql.connector.connect(

            host="206.189.224.185",
            user="Salesautomators_user",
            password="&S%9A8p58Wo5",
            database="token"
        )

        curs = db.cursor()
        now = datetime.now()
        sql = f"INSERT INTO token.amo_auth_service (domain, client_id, client_secret, redirect_uri, refresh_token, access_token, expires_in, timestamp)" \
                   f"VALUES ( %s, %s, %s, %s, %s, %s, %s,%s);"

        val = (domain, client_id, client_secret, redirect_uri, refresh_token, access_token, expires_in, now, )
        curs.execute(sql, val)

        db.commit()

        print(curs.rowcount, "record inserted.")
    def update_db(self):
        db = mysql.connector.connect(

            host="206.189.224.185",
            user="Salesautomators_user",
            password="&S%9A8p58Wo5",
            database="token"
        )

        curs = db.cursor()
        sql = 'UPDATE token.amo_auth_service SET refresh_token=%s,access_token=%s,expires_in=%s, timestamp=%s  where domain =%s;'


        val = ( self.refresh_token, self.access_token, self.expires_in, self.timestamp,self.domain )
        curs.execute(sql, val)

        db.commit()

        print(curs.rowcount, "record updated.")



