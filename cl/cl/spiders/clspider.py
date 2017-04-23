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


class clspider(scrapy.spiders.Spider):
    name = "cl"
    uh = "http://c6.bvaz.club/"
    allowed_domains = []
    start_urls = ["http://c6.bvaz.club/thread0806.php?fid=7"
                  ]
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Connection': 'keep-alive'}

    def __init__(self):
        str = "(.*("
        for ru in rules:
            str = str + ru + "|"
        str = str[:-1] + ").*([3-9][0-9])[p,P].*)|(.*一夜精品.*)"
        self.p = re.compile(str)
        del str
        
    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            for j in numpy.arange(1,2,1):
                self.headers['User-Agent'] = random.choice(USER_AGENTS)
                yield scrapy.Request(url+"&page={j}".format(j=j),headers=self.headers,callback=self.parse)

    
    
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
                    str = self.uh + str
                yield scrapy.Request(str, self.parse, headers=self.headers)
        except:
            s = traceback.format_exc()
            print(s)
            return
        
        item = ClItem()
        #nodes = response.css("html body div#main div.t table#ajaxtable tbody tr.tr3.t_one.tac td.tal h3 a").extract() #\
        #chardet.detect(response.body)
        #       and position()<last()]/td[2]/h3/a")
        
        yield item


