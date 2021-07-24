# -*- coding:utf-8 -*-
import pymysql
import requests
import sys   #reload()之前必須要引入模組

#reload(sys)
#sys.setdefaultencoding('utf-8')

#sql execution
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
             
#post token
newPostToken = 'tGGykhETyq81DyS5NP8yYi5gxUqcAWvvKaUmtsWbnE7'
newPostHeaders = {
    "Authorization" : "Bearer " + newPostToken,
    "Content-Type" : "application/x-www-form-urlencoded"
}  

newUpdateToken = 'r2N2Ka6bzLS3fzPswHeodtG2q6eZ6Hh5MMx2rEYK2eE'
newUpdateHeaders = {
    "Authorization" : "Bearer " + newUpdateToken,
    "Content-Type" : "application/x-www-form-urlencoded"
}
     
def send_message(execution, message, postHeaders):
    mysqlCon = pymysql.connect(host='162.241.252.14', 
                               port = 3306, 
                               user = 'toolsof6_YunXiuRZ', 
                               passwd = 'Jerrykao1022', 
                               charset = 'utf8', 
                               db = 'toolsof6_ckSchoolPost')
    cursor = mysqlCon.cursor()                                
    cursor.execute(execution)
    PostsInformation = cursor.fetchall()
 
    for PostInformation in PostsInformation:
        msg = message
        postID = PostInformation[0]
        postTitle = PostInformation[1]
        cursor.execute(setPostIsPosedExecution, postID)
        mysqlCon.commit()
        msg += postTitle
        msg += "\nhttps://www2.ck.tp.edu.tw/news/%s" % postID
        payload = {"message" : msg}
        notify = requests.post("https://notify-api.line.me/api/notify",
                               headers = postHeaders, params = payload)

def send_messages():
    send_message(getNewPostsExecution, "新公告！\n", newPostHeaders)
    send_message(getUpdatePostsExecution, "公告更新！\n", newUpdateHeaders)
        
if __name__ == '__main__':
    send_messages()
