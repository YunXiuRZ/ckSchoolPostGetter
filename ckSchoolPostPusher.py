# -*- coding:utf-8 -*-
import pymysql
import requests
import sys   

#上傳至雲主機設置文字編碼
#reload(sys)
#sys.setdefaultencoding('utf-8')

#所有密碼相關已改大寫單字

mysqlCon = pymysql.connect('IP', 
                           port = 3306, 
                           user = 'USER', 
                           passwd = 'PASSWORD', 
                           charset = 'utf8', 
                           db = 'DATABASE')
cursor = mysqlCon.cursor()
getNewPostsExecution = """SELECT post_id, 
                                post_title
                            FROM ckSchoolPost
                            WHERE is_posted = 0
                            """

getUpdatePostsExecution = """SELECT post_id,
                                post_title
                                FROM ckSchoolPost
                                WHERE is_posted = 2
                                """

setPostIsPosedExecution = """UPDATE ckSchoolPost
                                SET is_posted = 1
                                WHERE post_id = %s
                                """
                                
cursor.execute(getNewPostsExecution)
newPostsInformation = cursor.fetchall()
newPostToken = 'POSTTOKEN'
newPostHeaders = {
    "Authorization" : "Bearer " + newPostToken,
    "Content-Type" : "application/x-www-form-urlencoded"
}   
 
for newPostInformation in newPostsInformation:
    postID = newPostInformation[0]
    postTitle = newPostInformation[1]
    cursor.execute(setPostIsPosedExecution, postID)
    mysqlCon.commit()
    msg = "新公告！\n"
    msg += postTitle
    msg += "\nhttps://www2.ck.tp.edu.tw/news/%s" % postID
    payload = {"message" : msg}
    notify = requests.post("https://notify-api.line.me/api/notify",
        headers = newPostHeaders, params = payload)


cursor.execute(getUpdatePostsExecution)
updatePostsInformation = cursor.fetchall()

newUpdateToken = 'UPDATETOKEN'
newUpdateHeaders = {
    "Authorization" : "Bearer " + newUpdateToken,
    "Content-Type" : "application/x-www-form-urlencoded"
}
for updatePostInformation in updatePostsInformation:
    postID = updatePostInformation[0]
    postTitle = updatePostInformation[1]
    cursor.execute(setPostIsPosedExecution, postID)
    mysqlCon.commit()
    msg = "公告更新！\n"
    msg += postTitle
    msg += "\nhttps://www2.ck.tp.edu.tw/news/%s" % postID
    payload = {"message" : msg}
    notify = requests.post("https://notify-api.line.me/api/notify",
        headers = newUpdateHeaders, params = payload)
    
