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
            url = "https://www.hotels.com/search.do?&locale=en_US&q-destination=Chiang%20Mai,%20Thailand&q-check-in=2018-12-07&q-check-out=2018-12-08&q-rooms=1&q-room-0-adults=2&q-room-0-children=0"
            # url = "https://www.expedia.com/Hotel-Search?destination=Krabi%2C+Thailand+%28KBV-Krabi+Intl.%29&startDate=10/01/2018&endDate=10/06/2018&rooms=1&adults=1&sort=deals"
            # headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
            response = requests.get(url)
            # print(response.json)

            parser = html.fromstring(response.text)
            name_xpath = parser.xpath('//*[@id="listings"]/ol') 
            # name_xpath = parser.xpath('//*[@id="listings"]/ol/li[1]/article/div/div[1]/h3/a')
            test = html.tostring(name_xpath[0])

            hotel_list = str(test) 
            hotel_arr = hotel_list.split('<li class="hotel')
            
            # print(len(hotel_arr))
            for i in range(len(hotel_arr)):
                print(i)
                hotel_arr[i] = '<li class="hotel' + hotel_arr[i]
            

            # with open('detail-hotel7.html','w') as fp:
     	    #     fp.write(str(test))
            print(hotel_arr[1])
            print('=================')
            print(hotel_arr[2])
            # print(parser)
            # print(test)

            # raw_json =json.loads(json_data_xpath[0] if json_data_xpath else '')


            # flight_data = json.loads(raw_json["content"])
            # flight_info  = OrderedDict()

            # lists=[]

            # for i in flight_data['legs'].keys():
            #     total_distance =  flight_data['legs'][i].get("formattedDistance",'')
            #     exact_price = flight_data['legs'][i].get('price',{}).get('totalPriceAsDecimal','')

            #     departure_location_airport = flight_data['legs'][i].get('departureLocation',{}).get('airportLongName','')
            #     departure_location_city = flight_data['legs'][i].get('departureLocation',{}).get('airportCity','')
            #     departure_location_airport_code = flight_data['legs'][i].get('departureLocation',{}).get('airportCode','')

            #     arrival_location_airport = flight_data['legs'][i].get('arrivalLocation',{}).get('airportLongName','')
            #     arrival_location_airport_code = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCode','')
            #     arrival_location_city = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCity','')
            #     airline_name = flight_data['legs'][i].get('carrierSummary',{}).get('airlineName','')

            #     no_of_stops = flight_data['legs'][i].get("stops","")
            #     flight_duration = flight_data['legs'][i].get('duration',{})
            #     flight_hour = flight_duration.get('hours','')
            #     flight_minutes = flight_duration.get('minutes','')
            #     flight_days = flight_duration.get('numOfDays','')

            #     if no_of_stops==0:
            #         stop = "Nonstop"
            #     else:
            #         stop = str(no_of_stops)+' Stop'

            #     total_flight_duration = "{0} days {1} hours {2} minutes".format(flight_days,flight_hour,flight_minutes)
            #     departure = departure_location_airport+", "+departure_location_city
            #     arrival = arrival_location_airport+", "+arrival_location_city
            #     carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
            #     plane = carrier.get('plane','')
            #     plane_code = carrier.get('planeCode','')
            #     formatted_price = "{0:.2f}".format(exact_price)

            #     if not airline_name:
            #         airline_name = carrier.get('operatedBy','')

            #     timings = []
            #     for timeline in  flight_data['legs'][i].get('timeline',{}):
            #         if 'departureAirport' in timeline.keys():
            #             departure_airport = timeline['departureAirport'].get('longName','')
            #             departure_time = timeline['departureTime'].get('time','')
            #             arrival_airport = timeline.get('arrivalAirport',{}).get('longName','')
            #             arrival_time = timeline.get('arrivalTime',{}).get('time','')
            #             flight_timing = {
            #             'departure_airport':departure_airport,
            #             'departure_time':departure_time,
            #             'arrival_airport':arrival_airport,
            #             'arrival_time':arrival_time
            #             }
            #             timings.append(flight_timing)

            #     flight_info={'stops':stop,
            #             'ticket price':formatted_price,
            #             'departure':departure,
            #             'arrival':arrival,
            #             'flight duration':total_flight_duration,
            #             'airline':airline_name,
            #             'plane':plane,
            #             'timings':timings,
            #             'plane code':plane_code
            #             }
            #     lists.append(flight_info)
            # sortedlist = sorted(lists, key=lambda k: k['ticket price'],reverse=False)
            # return sortedlist

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
    destination = args.destination.replace('-','+') # whitespce replace by '+'
    date = args.date

    # Example URL
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3ALampang%2C+Thailand+%28LPT%29%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3AKrabi%2C+Thailand+%28KBV-Krabi+Intl.%29%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"
    # url = "https://www.expedia.com/Flights-Search?flight-type=on&starDate=10%2F01%2F2018&mode=search&trip=oneway&leg1=from%3ABangkok%2C+Thailand+%28BKK-All+Airports%29%2Cto%3AChiang+Mai%2Cdeparture%3A10%2F01%2F2018TANYT&passengers=children%3A0%2Cadults%3A1%2Cseniors%3A0%2Cinfantinlap%3AY"

    # Example input
    # python hotel.py Bangkok Chiang-Mai 10/13/2018

    print ("Fetching flight details")
    scraped_data = parse(source,destination,date)
    # print ("Writing data to output file")
    # with open('%s-%s-flight-results.json'%(source,destination),'w') as fp:
    #  	json.dump(scraped_data,fp,indent = 4)
