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
            data_xpath = parser.xpath('//*[@id="subtab1"]/table/tbody//text()')

            lists = []
            raw_list = []

            raw_list.append('41')

            for i in data_xpath:
                dataStr = str(i)
                if((dataStr[0] >= 'A' and dataStr[0] <='Z') or
                (dataStr[0] >= 'a' and dataStr[0] <= 'b') or
                (dataStr[0] >= '0' and dataStr[0] <= '9')):
                    # print(dataStr)
                    raw_list.append(dataStr)

            # print(raw_list)

            name = ''
            departureTime = ''
            arrivalTime = ''
            pickup = ''
            dropoff = ''
            price = ''
            count = 0

            for data in raw_list:
                if(count != len(raw_list) - 1):
                    if(len(data) == 2 and data[0] >= '0' and data[0] <= '9'):
                        # print('name: ', raw_list[count+1])
                        name = raw_list[count+1]
                        departureTime = raw_list[count+2]
                    if(data == 'Dropoff: '):
                        dropoff = raw_list[count+1]

                    if(data == 'Estimated Arrival :'):
                        time = raw_list[count+1]
                        # print(time)
                        if(time[0] >= '0' and time[0] <= '9'):
                            arrivalTime = time
                        else:
                            arrivalTime = ''
                    if(data == 'Pickup:'):
                        pickup = raw_list[count+1]

                    if(data[0] == 'T' and data[1] == 'H' and data[2] == 'B'):
                        dataSplit = data.split()
                        price = dataSplit[1]
                        bus_info = {
                        'name': name,
                        'departureTime': departureTime,
                        'arrivalTime': arrivalTime,
                        'pickup': pickup,
                        'dropoff': dropoff,
                        'price': price
                        }
                        print('======================================')
                        print('name', name)
                        print('departureTime ', departureTime)
                        print('arrivalTime ', arrivalTime)
                        print('pickup ', pickup)
                        print('dropoff ', dropoff)
                        print('price ', price)
                        print('======================================\n')
                        lists.append(bus_info)
                count += 1

            # bus_data = json.dumps(lists)

            # json_bus_data = json.loads(bus_data)
            # print(lists)

            with open('Bus-%s-%s-flight-results.json'%(source,destination),'w') as fp:
             	json.dump(lists,fp,indent = 4)

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


    print ("Fetching Bus details")
    scraped_data = parse(source,destination,date)
    # print ("Writing data to output file")
    # with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
    #  	json.dump(scraped_data,fp,indent = 4)
