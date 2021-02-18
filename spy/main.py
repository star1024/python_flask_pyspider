from flask import Flask, render_template, request,redirect,url_for
# from config import DevConfig
from spy import client # client.py
import pymysql
import base64
import uuid
app = Flask(__name__)#定位目前載入資料夾的位置
app.config["DEBUG"] = True

#選擇券商
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

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        broker = broker_val(request.form.get('broker'))
        user_id = str(uuid.uuid4())

        client.main(user,password,user_id,broker)#送參數給py檔啟動pyspider
        return redirect(url_for('result', name=user, projectid = user_id,broker=request.values['broker']))

    return render_template('login.html')

@app.route('/result',methods=['GET'])
def result():

    if 'project_id' in request.args:#查詢DB執行結果
        search_id = request.args.get('project_id')
        result_id = msyql(search_id)
        return render_template('result.html', result=result_id)
    
    return render_template('result.html',broker=request.args['broker'], name = request.args['name'], projectid = request.args['projectid'])
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2233)