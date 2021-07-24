from bs4 import BeautifulSoup
import requests
import pymysql
import re

def insertData(ID, title, date, time, office, room , article, annex):
    
    #連接資料庫
    mysqlCon = pymysql.connect('162.241.252.14', 
                           port = 3306, 
                           user = 'toolsof6_YunXiuRZ', 
                           passwd = 'Jerrykao1022', 
                           charset = 'utf8', 
                           db = 'toolsof6_ckSchoolPost')
    cursor = mysqlCon.cursor()
    
    #定義插入指令
    mysqlExecution = """
        INSERT INTO ckSchoolPost (post_id, 
                                post_title, 
                                post_date, 
                                post_time, 
                                post_office, 
                                post_room, 
                                article,
                                annex,
                                is_posted,
                                category
                                )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
    
    #執行指令
    cursor.execute(mysqlExecution,(ID,  title, date, time, office, room , article, annex, 0, "NoneCategory"))
    mysqlCon.commit()

def insertPostData(ID):
    
    #獲取網頁原始碼
    requestUrl = "https://www2.ck.tp.edu.tw/news/" + ID
    r = requests.get(requestUrl)
    r.encoding = "utf8"
    bs = BeautifulSoup(r.text,'lxml')
    
    #獲取公告標題
    title = bs.find("h4").text
    
    #獲取公告發佈日期
    date = bs.find(attrs = {"class" : "date"}).text
    dateList = date.split("/")
    
    #獲取公告發佈處室
    office = bs.find(attrs = {"class" : "office"}).text.split(" ")
    postOffice = office[0]
    postRoom = office[1]
    
    #獲取公告內文
    article = bs.find(attrs = {"class" : "Page__RedactorBlock-sc-1geffe8-0 redactor-styles hkzaDk"})
    lineList = article.find_all("p")
    articleText = ""
    for line in lineList:
        articleText +=line.text
        articleText +="\n"
    
    #獲取公告附加連接
    links = bs.find_all(attrs = {"class" : "Post__LinkWrapper-kr2236-3 iaPBqD"})   
    annex_dic = {}
    for link in links:
        header = link.find("p").text
        urls = link.find_all("a")
        dicIn = {}
        for url in urls:
            herf = url.get("href")
            dicIn[url.text] = herf
            annex_dic[header] = dicIn
            annex = str(annex_dic)
    
    #插入數據至資料庫
    insertData(ID, 
               title, 
               "%s-%s-%s" % (dateList[0], dateList[1], dateList[2]),
               "08:00:00",
               postOffice,
               postRoom,
               articleText,
               annex
               )

#爬蟲起始
url = input()
ID = re.search(r'[0-9]{5}$', url).group()
insertPostData(ID)