import asyncio
import os
import sys
import websockets
import Utils.AES as AES
import Utils.MD5 as MD5
import json
import Utils.PackHelper as PHelper
import _thread

password = "pwd"
url = "ws://127.0.0.1:8080"
ws = None

file_object = open('./data/config.json') 
try:
    file_context = file_object.read()
    cfg = json.loads(file_context)
    password = cfg['password']
    url = cfg['ws']
finally:
    file_object.close()


k = MD5.Encrypt(password)[0:16]
vi = MD5.Encrypt(password)[16:32]
runcmdid = {}

print(f"您的AES密匙为：{k},偏移量为：{vi}")

def AESEncrypt(k,iv,pack):
    p = {}
    p['type'] = 'encrypt'
    p['params'] = {
        'raw' : AES.AES_Encrypt(k,iv,pack),
        'mode': "aes_cbc_pck7padding"
    }
    return json.dumps(p)

async def send_msg(websocket):
    await websocket.send(AESEncrypt(k,vi,PHelper.GetRuncmdPack('list','114514')))
    while True:      
        recv_text = await websocket.recv()
        rece = json.loads(f"{recv_text}")["params"]["raw"]
        print(f'[RECE] {AES.AES_Decrypt(k,vi,rece)}')
        raw = json.loads(AES.AES_Decrypt(k,vi,rece))
        print(raw['cause'])


# 客户端主逻辑
async def main_XBridge():
    while(True):
        try:
            async with websockets.connect(url) as websocket:
                ws = websocket
                await send_msg(websocket)
        except Exception as e:
            print(f'[ERROR] {e}')
            print(f'[ERROR] websocket连接出错')
   

async def func2():
    # 您可以在这个线程处理别的数据，例如QQ机器人
    while(True):
        print(3)
        await asyncio.sleep(2)
        print(4)


tasks = [
    asyncio.ensure_future(main_XBridge()),
    asyncio.ensure_future(func2())
]


asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))