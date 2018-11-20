import json
import regex
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from lxml import html
from collections import OrderedDict
import argparse

def parse(url):
    for i in range(1):
        try:
            name = ''
            detailName = ''
            tel = ''
            dayOpen = ''
            timeOpen = ''
            province = ''
            travelType = ''
            detail = ''

            # url = "https://thai.tourismthailand.org/\u0e2a\u0e16\u0e32\u0e19\u0e17\u0e35\u0e48\u0e17\u0e48\u0e2d\u0e07\u0e40\u0e17\u0e35\u0e48\u0e22\u0e27/\u0e20\u0e39\u0e17\u0e2d\u0e01--6314"
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            response = requests.get(url)
            parser = html.fromstring(response.text)
            name_data_xpath = parser.xpath('/html/body/article/div[2]/div[2]//text()')
            detailname_data_xpath = parser.xpath('/html/body/article/div[3]/div[2]/div/div/div/div[2]/div[1]//text()')
            tel_data_xpath = parser.xpath('/html/body/article/div[3]/div[2]/div/div/div/div[2]/div[2]//text()')
            day_data_xpath = parser.xpath('/html/body/article/div[3]/div[2]/div/div/div/div[2]/div[3]//text()')
            time_data_xpath = parser.xpath('/html/body/article/div[3]/div[2]/div/div/div/div[2]/div[4]//text()')
            province_data_xpath = parser.xpath('/html/body/article/div[3]/div[3]/div/div[2]/div[1]//text()')
            type_data_xpath = parser.xpath('/html/body/article/div[3]/div[3]/div/div[2]/div[2]//text()')
            detail_data_xpath = parser.xpath('/html/body/article/div[3]/div[3]/div/div[3]//text()')


            for data in detail_data_xpath:
                for i in range(len(data)):
                    if (data[i] != '\r') and (data[i] != '\n') and (data[i] != '\t'):
                        detail = detail + data
                        break

            name = name_data_xpath[0].replace(' ','')

            if('ที่อยู่ : ' in detail_data_xpath):
                detailName = detailname_data_xpath[1].replace('\xa0','')
            if(' เบอร์โทร : ' in tel_data_xpath):
                tel = tel_data_xpath[len(tel_data_xpath)-1]
            if('วันเปิดทำการ : ' in day_data_xpath):
                dayOpen = day_data_xpath[1]
            if('เวลาเปิดทำการ : ' in time_data_xpath):
                timeOpen = time_data_xpath[1]
            if('หมวดหมู่ : ' in type_data_xpath):
                travelType = type_data_xpath[1]

            province = province_data_xpath[1].replace(' ','')
            detail = detail.replace('\r\n\t','')

            travel_info = {
                'name': name,
                'detailName': detailName,
                'tel': tel,
                'dayOpen': dayOpen,
                'timeOpen': timeOpen,
                'province': province,
                'travelType': travelType,
                'detail': detail
            }

            return travel_info

            # with open('travel-results-2.json','w') as fp:
            #     json.dump(travel_info,fp,indent = 4,ensure_ascii=False)
            # for data in data_xpath:
                # print(data)
            # with open('travel-html.json','w') as fp:
            #     fp.write(response.text)


        except ValueError:
            print ("Rerying...")

            return {"error":"failed to process the page",}

if __name__=="__main__":
    # Example URL
    # https://www.busonlineticket.co.th/booking/bangkok-to-chiang-mai-bus-tickets

    # Example input
    # python travel.py Bangkok Chiang-mai 2018-11-01

    # parse('https://thai.tourismthailand.org/สถานที่ท่องเที่ยว/ภูทอก--6314')

    with open('Attraction-1-thai.json') as data_file:
        data = json.load(data_file)

    scraped_data = []
    count = 0

    for url in data['attraction']:
        print('count: ',count)
        print ("travel :",url)
        scraped_data.append(parse(url))
        count += 1

    print ("Writing data to output file")
    with open('Travel-1-50-results.json','w') as fp:
        json.dump(scraped_data,fp,indent = 4,ensure_ascii=False)
