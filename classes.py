#Used to track physical location in the world
class Location:
    def __init__(self, lat, lon, street=None, city=None, region=None,
            country=''):
        self.lat=lat
        self.lon=lon
        self.street=street
        self.city=city
        self.region=region
        self.country=country

    #Ignore None values. Usually just lat/long, at least for now. 
    def __str__(self):
        return ' '.join([str(x) for x in [self.lat, self.lon, self.street, 
            self.city, self.region] if x is not None])

class Person:
    def __init__(self, name, location, income, blood_sugar):
        self.location = location 
        self.name=name
        self.income=income
        self.blood_sugar=blood_sugar

    #Separate on different lines because some fields (location) have multiple
    #fields in themselves
    def __str__(self):
        return ' \n'.join([str(x) for x in [self.name, self.location, self.income, self.blood_sugar]])

class Kiosk:
    def __init__(self, location, operator):
        self.location=location
        self.operator=operator

#Use as a pseudo-database until we have proper database integration
class Database:
    def __init__(self):
        self.all_people=dict()
        self.all_people['John Doe'] = Person(name='John Doe', 
                location=Location(0, 0), income=100, blood_sugar=50)
        self.all_people['Jane Smith'] = Person(name='Jane Smith', 
            location=Location(0, 0), income=200, blood_sugar=100)

    def get_patient_info(self, patient_name):
        return self.all_people[patient_name]
        
