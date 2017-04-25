import random

import chardet
import numpy
import re
import traceback
import scrapy
from settings import USER_AGENTS
from settings import rules
from bs4 import BeautifulSoup
from items import ClItem
from settings import headers
from settings import num_page
from settings import start_urls
from settings import head_if_not_exist
from settings import keep_if_exist_word

class clspider(scrapy.spiders.Spider):
    name = "cl"
    add_head = head_if_not_exist
    allowed_domains = []
    start_urls = start_urls

    def __init__(self):
        str = "(.*("
        for ru in rules:
            str = str + ru + "|"
        str = str[:-1] + ").*([3-9][0-9])[p,P].*)"
        for aru in keep_if_exist_word:
            str = str + "|(.*"+ aru +".*)"
        self.p = re.compile(str)
        del str
        
    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            for j in numpy.arange(1,num_page,1):
                headers['User-Agent'] = random.choice(USER_AGENTS)
                yield scrapy.Request(url+"&page={j}".format(j=j),headers=headers,callback=self.parse)
    
    
    def has_text(self, tag):
        if tag.name == u'a':
            return self.p.match(tag.text)
        else:
            return False
        

    def parse(self, response):
        try:
            bs = BeautifulSoup(response.body, "html5lib")
            nodes = bs.findAll(self.has_text)
            for node in nodes:
                str = node['href']
                if not str.startswith("http"):
                    str = self.add_head + str
                yield scrapy.Request(str, self.parse_item, headers=headers)
        except:
            s = traceback.format_exc()
            print(s)
    
    def parse_item(self, response):
        try:
            item = ClItem()
            bs = BeautifulSoup(response.body, "html5lib")
            nodes = bs.findAll("img")
            for nd in nodes:
                if nd.has_attr("onclick"):
                    uri = nd["src"]
                    if not uri.startswith("http"):
                        scrapy.log.ERROR("src img  not startswith http")
                        return
                    item["url"] = uri
                    yield item
                    
        except:
            s = traceback.format_exc()
            print ("parse iterm === \n" + s)


