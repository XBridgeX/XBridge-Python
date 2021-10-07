import uuid
import json

def GetSendTextPack(t):
    p = {}
    p['type'] = 'pack'
    p['action'] = "sendtext"
    p['params'] = {'text':t,'id':uuid.uuid1()}
    return json.dumps(p)

def GetRuncmdPack(cmd,id):
    p = {}
    p['type'] = 'pack'
    p['action'] = "runcmdrequest"
    p['params'] = {'cmd':cmd,'id':id}
    return json.dumps(p)
