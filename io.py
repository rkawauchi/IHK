import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

Base = declarative.declarative_base()

class District(Base):
    __tablename__ = 'district'
    id = sqlalchemy.Column('rowid', sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    state = sqlalchemy.Column(sqlalchemy.String)
    classification = sqlalchemy.Column(sqlalchemy.String)
    household_total = sqlalchemy.Column(sqlalchemy.Integer)
    population_total = sqlalchemy.Column(sqlalchemy.Integer)
    #population_male = sqlalchemy.Column(sqlalchemy.Integer) 
    #population_female =  sqlalchemy.Column(sqlalchemy.Integer) 
    
    def __init__(self, name, is_for_profit):
        self.name=name

    def __repr__(self):
        return 'Solution({0}, {1})'.format(self.name, self.is_for_profit)

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
    print session.query(District).all()
