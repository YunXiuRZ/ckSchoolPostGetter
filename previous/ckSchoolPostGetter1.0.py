from bs4 import BeautifulSoup
import requests
import pymysql
import re




requestUrl = input()
ID = repr(re.search(r'[0-9]{5}$', requestUrl).group())
r = requests.get(requestUrl)
r.encoding = "utf8"
bs = BeautifulSoup(r.text,'lxml')
title = bs.find("h4").text
date = bs.find(attrs = {"class" : "date"}).text
dateList = date.split("/")
office = bs.find(attrs = {"class" : "office"}).text.split(" ")
postOffice = office[0]
postRoom = office[1]
article = bs.find(attrs = {"class" : "Page__RedactorBlock-sc-1geffe8-0 redactor-styles hkzaDk"})
lineList = article.find_all("p")
links = bs.find_all(attrs = {"class" : "Post__LinkWrapper-kr2236-3 iaPBqD"})
articleText = ""
for line in lineList:
    articleText +=line.text
    articleText +="\n"
        
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
mysqlCon = pymysql.connect('151.106.116.103', 
                           port = 3306, 
                           user = 'u435584478_YunXiuRZ', 
                           passwd = 'Jerrykao1022', 
                           charset = 'utf8', 
                           db = 'u435584478_Schoolpost')
cursor = mysqlCon.cursor()
#插入指令
mysqlExecution = """
        INSERT INTO SchoolPost (article_id, 
                                article_title, 
                                post_date, 
                                post_time, 
                                post_office, 
                                post_room, 
                                article_text,
                                article_annex)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """%(ID, 
             repr(title), 
             repr("%s-%s-%s" %(dateList[0], dateList[1], dateList[2])),
             repr('08:00:00'),
             repr(postOffice),
             repr(postRoom),
             repr(articleText),
             repr(str(annex_dic))
             )
        
cursor.execute(mysqlExecution)
mysqlCon.commit()         
