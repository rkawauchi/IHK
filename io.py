import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative
import util
import csv
import os
import re

Base = declarative.declarative_base()

class District(Base):
    __tablename__ = 'districts'
    id = sqlalchemy.Column('rowid', sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)
    classification = sqlalchemy.Column(sqlalchemy.String)
    household_total = sqlalchemy.Column(sqlalchemy.Integer)
    population_total = sqlalchemy.Column(sqlalchemy.Integer)
    #population_male = sqlalchemy.Column(sqlalchemy.Integer) 
    #population_female =  sqlalchemy.Column(sqlalchemy.Integer) 
    
    def __init__(self, name, state, classification, household_total,
            population_total):
        self.name=name
        self.state=state
        self.classification=classification
        self.household_total=household_total
        self.population_total=population_total

    def __repr__(self):
        return 'District({0}, {1}, {2}, {3}, {4})'.format(self.name, self.state,
                self.classification, self.household_total,
                self.population_total)

class State(Base):
    __tablename__ = 'states'
    id = sqlalchemy.Column('rowid', sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    abbreviation = sqlalchemy.Column(sqlalchemy.String)
    classification = sqlalchemy.Column(sqlalchemy.String)
    household_total = sqlalchemy.Column(sqlalchemy.Integer)
    population_total = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, name, abbreviation, classification, household_total,
            population_total):
        self.name=name
        self.abbreviation=abbreviation
        self.classification=classification
        self.household_total=household_total
        self.population_total=population_total

    def __repr__(self):
        return 'State({0}, {1}, {2}, {3}, {4})'.format(self.name,
                self.abbreviation, self.classification, self.household_total,
                self.population_total)

    def to_dict(self):
        return {'name': self.name, 'abbreviation': self.abbreviation, 
                'classification': self.classification,
                'household_total': self.household_total,
                'population_total': self.population_total}

class Mpce(Base):
    __tablename__ = 'mpce'
    id = sqlalchemy.Column('rowid', sqlalchemy.Integer, primary_key = True)
    #urban or rural
    classification = sqlalchemy.Column(sqlalchemy.String)
    #those funky mpce acronyms
    mpce_type = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)
    d1 = sqlalchemy.Column(sqlalchemy.Integer)
    d2 = sqlalchemy.Column(sqlalchemy.Integer)
    d3 = sqlalchemy.Column(sqlalchemy.Integer)
    d4 = sqlalchemy.Column(sqlalchemy.Integer)
    d5 = sqlalchemy.Column(sqlalchemy.Integer)
    d6 = sqlalchemy.Column(sqlalchemy.Integer)
    d7 = sqlalchemy.Column(sqlalchemy.Integer)
    d8 = sqlalchemy.Column(sqlalchemy.Integer)
    d9 = sqlalchemy.Column(sqlalchemy.Integer)
    mpce_average = sqlalchemy.Column(sqlalchemy.Integer)
    household_total = sqlalchemy.Column(sqlalchemy.Integer)
    household_sample = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, mpce_type, classification, state, 
            d1, d2, d3, d4, d5, d6, d7, d8, d9,
            mpce_average, household_total, household_sample):
        self.mpce_type = mpce_type
        self.classification = classification
        self.state = state
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.d4 = d4
        self.d5 = d5
        self.d6 = d6
        self.d7 = d7
        self.d8 = d8
        self.d9 = d9
        self.mpce_average = mpce_average
        self.household_total = household_total
        self.household_sample = household_sample

    def __repr__(self):
        return 'MPCE({0}, {1}, {2})'.format(self.mpce_type, 
                self.classification, self.state)

class Person(Base):
    __tablename__ = 'people'
    id = sqlalchemy.Column('rowid', sqlalchemy.Integer, primary_key = True)
    money = sqlalchemy.Column(sqlalchemy.Integer)
    #currently assuming 0-1 ranking for health measures
    #the data type may change laters
    diabetes = sqlalchemy.Column(sqlalchemy.Float)
    cardio = sqlalchemy.Column(sqlalchemy.Float)
    district = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)
    #urban or rural
    classification = sqlalchemy.Column(sqlalchemy.String)

    def __init__(self, money, diabetes, cardio, district, state,
            classification):
        self.money = money
        self.diabetes = diabetes
        self.cardio = cardio
        self.district = district
        self.state = state
        self.classification = classification

    #missing proper __repr__

