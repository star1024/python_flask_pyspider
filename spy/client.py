from xmlrpc.client import ServerProxy
import hashlib
import base64
from spy.std import model# model.py 自定義模組

def main(user,pwd,user_id,broker):
    server = ServerProxy("http://127.0.0.1:23333") # 初始化服務器
    
    params = {
        'username':user,
        'password':pwd,
        'taskid':user_id# 產生第四版 UUID（隨機）
    }
    b64 = model.b64e(str(params))
    url = 'https://www.careone.com.tw/?params='+b64

    h1=hashlib.md5()
    h1.update(url.encode(encoding='utf-8'))
    # print(params)
    print (server.newtask({
        'taskid':h1.hexdigest(),
        'project':broker,
        'url':url,
        'process': {
                'callback': 'index_page',
            }
    })) # 调用函数傳參數

if __name__ == '__main__':
    main(user,pwd,user_id,broker)