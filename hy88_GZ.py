#-*- coding: utf-8 -*-
import sys
import requests
import re 
import csv
import time
from bs4 import BeautifulSoup

'''This script is written to crawl company
contact informtion in 9 industries in Guangzhou
from huangye88, a Chinese yellow page website
'''

def getPageUrl():
    
    list = []
    #define the list of industries we want to get company information in
    catelist = ['fuwu','wangluo1438','ruanjian1720','guanggao','fanyi','xiangmuhezuo','wangzhan','zhanhui','jiaoyu']

    for cate in catelist:
        #get the first result page's url
        #for companies in other cities, just change guangzhou in url to beijing etc.
        page1Url = r"http://b2b.huangye88.com/guangzhou/" + cate
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
        page1 = requests.get(page1Url, headers=headers)
        #to avoid being detected as a crawler
        time.sleep(2)
        soup = BeautifulSoup(page1.text, 'lxml')  

        #find out the total number of search results 
        resultNo = int(soup.find('em').string)
        pageNo = resultNo/20 + 1
        
        #append all pages' urls to list for one category
        for i in range(1, pageNo):
            pageUrl = page1Url + '/pn' + str(i)
            list.append(pageUrl)

    return list

def getComInfoList(url):
    infoList = []
    
    #open the result page
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}
    try:
        resultPage = requests.get(url,headers=headers)
    except requests.ConnectionError:
        time.sleep(10)
        print "Connection Error!"
        return None
    
    #make the page a beautifulsoup object
    soup = BeautifulSoup(resultPage.text, "lxml")

    #find the form that holds the list of companies
    companies = soup.find('form', id='jubao')
    if companies == None:
        return None

    #find all <dl> tags that contains company info
    companies = companies.find_all('dl')
    for company in companies:
        comInfo = {}

        h4 = company.find('h4')
        if h4 == None:
            continue
        else:
            name = h4.a.string
            comInfo['name'] = name
            
        comInfo['mobile'] = company.find('span').a.string

        infoList.append(comInfo)
        
    return infoList



if __name__ == '__main__':
    #to output Chinese character without error
    reload(sys)
    sys.setdefaultencoding('utf-8')
        
    #get every search result page's url
    pageUrlList = getPageUrl()
    print "There are %s pages" %len(pageUrlList)

    #to count page number
    page = 0
    
    with open('88_Guangzhou.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name','mobile', 'city', 'infoSrc'])
        
        for pageUrl in pageUrlList:
            comInfoList = getComInfoList(pageUrl)
            if comInfoList == None:
                time.sleep(10)
                continue
            for company in comInfoList:
                writer.writerow([company['name'],company['mobile'],'Guangzhou','hy88'])
            time.sleep(1)
            if page%8 == 0:   #every 8 pages crawled, pause for 2 second
                time.sleep(2)
            page += 1
            print page

    