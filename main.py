import argparse
import io
import people

#Define commmand line arguments which can be passed to main.py
#Currently irrelevant, but could be useful later
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Simulate Indian health solutions')
    parser.add_argument('-s', '--solution', dest='solution', 
            help='the solution to test', default='health kiosk')
    parser.add_argument('--import-data', dest='import_data',
            action='store_true', default=False,
            help='Recreate database from raw data files')
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = initialize_argument_parser()
    data = io.Database(import_data=args['import_data'])
    test_state_name = 'Meghalaya'
    test_state = data.get_state_by_name(test_state_name)
    print 'test_state', test_state
    test_district = data.get_districts_by_state_name(test_state_name)[0]
    print 'test:', test_district.name, 'in', test_state.name
    #people.generate_district_population(data, test_state, test_district)
    
    #demonstrate_queries(data)
