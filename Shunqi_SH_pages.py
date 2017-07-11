import requests
import time
import sys
from bs4 import BeautifulSoup

'''This script is written to get all pages urls for 
business service enterprises in Shanghai from this 
open source B2B platform "www.11467.com", for crawling
company contact information
'''


def main():    
    f = open('Shunqi_SH_pages.txt','w')
    startUrl = r"http://www.11467.com/shanghai/search/11739.htm"   #business service enterprises in Shanghai

    general = requests.get(startUrl)
    time.sleep(2)
    soup = BeautifulSoup(general.text, "lxml")

    categories = soup.find(class_='listtxt').find_all('a')     #find div that holds sub-categories of business service
    for cate in categories:
        cateUrl = cate.get('href')                             #get each sub-category's url
        catePage = requests.get(cateUrl)
        time.sleep(2)
        soup2 = BeautifulSoup(catePage.text, "lxml")

        districts = soup2.find(class_='boxtitle')              #find div that holds districts of each sub-category
        if districts == None:                                  #if there is no division of districts for that sub-category 
            f.write(cateUrl)
            f.write('\n')
            continue
        
        districts = districts.parent.find_all('a')             #store all anchors of districts into a list
        for district in districts:
            districtUrl = district.get('href')
            
            districtPage = requests.get(districtUrl)
            time.sleep(2)
            soup3 = BeautifulSoup(districtPage.text, "lxml")
            pages = soup3.find(class_='pages')                 #find div that holds page numbers 
            
            if pages != None:
                pages = pages.find_all('a')
                pages = pages[0:len(pages)-2]
                for page in pages:
                    f.write(page.get('href'))
                    f.write('\n')
            else:                                              #if there's only 1 page for this district
                f.write('\n')
    f.close()
    return

if __name__ == '__main__':
    main()
