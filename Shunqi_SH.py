#-*- coding: utf-8 -*-
import sys
import requests
import re 
import time
import csv
from bs4 import BeautifulSoup



def getComUrlList(url):
    comUrlList = []
    
    resultPage = requests.get(url)
    soup = BeautifulSoup(resultPage.text, "lxml")

    try:
        comUrls = soup.find(class_='companylist').find_all('h4')
    except:
    	print "Error url, no company in this page"  
    	print url
    	newPage = requests.get(r'http://shanghai.11467.com/php/banip.php?sid=a57f9e4c0ea4f82548581612573b0e61')
    	print "\n"
    	return

    for h4 in comUrls:
        comUrl = h4.a.get('href')
        comUrlList.append(comUrl)

    return comUrlList

def getComDict(url):
    
    comPage = requests.get(url)
    #time.sleep(2)
    soup = BeautifulSoup(comPage.text, "lxml")

    try:
        contactTable = soup.find(class_='codl')
        infoTable = soup.find_all(class_='codl')[1]
    except:                                             #crawler detected when too many requests during a certain period
        print "Crawler detected!"
        print url
        newPage = requests.get(r'http://www.11467.com/php/banip.php?sid=a57f9e4c0ea4f82548581612573b0e61')
        print "\n"
        return
    
    name = infoTable.find_all('dd')[0].string
    
    pic = contactTable.find_all('dd')[2].string
    
    address = contactTable.find_all('dd')[0].string
    
    telephone = contactTable.find_all('dd')[1].string
    
    mobpicA = contactTable.find('a')
    mobpicA = mobpicA.get('onclick')
    codeMobile = re.findall('([0-9]+).jpg',mobpicA)[0]
    mobile = '' 
    for i in range(11):
        mobile += codeMobile[2*i + 1]
    if mobile[0] != '1':
        mobile = 'NA'
        
    email = contactTable.find_all('dd')[4].string
    if '@' not in email:
        email = 'NA'
    
    writer.writerow([name, pic, address, telephone, mobile, email, 'Shanghai', 'Shunqi'])

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
        
    with open('Shunqi_SH.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')
        writer.writerow(['name', 'contactPerson', 'address', 'telephone','mobile','email','city', 'infoSrc'])
        
        f = open('Shunqi_SH_pages.txt')
        lines = f.readlines()
        totalPage = len(lines)
        print "There are %s pages" %totalPage
        
        numPage = 0
        
        for line in lines:
            pageUrl = line.strip('\n')
            
            comUrlLists = getComUrlList(pageUrl) 

            if comUrlLists == None:
            	continue

            for comUrl in comUrlLists:
                getComDict(comUrl)
                
            numPage += 1
            print "%s out of %s pages crawled" %(numPage, totalPage)
                
    




