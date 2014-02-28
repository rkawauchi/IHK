import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

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
    household_poor = sqlalchemy.Column(sqlachemy.Integer)
    household_middle = sqlalchemy.Column(sqlachemy.Integer)
    household_rich = sqlalchemy.Column(sqlachemy.Integer)
    
    def __init__(self, name):
        self.name=name
        self.household_poor=household_poor
        self.household_middle=household_middle
        self.household_rich=household_rich

    def __repr__(self):
        return 'District({0}, {1}, {2}, {3}, {4})'.format(self.name,
                self.household_poor, self.household_middle,
                self.household_rich)

def fetch_session(db_filename = 'database.sqlite3'):
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db_filename))
    session = orm.sessionmaker(bind=engine)
    #Creates tables if they don't exist. If district doesn't exist, this
    #won't work, so don't do that.
    #Base.metadata.create_all(engine)
    return orm.scoped_session(session)

if __name__ == '__main__':
    session = fetch_session()
            
    #print session.query(District.classification=='Urban').all()
    print session.query(District).first()
