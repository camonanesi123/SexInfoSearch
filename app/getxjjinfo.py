# -*- coding:utf-8 -*-  
import pymysql
import json

def getXjjInfo(district="北京",style="楼凤兼职"):
    #params 城市 district、类型 style
    # 打开数据库连接
    db = pymysql.connect(host='localhost', port=3306,user='root', passwd='123qwe', db='gatherinfo', charset='utf8')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    sqlSel = "select * from detail_info where district like '%{0}%'  and style='{1}' ORDER BY RAND()  limit 1".format(district,style)
    #print(sqlSel)
    # 使用 execute()  方法执行 SQL 查询
    try:
        cursor.execute(sqlSel)
        rs = cursor.fetchone()
        xiaojj = {}
        data = {}
        if rs==None:
            data['success'] = 0
            data['xiaojj'] = xiaojj
        else:
            #print("Database version : %s " % rs[1])
            xiaojj['id'] = rs[0]
            xiaojj['title']=rs[3]
            xiaojj['district']=rs[5]
            xiaojj['detailAddr']=rs[6]
            xiaojj['age']=rs[9]
            xiaojj['appear']=rs[11]
            xiaojj['price']=rs[13]
            xiaojj['serive']=rs[12]
            #xiaojj['contact']=rs[18]
            xiaojj['detail']=rs[19]
            data['success'] = 1
            data['xiaojj'] = xiaojj
        jsonStr = json.dumps(data, ensure_ascii=False)
        print(jsonStr)
    # 关闭游标
        cursor.close()
    # 关闭数据库连接
        db.close()
        #return jsonStr
    except Exception as e:
        print(e)

if __name__ == '__main__':
    getXjjInfo()


