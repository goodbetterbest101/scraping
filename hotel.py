import json
import regex
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from lxml import html
from collections import OrderedDict
import argparse
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

import random


ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

def parse(destination,startDate,endDate):
    for i in range(1):
        try:
            # prox = Proxy()
            # proxy_index = random_proxy()
            # proxy = proxies[proxy_index]

            # pxy = proxy['ip'] + ':' + proxy['port']

            # print('Proxy is ',pxy)

            # ### comment here
            # prox.proxy_type = ProxyType.MANUAL
            # prox.http_proxy = pxy
            # prox.socks_proxy = pxy
            # prox.ssl_proxy = pxy

            # capabilities = webdriver.DesiredCapabilities.CHROME
            # prox.add_to_capabilities(capabilities)

            ###########################################

            # url = "https://www.hotels.com/search.do?&locale=en_TH&q-destination=Chiang%20Mai,%20Thailand&q-check-in=2018-12-07&q-check-out=2018-12-08&q-rooms=1&q-room-0-adults=2&q-room-0-children=0"
            url = "https://www.expedia.com/Hotel-Search?destination={0}&startDate={1}&endDate={2}&rooms=1&adults=1&sort=deals".format(destination,startDate,endDate)
            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            opts = ChromeOptions()
            opts.add_experimental_option("detach", True)
            driver = webdriver.Chrome(
                executable_path="/Users/khathawut/Documents/My works/Project/expedia/chromedriver"
                ,chrome_options=opts)
                # ,desired_capabilities=capabilities)

            driver.get(url)
            time.sleep(0.5)

            ### scrolling webpage
            # elem = driver.find_element_by_tag_name("body")
            # print('1')
            # no_of_pagedowns = 6
            # while no_of_pagedowns:
            #     print('while')
            #     elem.send_keys(Keys.PAGE_DOWN)
            #     time.sleep(0.25)
            #     no_of_pagedowns-=1

            time.sleep(30)

            # post_elems = driver.find_elements_by_class_name("listings")
            post_elems = driver.find_elements_by_id("resultsContainer")

            #### comment end here
           
            detail_hotel = ''

            for post in post_elems:
                print('for')
                detail_hotel = post.text
                # print(post.text)

            raw_list = detail_hotel.split('\n')
            list = []
            name = ''
            address = ''
            star = ''
            near = ''
            review = ''
            numReview = ''
            price = ''

            # print(raw_list[0])
            count = 0
            checkRound = 0
            # isFirst = True
            for data in raw_list:
                if data:
                    dataCheck = data.split(' ')
                    dataStr = str(data)
                    if count == 0 and dataStr[0] >= '0' and dataStr[0] <= '9' and len(dataCheck) == 4:
                        star = data
                        if dataCheck[1] == 'out':
                            name = raw_list[checkRound - 1]
                        # print('=========== name: %s, star: %s',name,star)
                        count += 1
                    elif count == 1 and dataCheck[0] != 'VIP':
                        address = data
                        count += 1
                    elif dataCheck[0] == 'Hotel':
                        near = data
                        count += 1
                    elif dataCheck[0] == 'Guest' and dataCheck [2] == 'is':
                        review = data
                    elif dataCheck[0] == 'Based':
                        numReview = data       
                    elif dataStr[0] == '$':
                        price = data.strip('$')
                    elif data == 'Sale!':
                        info_hotel = {
                            'name': name,
                            'address': address,
                            'star': star,
                            'near': near,
                            'review': review,
                            'numReview': numReview,
                            'price': price
                        }
                        name = ''
                        address = ''
                        star = ''
                        near = ''
                        review = ''
                        numReview = ''
                        price = ''
                        count = 0
                        list.append(info_hotel)  
                checkRound += 1  
             
            # print(list)
            # with open('hotel-results-5.json','w') as fp:
            #  	json.dump(list,fp,indent = 4)
            # with open('hotel-results-6.txt','w') as fp:
            #  	fp.write(detail_hotel)
            return list 

        except ValueError:
            print ("Rerying...")

            return {"error":"failed to process the page",}

def getProxy():
    # Retrieve latest proxies
    proxies_req = Request('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = urlopen(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
        'ip':   row.find_all('td')[0].string,
        'port': row.find_all('td')[1].string
    })

def random_proxy():
  return random.randint(0, len(proxies) - 1)

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('destination',help = 'Destination airport code')
    argparser.add_argument('startDate',help = 'MM/DD/YYYY')
    argparser.add_argument('endDate',help = 'MM/DD/YYYY')

    args = argparser.parse_args()
    destination = args.destination.replace('-','+') # whitespce replace by '+'
    startDate = args.startDate
    endDate = args.endDate

    # getProxy()

    # Example URL
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3ALampang%2C+Thailand+%28LPT%29%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3AKrabi%2C+Thailand+%28KBV-Krabi+Intl.%29%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3AChiang+Mai%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"

    # Example input
    # python hotel.py Chiang-Mai 10/20/2018 10/23/2018

    print ("Fetching hotel details")
    scraped_data = parse(destination,startDate,endDate)
    print ("Writing data to output file")
    # print(scraped_data)
    with open('%s-%s-hotel-results.json'%(destination,startDate.replace('/','-')),'w') as fp:
     	json.dump(scraped_data,fp,indent = 4)
