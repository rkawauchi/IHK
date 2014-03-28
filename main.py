import argparse
import io
import util

#Define commmand line arguments which can be passed to main.py
#Currently irrelevant, but could be useful later
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Simulate Indian health solutions')
    parser.add_argument('--solution', dest='solution', 
            help='the solution to test', default='health kiosk')
    parser.add_argument('-i', '--import-data', dest='import_data',
            action='store_true', default=False,
            help='Recreate database from raw data files')
    parser.add_argument('-s', '--test-state', dest='test_state', type=str,
            choices = util.state_names)
    parser.add_argument('-d', '--test-district', dest='test_district', type=str)
    return vars(parser.parse_args())

#Put test code here so it doesn't clutter up the main method
def test(data, args):
    test_state_name = args['test_state']
    test_state = data.get_state_by_name(test_state_name)
    print 'test_state', test_state
    if args['test_district']:
        test_district = data.get_district_by_name(args['test_district'])
    else:
        test_district = data.get_districts_by_state_name(test_state_name)[0]
    print 'test:', test_district.name, 'in', test_state.name
    
    data.init_district(test_district, force=True)
    
    #util.demonstrate_queries(data)

if __name__ == "__main__":
    args = initialize_argument_parser()
    data = io.Database(import_data=args['import_data'])
    test(data, args)
