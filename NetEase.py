#-*- coding: utf-8 -*-
import sys
import requests
import re
import csv
from bs4 import BeautifulSoup

'''This script is written to crawl company
contact informtion in 4 industries in 4 cities
from NetEase's yellow page
'''

def getPageUrls():
    urlList = []
    
    #representing 4 cities respectively
    cityCode = {'31', '11', '1983', '2007'}
    
    #10003 etc. are subcategories of an industry
    IT = r"http://114.163.com/search/10003-10001-10004-10002/" 
    comm1 = r"http://114.163.com/search/40000/"
    comm2 = r"http://114.163.com/search/40001/"
    prof = r"http://114.163.com/search/70000-70002-70003/"

    industry = [IT, comm1, comm2, prof]

    #access to pages over 100 is forbidden by database
    for indu in industry:
        for city in cityCode:
            for i in range(1,100):      
                urlList.append(indu+city+r"/?q=&s=10&p=" + str(100-i))

    return urlList    

def getComInfoList(url):
    comInfoList = []

    #open the result page, each result page contains 10 companies
    resultPage = requests.get(url)
    soup = BeautifulSoup(resultPage.text, "lxml")

    companies = soup.find_all('div', class_='info')
    
    if len(companies) == 0:
        return None

    for company in companies:
        #use an empty dictionary to store company information
        comInfo = {}
        
        phone = company.find(class_='icon-tel')
        #check whether the company has provided contact info
        if phone == None:
            comInfo['telephone'] = 'NA'
            comInfo['mobile'] = 'NA'
        else:    
            phone = phone.previous_element.string
            mobile = re.findall("(1[3458]\\d{9})",phone)
            if len(mobile) != 0:
                comInfo['mobile'] = mobile[0]
                comInfo['telephone'] = 'NA'
            else:
                comInfo['mobile'] = 'NA'
                comInfo['telephone'] = phone

        email = company.find(class_='icon-email')
        #check whether the company has provided email
        if email != None:
            comInfo['email'] = email.previous_sibling.string
        else:
            comInfo['email'] = 'NA'

        
        address = company.find(class_='icon-addr')
        if address == None:
            continue
        address = address.previous_element.string
        comInfo['address'] = address
        
        comInfo['name'] = company.find(class_='tit').a.string
        
        if '深圳' in address:
            comInfo['city'] = 'Shenzhen'
        elif '北京' in address:
            comInfo['city'] = 'Beijing'
        elif '上海' in address:
            comInfo['city'] = 'Shanghai'
        elif '广州' in address:
            comInfo['city'] = 'Guangzhou'
        else:
            comInfo['city'] = 'NA'
        
        comInfoList.append(comInfo)

    return comInfoList

def opToCSV(list):
    with open('NetEase.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name','address','mobile','telephone','email','city','infoSrc'])
        for company in list:
            writer.writerow([company['name'],company['address'],company['mobile'],company['telephone'],company['email'],company['city'],'NetEase'])

if __name__ == "__main__":
    #to output Chinese characters without error
    reload(sys)
    sys.setdefaultencoding('utf-8')

    comInfoLists = []

    pageUrlList = getPageUrls()
    #print len(pageUrlList)

    #page = 0
    for pageUrl in pageUrlList:
        comInfoList = getComInfoList(pageUrl)
        if comInfoList == None:
            continue
        comInfoLists += comInfoList
        #page += 1
        #print page

    #output company information to a csv file
    opToCSV(comInfoLists)



    
