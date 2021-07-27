# -*- coding:utf-8 -*-
import pymysql
import requests
import json
import sys   #reload()之前必須要引入模組

#reload(sys)
#sys.setdefaultencoding('utf-8')

#sql execution
executions = {}
executions['newPost'] = """SELECT post_id, 
                                post_title
                            FROM ckSchoolPost
                            WHERE is_posted = 0
                            """

executions['updatedPost'] = """SELECT post_id,
                                post_title
                                FROM ckSchoolPost
                                WHERE is_posted = 2
                                """

executions['setPosted'] = """UPDATE ckSchoolPost
                                SET is_posted = 1
                                WHERE post_id = {}
                                """

executions['getUser'] = """ SELECT user_name,
                                   new_post_token,
                                   updated_post_token
                                   FROM user
                                   WHERE enable = 1
                                   """

#訊息開頭
messages = {}
messages['newPost'] = "新公告！\n"
messages['updatedPost'] = "公告更新！\n"

#取得登入資料庫的帳號密碼
sql_login = {}
with open('SqlLogin.json', 'r') as f:
    sql_login = json.load(f)

#傳入訊息token，回傳用於發送訊息的header
def generate_header(postToken): 
    return {"Authorization" : "Bearer " + postToken,
            "Content-Type" : "application/x-www-form-urlencoded"
            }

#發送訊息給指定用戶
def notify(message, postHeader):
    payload = {"message" : message}
    notify = requests.post("https://notify-api.line.me/api/notify",
                           headers = postHeader, params = payload)
    return notify

#從資料庫中搜尋資料
def select_SQL(execution):
    mysqlCon = pymysql.connect(host='162.241.252.14', 
                               port=3306, 
                               user=sql_login['user'], 
                               passwd=sql_login['passwd'], 
                               charset='utf8', 
                               db='toolsof6_ckSchoolPost')
    cursor = mysqlCon.cursor()                                
    cursor.execute(execution)
    return cursor.fetchall()

#對資料庫進行增刪查改，噢不，查是上面那個
def commit_SQL(execution):
    mysqlCon = pymysql.connect(host='162.241.252.14', 
                                   port=3306, 
                                   user=sql_login['user'], 
                                   passwd=sql_login['passwd'], 
                                   charset='utf8', 
                                   db='toolsof6_ckSchoolPost')
    cursor = mysqlCon.cursor()
    cursor.execute(execution)
    mysqlCon.commit()

#傳入發送公告的條件以及訊息開頭
def send_message(action):
    #取得要推送的公告
    PostsInformation = select_SQL(executions[action])

    #取得要推送的用戶
    userTokens = select_SQL(executions['getUser'])

    for userToken in userTokens:
        userName = userToken[0]
        postHeader = generate_header(userToken[1] if action == 'newPost' else userToken[2])

        counter = 0 #偵錯計數器
        for PostInformation in PostsInformation:
            counter+=1
            if(counter >= 10):#發送超過九個公告，發生問題
                notify("發送公告出錯，請聯繫維護者", postHeader)
                return 1
        
            postID = PostInformation[0]
            postTitle = PostInformation[1]

            #將要推送的公告設成已推送
            commit_SQL(executions['setPosted'].format(postID))

            #合成訊息：訊息類型＋公告標題＋公告網址
            msg = messages[action] + postTitle + "\nhttps://www2.ck.tp.edu.tw/news/%s" % postID
            print("推送編號%s的公告給%s" % (postID, userName))
            notify(msg, postHeader)

def send_messages():
    send_message('newPost')
    send_message('updatedPost')
        
if __name__ == '__main__':
    send_messages()
