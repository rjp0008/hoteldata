import requests
import json
import apiKey
import sys
import sqlite3

class Hotel:
    def __init__(self):
        self.url = ""
        self.address = ""
        self.name = ""
        self.lat = 0
        self.lng = 0
        self.group = ""
        self.category = 0
        self.google_text = ""

    def __str__(self):
        return self.url + " " + self.address

    def update_from_google(self):
        try:
            res = requests.get('https://maps.google.com/maps/api/geocode/json?address=' + self.address + '&key=' + apiKey.key)
            res.raise_for_status()
            jsonObj = json.loads(res.text)
            self.google_text = res.text
            self.lat = jsonObj.get('results')[0].get('geometry').get('location')['lat']
            self.lng = jsonObj.get('results')[0].get('geometry').get('location')['lng']
            return True
        except:
            return False

    def save_to_db(self):
        values = "'" + self.name.replace("'","''").encode(sys.stdout.encoding, errors='replace').decode('utf-8').strip() + "','" + self.url.replace("'","''") + "','" +str(self.lat) + "','" +str(self.lng) + "','" + self.group + "'," +str(self.category) + ",'" +self.google_text.replace("'","''") + " ','"+self.address.replace("'","''").encode(sys.stdout.encoding, errors='replace').decode('utf-8').strip()+" '"
        conn = sqlite3.connect('hotel.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO Hotels VALUES (" + values + ")" )
        except Exception as e:
            c.execute("INSERT INTO errors VALUES('" + str(e).replace("'","''")+"'")
        conn.commit()
        conn.close()