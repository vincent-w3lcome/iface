# -*- coding: utf-8 -*-#
import MySQLdb

db = MySQLdb.connect("localhost","root","","yuwenmao", charset='utf8')
print("successfully connected")

def querydb(db):
    cursor = db.cursor()
    #sql = "SELECT * FROM tag where style='common'"
    sql = "SELECT * FROM tag where name='间接说明'"
    cursor.execute(sql) # 获取所有记录列表
    results = cursor.fetchall()
    print(results)
    print(type(results))
    for row in results:
        if row[1] == "语言文字运用":
            print("--------------------------------------")

querydb(db)
