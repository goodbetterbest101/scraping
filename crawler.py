import requests
import re
import os.path
import codecs
import json
from bs4 import BeautifulSoup

base = 'https://na.tourismthailand.org/Attraction'
downloaded = []
count = 0

def find_links(doc):
    soup = BeautifulSoup(doc.text, 'html.parser')
    # print(soup)
    for a in soup.find_all('a'):
        if a.has_attr('href'):
            href = str(a['href'])
            if '/สถานที่ท่องเที่ยว/' in href and '/ค้นหา?' not in href and href not in downloaded:
                print('href: ',href)
                downloaded.append(href)

if __name__=="__main__":

    for i in range(50,100):
        doc = ''
        url = 'https://thai.tourismthailand.org/สถานที่ท่องเที่ยว/ค้นหา?lifestyle_id=&cat_id=&subcat_id=&view=&keyword=&sort=0&page=' + str(i)
        try:
            print('Requesting...', url)
            doc = requests.get(url)
        except:
            print('Error request')
        find_links(doc)

    # print('Result')
    # print(downloaded)

    link = {
        'attraction': downloaded
    }
    with open('Attraction-thai-50-100.json','w') as fp:
        json.dump(link,fp,indent = 4,ensure_ascii=False)
