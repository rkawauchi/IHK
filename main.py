import argparse
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Debugging output')
    parser.add_argument('-n', '--name', dest='name', type=str,
            help='The name of the solution')
    parser.add_argument('--is_for_profit', dest='is_for_profit', type=int,
            help='1 if for profit, 0 if nonprofit')
    return vars(parser.parse_args())

class Solution(declarative.declarative_base()):
    __tablename__ = 'solutions'
    id = sqlalchemy.Column("rowid", sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    is_for_profit = sqlalchemy.Column(sqlalchemy.Integer)
    
    def __init__(self, name, is_for_profit):
        self.name=name

    def __repr__(self):
        return 'Solution({0}, {1})'.format(self.name, self.is_for_profit)

def fetch_session(db_filename = 'database.sqlite3'):
    engine = sqlalchemy.create_engine('sqlite:///{0}'.format(db_filename))
    session = orm.sessionmaker(bind=engine)
    return orm.scoped_session(session)

if __name__ == '__main__':
    args = initialize_argument_parser()
    print 'Hello world'
    print "Emilie"
    print "second test"
    session = fetch_session()
    print session.query(Solution).all()
