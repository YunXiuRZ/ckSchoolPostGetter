import json
import pymysql


sql_login = {}
with open('../SqlLogin.json', 'r') as f:
    sql_login = json.load(f)

execution = """ SELECT user_name,
                                   new_post_token,
                                   updated_post_token
                                   FROM user
                                   WHERE enable = 1
                                   """

mysqlCon = pymysql.connect(host='162.241.252.14', 
                               port=3306, 
                               user=sql_login['user'], 
                               passwd=sql_login['passwd'], 
                               charset='utf8', 
                               db='toolsof6_ckSchoolPost')
cursor = mysqlCon.cursor()                                
cursor.execute(execution)
print(cursor.fetchall())