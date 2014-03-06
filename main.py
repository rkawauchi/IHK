import argparse
import io

#Define commmand line arguments which can be passed to main.py
#Currently irrelevant, but could be useful later
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Simulate Indian health solutions')
    parser.add_argument('-s', '--solution', dest='solution', 
            help='the solution to test', default='health kiosk')
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = initialize_argument_parser()
    data = io.Database()
    
    print data.get_state_by_name('Mizoram')
    print data.get_state_by_abbreviation('KA')

    #for state in data.get_all_states():
    #    print state.to_dict()
