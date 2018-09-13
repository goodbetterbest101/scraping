import json
import regex
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from lxml import html
from collections import OrderedDict
import argparse

def parse(source,destination,date):
    for i in range(1):
        try:
            url = "https://www.busonlineticket.co.th/booking/bangkok-to-chiang-mai-bus-tickets".format(source,destination,date)
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            response = requests.get(url)
            # with open('res.text','w') as fw:
            #  	fw.write(response.text)

            parser = html.fromstring(response.text)
            # json_data_xpath = parser.xpath('//*[@id="subtab1"]/table/tbody/tr[1]//text()')
            json_data_xpath = parser.xpath('//*[@id="subtab1"]/table/tbody//text()')

            lists = []
            for i in json_data_xpath:
                a = str(i)
                if((a[0] >= 'A' and a[0] <='Z') or (a[0] >= 'a' and a[0] <= 'b') or (a[0] >= '0' and a[0] <= '9')):
                    print(a)
            # with open('xpath.txt','w') as fw:
            #  	fw.write(json_data_xpath)

            # raw_json =json.loads(json_data_xpath[0] if json_data_xpath else '')
            #
            #
            # flight_data = json.loads(raw_json["content"])
            # flight_info  = OrderedDict()
            #
            # lists=[]


        except ValueError:
            print ("Rerying...")

            return {"error":"failed to process the page",}

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('source',help = 'Source airport code')
    argparser.add_argument('destination',help = 'Destination airport code')
    argparser.add_argument('date',help = 'MM/DD/YYYY')

    args = argparser.parse_args()
    source = args.source
    destination = args.destination
    date = args.date
    # print(source)


    print ("Fetching flight details")
    scraped_data = parse(source,destination,date)
    # print ("Writing data to output file")
    # with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
    #  	json.dump(scraped_data,fp,indent = 4)
