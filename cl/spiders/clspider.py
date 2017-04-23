import chardet
import scrapy
from items import ClItem


class clspider(scrapy.spiders.Spider):
    name = "cl"
    allowed_domains = []
    start_urls = ["http://c6.bvaz.club/thread0806.php?fid=7"
                  ]
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br',
               'Connection': 'keep-alive'}

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield scrapy.Request(url,headers=self.headers,callback=self.parse)

    uh = "ttp://c6.bvaz.club/"

    def parse(self, response):
        item = ClItem()
        nodes = response.css("html body div#main div.t table#ajaxtable tbody tr.tr3.t_one.tac td.tal h3 a").extract() #\
        print(nodes[10])
        print(chardet.detect(response.body))
 #       and position()<last()]/td[2]/h3/a")
        with open("test",'wb') as f:
            f.write(response.body)

        yield item



