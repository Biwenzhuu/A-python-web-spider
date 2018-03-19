#coding:cp936
import sqlite3
import re
class dbhand:
    def __init__(self,logger):
        self.logger = logger
    def dbconnect(self,info):
        self.dbcon = None
        try:
            self.dbcon = sqlite3.connect(info,isolation_level="DEFERRED",check_same_thread=False)
            self.con = self.dbcon.cursor()
            self.logger.info("蔴as already connetced to database.")
        except:
            self.logger.info("Failed to connect to database.")
            print("Failed to connect to database.")
            quit()
    def initdatabase(self):
       
        try:
            sql1 = """create table if not exists urls
(url text primary key,title text,inurl integer default 0,outurl integer default 0,jumpnumber integer default 0,jumptype text default null ,deep integer default 0,response integer default 0,jumpinfo text default null)

"""
            self.con.execute(sql1)
            self.logger.info("Init the data table successfully ")
        except:
            self.logger.error("蔉ail to init the data table")
            pass

    def insertone(self,info,table):
        sql1 = "insert or ignore into `%s` "%table
        name = []
        value = []
        try:
            for k,v in info.iteritems():
                name.append("`%s`"%(str(k)))
                value.append("'%s'"%(str(v)))
        except UnicodeEncodeError:
            pass
        namestr = ','.join(name)
        valuestr = ','.join(value)
        sql2 = "(%s)values(%s)"%(namestr, valuestr)
        sql = sql1+sql2
        print "#######"+sql
        try:
            self.con.execute(sql)
            self.dbcon.commit()
        except sqlite3.IntegrityError:
            pass
        except:
            pass

        pass
    def commitall(self):
        try:
            self.dbcon.commit()
        except sqlite3.IntegrityError:
            pass
        except:
            pass

    def updateone(self,info,table,where = ''):
  
        print "*******************************************"
        try:
            self.con.execute("""update `urls` set title=?,inurl=?,jumpnumber=?,
jumpinfo=?,outurl=?,response=? where url = ?
""",(info['title'],info['inurl'],info['jumpnumber'],info['jumpinfo'],info['outurl'],info['response'],info['url']))
            self.dbcon.commit()
        except TypeError:#sqlite3.IntegrityError:
            pass


        pass
    def geturls(self,info,workid):
    
        sql = "insert into urls (url,did,wid) values ('%s','%s','%s')"%(info['url'],info['did'],workid)
        try:
            self.con.execute(sql)
            self.dbcon.commit()
        except sqlite3.IntegrityError:
            pass
        except:
            self.logger.error(str(info['did'])+"depth"+str(info['url'])+"cannot connect to database")


    def selecturls2(self):
        info = {}
        allurl = []
        sql = "select url from urls where response = '0'"
        self.con.execute(sql)
        for i in self.con.fetchall():
            info['url'] = i[0]
            allurl.append(info)
            info = {}
        return allurl

    def getone(self,table,var = '*', where = ''):
        sql = "select "+var+" from "+table+where
        self.con.execute(sql)
        result = self.con.fetchone()
        return result[1]
