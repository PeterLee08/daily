# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib


class ClPipeline(object):
    def process_item(self, item, spider):

        return item

    def getmd5(self, filename):
        m = hashlib.md5()
        with open(filename) as f:
            return m.update(f.read())