class Database(object):

    def __init__(self, db_filename = 'database.sqlite3', import_data=False):
        self.engine, self.session = fetch_session(db_filename)
        self.connection = self.session.connection()
        if import_data:
            #Creates tables if they don't exist.
            Base.metadata.create_all(self.engine)
            self._init_mpce()
            self._init_states()
            #self._init_districts()
            self.session.commit()

    def _init_states(self):
        self._wipe_states()
        for i, state_name in enumerate(util.state_names):
            population_urban = self._get_district_population_by_state(
                    state_name, 'urban', District.population_total)
            household_urban = self._get_district_population_by_state(
                    state_name, 'urban', District.household_total)
            population_rural = self._get_district_population_by_state(
                    state_name, 'rural', District.population_total)
            household_rural = self._get_district_population_by_state(
                    state_name, 'rural', District.household_total)
            population_total = population_urban + population_rural
            household_total = household_urban + household_rural
            self._add_state(state_name, util.state_abbreviations[i], 'urban',
                    population_urban, household_urban)
            self._add_state(state_name, util.state_abbreviations[i], 'rural',
                    population_rural, household_rural)
            self._add_state(state_name, util.state_abbreviations[i], 'total',
                    population_total, household_total)

    def _get_district_population_by_state(self, state_name, classification, population_type):
        query = self.session.query(
                District.state, District.classification,
                sqlalchemy.func.sum(population_type)) \
                .filter(District.state == state_name) \
                .filter(District.classification == classification) \
                .group_by(District.state).first()
        return query[2]

    def _wipe_states(self):
        table = State.__table__
        delete = table.delete()
        self.connection.execute(delete)

    def _add_state(self, name, abbreviation, classification,
            population_total, household_total):
        table = State.__table__
        insert = table.insert()
        self.connection.execute(insert, name=name, abbreviation = abbreviation,
                classification=classification, 
                population_total=population_total,
                household_total = household_total)

    #import all MPCE data
    #single underscore implies that the method is private
    def _init_mpce(self):
        #wipe the existing MPCE table so we don't have duplicates
        delete = Mpce.__table__.delete()
        self.connection.execute(delete)

        mpce_directory = 'data/mpce/'
        for filename in os.listdir(mpce_directory):
            if filename.endswith('.csv'):
                mpce_type, classification = extract_mpce_info(filename)
                with open(mpce_directory + filename, 'r') as input_file:
                    self._import_mpce_file(input_file, mpce_type,
                            classification)

    def _import_mpce_file(self, input_file, mpce_type, classification):
        #http://www.blog.pythonlibrary.org/2014/02/26/python-101-reading-and-writing-csv-files/
        reader = csv.reader(input_file)
        for row in reader:
            #The first row is just the headers, so we skip it 
            if row[0] == 'state':
                continue
            #remove extra spaces around each element in the row
            row = [value.strip() for value in row]
            #Create a Mpce object - makes things easier to insert
            #This is not a very efficient method, but it works
            mpce = Mpce(mpce_type, classification, *row)
            #add the row to the mpce table
            insert = Mpce.__table__.insert()
            self.connection.execute(insert, mpce.__dict__)

    #todo - NOT FINISHED
    def _init_districts(self):
        #wipe the existing districts table so we don't have duplicates
        delete = District.__table__.delete()
        self.connection.execute(delete)

        district_directory = 'data/districts/'
        for filename in os.listdir(district_directory):
            if filename.endswith('.CSV'):
                state_name = clean_state_name(filename)
                with open(district_directory + filename, 'r') as input_file:
                    self._import_district_file(input_file, state_name)
                """
                with open(district_directory + filename, 'r') as input_file:
                    self._import_mpce_file(input_file, mpce_type,
                            classification)
                """

    def _import_district_file(self, input_file, state_name):
        #http://stackoverflow.com/questions/3122206/how-to-define-column-headers-when-reading-a-csv-file-in-python
        #http://courses.cs.washington.edu/courses/cse140/13wi/csv-parsing.html
        reader = csv.DictReader(input_file)
        headers = reader.next()
        insert = District.__table__.insert()
        for row in reader:
            #we only care about districts
            if row['Level'] == 'STATE': continue
            name = row['Name'].strip()
            classification = row['TRU'].lower()
            households = int(row['No of Households'])
            population = int(row['Total Population Person'])
            district = District(name, state_name, classification, 
                    households, population)
            self.connection.execute(insert, district.__dict__)

    def get_all_states(self):
        return self.session.query(State).all()

    def get_state_by_name(self, name):
        return self.session.query(State).filter(State.name == name).first()

    def get_state_by_abbreviation(self, abbreviation):
        return self.session.query(State).filter(
                State.abbreviation == abbreviation).first()

    def get_districts_by_state_name(self, state_name):
        return self.session.query(District).filter(
                District.state == state_name).all()

    def get_districts_by_state(self, state):
        return self.session.query(District).filter(
                District.state == state.name).all()

#given a filename, determine classification and mpce_type
#filename is assumed to be of a format like "mmrp_rural.csv" 
#because that's how I named them.
def extract_mpce_info(filename):
    filename = re.sub('.csv', '', filename)
    filename_split = filename.split('_')
    mpce_type = filename_split[0]
    classification = filename_split[1]
    return mpce_type, classification

def extract_district_name(filename):
    #The name is the first thing in the filename
    #it is always followed by a non-word character
    #sometimes & is in the name, so allow that 
    district = re.sub(r'\.CSV', '', filename)
    district = re.sub(r'\([A-Z&]*\)', '', district)
    district = re.sub(r'[()\d]', '', district)
    district = re.sub('Nct of Delhi', 'Delhi', district)
    district = re.sub('JAMMU', 'Jammu', district)
    district = re.sub('Utter', 'Uttar Pradesh', district)
    district = re.sub('&', 'and', district)
    district = district.strip()
    return district

def fetch_session(db_filename):
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db_filename))
    session = orm.sessionmaker(bind=engine)
    return engine, orm.scoped_session(session)


if __name__ == '__main__':
    data = Database()
    print data.session.query(Mpce).filter(Mpce.state=='Andhra Pradesh').limit(10).all()
