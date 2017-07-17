#-*- coding: utf-8 -*-
import sys
import requests
import re
import csv
from bs4 import BeautifulSoup

def getPageUrl():
    list = [r"http://www.szlawyers.com/searchLawFirm?name=%E4%BA%8B%E5%8A%A1%E6%89%80&x=0&y=0&page="+str(i) for i in range(1, 37)] #37
    return list

def getComUrlList(url):
    comUrlList = []
    
    resultPage = requests.get(url)
    soup = BeautifulSoup(resultPage.text, "lxml")

    comUrls = soup.find_all('tr', attrs={"bgcolor":"#f0f0f0"})
    comUrls = comUrls[0:len(comUrls)-1]
    for tr in comUrls:
        comUrl = tr.td.a
        if comUrl == None:
            continue
        else:
            comUrl = r"http://www.szlawyers.com" + comUrl.get('href')
            comUrlList.append(comUrl)
    return comUrlList

def getComDict(url):
    comInfo = {}

    comPage = requests.get(url)
    soup = BeautifulSoup(comPage.text, "lxml")

    tbody = soup.find('tbody')
    tr = tbody.find_all('tr')

    name = tr[0].find_all('td')[1].string
    comInfo['name'] = name
    print comInfo['name']
    
    pic = tr[6].find_all('td')[1].a
    if pic == None:
        comInfo['contactPerson'] = "NA"
    else:
        comInfo['contactPerson'] = pic.string

    comInfo["size"] = tr[8].find_all('td')[1].string
    
    comInfo['address'] = tr[10].find_all('td')[1].string
    
    phone = tr[12].find_all('td')[1].string
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
            comInfo['telephone'] = phone
    
    email = tr[14].find_all('td')[1].string
    if email == None:
        comInfo['email'] = "NA"
    else:
        comInfo['email'] = email
    
    return comInfo

def opToCSV(list):
    with open('Law Firms in Shenzhen.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name', 'contactPerson','size','address', 'mobile','telephone', 'email','city', 'infoSrc'])
        for company in list:
            writer.writerow([company['name'],company['contactPerson'],company['size'], company['address'],company['mobile'],company['telephone'],company['email'],'Shenzhen','Shenzhen Lawyer Association'])

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
        
    #get every search result page's url
    pageUrlList = getPageUrl()

    #create an empty list to store company information
    comInfoList = []
     
    page = 0
    for pageUrl in pageUrlList:
        #get firms' url in this page to a list
        comUrlLists = getComUrlList(pageUrl)

        for comUrl in comUrlLists:
            comDict = getComDict(comUrl)
            comInfoList.append(comDict)
        page += 1
        print page

    #output info stored in comInfoList
    opToCSV(comInfoList)

