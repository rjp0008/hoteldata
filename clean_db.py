import sqlite3
import requests
import apiKey
import json
#Cardinal Rosales Avenue Cebu City
google_error = 'OVER_QUERY_LIMIT'

conn = sqlite3.connect('hotel.db')
c = conn.cursor()
c = c.execute("SELECT * FROM Hotels WHERE google_text LIKE '%OVER_QUERY_LIMIT%'")
list = c.fetchall()
addresses = []
for item in list:
    addresses.append(item[7])
for item in addresses:
    try:
        res = requests.get(
            'https://maps.google.com/maps/api/geocode/json?address=' + item + '&key=' + apiKey.key)
        res.raise_for_status()
        jsonObj = json.loads(res.text)
        google_text = res.text
        lat = jsonObj.get('results')[0].get('geometry').get('location')['lat']
        lng = jsonObj.get('results')[0].get('geometry').get('location')['lng']
        c.execute("UPDATE Hotels SET lat='"+str(lat)+"', lng='"+str(lng)+"',google_text='"+google_text+"' WHERE address LIKE '%"+item+"%'")
        conn.commit()
        print(item)
        if google_error in google_text:
            break
    except Exception as e:
        print(e)
        pass

conn.close()