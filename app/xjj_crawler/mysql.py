#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql
conn = pymysql.connect(host='127.0.0.1', user = "root", passwd="123qwe", db="gatherinfo", port=3306, charset="utf8")
cur = conn.cursor()
sql = "insert into detail_info(url) value(%s)"

count = cur.execute(sql, 'sdfdf')

conn.commit()

#关闭资源连接
cur.close()
conn.close()
print("数据库断开连接！");
