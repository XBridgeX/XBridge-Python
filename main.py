import asyncio
from ctypes import pythonapi
import websockets
import Utils.AES as AES
import Utils.MD5 as MD5
import json

password = "password"

k = MD5.Encrypt(password)[0:16]
vi = MD5.Encrypt(password)[16:32]

print(f"您的AES密匙为：{k},偏移量为：{vi}")

async def send_msg(websocket):
    while True:
        #await websocket.close(reason="user exit")  
        #await websocket.send('smoething')
        recv_text = await websocket.recv()
        print(f"{recv_text}")
        rece = json.loads(f"{recv_text}")["params"]["raw"]
        print(AES.AES_Decrypt(k,vi,rece))

# 客户端主逻辑
async def main_XBridge():
    async with websockets.connect('ws://127.0.0.1:8080') as websocket:
        await send_msg(websocket)

asyncio.get_event_loop().run_until_complete(main_XBridge())