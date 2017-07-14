#-*- coding: utf-8 -*-
import sys
import requests
import re 
import time
import csv

'''This script is written to crawl contact information
of companies in some given industries in Shenzhen, China, 
from Baidu Map, adapted from script in this website: 
https://zhuanlan.zhihu.com/p/25778570'''

def comFromBaidu(key_word, pageno):
    parameter = {
    "newmap":"1",
    "reqflag":"pcmap",
    "biz": "1",
    "from": "webmap",
    "da_par": "direct",
    "pcevaname": "pc4.1",
    "qt": "con",
    "c": '340',           #city code
    "wd": key_word,       #search key word
    "wd2": "",
    "pn": pageno,         #page number
    "nn": pageno * 10,
    "db": "0",
    "sug": "0",
    "addr": "0",
    "da_src": "pcmappg.poi.page",
    "on_gel": "1",
    "src": "7",
    "gr": "3",
    "l": "12",
    "tn": "B_NORMAL_MAP",
    "ie": "utf-8"}

    #pretend to be a browser
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'}

    url = 'http://map.baidu.com/'
    htm = requests.get(url, params=parameter, headers=headers)
    htm = htm.text.encode('latin-1').decode('unicode_escape') 
    
    
    pattern = r'(?<=\baddress_norm":"\[).+?(?="ty":)'
    htm = re.findall(pattern, htm)  
    print "There are %s results in this page" %len(htm)     #print out the number of search results in the page

    for r in htm:                                           #loop over each enterprise 
        pattern = r'"name":"(.+?)"'                         #get the name
        name = re.findall(pattern, r)

        if not name:
            pattern = r'(?<=\b,"name":").+?(?=")'
            name = re.findall(pattern, r)
        name = ''.join(name[1:])

        if len(name) > 25:                                  #filter out advertisements
            continue
        
        pattern = r'.+?(?=")'                               #get address
        adr = re.findall(pattern, r)
        pattern = r'\(.+?\['
        address = re.sub(pattern, ' ', adr[0])              #format address
        pattern = r'\(.+?\]'
        address = re.sub(pattern, ' ', address)

        pattern = r'(?<="phone":").+?(?=")'
        phone = re.findall(pattern, r)
        
        if len(phone) != 0 and phone[0] != '",':
            phone = phone[0]
            mobile = re.findall("(1\\d{10})",phone)
            if len(mobile) != 0:
                #print name
                #print mobile[0]
                writer.writerow([name, address, mobile[0],'NA','Shenzhen','Baidu'])
            else:
                #print name 
                #print phone
                writer.writerow([name, address, 'NA', phone, 'Shenzhen', 'Baidu'])

    return len(htm)


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')

    
    #get list of keywords
    keyWordList = ['管理咨询','计算机科技','网络科技','信息科技','广告公司',\
                   '电子商务','房地产中介','创业管理','教育咨询','投资管理',\
                   '软件开发','市场调研','营销策划','企业形象策划','项目咨询',\
                   '会展服务','投资咨询','人力资源公司','房地产评估','翻译服务',\
                   '庆典策划','婚姻介绍','家教服务','影视文化传播','平面设计',\
                   '艺术设计公司','技术咨询','公关','文化传播公司']
    
    
    
    with open('Baidu_Shenzhen.csv', 'wb') as csvfile:      #setup csv file
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name', 'address', 'mobile','telephone', 'city', 'infoSrc'])
        
        for kw in keyWordList:
            curPage = 0
            
            while True:
                if comFromBaidu(kw, curPage) == 0:
                    break                                  #loop until the page has no result
                curPage += 1         

                time.sleep(1)                             #delibrately sleep to avoid being detected as a crawler
                if curPage%20 == 0:   
                    time.sleep(1)
                if curPage%100 == 0:
                    time.sleep(2)
                if curPage%200 == 0:
                    time.sleep(7)
                
                print "%s pages done!" %curPage

