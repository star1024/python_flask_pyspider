import os
import datetime, time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pymysql
import requests
import json
from PIL import Image,ImageDraw#截圖
from spy.std import model # model.py 自定義模組
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
#刪除圖檔
def delete_img():
    image1 = '/tmp/PrtSrn.png'
    image2 = '/tmp/redraw.png'
    image3 = '/tmp/redraw.jpg'
    try:
        os.remove(image1)
        os.remove(image2)
        os.remove(image3)
    except OSError as e:
        print(e)
    else:
        print("image is deleted successfully")
def Parsing_img(browser):
    js = 'window.open("https://global.yuanta.com.tw/NexusWebTrade/login/VerificationCode?width=120&height=35&1610349594058");'
    browser.execute_script(js)

    # 輸出當前視窗控制代碼（元大）
    first_handle = browser.current_window_handle

    # 獲取當前視窗控制代碼集合（列表型別）
    handles = browser.window_handles
    # print(handles)  # 輸出控制代碼集合

    # 獲取驗證碼視窗
    sec_handle = None
    for handle in handles:
        if handle != first_handle:
            sec_handle = handle

    # 輸出當前視窗控制代碼（視窗二）
    # print('switch to ', handle)
    browser.switch_to.window(sec_handle)
    browser.save_screenshot('/tmp/PrtSrn.png')
    element = browser.find_element_by_xpath('/html/body/img')
    left = element.location['x']
    right = element.location['x'] + element.size['width']
    top = element.location['y']
    bottom = element.location['y'] + element.size['height']
    img = Image.open('/tmp/PrtSrn.png')
    img = img.crop((left, top, right, bottom))
    img.save('/tmp/redraw.png', 'png')
    '''
    image png convert to jpg
    '''
    rgba_image = Image.open('/tmp/redraw.png')
    rgba_image.load()
    background = Image.new("RGB", rgba_image.size, (255, 255, 255))
    background.paste(rgba_image, mask = rgba_image.split()[3])
    background.save("/tmp/redraw.jpg", "JPEG", quality=100)
    browser.close() #關閉當前視窗（視窗二）
    # 切換回視窗一
    browser.switch_to.window(first_handle)
    time.sleep(1)
    
    url = 'http://220.132.209.131:5569/predict'
    files = {'image': open('/tmp/redraw.jpg', 'rb')}
    r=requests.post(url, files=files)
    data=json.loads(r.content)
    code=data['predictions']
    delete_img()#刪除圖檔
    time.sleep(1)
    # print(code)
    return code

#存入資料庫1
def insert_db(tmp,taskid):
    # print("start")
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    arr_val = [("元大帳務查詢",taskid,"歷史查詢",json.dumps(tmp),timestamp)]
    db = pymysql.connect(host='localhost',port=3306,user='root',password='',db='mytodo',charset='utf8')
    cursor = db.cursor()
    #cursor.execute("SELECT * FROM table1")
    sql = "INSERT INTO table1 (projname,projid,category,content,create_at) VALUES (%s,%s,%s,%s,%s);"
    cursor.executemany(sql,arr_val)
    db.commit()
    db.close()
    time.sleep(1)

#selenium WebDriverWait
def wait(browser,By,string):
    element = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, string))
    )
    return element

#模擬登入
def login_behavior(browser,username,userpassword):
    VerificationCode = Parsing_img(browser)

    selectid = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID, "loginid")))#選擇帳號
    # selectid= browser.find_element_by_id('loginid')#選擇帳號
    # selectid.clear()
    selectid.send_keys(str(username))

    selectPwd = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID, "loginPWD")))#選擇帳號
    # selectPwd= browser.find_element_by_id("loginPWD")#選擇密碼
    # selectPwd.clear()
    selectPwd.send_keys(str(userpassword))
    
    selectCode = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID, "code")))#選擇驗證碼
    # selectCode= browser.find_element_by_id("code")#選擇驗證碼
    selectCode.send_keys(VerificationCode)
    
    WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.ID,"button1"))).click()#模擬登入
    # searchBtn=browser.find_element_by_id('button1')
    # searchBtn.click()#模擬登入

#已實現表格
def fetch1(browser,taskid):
    wait(browser,By,'//a[@data-link="nexuswebtrade/RealPF"]').click()#模擬登入
    # elements = browser.find_element_by_xpath('//a[@data-link="nexuswebtrade/RealPF"]')
    # elements.click()#模擬選項
    # time.sleep(3)
    table_col = browser.find_element_by_xpath('//*[@id="tbdyrealPF"]/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/table/thead')#欄位名稱
    table_val = browser.find_element_by_xpath('//*[@id="tbdyrealPF"]/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/table/tbody')#欄位內容
    tmps_col = table_col.text.split()
    tmps_col = tmps_col[1:]#明細欄位不需要
    tmps_val = table_val.text.split()

    data= [[],[],[],[]]
    #print(tmps_col)
    
    for i , ele in  enumerate(tmps_val):
        if i%4 ==0:
            data[0].append(ele)
        elif i%4 ==1:
            data[1].append(ele)    
        elif i%4 ==2:
            data[2].append(ele) 
        elif i%4 ==3: 
            data[3].append(ele)
    #print(data)
    
    if(len(tmps_col) == len(data)):
        tmp = dict(zip(tmps_col, data))#two list convert to dict
    #print(tmp)
    insert_db(tmp,taskid)
    model.insert_db2(taskid,"success")
#下載檔案
def selenium(username,userpassword,taskid):
    start = time.time()

    chrome_options = Options() 
    #chrome_options.add_experimental_option("detach", True)#不自动关闭浏览器
    #chrome_options.add_argument('--headless')  #瀏覽器不提供可視化頁面
    chrome_options.add_argument('--disable-gpu') #規避google bug
    chrome_options.add_argument('--no-sandbox') #以最高權限運行
    # chrome_options.add_argument('--disable-plugins') #禁止載入所有外掛，可以增加速度
    # chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加載圖片, 提升速度

    driverpath=model.path()
    browser=webdriver.Chrome(executable_path=driverpath,options=chrome_options)
    url='https://global.yuanta.com.tw/NexusWebTrade/Login/UserLogin?returnurl=nexuswebtrade%2Fholding2'

    browser.implicitly_wait(30)#隐性等待
    browser.get(url)#get方式進入網站
    time.sleep(2)#網站有loading時間

    try:
        login_behavior(browser,username,userpassword)
        fetch1(browser,taskid)
        browser.quit()
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
        return "success" #回傳給pyspider result_db
    except Exception as e:
        model.insert_db2(taskid,"fail")
        error_string = repr(e)
        browser.quit()
        return error_string #回傳給pyspider result_db
#selenium(username,userpassword,taskid)

#解析pyspider取得遠端api的參數
def Parsing(url):
    para = model.analysis(url)
    username = para[0]
    userpassword = para[1]
    taskid = para[2]
    data_provider = selenium(username,userpassword,taskid)
    return [taskid,data_provider]
