#coding:utf-8
'''我的网页爬虫程序'''
import urllib, urllib2, socket
from bs4 import BeautifulSoup
import re
import random, zlib

def getHtmlHeader(url):
    '''
    @伪造头信息访问网页
    '''
    my_headers = [
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
              "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/5.0)"
              ]
    random_header = random.choice(my_headers)
    return random_header

class linkQuence:
    '''
    @链队列，操作访问的连接，确保每个连接只访问一次。防止重复抓取。
    '''
    def __init__(self):
        #已访问的url集合
        self.visited=[]
        #待访问的url集合
        self.unVisited=[]
    #获取访问过的url队列
    def getVisitedUrl(self):
        return self.visited
    #获取未访问的url队列
    def getUnvisitedUrl(self):
        return self.unVisited
    #添加到访问过的url队列中
    def addVisitedUrl(self, url):
        self.visited.append(url)
    #移除访问过的url
    def removeVisitedUrl(self, url):
        self.visited.remove(url)
    #未访问过的url出队列
    def unVisitedUrlDequence(self):
        try:
            return self.unVisited.pop()
        except:
            return None
    #保证每个url只被访问一次
    def addUnvisitedUrl(self, url):
        if url != "" and url not in self.visited and url not in self.unVisited:
            self.unVisited.insert(0, url)
    #获得已访问的url数目
    def getVisitedUrlCount(self):
        return len(self.visited)
    #获得未访问的url数目
    def getUnvisitedUrlCount(self):
        return len(self.unVisited)
    #判断未访问的url队列是否为空
    def unVisitedUrlEnmpy(self):
        return len(self.unVisited) == 0
    
#照网上的抄吧。爬虫的类
class MyCrawler():
    def __init__(self, seeds):
        #初始化当前抓取的深度
        self.current_deepth = 1
        #使用种子初始化url队列
        self.linkQuence = linkQuence()
        if isinstance(seeds, str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds, list):
            for i in seeds:
                self.linkQuence.addUnvisitedUrl(i)
        print u"种子连接\"%s\"加入了未访问链接列表" % str(self.linkQuence.unVisited)
    #判断currentUrl与aimUrl是否是一个网站
    def judgeUrl(self, currentUrl, aimUrl):
        currentUrl = re.findall(r'http://.*?(?=/)', currentUrl)
        if currentUrl == aimUrl:
            return True
        return False
    #抓取过程主函数
    def crawling(self, seeds, aimUrl, crawl_deepth):
        #循环条件：抓取深度不超过crawl_deepth
        while self.current_deepth <= crawl_deepth:
            tempList = []    #用来保存循环中找到的新的链接
            #循环条件：待抓取的链接不空
            while not self.linkQuence.unVisitedUrlEnmpy():
                #队头url出列
                visitUrl = self.linkQuence.unVisitedUrlDequence()
                print u"\"%s\"正在抓这个网址" % visitUrl
                if visitUrl is None or visitUrl == "":
                    continue
                if self.judgeUrl(visitUrl, aimUrl):
                    return self.current_deepth
                #获取超链接
                links = self.getHyperLinks(visitUrl)
                #未访问的url放入临时的列表中
                for link in links:
                    tempList.append(link)
                #将url放入已访问的url中
                self.linkQuence.addVisitedUrl(visitUrl)
                print u"访问链接计数:" + str(self.linkQuence.getVisitedUrlCount()) + u" 未访问链接计数:" + str(self.linkQuence.getUnvisitedUrlCount()) + u"当前深度:" + str(self.current_deepth)
            #将上面循环中找到的所有未访问的url入列
            for link in tempList:
                self.linkQuence.addUnvisitedUrl(link)
            print u"%d个未访问链接:" % len(self.linkQuence.getUnvisitedUrl())
            print u"当前抓取深度为:%d" % self.current_deepth
            self.current_deepth += 1
        return -1
    
    #获取源码中的超链接
    def getHyperLinks(self, url):
        links = []
        data = self.getPageSource(url)
        
        if data[0] == "200":
            soup = BeautifulSoup(data[1])
            a = soup.findAll("a", {"href":re.compile(".*")})
            for i in a:
                if i["href"].find("http://") != -1:
                    links.append(i["href"])
        else:
            print u"获取当前网页失败，错误信息:", data[0]
        return links
    
    #获取网页源码
    def getPageSource(self, url, timeout=100, coding=None):
        try:
            socket.setdefaulttimeout(timeout)
            req = urllib2.Request(url)
            header = getHtmlHeader(url)
            req.add_header("User-Agent", header)
            response = urllib2.urlopen(req)
            page = ''
            if response.headers.get('Content-Encoding') == 'gzip':
                page = zlib.decompress(page, 16+zlib.MAX_WBITS)
                
            if coding is None:
                coding = response.headers.getparam("charset")
            #如果获取的网站编码为None
            if coding is None:
                page = response.read()
            #获取网站编码并转化为utf-8
            else:
                page = response.read()
                page = page.decode(coding).encode('utf-8')
            return ["200", page]
        except Exception, e:
            print str(e)
            return [str(e), None]
        
def main(seeds, aimUrl, crawl_deepth):
    craw = MyCrawler(seeds)
    dis = craw.crawling(seeds, aimUrl, crawl_deepth)
    print seeds + u"与" + aimUrl + u"之间的距离为:" + str(dis)
    
if __name__ == "__main__":
    url = raw_input(u"输入种子网址:")
    aimUrl = raw_input(u"输入目标网址:")
    if url[0:7] != "http://":
        url = "http://" + url
    if aimUrl[0:7] != "http://":
        aimUrl = "http://" + aimUrl
    main(url, aimUrl, 10)