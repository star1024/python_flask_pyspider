from flask import Flask, render_template, request
from config import DevConfig
import client # client.py
import pymysql
import base64
import uuid
from flask_httpauth import HTTPDigestAuth
app = Flask(__name__)#定位目前載入資料夾的位置
app.config.from_object(DevConfig)
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "john": "hello",
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None
def broker_val(data):
    return {
    '元大': 'yuanta',
    '永豐': 'sinotrade_v3',
    }.get(data,'yuanta')  #'yuanta'為預設返回值，可自設定
def msyql(data):
    data = "'"+data+"'"
    db = pymysql.connect(host='localhost',port=3306,user='root',password='',db='mytodo',charset='utf8')
    sql = sql = 'Select * FROM table2 Where projid='+data+';'
    print(data)
    cursor = db.cursor()
    cursor.execute(sql)
    myresult = cursor.fetchall()
    if len(myresult)>0:
        for x in myresult:
            data_provider = x[3]
        return data_provider
    return "查無資料"

@app.route('/')
@auth.login_required
def main():
    return render_template('login.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        user = request.values['user']
        password = request.values['password']
        broker = broker_val(request.values['broker'])
        
        #exec(open('client.py').read())
        #user = 'H121666748'  pwd ='isam1689'
        user_id = str(uuid.uuid4())
        client.main(user,password,user_id,broker)#送參數給py檔啟動pyspider
        return render_template('result.html', name=user, projectid = user_id,broker=request.values['broker'])

    if request.method == 'GET' and len(request.args.get('project_id'))>0:
        search_id = request.args.get('project_id')
        result_id = msyql(search_id)
        return render_template('result.html', result=result_id)
    elif request.method == 'GET':
        return render_template('login.html')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2222)