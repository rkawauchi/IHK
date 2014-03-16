import argparse
import io
import people

#Define commmand line arguments which can be passed to main.py
#Currently irrelevant, but could be useful later
def initialize_argument_parser():
    parser = argparse.ArgumentParser(description='Simulate Indian health solutions')
    parser.add_argument('-s', '--solution', dest='solution', 
            help='the solution to test', default='health kiosk')
    return vars(parser.parse_args())

def demonstrate_queries(data):
    
    mizoram = data.get_state_by_name('Mizoram')
    karnataka = data.get_state_by_abbreviation('KA')

    print mizoram
    print karnataka

    mizoram_districts = data.get_districts_by_state_name('Mizoram')
    same_mizoram_districts = data.get_districts_by_state_name(mizoram.name)
    also_same_mizoram_districts = data.get_districts_by_state(mizoram)
    
    print mizoram_districts
    print mizoram_districts == also_same_mizoram_districts

    #for state in data.get_all_states():
    #    print state.to_dict()

if __name__ == "__main__":
    args = initialize_argument_parser()
    data = io.Database()
    test_state_name = 'Andhra Pradesh'
    test_state = data.get_state_by_name(test_state_name)
    test_district = data.get_districts_by_state_name(test_state_name)[0]
    print 'test:', test_district.name, 'in', test_state.name
    people.generate_district_population(data, test_state, test_district)
    
    #demonstrate_queries(data)
