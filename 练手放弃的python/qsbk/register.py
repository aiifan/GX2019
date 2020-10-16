import base64
import requests
import math
import random
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def open_url(url,wangfan,xuehao_nums):
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)
    username = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入账号"]')
    name = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入姓名"]')
    driver.find_element_by_css_selector('input[placeholder="请选择班级"]').click()
    # driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div[1]/ul/li[1]/span').click()
    time.sleep(2)
    xuehao = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入学号"]')
    password = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入密码"]')
    password2 = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请再次输入密码"]')
    code_in = driver.find_element_by_css_selector('input[placeholder="请输入验证码"]')
    base64_decode = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div[7]/img').get_attribute("src").split(',')[-1]
    code_str = uma_codec_mode(base64_decode, ac_tk)
    username.send_keys(wangfan)
    name.send_keys(wangfan)
    xuehao.send_keys(xuehao_nums)
    password.send_keys("123456")
    password2.send_keys("123456")
    code_in.send_keys(code_str)
    driver.find_element_by_css_selector("button span").click()
    time.sleep(30)
    print("注册成功")


def input_name():
    for i in range(12,13):
        wangfan = "wangfan" + str(i)
    
    xuehao_nums = math.floor(1e5 * random.random())
    return wangfan, xuehao_nums

def uma_codec_mode(b64_decode, access_token):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    #image_data = base64.b64decode(b64_decode)
    params = {
        "image": b64_decode,
        "access_token": access_token
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        code_lists = response.json()["words_result"]
        for i in code_lists:
            return i["words"]


def baidu():
    APP_ID = "18090044"
    API_KEY = "Kpkv6KT3jDgRu2n3019QmWiZ"
    SECRET_KEY = "i4uUXSPenyGIubwW736RPGe1eH37QXkf"
    host = 'https://aip.baidubce.com/oauth/2.0/token'
    data = {
        "grant_type": "client_credentials",
        "client_id": API_KEY,
        "client_secret": SECRET_KEY
    }
    response = requests.post(host, data=data)
    if response:
        data = response.json()
        return data["expires_in"], data["access_token"]

if __name__ == "__main__":
    # open_url("http://192.168.0.124")
    expire, ac_tk = baidu()
    wangfan, xuehao_nums = input_name()

    open_url("http://192.168.0.122/#/register",wangfan, xuehao_nums)