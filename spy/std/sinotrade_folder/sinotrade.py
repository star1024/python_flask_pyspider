import datetime, time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymysql
import json
import sys
from spy.std import model# model.py 自定義模組
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    def on_start(self):
        self.crawl('', callback=self.index_page)

    def index_page(self, response):
    
        para = Parsing(str(response.url))

        return {
            'taskid':para[0],
            'result':para[1],
        }

#存入資料庫1
def insert_db(tmp,taskid):
    # print("start")
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    arr_val = [("永豐帳務查詢",taskid,"庫存查詢",json.dumps(tmp),timestamp)]
    db = pymysql.connect(host='localhost',port=3306,user='root',password='',db='mytodo',charset='utf8')
    cursor = db.cursor()
    #cursor.execute("SELECT * FROM table1")
    sql = "INSERT INTO table1 (projname,projid,category,content,create_at) VALUES (%s,%s,%s,%s,%s);"
    cursor.executemany(sql,arr_val)
    db.commit()
    db.close()
    time.sleep(1)

def wait(browser,By,string):
    element = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, string))
    )
    return element

#啟動selenium
def selenium(username,userpassword,taskid):
    start = time.time()
    chrome_options = Options() 
    #chrome_options.add_argument('--headless')  #瀏覽器不提供可視化頁面
    chrome_options.add_argument('--disable-gpu') #規避google bug
    #chrome_options.add_argument('--no-sandbox') #以最高權限運行
    #chrome_options.add_argument('--disable-plugins') #禁止載入所有外掛，可以增加速度
    #chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加載圖片, 提升速度

    driverpath=model.path()
    browser=webdriver.Chrome(executable_path=driverpath,options=chrome_options)
    url='https://www.sinotrade.com.tw/newweb/SinoTrade_login'

    browser.implicitly_wait(20)#隐性等待
    browser.get(url)#get方式進入網站
    time.sleep(1)
    try:
        # WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))#WebDriverWait顯性等待
        selectid= browser.find_element_by_id('complex-form_account')#選擇帳號
        selectid.send_keys(str(username))
    
        selectPwd= browser.find_element_by_id("complex-form_password")#選擇密碼
        selectPwd.send_keys(str(userpassword))

        wait(browser,By,'//*[@id="complex-form"]/div[4]/div/div/div/button').click()#模擬登入
        time.sleep(1)
        WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[4]/div/div[2]/div/div[2]/div/div/div[2]/button[1]/span"))).click()#關掉alert

        # time.sleep(2)
        # wait(browser,By,'//*[@id="__next"]/header/div/div[3]/div[1]').click()#選擇會員專區
        # # time.sleep(2)
        # wait(browser,By,'//*[@id="__next"]/header/div/div[3]/div[2]/div/div/div/div[2]/div/div/div/div/div/div[1]/div[1]/div/ul/li[2]/a').click()#我的帳號
        # time.sleep(2)
        # print(browser.current_url)
        browser.get('https://www.sinotrade.com.tw/inside/TradingAccount')#get新URL
        time.sleep(1)
        wait(browser,By,'//a[@href="#tabs-2"]').click()#庫存分頁
        # browser.find_element_by_xpath('//a[@href="#tabs-2"]').click()#庫存分頁
        
        table_col = browser.find_element_by_class_name('inventoryTitleContainer')#欄位名稱
        table_val = browser.find_element_by_css_selector('table > tbody > tr:nth-child(1)')#欄位內容
        #print(table_col.text)
        #print(table_val.text)
        for i in [table_col.text]:
            tmps_col = i.split()
        tmps_col.insert( 2, "代號") #欄位缺代號補上
        for i in [table_val.text]:
            tmps_val = i.split()
        # print(tmps_col)
        # print(tmps_val)
        if(len(tmps_col) == len(tmps_val)):
            tmp = dict(zip(tmps_col, tmps_val))#two list convert to dict

        insert_db(tmp,taskid)
        model.insert_db2(taskid,"success")
        browser.quit()

        end = time.time()
        print("執行時間:%f秒"%(end-start))
        
        return "success"
    except Exception as e:
        model.insert_db2(taskid,"fail")
        error_string = repr(e)
        browser.quit()
        return error_string
#selenium("H121666748","isam1689","test")

#解析pyspider取得遠端api的參數
def Parsing(url):
    para = model.analysis(url)
    username = para[0]
    userpassword = para[1]
    taskid = para[2]
    data_provider = selenium(username,userpassword,taskid)
    return [taskid,data_provider]