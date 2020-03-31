# !/usr/bin/env python

from selenium import webdriver
import datetime
import time
import urllib.request
import re
import pymysql
import http.cookiejar

def getinfo(url,cur,sql,header):

        patternTitle = re.compile(r'<tdclass="sm-tit">信息标题</td><td>(.*?)</td>')
        patternStyle = re.compile(r'<tdclass="sm-tit">信息分类</td><td>(.*?)</td>')
        patternDistrict1 = re.compile(r'所属地区.*?&typeid=">(.*?)</a>-<ahref=')
        patternDistrict2 = re.compile(r'</a>-<ahref=.*?&typeid=">(.*?)</a></td></tr><tr><tdclass="sm-tit">详细地址')
        patternDetailAddr = re.compile(r'<tdclass="sm-tit">详细地址</td><td><strongclass="text-red">(.*?)</strong></td>')
        patternSource = re.compile(r'<tdclass="sm-tit">信息来源</td><td>(.*?)</td>')
        patternAmount = re.compile(r'<tdclass="sm-tit">小姐数量</td><td>(.*?)</td>')
        patternAge = re.compile(r'<tdclass="sm-tit">小姐年龄</td><td>(.*?)</td>')
        patternLevelDesc = re.compile(r'<tdclass="sm-tit">小姐素质</td><td>(.*?)</td>')
        patternAppear = re.compile(r'<tdclass="sm-tit">小姐外形</td><td>(.*?)</td>')
        patternService = re.compile(r'<tdclass="sm-tit">服务项目</td><td>(.*?)</td>')
        patternPrice = re.compile(r'<tdclass="sm-tit">价格一览</td><td>(.*?)</td>')
        patternTimeopen = re.compile(r'<tdclass="sm-tit">营业时间</td><td>(.*?)</td>')
        patternEnviron = re.compile(r'<tdclass="sm-tit">环境设备</td><td>(.*?)</td>')
        patternSafe = re.compile(r'<tdclass="sm-tit">安全评估</td><td>(.*?)</td>')
        patternJudge = re.compile(r'<tdclass="sm-tit">综合评价</td><td>(.*?)</td>')
        patternContact = re.compile(r'<tdclass="sm-tit">联系方式</td><td><strongclass="text-red"><imgsrc="(.*?)"/></strong></td>')
        patternDetail = re.compile(r'详细介绍：</div>(.*?)</div><!--投诉-->')
        
        rq = urllib.request.Request(url,headers=header)
        page = urllib.request.urlopen(rq)
        buff = page.read()
        pageStr = buff.decode("utf8").replace('\n','').replace('\t','').replace(' ','').replace('\r','')
        page.close()

        try:

                title = patternTitle.findall(pageStr)
                style = patternStyle.findall(pageStr)
                district = patternDistrict1.findall(pageStr)[0]+'-'+patternDistrict2.findall(pageStr)[0]
                detailAddr = patternDetailAddr.findall(pageStr)
                source = patternSource.findall(pageStr)
                amount = patternAmount.findall(pageStr)
                age = patternAge.findall(pageStr)
                levelDesc = patternLevelDesc.findall(pageStr)
                appear = patternAppear.findall(pageStr)
                service = patternService.findall(pageStr)
                price = patternPrice.findall(pageStr)
                timeOpen = patternTimeopen.findall(pageStr)
                environ = patternEnviron.findall(pageStr)
                safe = patternSafe.findall(pageStr)
                judge = patternJudge.findall(pageStr)
                contactUrl = patternContact.findall(pageStr)
                bytesImg = ''
                if(len(contactUrl)>0):
                        picUrl = 'http://www.pahualou123.com/'+contactUrl[0]
                        print(url)
                        bytesImg = savePic(picUrl,header)
                
                
                detail = patternDetail.findall(pageStr)
                
                param = (title[0],style[0],district,detailAddr[0],source[0],amount[0],age[0],levelDesc[0],appear[0],service[0],price[0],timeOpen[0],environ[0],safe[0],judge[0],bytesImg,detail[0])
                print(sql)
                count = cur.execute(sql,param)
                conn.commit()
        except Exception as e:
                print('error:',url)
                print(e)

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

        


def savePic(url,header):
        #header = {'Accept':'image/webp,*/*'}
        rq = urllib.request.Request(url,headers=header)
        page = urllib.request.urlopen(rq)
        data = page.read()
        return data


                
conn = pymysql.connect(host='127.0.0.1', user = "root", passwd="123qwe", db="gatherinfo", port=3306, charset="utf8")
cur = conn.cursor()
header = {
        'User-Agent':' Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}
browser = webdriver.Chrome()
login(header)
#查询sql
sqlSel = 'select id,url from detail_info where isGet=0'
try:
        cur.execute(sqlSel)
        results = cur.fetchall()
        for row in results:
                id = row[0]
                url = row[1]
                #print(url)
                sql = 'update detail_info set isGet=1,title=%s,style=%s,district=%s,detailAddr=%s,source=%s,amount=%s,age=%s,leveldesc=%s,appear=%s,service=%s,price=%s,timeopen=%s,environ=%s,safe=%s,judge=%s,contact=%s,detail=%s where id='+str(id)
                #print(url)
                getinfo(url,cur,sql,header)
                time.strftime('%H:%M:%S',time.localtime(time.time()))
                time.sleep(1)
except Exception as e:
        print(e)
        
#getinfo('http://www.pahualou123.com/ShowInfo.asp?id=527163&areaid=1&typeid=',cur,sql)
#关闭资源连接

cur.close()
conn.close()
print("数据库断开连接！");





