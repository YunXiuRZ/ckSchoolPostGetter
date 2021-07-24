# -*- coding: utf-8 -*
import pymysql
import re
import sys
sys.path.append('/module')
from PostInformationGetter import PostInformationGetter
from MysqlPostConnector import MysqlPostConnector

#爬蟲起始
#輸入公告ID
mysqlCon = pymysql.connect('162.241.252.14', 
                           port = 3306, 
                           user = 'toolsof6_YunXiuRZ', 
                           passwd = 'Jerrykao1022', 
                           charset = 'utf8', 
                           db = 'toolsof6_ckSchoolPost')#連接資料庫
cursor = mysqlCon.cursor()
mysqlExecution = """SELECT post_id
                From ckSchoolPost"""#取得資料庫中公告id
cursor.execute(mysqlExecution)
IDList = cursor.fetchall()
for ID in IDList:
    Id = re.search(r'[0-9]{5}', str(ID)).group()
    pig = PostInformationGetter(Id)
    pig.setInformation()#取得公告信息
    mpc = MysqlPostConnector()
    mpc.execute(pig)
    