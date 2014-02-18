import argparse
import sqlalchemy

def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Debugging output')
    parser.add_argument('-n', '--name', dest='name', type=str,
            help='The name of the solution')
    parser.add_argument('--is_for_profit', dest='is_for_profit', type=int,
            help='1 if for profit, 0 if nonprofit')
    return vars(parser.parse_args())

class Solution(base):
    __tablename__ = 'solutions'
    id = sqlalchemy.Column("rowid", sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    is_for_profit = sqlalchemy.Column(sqlalchemy.Integer)
    
    def __init__(self, name, is_for_profit):
        self.name=name

    def __repr__(self):
        return 'Solution({0}, {1})'.format(self.name, self.is_for_profit)

if __name__ == '__main__':
    args = initialize_argument_parser()
    print 'Hello world'
    print "Emilie"
    print "second test"
    database = classes.Database()
    print 'patient info: ', database.get_patient_info(args['patient_name'])
