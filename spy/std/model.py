import base64
import pymysql
import datetime, time

'''selenium model''' 
def path():
    driverpath = '/Users/yang/Desktop/python_file/chromedriver'
    return driverpath


'''decode model''' 

#請求的網址(未含參數)
def client_url():
    return 'https://www.careone.com.tw/?params='
def b64e(s):
    return base64.b64encode(s.encode()).decode()

def b64d(s):
    return base64.b64decode(s).decode()

#解析pyspider取得遠端api的參數
def analysis(url):
    num = len(client_url())
    target_para = url[num:]#取出URL後段加密的字串
    para = b64d(target_para)
    username = eval(para)['username']#去除雙引號
    password = eval(para)['password']#去除雙引號
    taskid = eval(para)['taskid']#去除雙引號

    return [username,password,taskid]

'''mysql model''' 

def insert_db2(taskid,status):
    # print("start")
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    arr_val = [(taskid,timestamp,status)]
    db = pymysql.connect(host='localhost',port=3306,user='root',password='',db='mytodo',charset='utf8')
    cursor = db.cursor()
    #cursor.execute("SELECT * FROM table2")
    sql = "INSERT INTO table2 (projid,create_at,status) VALUES (%s,%s,%s);"
    #print(arr_val)
    cursor.executemany(sql,arr_val)
    db.commit()
    db.close()
    time.sleep(1)