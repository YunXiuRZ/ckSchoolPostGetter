# -*- coding: utf-8 -*
from bs4 import BeautifulSoup
import requests
import pymysql
import re
import time


def insertData(ID, title, date, time, office, room , article, annex, categoryName):
    
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
    cursor.execute(mysqlExecution,(ID, 
             title, 
             date,
             time,
             office,
             room,
             article,
             annex,
             0,
             categoryName))
    mysqlCon.commit()

def checkIdIfExtist(Id, date):
    
    #連接資料庫
    mysqlCon = pymysql.connect('162.241.252.14', 
                           port = 3306, 
                           user = 'toolsof6_YunXiuRZ', 
                           passwd = 'Jerrykao1022', 
                           charset = 'utf8', 
                           db = 'toolsof6_ckSchoolPost')
    cursor = mysqlCon.cursor()
    
    #定義搜尋指令
    mysqlExecution = """
    SELECT post_id
    FROM ckSchoolPost
    WHERE post_date = %s"""
    
    #執行搜尋
    cursor.execute(mysqlExecution, date)
    sqlidList = cursor.fetchall()
    
    #存在則回傳True，反之則回傳False
    for sqlId in sqlidList:
        checkId = re.search('[0-9]{5}', str(sqlId)).group()
        if(checkId == Id):
            return True
    return False

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
    postDate = "%s-%s-%s" % (dateList[0], dateList[1], dateList[2])
    localDate = time.strftime("%Y-%m-%d", time.localtime())
    
    
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
    
    #獲取公告附加鏈接
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
    
    #取得公告類別
    categoryName = getCategory(ID)
    
    #插入數據至資料庫
    if(localDate == postDate):
        localTime = time.strftime("%H:%M", time.localtime())
        insertData(ID, 
               title, 
               postDate,
               localTime,
               postOffice,
               postRoom,
               articleText,
               annex,
               categoryName
               )
    else:
        insertData(ID, 
               title, 
               postDate,
               "08:00(預設值)",
               postOffice,
               postRoom,
               articleText,
               annex,
               categoryName
               )


def getCategory(ID):
    
    #取得公告類別列表
    postUrl = "https://www2.ck.tp.edu.tw/news?page=1"
    r = requests.get(postUrl)
    r.encoding = 'utf8'
    bs = BeautifulSoup(r.text, 'lxml')
    remarksUrl = bs.find(attrs = {"class" : "NavLinks__NavListContent-sc-3sx2bx-7 bOgVYk"})
    
    remarkUrlList = remarksUrl.find_all(attrs = {"class" : "NavLinks__NavList-sc-3sx2bx-1 bdczja"})
    remarkUrlList.reverse()
    remarkUrlList.pop()
    for remarkUrl in remarkUrlList:
        
        Id = re.search(r'category/[0-9]{1}$', remarkUrl.get("href")).group()
        
        categoryUrl = "https://www2.ck.tp.edu.tw/news/" + Id
        r = requests.get(categoryUrl)
        r.encoding = 'utf8'
        bs = BeautifulSoup(r.text, 'lxml')
        posts = bs.find(attrs = {"class" : "List__ListContainer-sc-1li2krx-10 hGuVdB"})
        postList = posts.find_all(attrs = {"class" : "List__ItemLink-sc-1li2krx-8 fiVYKj"})
        for post in postList:
            if(("/news/" + ID) == post.get("href")):
                return remarkUrl.text
    return "noneCategory"
    
#爬蟲起始
#取得公告總覽原始碼
postUrl = "https://www2.ck.tp.edu.tw/news?page=1"
r = requests.get(postUrl)
r.encoding = 'utf8'
bs = BeautifulSoup(r.text, 'lxml')

#取得9項公告ID
posts = bs.find(attrs = {"class" : "List__ListContainer-sc-1li2krx-10 hGuVdB"})
postList = posts.find_all(attrs = {"class" : "List__ItemLink-sc-1li2krx-8 fiVYKj"})
idList = []
for post in postList:
    
    #取最後五位數組爲ID
    Id = re.search(r'[0-9]{5}$', post.get("href")).group()
    idList.append(Id)




#檢查該ID是否已存在在資料庫
for Id in idList:
    
    requestUrl = "https://www2.ck.tp.edu.tw/news/" + Id
    r = requests.get(requestUrl)
    r.encoding = "utf8"
    bs = BeautifulSoup(r.text,'lxml')
    date = bs.find(attrs = {"class" : "date"}).text
    dateList = date.split("/")
    postDate = "%s-%s-%s" % (dateList[0], dateList[1], dateList[2])
    if(checkIdIfExtist(Id, postDate) == False):
        insertPostData(Id)
    else:
        break
