# -*- coding: utf-8 -*
import pymysql
import re
import requests
from bs4 import BeautifulSoup
import sys
sys.path.append('module/')
from PostInformationGetter import PostInformationGetter
from MysqlPostConnector import MysqlPostConnector

def get_post():
    print("獲取近期公告")
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
        print(Id, end=' ')
    print('')

    #檢查該ID是否已存在在資料庫
    for Id in idList:
        print("取得編號%s公告內容" % Id)
        pig = PostInformationGetter(Id)
        pig.setInformation()
        print("處理編號%s公告內容" % Id)
        mpc = MysqlPostConnector()
        mpc.execute(pig)
   
if __name__ == '__main__':
    get_post()
