import io
import os
from hotel import Hotel
import math
import sqlite3

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

def get_hotel_data_from_db(group: str):
    conn = sqlite3.connect('hotel.db')
    c = conn.cursor()
    c = c.execute("SELECT * FROM Hotels WHERE hotel_group='"+group+"' AND lat<>'0'")
    list = c.fetchall()
    output = {}
    hotels = []
    for item in list:
        hotel = Hotel()
        hotel.lat = float(item[2])
        hotel.lng = float(item [3])
        hotel.name = item [0]
        hotel.url = item[1]
        hotel.address = item[7]
        try:
            if output[item[5]] is None:
                output[item[5]] = []
        except KeyError:
            output[item[5]] = []
        output[item[5]].append(hotel)
    return output


def find_optimal(list1: dict,list2:dict,list3:dict) -> dict:
    mappings = {}
    for hotelList in list1.values():
        for hotel in hotelList:
            if hotel.lat == 0.0 or hotel.lng == 0.0:
                continue
            for hotelList2 in list2.values():
                for hotel2 in hotelList2:
                    if hotel2.lat == 0.0 or hotel2.lng == 0.0:
                        continue
                    for hotelList3 in list3.values():
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
    return (float(first)+float(second)+float(third))/3

hyattHotels = []
ihgHotels = []
marriottHotels = []


hyattHotels = get_hotel_data_from_db('hyatt')
ihgHotels = get_hotel_data_from_db('ihg')
marriottHotels = get_hotel_data_from_db('marriott')

for item in find_optimal(hyattHotels,marriottHotels,ihgHotels):
    print(item)

