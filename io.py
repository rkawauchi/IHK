import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative
import util
import csv

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

class Database(object):

    def __init__(self, db_filename = 'database.sqlite3'):
        self.session = fetch_session(db_filename)
        self.connection = self.session.connection()

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

def fetch_session(db_filename):
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db_filename))
    session = orm.sessionmaker(bind=engine)
    #Creates tables if they don't exist.
    Base.metadata.create_all(engine)
    return orm.scoped_session(session)

def import_mpce():
    #http://www.blog.pythonlibrary.org/2014/02/26/python-101-reading-and-writing-csv-files/
    with open('data/mpce/urp_rural.csv', 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            #remove extra spaces around each element in the row
            row = [value.strip() for value in row]
            print row

if __name__ == '__main__':

    import_mpce()
