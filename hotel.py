import requests
import json
import apiKey

class Hotel:
    def __init__(self):
        self.url = ""
        self.address = ""
        self.name = ""
        self.long_names = []
        self.short_names = []
        self.lat = 0
        self.lng = 0

    def __str__(self):
        return self.url + " " + self.address

    def update_from_google(self):
        try:
            res = requests.get('https://maps.google.com/maps/api/geocode/json?address=' + self.address + '&key=' + apiKey.key)
            res.raise_for_status()
            jsonObj = json.loads(res.text)
            self.lat = jsonObj.get('results')[0].get('geometry').get('location')['lat']
            self.lng = jsonObj.get('results')[0].get('geometry').get('location')['lng']
            return True
        except:
            return False
