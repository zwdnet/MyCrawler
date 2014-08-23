#coding:utf-8
'''我的网页爬虫程序'''
import urllib, urllib2
from bs4 import BeautifulSoup
import re
import random

def getWeb(url):
    '''
    @抓取指定链接的网页
    '''
    html = getHtml(url)
    if html == 0:
        return 0
    elif html.getcode() != 200:
        return 0
    return html

def getNextUrl(html):
    '''
    @获取html页面中的链接
    '''
    urls = []
    soup = BeautifulSoup(html)
    a = soup.findAll("a", {"href":re.compile(".*")})
    for i in a:
        if i["href"].find("http://") != -1:
            urls.append(i["href"])
    return urls

def getHtml(url):
    '''
    @伪造头信息访问网页
    '''
    my_headers = [
              "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
              "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)",
              "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/5.0)"
              ]
    random_header = random.choice(my_headers)
    req = urllib2.Request(url)
    req.add_header("User-Agent", random_header)
    req.add_header("GET", url)
    try:
        html = urllib2.urlopen(req)
    except:
        html = 0
    return html

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

if __name__ == "__main__":
    url = "http://bl.cdn.net/"
    html = getWeb(url)
    if html != 0:
        print html.info()
        urls = getNextUrl(html)
        if urls != []:
            print urls
        html.close()
    else:
        print u"抓取失败"
