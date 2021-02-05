import os
import pymysql
import datetime, time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlrd
import requests

def wait(browser,By,string):
    element = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, string))
    )
    return element
###下載檔案方法一
def download():
    start = time.time()

    chrome_options = Options() 
    chrome_options.add_argument('--headless')  #瀏覽器不提供可視化頁面
    chrome_options.add_argument('--disable-gpu') #規避google bug
    chrome_options.add_argument('--no-sandbox') #以最高權限運行
    chrome_options.add_argument('--disable-plugins') #禁止載入所有外掛，可以增加速度
    chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加載圖片, 提升速度

    driverpath='/Users/yang/Desktop/python_file/chromedriver'
    browser=webdriver.Chrome(executable_path=driverpath,chrome_options=chrome_options)
    url='https://global.yuanta.com.tw/NexusWebTrade/Login/UserLogin?returnurl=nexuswebtrade%2Fholding2'

    browser.implicitly_wait(30)#隐性等待
    browser.get(url)#get方式進入網站
    locator = (By.ID, 'button1')
    #time.sleep(2)#網站有loading時間

    try:

        WebDriverWait(browser, 20, 0.5).until(EC.presence_of_element_located(locator))#WebDriverWait顯性等待

        selectid= browser.find_element_by_id('loginid')#選擇帳號
        # selectid.clear()
        selectid.send_keys(str("R221754886"))
        #time.sleep(2)

        selectPwd= browser.find_element_by_id("loginPWD")#選擇密碼
        # selectPwd.clear()
        selectPwd.send_keys(str("isam1689"))
        #time.sleep(2)

        
        searchBtn=browser.find_element_by_id('button1')
        searchBtn.click()#模擬登入
        
        elements = browser.find_element_by_xpath('//a[@data-link="nexuswebtrade/RealPF"]')
        elements.click()#模擬選項
        time.sleep(1)
        
        lists = browser.find_element_by_xpath('//*[@id="tbdyrealPF"]/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/table/tbody')
        # # //*[@id="tbdyrealPF"]/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/table/tbody
        # # //*[@id="tbdyrealPF"]/tr/td/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/table/tbody
        tmps = lists.text.split()
        data= [[],[],[],[]]
        for i , ele in  enumerate(tmps):
            if(i%4 ==0):
                data
        # print(browser.find_elements_by_class_name('unrealPFtablebg1'))
        print(tmps)
        time.sleep(1)
        browser.quit()
        # print('頁面加載成功')
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
    except Exception as e:
        print(e)
        print('頁面加載失敗')
        browser.quit()

download()