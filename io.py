import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative
import util

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

def fetch_session(db_filename = 'database.sqlite3'):
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db_filename))
    session = orm.sessionmaker(bind=engine)
    #Creates tables if they don't exist.
    Base.metadata.create_all(engine)
    return orm.scoped_session(session)

def init_states():
    session = fetch_session()
    connection = session.connection()
    wipe_states(connection)
    for state in util.state_names: 
        add_state(connection, state, 'temp')
    session.commit()

def wipe_states(connection):
    table = State.__table__
    delete = table.delete()
    connection.execute(delete)

def add_state(connection, state_name, state_abbreviation):
    table = State.__table__
    insert = table.insert()
    connection.execute(insert, name=state_name, abbreviation = state_abbreviation)

if __name__ == '__main__':
    session = fetch_session()
            
    #print session.query(District.classification=='Urban').all()
    print session.query(District).first()
