#-*- coding: utf-8 -*-
import sys
import requests
import re 
import csv
from bs4 import BeautifulSoup

def getPageUrl():
    
    urlList = []
    
    for i in range(1, 240):  #240
        urlList.append("http://www.beijinglawyers.org.cn/cgi/RnewsActionsearchLawfirm2.do?text5=%25E4%25BA%258B%25E5%258A%25A1%25E6%2589%2580&text6=&typeid=0&cur=" + str(i))
        
    return urlList

def getComUrlList(url):
    comUrlList = []
    
    resultPage = requests.get(url)
    soup = BeautifulSoup(resultPage.text, "lxml")

    comUrls = soup.find_all('td', attrs={"width":"46%", "height":"34"})
    comUrls = comUrls[1:]
    for td in comUrls:
        comUrl = r"http://www.beijinglawyers.org.cn" + td.a.get('href')
        comUrlList.append(comUrl)
    return comUrlList

def getComDict(url):
    comInfo = {}

    comPage = requests.get(url)
    soup = BeautifulSoup(comPage.text, "lxml")

    table = soup.find('table', attrs={'style':'font-size:16px;'})
    tr = table.find_all('tr')
    comInfo['name'] = tr[0].find_all('td')[0].string[3:]
    print comInfo['name']
    pic = tr[1].find_all('td')[1].string[3:]
    pic = ''.join(pic.split())
    comInfo['contactPerson'] = pic
    comInfo['address'] = tr[3].td.string[3:]
    comInfo['workArea'] = tr[5].find_all('td')[0].string[5:]
    
    phone = tr[6].find_all('td')[1].string[5:]
    mobile = re.findall('(1[3458]\\d{9})',phone)
    if len(mobile) != 0:
        comInfo['mobile'] = mobile[0]
        comInfo['telephone'] = 'NA'
    else:
        comInfo['mobile'] = 'NA'
        comInfo['telephone'] = phone.split('、')[0]
    
    return comInfo

def opToCSV(list):
    with open('Law Firms in Beijing.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name', 'contactPerson', 'address', 'workArea', 'mobile','telephone', 'city', 'infoSrc'])
        for company in list:
            writer.writerow([company['name'],company['contactPerson'],company['address'],company['workArea'],company['mobile'],company['telephone'],'Beijing','Beijing Lawyer Association'])

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
        
    #get every search result page's url
    pageUrlList = getPageUrl()

    #create an empty list to store company information
    comInfoList = []
    
    for pageUrl in pageUrlList:
        #get firms' url in this page to a list
        comUrlLists = getComUrlList(pageUrl)

        for comUrl in comUrlLists:
            comDict = getComDict(comUrl)
            comInfoList.append(comDict)
    
    
    #output info stored in comInfoList
    opToCSV(comInfoList)





