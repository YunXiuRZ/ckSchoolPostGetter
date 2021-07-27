# ckSchoolPostGetter



PostInformationGetter.py:

	PostInformationGetter會根據輸入的公告id進行信息爬取，將id、標題、發佈日期、發佈時間、發佈處室、內文、附件以及公告類別儲存為資料結構
	
MysqlPostConnector.py:

	會將PostInformationGetter與資料庫對比，判別是新公告、重複公告抑或公告更新，執行對應操作更新資料庫

ckSchoolPostGetter.py:

	會將校網上最新的9則公告爬取下來，並利用PostInformationGetter取得該公告的信息後，交給MysqlPostConnector執行操作

ckSchoolPostPusher:

	每次執行會從資料庫中傳回未推送過的公告，並利用line notify推送消息
