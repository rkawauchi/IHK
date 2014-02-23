import argparse
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

Base = declarative.declarative_base()

def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Debugging output')
    parser.add_argument('-n', '--name', dest='name', type=str,
            help='The name of the solution')
    parser.add_argument('--is-for-profit', dest='is_for_profit', type=int,
            help='1 if for profit, 0 if nonprofit')
    parser.add_argument('--founder-count', dest='founder_count', type=int,
            help='Number of founders')
    return vars(parser.parse_args())

class Solution(Base):
    __tablename__ = 'solutions'
    id = sqlalchemy.Column("rowid", sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    is_for_profit = sqlalchemy.Column(sqlalchemy.Integer)
    founder_count = sqlalchemy.Column(sqlalchemy.Integer)
    
    def __init__(self, name, is_for_profit):
        self.name=name

    def __repr__(self):
        return 'Solution({0}, {1})'.format(self.name, self.is_for_profit)

def fetch_session(db_filename = 'database.sqlite3'):
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db_filename))
    session = orm.sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return orm.scoped_session(session)

if __name__ == '__main__':
    args = initialize_argument_parser()
    session = fetch_session()
    table = Solution.__table__
    test = Solution('Herp', 1)
    insert = table.insert()
            
    conn = session.connection()
    keys = args.keys();
    conn.execute(insert, [args])

    #sqlalchemy.sql.expression.insert(table, test)
    #session.connection().execute(table.insert(test))
    print session.query(Solution).all()
    session.commit()
