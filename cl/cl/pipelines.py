# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib
import random
from urllib import request
from settings import save_local
from settings import save_mongo
from settings import mongo_conn
from settings import save_dir
from settings import headers
from settings import USER_AGENTS
from settings import item_exclude
import traceback
import sqlite3
import redis

class ClPipeline(object):
    m = hashlib.md5()

    def __init__(self):
        self.conn = redis.Redis(host='localhost', port=6379, db=0)
#        self.conn = sqlite3.connect(save_dir + "pic_key.db")
#        self.conn.execute("create table if not exists md5_filename(id text primary key, filename text);")
#        self.conn.commit()

    @staticmethod
    def report_hook(count, block_size, total_size):
        print('%02d%%' % (100.0 * count * block_size / total_size))
    
    def process_item(self, item, spider):
        url = item["url"]
        for exc in item_exclude:
            if exc in url:
                return
        headers['User-Agent'] = random.choice(USER_AGENTS)
        req = request.Request(url,headers = headers)
        try:
            filename = url.split("/")[-1]
            print("dealing with file %s ..."%filename)
            res = request.urlopen(req,timeout=20)
        except:
            s = traceback.format_exc()
            print(url +" headers\t:"+str(headers)+"\n" + s)
            return
        bc = res.read()
        self.m.update(bc)
        if save_local:
            md5 = self.m.hexdigest()
            if self.insert_value(md5,url):
                with open(save_dir+md5+"."+filename.split(".")[-1],"wb") as f:
                    f.write(bc)
            else:
                print("%s skiped"%filename)
            print("file %s done" % filename)

    def insert_value(self,md5,filename):
        if self.conn.setnx("file:"+md5,filename):
            print("keep %s"%filename)
            return True
        else:
            print("skip")
            return False
 #       try:
 #           self.conn.execute("insert into md5_filename values(?,?);",(md5,filename))
 #           return True
 #       except:
 #           s = traceback.format_exc()
 #           print(s)
 #           return False

 #   def __del__(self):
 #       self.conn.commit()
 #       self.conn.close()
