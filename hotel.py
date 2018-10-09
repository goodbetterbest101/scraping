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

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random


ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

def parse(source,destination,date):
    for i in range(1):
        try:
            url = "https://www.hotels.com/search.do?&locale=en_TH&q-destination=Chiang%20Mai,%20Thailand&q-check-in=2018-12-07&q-check-out=2018-12-08&q-rooms=1&q-room-0-adults=2&q-room-0-children=0"
            # url = "https://www.expedia.com/Hotel-Search?destination=Krabi%2C+Thailand+%28KBV-Krabi+Intl.%29&startDate=10/01/2018&endDate=10/06/2018&rooms=1&adults=1&sort=deals"
            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            opts = ChromeOptions()
            opts.add_experimental_option("detach", True)
            driver = webdriver.Chrome(executable_path="/Users/khathawut/Documents/My works/Project/expedia/chromedriver",chrome_options=opts) 
            driver.get(url)
            # time.sleep(0.3)
            elem = driver.find_element_by_tag_name("body")
            print('1')
            no_of_pagedowns = 10
            while no_of_pagedowns:
                print('while')
                elem.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
                no_of_pagedowns-=1

            print('finish while and wait for 25 sec')

            driver.implicitly_wait(25) # seconds

            print('pass 25 sec!')
            

            post_elems = driver.find_elements_by_class_name("listings")

            for post in post_elems:
                print('for')
                print(post.text)

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
    argparser.add_argument('source',help = 'Source airport code')
    argparser.add_argument('destination',help = 'Destination airport code')
    argparser.add_argument('date',help = 'MM/DD/YYYY')

    args = argparser.parse_args()
    source = args.source
    destination = args.destination.replace('-','+') # whitespce replace by '+'
    date = args.date

    getProxy()
    # Choose a random proxy
    proxy_index = random_proxy()
    proxy = proxies[proxy_index]

    print('proxy is ',proxy)

    # Example URL
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3ALampang%2C+Thailand+%28LPT%29%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3AKrabi%2C+Thailand+%28KBV-Krabi+Intl.%29%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3AChiang+Mai%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"

    # Example input
    # python hotel.py Bangkok Chiang-Mai 10/13/2018

    print ("Fetching hotel details")
    scraped_data = parse(source,destination,date)
    # print ("Writing data to output file")
    # with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
    #  	json.dump(scraped_data,fp,indent = 4)
