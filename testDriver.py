import io
import os
from hotel import Hotel
import math

def verify_data(path: str):
    for file in os.listdir(path):
        with open(path + file) as data:
            content = data.readlines()
            state = 4
            counter = 1
            for line in content:
                if state is 1 or state is 2 or state is 3:
                    if not line.startswith('\t'):
                        print('FAIL: ' + str(counter))
                        print(file)
                    state = state + 1
                    counter = counter + 1
                    continue
                if state is 4:
                    state = 0
                    if line.startswith('\t'):
                        print('FAIL: ' + str(counter))
                        print(file)
                    state = state + 1
                counter = counter + 1

def get_hotel_data(path: str):
    output = []
    for file in os.listdir(path):
        list = []
        with open(path + file) as data:
            content = data.readlines()
            state = 4
            counter = 1
            hotel = Hotel()
            for line in content:
                if state is 1:
                    hotel.url = line.strip()
                    state = state + 1
                    counter = counter + 1
                    continue
                if state is 2:
                    hotel.address = line.strip()
                    state = state + 1
                    counter = counter + 1
                    continue
                if state is 3:
                    string = line.strip()
                    hotel.lat = float(string.split(' ')[0])
                    hotel.lng = float(string.split(' ')[1])
                    state = state + 1
                    counter = counter + 1
                    continue
                if state is 4:
                    list.append(hotel)
                    hotel = Hotel()
                    state = 1
                    hotel.name = line.strip()
                counter = counter + 1
        list.remove(list[0])
        output.append(list)
    return output

def find_optimal(list1: list,list2:list,list3:list) -> dict:
    mappings = {}
    for hotelList in list1:
        for hotel in hotelList:
            if hotel.lat == 0.0 or hotel.lng == 0.0:
                continue
            for hotelList2 in list2:
                for hotel2 in hotelList2:
                    if hotel2.lat == 0.0 or hotel2.lng == 0.0:
                        continue
                    for hotelList3 in list3:
                        for hotel3 in hotelList3:
                            if hotel3.lat == 0.0 or hotel3.lng == 0.0:
                                continue
                            avg_lat = average_lat_coord(hotel,hotel2,hotel3)
                            avg_lng = average_lng_coord(hotel,hotel2,hotel3)
                            distance = max(abs(hotel.lat - avg_lat) + abs(hotel.lng - avg_lng),abs(hotel2.lat - avg_lat) + abs(hotel2.lng - avg_lng),abs(hotel3.lat - avg_lat) + abs(hotel3.lng - avg_lng))
                            if distance < .1:
                                print(hotel.name + " - " + hotel2.name + " - " +  hotel3.name)
                                print(distance)
                                mappings[hotel.name + " - " + hotel2.name + " - " +  hotel3.name] = distance
    mappings = sorted(mappings.values())
    return mappings

def average_lat_coord(h1: Hotel, h2:Hotel, h3: Hotel):
    return avg_coord(h1.lat,h2.lat,h3.lat)

def average_lng_coord(h1: Hotel, h2: Hotel, h3: Hotel):
    return avg_coord(h1.lng,h2.lng,h3.lng)

def avg_coord(first,second,third):
    return (first+second+third)/3

hyattHotels = []
ihgHotels = []
marriottHotels = []


verify_data('.\\data\\hyatt\\')
verify_data('.\\data\\ihg\\')
verify_data('.\\data\\marriott\\')

hyattHotels = get_hotel_data('.\\data\\hyatt\\')
ihgHotels = get_hotel_data('.\\data\\ihg\\')
marriottHotels = get_hotel_data('.\\data\\marriott\\')

for item in find_optimal(hyattHotels,marriottHotels,ihgHotels):
    print(item)

