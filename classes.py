class Location:
    def __init__(self, lat, lon, street='', city='', region='',
            country=''):
        self.lat=lat
        self.lon=lon
        self.street=street
        self.city=city
        self.region=region
        self.country=country

class Person:
    def __init__(self, location, name='', income=0):
        self.location = location 
        self.name=name
        self.income=income

class Kiosk:
    def __init__(self, location, operator):
        self.location=location
        self.operator=operator

