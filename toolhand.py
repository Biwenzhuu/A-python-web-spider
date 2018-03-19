import urllib2
from BeautifulSoup import BeautifulSoup
import re
from sqlhand import dbhand
import logging
from collections import deque
import time
from urlparse import urlparse
from httphand import httphand
from Queue import Queue
import cPickle
from sets import Set
def getlog(info):
      logger = logging.getLogger()
      hdlr = logging.FileHandler(info['logfile'])
      formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
      hdlr.setFormatter(formatter)
      logger.addHandler(hdlr)
      try:
          logger.setLevel(info['loglevel'])
      except:
          print "the log you typed is not correct."
      return logger

def getaurl(info):
    tmp = {}
    urls = {}
    try:
        xsdanx = httphand()
        result = xsdanx.geturl(info)
        if result is None:
              tmp['url'] = info
              tmp['response'] = 404
              tmp['title'] = ''
              tmp['inurl'] = 0
              tmp['outurl'] = 0
              tmp['jumpnumber'] = 0
              tmp['jumpinfo'] = ''
              pass
        else:
              sop = BeautifulSoup(result['data'])
              urls = sop.findAll("a",{'href':True})
              try:
                    title = sop.head.title.string
              except AttributeError:
                    title = "null"
              tmp['response'] = result['response']
              tmp['title'] = title
              tmp['url'] = info
              urltype = checkurl2(info,urls)
              tmp['inurl'] = urltype['inurl']
              tmp['outurl'] = urltype['outurl']
              tmp['jumpnumber'] = result['jumpnumber']
              tmp['jumpinfo'] = mkjumpinfo(result['jumpinfo'])
        return (tmp,urls)
    except (urllib2.URLError,TypeError,UnicodeEncodeError):
          return (tmp,urls)
def mkjumpinfo(info):
      tmp = []
      for i in info:
            tmp.append(re.escape(cPickle.dumps(i)))
      return "|".join(tmp)
      pass
def checkurl2(url,text):
    inurl = 0
    outurl = 0
    valid = re.compile("^"+url+".*$")
    tmp = {}
    tmp['inurl'] = 0
    tmp['outurl'] = 0
    for i in text:
        try:
            if valid.match(i['href']) is None:
                tmp['outurl'] += 1
            else:
                tmp['inurl'] += 1
        except:
            pass
    return tmp
def allstar(info,db):
    (thetest,urls) = getaurl(info['url'])
    if len(thetest)  > 0 :
          db.updateone(thetest,'urls')
    if len(urls) > 0 :
          urlsget(urls,db)

def checkurl(text):
    valid = re.compile("^[http|https].*$")

    if valid.match(text) is None:
        return False
    else:
        return True

def urlsget(urls,db):
    tmp = {}
    tmp2 = ''
    ttmp = set([])
    for i in urls:
          try:
                tmp2 = urlparse(i['href'])
                tmp['url'] = tmp2.scheme+"://"+tmp2.netloc
                if checkurl(tmp['url']) :
                      if tmp['url'] not in ttmp:
                            db.insertone(tmp,'urls')
                            ttmp.add(tmp['url'])
          except (TypeError,KeyError,ValueError):
                pass

