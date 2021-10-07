import asyncio
import os
import sys
sys.path.append(f"{os.getcwd()}/Utils/")
import websockets
import AES
import MD5
import json
import PackHelper as PHelper
import nonebot
import config

password = "password"

k = MD5.Encrypt(password)[0:16]
vi = MD5.Encrypt(password)[16:32]
runcmdid = {}

bot = nonebot.get_bot()

async def bot_online():
    await bot.send_private_msg(user_id=12345678, message='你好～')

bot_online()
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
        #await websocket.close(reason="user exit")  
        #await websocket.send('smoething')
        recv_text = await websocket.recv()
        rece = json.loads(f"{recv_text}")["params"]["raw"]
        print(f'[RECE] {AES.AES_Decrypt(k,vi,rece)}')
        raw = json.loads(AES.AES_Decrypt(k,vi,rece))
        print(raw['cause'])


# 客户端主逻辑
async def main_XBridge():
    try:
        async with websockets.connect('ws://127.0.0.1:8080') as websocket:
            #websocket.enableTrace(True)
            await send_msg(websocket)
    except Exception as e:
        print(f'[ERROR] {e}')
        print(f'[ERROR] websocket连接出错，程序即将退出')
    finally:
        pass
   
asyncio.get_event_loop().run_until_complete(main_XBridge())

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.run()