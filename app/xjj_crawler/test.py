# !/usr/bin/env python

from selenium import webdriver
import datetime
import time
import urllib.request
import re
import pymysql

def login(header):
    browser.get("http://www.pahualou123.com/user/login.asp")
    username = browser.find_element_by_id('username')
    username.send_keys('rekcard')
    password =  browser.find_element_by_id('password')
    password.send_keys('rekcard')
    checkcode = browser.find_element_by_id('checkcode')
    code = input("请输入登录验证码：")
    checkcode.send_keys(code)
    browser.find_element_by_class_name('btn-submit').submit()
    time.sleep(2)
    cookie = browser.get_cookies()
    cookiestr=''
    for cook in cookie:
            cookiestr = cookiestr + cook['name'] +'='+cook['value']+';'
    header['Cookie'] = cookiestr

def nologin():
        browser.get("http://www.pahualou123.com/user/login.asp")

def cityurl():
        html = browser.page_source
        ul = browser.find_elements_by_xpath('//ul[@class="city-inlist clearfix"]/li/a')
        cityUrls = []
        for eachcity in ul:
              cityUrls.append(eachcity.get_attribute("href"))
        return cityUrls

def cityEachPageUrl(cityUrl,header):
        cityPageUrl = []
        pageNum = 0
        pattern = re.compile(r'>></a></li>\r\n\r\n\r\n<li><p>(.*?)</p></li>\r\n</ul>')
        try:
                page = urllib.request.urlopen(cityUrl,headers=header)
                buff = page.read()
                pageStr = buff.decode("utf8")
                page.close()
                pageNumStr = pattern.findall(pageStr)
                pageNum = int(pageNumStr[0])
        except (Exception):
                print('not used')        
          
        for i in range(1,pageNum):
                cityPageUrl.append(cityUrl+'&page='+str(i))      
        return cityPageUrl

def eachInfo(eachCityPage):
        eachInfoUrl = []
        pattern = re.compile(r'<a class="info-tit" href="(.*?)"')
        pattern2 = re.compile(r'<a class="info-tit"  target="_blank" href="(.*?)"')
        try:
                eachInfoPage = urllib.request.urlopen(eachCityPage)
                buff = eachInfoPage.read()
                eachInfoPageStr = buff.decode("utf8")
                eachInfoPage.close()
                urls =  pattern.findall(eachInfoPageStr)
                urls2 = pattern2.findall(eachInfoPageStr)
                urls.extend(urls2)
        except (Exception,e):
                print('e:',str(e))
                print('not used')
        for eachUrl in urls:
                eachUrl = 'http://www.pahualou123.com'+eachUrl
                eachInfoUrl.append(eachUrl)
        return eachInfoUrl


header = {
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}	
browser = webdriver.Chrome()

login(header)
cityUrl = cityurl()
conn = pymysql.connect(host='127.0.0.1', user = "root", passwd="123qwe", db="gatherinfo", port=3306, charset="utf8")
cur = conn.cursor()
i=0
sql = "insert ignore into detail_info(url) value(%s)"
for city in cityUrl:
        cityPageUrl = cityEachPageUrl(city,header)
        for cityPage in cityPageUrl:
                eachInfoUrls = eachInfo(cityPage)
                for each in eachInfoUrls:
                        count = cur.execute(sql, each)
                        conn.commit()
                        i=i+1
                        print(i)
						

#关闭资源连接
cur.close()
conn.close()
print("数据库断开连接！");
        

