import AES
import uuid
import json

def GetSendTextPack(k,iv,t):
    p = {}
    p['type'] = 'pack'
    p['action'] = "sendtext"
    p['params'] = {'text':t,'id':uuid.uuid1()}
    return AESEncrypt(k,iv,json.dumps(p))

def GetRuncmdPack(k,iv,cmd,id):
    p = {}
    p['type'] = 'pack'
    p['action'] = "runcmdrequest"
    p['params'] = {'cmd':cmd,'id':id}
    return AESEncrypt(k,iv,json.dumps(p))

def AESEncrypt(k,iv,pack):
    p = {}
    p['type'] = 'encrypt'
    p['params'] = {
        'raw' : AES.AES_Encrypt(k,iv,pack),
        'mode': "aes_cbc_pck7padding"
    }
    return json.dumps(p)