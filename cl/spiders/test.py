import hashlib
from urllib import request

import wget as wget
from matplotlib import pyplot


def getmd5( filename):
    m = hashlib.md5()
    with open(filename) as f:
        return m.update(f.read())

headers = {'User-Agent':
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language':'en-US,en;q=0.5',
           'Accept-Encoding':'gzip, deflate, br',
           'Connection':'keep-alive'}

#req = request.Request("https://go.imgs.co/u/2017/04/17/6h1v3s.gif",headers=headers)#"https://go.imgs.co/u/2017/04/17/6h1v3s.gif")
#req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0')
#request.urlretrieve("http://wanzao2.b0.upaiyun.com/system/pictures/40342003/original/1492591077_444x211.gif",'test.gif')
#res = request.urlopen(req)
#print("===")
#with open("test.gif","wb") as f:
#    f.write(res.read())
def report_hook(count, block_size, total_size):
    print('%02d%%'%(100.0 * count * block_size/ total_size))
#request.urlretrieve("http://img1.mm131.com/pic/1724/30.jpg",filename="test.jpg",
#                    reporthook=report_hook)
"""
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read())
"""

