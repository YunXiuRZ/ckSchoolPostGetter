# -*- coding: utf-8 -*
from bs4 import BeautifulSoup
import requests
import re
import time


class PostInformationGetter():
    
    postTime = "08:00(default)"
    postCategory = "noneCategory"
    
    def __init__(self, ID):
        self.postID = ID
        requestUrl = "https://www2.ck.tp.edu.tw/news/" + self.postID
        r = requests.get(requestUrl)
        r.encoding = "utf8"
        self.bs = BeautifulSoup(r.text,'lxml')
        
    def setID(self, ID):
        self.postID = ID
        requestUrl = "https://www2.ck.tp.edu.tw/news/" + self.postID
        r = requests.get(requestUrl)
        r.encoding = "utf8"
        self.bs = BeautifulSoup(r.text,'lxml')
        
    def setPostTitle(self):
        self.postTitle = self.bs.find("h4").text
        
    def setPostDate(self):
        date = self.bs.find(attrs = {"class" : "date"}).text
        dateList = date.split("/")
        self.postDate = "%s-%s-%s" % (dateList[0], dateList[1], dateList[2])   

    def setPostTime(self):
        localDate = time.strftime("%Y-%m-%d", time.localtime())
        if(localDate == self.postDate):
            self.postTime = time.strftime("%H:%M", time.localtime())

    def setPostOfficeAndRoom(self):
        officeList = self.bs.find(attrs = {"class" : "office"}).text.split(" ")
        self.postOffice = officeList[0]
        self.postRoom = officeList[1]

    def setPostText(self):
        article = self.bs.find(attrs = {"class" : "Page__RedactorBlock-sc-1geffe8-0 redactor-styles hkzaDk"})
        lineList = article.find_all("p")
        self.postText = ""
        for line in lineList:
            self.postText +=line.text
            self.postText +="\n"
        self.postText+=article.text

    def setAnnex(self):
        links = self.bs.find_all(attrs = {"class" : "Post__LinkWrapper-kr2236-3 iaPBqD"})   
        annex_dic = {}
        for link in links:
            header = link.find("p").text
            urls = link.find_all("a")
            dicIn = {}
            for url in urls:
                herf = url.get("href")
                dicIn[url.text] = herf
                annex_dic[header] = dicIn
        self.postAnnex = str(annex_dic)
        
    def setCategory(self):
    
        #取得公告類別列表
        postUrl = "https://www2.ck.tp.edu.tw/news?page=1"
        r = requests.get(postUrl)
        r.encoding = 'utf8'
        bsc = BeautifulSoup(r.text, 'lxml')
        categoriesUrl = bsc.find(attrs = {"class" : "NavLinks__NavListContent-sc-3sx2bx-7 bOgVYk"})
    
        categoryUrlList = categoriesUrl.find_all(attrs = {"class" : "NavLinks__NavList-sc-3sx2bx-1 bdczja"})
        categoryUrlList.reverse()
        categoryUrlList.pop()
        for categoryUrl in categoryUrlList:
        
            Id = re.search(r'category/[0-9]{1}$', categoryUrl.get("href")).group()
        
            categoryPostsUrl = "https://www2.ck.tp.edu.tw/news/" + Id
            r = requests.get(categoryPostsUrl)
            r.encoding = 'utf8'
            bsc = BeautifulSoup(r.text, 'lxml')
            posts = bsc.find(attrs = {"class" : "List__ListContainer-sc-1li2krx-10 hGuVdB"})
            postList = posts.find_all(attrs = {"class" : "List__ItemLink-sc-1li2krx-8 fiVYKj"})
            for post in postList:
                if(("/news/" + self.postID) == post.get("href")):
                    self.postCategory = categoryUrl.text

    def setInformation(self):
        self.setPostTitle()
        self.setPostDate()
        self.setPostTime()
        self.setPostOfficeAndRoom()
        self.setPostText()
        self.setAnnex()
        self.setCategory()
        
