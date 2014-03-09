import io

class Person():
    def __init__(self, money, diabetes, cardio, district, state, classification):
        self.money = money
        self.diabetes = diabetes
        self.cardio = cardio
        self.district = district
        self.state = state
        self.classification = classification

    def __str__(self):
        return 'I am a person'

def generate_population(data):
    for state in data.session.query(io.State):
        generate_state_population(data, state)

def generate_state_population(data, state):
    for district in data.get_districts_by_state_name(state.name):
        generate_district_population(data, state, district)

#Accept district and state objects, plus the Database object from io.py
def generate_district_population(data, state, district):
    for i in xrange(district.population_total):
        person = io.Person(money = 1337, diabetes = 0.1, cardio = 0.2, 
                district = district.name, state = state.name,
                classification = 'ignored')
        insert = io.Person.__table__.insert()
        data.connection.execute(insert, person.__dict__)
    #commit the changes; otherwise, they will be wasted!
    data.session.commit()
    print 'Population of', district.name, 'inserted'
    

#THIS METHOD DOES NOT WORK
#It is kept as a reminder of why we can't generate the entire population at once
#Accept Database object from io.py as input
def generate_people(data):
    population = list()
    for state in data.session.query(io.State).all():
        for district in data.get_districts_by_state_name(state.name):
            for i in xrange(district.population_total):
                population.append(Person('money', 'diabetes', 'cardio', 
                    district.name, state.name, 'ignored'))
            print 'district', district.name
        print 'state', state.name
    return population
