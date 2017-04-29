import requests ##导入requests
import re
from bs4 import BeautifulSoup
from urllib.request import *
from  gzip import GzipFile
from io import BytesIO
from settings import test_URl
from settings import num_IP

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'Accept-Encoding':'gzip',
           }


IP_test_timeout=1#测试IP时超过多少秒不响应就舍弃了


'''
有效ip太少
def get_url_ip():
    ip_list = []
    for i in np.arange(1,9,1):
        if i == 1:
            proxy_net = 'http://www.kuaidaili.com'
        else:
            proxy_net = 'http://www.kuaidaili.com/proxylist/{i}'.format(i=i)
        html = requests.get(proxy_net,headers=headers)
        bs = BeautifulSoup(html.text,"lxml")
        ip = bs.find_all("td",attrs={"data-title":"IP"})
        port = bs.find_all("td",attrs={"data-title" : "PORT"})
        for j in np.arange(len(ip)):
            span_IP = ip[j].text+":"+port[j].text
            if IP_Test(span_IP, test_URl):  # 测试通过
                ip_list.append(span_IP)
                print('测试通过，IP地址为' + str(span_IP))
                if len(ip_list) > num_IP - 1:  # 搜集够N个IP地址就行了
                    print('搜集到' + str(len(ip_list)) + '个合格的IP地址')
    return ip_list
'''
def IP_Test(IP,URL_test,set_timeout=IP_test_timeout):#测试IP地址是否可用,时间为3秒
    try:
        requests.get(URL_test, headers=headers, proxies={'http': IP }, timeout=set_timeout)
        return True
    except:
        return False

def get_IPlist(URL,testurl):#获取可用的IP地址
    IP_list=[]
    start_html = requests.get(URL, headers=headers)
    start_html.encoding = 'utf-8'
    bsObj = BeautifulSoup(start_html.text, 'html.parser')
    for span in bsObj.find("div", {"class": "content"}).findAll("p"):
        span_IP=re.findall(r'\d+.\d+.\d+.\d+:\d+', span.text)
        if IP_Test(span_IP[0],testurl):#测试通过
            IP_list.append(span_IP[0])
            print('测试通过，IP地址为'+str(span_IP))
            if len(IP_list)>num_IP-1: #搜集够N个IP地址就行了
                print('搜集到'+str(len(IP_list))+'个合格的IP地址')
                return IP_list
    return IP_list

def get_new_url():
    net = "http://www.youdaili.net/Daili/http/"
    req = Request(net, headers=headers)
    res = urlopen(req)
    bc = res.read()
    gz = GzipFile(fileobj=BytesIO(bc))
    bs = BeautifulSoup(gz.read(),"lxml")
    tag = bs.find("div",attrs={"class":"chunlist"})
    return tag.a["href"]

base_url = get_new_url()
PROXIES = get_IPlist(base_url,test_URl)

