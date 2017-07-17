#-*- coding: utf-8 -*-
import sys
import requests
import re 
import csv
from bs4 import BeautifulSoup 


def getPageUrl():
    
    list = []
    
    #303
    for i in range(1, 303):
        pageUrl = r"http://www.lawyers.org.cn/searchLawFirm?page=" + str(i)
        list.append(pageUrl)

    return list


def getComInfoList(url):
    infoList = []
    
    comPage = requests.get(url)
    soup = BeautifulSoup(comPage.text, "lxml")

    companies = soup.find_all(class_='office_list')
    
    for company in companies:
        comInfo = {}
        
        comInfo['name'] = company.h3.a.string
        print comInfo['name']

        contact = company.find_all('dd')[7]
        contactPerson = ''.join(contact.stripped_strings)
        comInfo['contactPerson'] = contactPerson
        
        phone = company.find_all('dd')[4].string
        if phone == None:
            comInfo['mobile'] = 'NA'
            comInfo['telephone'] = 'NA'
        else:
            mobile = re.findall('(1[3458]\\d{9})',phone)
            if len(mobile) != 0:
                comInfo['mobile'] = mobile[0]
                comInfo['telephone'] = 'NA'
            else:
                comInfo['mobile'] = 'NA'
                comInfo['telephone'] = ''.join(phone.split())[3:]
        
        address = company.find_all('dd')[2].string
        addr = ''.join(address.split())
        comInfo['address'] = addr

        lawyers = company.find('table').find_all('a')
        comInfo['size'] = len(lawyers)

        infoList.append(comInfo)

    return infoList
    

def opToCSV(list):
    with open('Law Firms in Shanghai.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name','contactPerson','address','mobile','telephone','size','city','infoSrc'])
        for company in list:
            writer.writerow([company['name'],company['contactPerson'],company['address'],company['mobile'],company['telephone'],company['size'],'Shanghai','Shanghai Lawyer Association'])

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
        
    #get every search result page's url
    pageUrlList = getPageUrl()

    #create an empty list to store company information
    comInfoLists = []

    page = 0
    for pageUrl in pageUrlList:
        comInfoLists += getComInfoList(pageUrl)
        
        page += 1
        print page

    #output info stored in comInfoList
    opToCSV(comInfoLists)





