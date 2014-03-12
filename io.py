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
    
    def __init__(self, name, abbreviation):
        self.name=name
        self.abbreviation = abbreviation

    def __repr__(self):
        return 'State({0}, {1})'.format(self.name, self.abbreviation)

    def to_dict(self):
        return {'name': self.name, 'abbreviation': self.abbreviation}

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
            Base.metadata.create_all(engine)
            self._import_mpce()

    def init_states(self):
        self.wipe_states()
        for i, state in enumerate(util.state_names):
            self.add_state(state, util.state_abbreviations[i])
        self.session.commit()

    def wipe_states(self):
        table = State.__table__
        delete = table.delete()
        self.connection.execute(delete)

    def add_state(self, state_name, state_abbreviation):
        table = State.__table__
        insert = table.insert()
        self.connection.execute(insert, name=state_name, abbreviation = state_abbreviation)

    #import all MPCE data
    #single underscore implies that the method is private
    def _import_mpce(self):
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
        self.session.commit()

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
    
def fetch_session(db_filename):
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db_filename))
    session = orm.sessionmaker(bind=engine)
    return engine, orm.scoped_session(session)


if __name__ == '__main__':
    data = Database()
    print data.session.query(Mpce).filter(Mpce.state=='Andhra Pradesh').limit(10).all()
