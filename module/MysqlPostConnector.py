import pymysql
from PostInformationGetter import PostInformationGetter
       

class MysqlPostConnector():
    
    mysqlCon = pymysql.connect(host='162.241.252.14', 
                           port=3306, 
                           user='toolsof6_YunXiuRZ', 
                           passwd='Jerrykao1022', 
                           charset='utf8', 
                           db='toolsof6_ckSchoolPost')
    cursor = mysqlCon.cursor()

    def checkPostExist(self, ID):
        mysqlExecution ="""
                        SELECT post_id
                        FROM ckSchoolPost
                        WHERE post_id = %s 
                        """
        self.cursor.execute(mysqlExecution, ID)
        sqlid = self.cursor.fetchone()
        if(sqlid == None):
            return False
        else:
            return True
        
    def checkIfPostUpdate(self, pig):
        mysqlExecution ="""
                        SELECT post_title, post_date, article
                        FROM ckSchoolPost
                        WHERE post_id = %s 
                        """
        self.cursor.execute(mysqlExecution, pig.postID)
        datas = self.cursor.fetchall()
        if(datas[0][0] != pig.postTitle):
            return True
        if(str(datas[0][1]) != pig.postDate):
            return True
        if(datas[0][2] != pig.postText):
            return True
    
    def execute(self, pig):
        if(self.checkPostExist(pig.postID)):
            if(self.checkIfPostUpdate(pig)):
                self.updatePostData(pig)
        else:
            self.insertPostData(pig)
    
    def updatePostData(self, pig):
        mysqlExecution ="""
                        UPDATE ckSchoolPost
                        SET post_title = %s,
                            post_date = %s,
                            post_time = %s,
                            article = %s,
                            annex = %s,
                            is_posted
                        """
        self.cursor.execute(mysqlExecution, (pig.postTitle,
                                            pig.postDate,
                                            pig.postTime,
                                            pig.postText,
                                            pig.postAnnex,
                                            2)
                                            )
        self.mysqlCon.commit()
        
                        
    def insertPostData(self, pig):
        
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
        self.cursor.execute(mysqlExecution, (pig.postID, 
                                            pig.postTitle,
                                            pig.postDate,
                                            pig.postTime,
                                            pig.postOffice,
                                            pig.postRoom,
                                            pig.postText,
                                            pig.postAnnex,
                                            0,
                                            pig.postCategory)
                                            )
        self.mysqlCon.commit()
        
"""pig = PostInformationGetter("13511")
pig.setInformation()
mpc = MysqlPostConnector()
mpc.execute(pig)"""
