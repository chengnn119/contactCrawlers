#-*- coding: utf-8 -*-
import sys
import requests
import re 
import csv
from bs4 import BeautifulSoup 


def getPageUrl():
    
    list = []
    
    #33
    for i in range(1, 33):
        pageUrl = r"http://www.gzlawyer.org/searchLawFirm?name=%E4%BA%8B%E5%8A%A1%E6%89%80&x=20&y=10&licenseNumber=&page=" + str(i)
        list.append(pageUrl)

    return list

def getComUrlList(url):
    comUrlList = []
    
    resultPage = requests.get(url)
    soup = BeautifulSoup(resultPage.text, "lxml")

    comUrls = soup.find(class_='chengxin').table.find_all('a')
    for a in comUrls:
        comUrl = r"http://www.gzlawyer.org" + a.get('href')
        comUrlList.append(comUrl)
    return comUrlList

def getComDict(url):
    comInfo = {}

    comPage = requests.get(url)
    soup = BeautifulSoup(comPage.text, "lxml")

    table = soup.find(class_='infodetail')
    if table == None:
        return None
    
    tr = table.find('table').tbody.find_all('tr')
    
    comInfo['name'] = tr[0].find_all('td')[1].string
    print comInfo['name']
    
    comInfo['contactPerson'] = tr[2].find_all('td')[3].string
    
    comInfo['address'] = tr[3].find_all('td')[1].string
    
    phone = tr[4].find_all('td')[1].string
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
            comInfo['telephone'] = phone.split(',')[0]
    
    email = comInfo['email'] = tr[5].find_all('td')[1].string
    if email == None:
        comInfo['email'] = "NA"
    else:
        comInfo['email'] = email
    
    lawyers = len(tr[6].find_all('a')) + len(tr[7].find_all('a'))
    comInfo['size'] = lawyers
    
    return comInfo

def opToCSV(list):
    with open('Law Firms in Guangzhou.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name','contactPerson','address','mobile','telephone','email','size','city','infoSrc'])
        for company in list:
            writer.writerow([company['name'],company['contactPerson'],company['address'],company['mobile'],company['telephone'],company['email'],company['size'],'Guangzhou','Guangzhou Lawyer Association'])

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
            if comDict == None:
                continue
            comInfoList.append(comDict)

        page += 1
        print page

    #output info stored in comInfoList
    opToCSV(comInfoList)





