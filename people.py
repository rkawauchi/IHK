import io

def generate_population(data):
    for state in data.session.query(io.State):
        generate_state_population(data, state)

def generate_state_population(data, state):
    #get only the "total population" entry for each district
    for district in data.session.query(io.District).filter(
            io.District.state == state.name).filter(
            io.District.classification == 'Total'):
        generate_district_population(data, state, district)

#Accept district and state objects, plus the Database object from io.py
def generate_district_population(data, state, district):
    #Bulk insert as per http://docs.sqlalchemy.org/en/rel_0_8/faq.html
    #split into multiple insertion waves due to memory limitations
    insertions_per_wave = 1000000
    #insert the population in waves of 1000000 people 
    for i in xrange(district.population_total/insertions_per_wave):
        insert_wave(data, state, district, insertions_per_wave)
        print 'wave inserted'
    #insert the last few people
    insert_wave(data, state, district, district.population_total % insertions_per_wave)
    #commit the changes; otherwise, they will be wasted!
    data.session.commit()
    print 'Population of', district.name, 'inserted'

def insert_wave(data, state, district, insertion_count):
    insert = io.Person.__table__.insert()
    data.engine.execute(insert, [generate_person_dict(data, state, district)
            for j in xrange(insertion_count)])

#generate a dict of values corresponding to the attributes of a Person
def generate_person_dict(data, state, district):
    #This is where math and statistics comes in
    return {'money': 1337, 'diabetes': 0.1,
            'cardio': 0.2, 'district': district.name, 'state': state.name,
            'classification': 'ignored'}

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
