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
from PIL import Image,ImageDraw
import pytesseract
# from matplotlib import pyplot as plt


def binarizing(img,threshold): #input: gray image
    pixdata = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if pixdata[x, y] < threshold:
                pixdata[x, y] = 0
            else:
                pixdata[x, y] = 255
    return img
def getPixel(image,x,y,G,N):
    L = image.getpixel((x,y))
    if L > G:
        L = True
    else:
        L = False
 
    nearDots = 0
    if L == (image.getpixel((x - 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x - 1,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x,y + 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y - 1)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y)) > G):
        nearDots += 1
    if L == (image.getpixel((x + 1,y + 1)) > G):
        nearDots += 1
 
    if nearDots < N:
        return image.getpixel((x,y-1))
    else:
        return None
def clearNoise(image,G,N,Z):
    draw = ImageDraw.Draw(image)
 
    for i in range(0,Z):
        for x in range(1,image.size[0] - 1):
            for y in range(1,image.size[1] - 1):
                color = getPixel(image,x,y,G,N)
                if color != None:
                    draw.point((x,y),color)
    code = pytesseract.image_to_string(image) 
    print("code:", code)
    image.save("output2.jpg")
    return code
def Parsing_img(element):
    left = element.location['x']
    right = element.location['x'] + element.size['width']
    top = element.location['y']
    bottom = element.location['y'] + element.size['height']
    img = Image.open('test2.jpg')
    img = img.crop((left, top, right, bottom))
    img.save('redraw.png', 'png')
    # captcha = Image.open("redraw.png")  

    # img = captcha.convert("L") # 處理灰度 
    image = Image.open("redraw.png").convert("L")
    image.show()
    image_binary = binarizing(image, 150)
    result = clearNoise(image_binary,50,4,6)
    # print(result)
    time.sleep(2)

    return result
def wait(browser,By,string):
    element = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, string))
    )
    return element
#下載檔案
def download(name,password):
    start = time.time()

    chrome_options = Options() 
    #chrome_options.add_argument('--headless')  #瀏覽器不提供可視化頁面
    # chrome_options.add_argument('--disable-gpu') #規避google bug
    # chrome_options.add_argument('--no-sandbox') #以最高權限運行
    # chrome_options.add_argument('--disable-plugins') #禁止載入所有外掛，可以增加速度
    # chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加載圖片, 提升速度

    driverpath='/Users/yang/Desktop/python_file/chromedriver'
    browser=webdriver.Chrome(executable_path=driverpath,chrome_options=chrome_options)
    url='https://global.yuanta.com.tw/NexusWebTrade/Login/UserLogin?returnurl=nexuswebtrade%2Fholding2'

    browser.implicitly_wait(30)#隐性等待
    browser.get(url)#get方式進入網站

    #time.sleep(2)#網站有loading時間

    try:
        selectid= browser.find_element_by_id('loginid')#選擇帳號
        # selectid.clear()
        selectid.send_keys(str(name))
        #time.sleep(2)

        selectPwd= browser.find_element_by_id("loginPWD")#選擇密碼
        # selectPwd.clear()
        selectPwd.send_keys(str(password))
        time.sleep(2)

        browser.save_screenshot('test2.jpg')
        element = browser.find_element_by_id('imgCode')
        time.sleep(2)
        # Parsing_img(element)
        selectCode= browser.find_element_by_id("code")#選擇驗證碼
        
        selectCode.send_keys(str(Parsing_img(element)))
        time.sleep(2)
        searchBtn=browser.find_element_by_id('button1')
        searchBtn.click()#模擬登入
        

        # elements = browser.find_element_by_xpath('//a[@data-link="nexuswebtrade/RealPF"]')
        # elements.click()#模擬選項
        # time.sleep(1)
        
        # lists = browser.find_element_by_xpath('//*[@id="tbdyrealPF"]/tr/td/table/tbody/tr/td[1]/table/tbody/tr[2]/td/div/table/tbody')

        # time.sleep(1)
        browser.quit()
        # # print('頁面加載成功')
        end = time.time()
        print("執行時間：%f 秒" % (end - start))
    except Exception as e:
        print(e)
        print('頁面加載失敗')
        browser.quit()
#download()
download("R221754886","isam1689")












