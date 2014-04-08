import argparse
import io_data
import util
import health
import cProfile

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
    parser.add_argument('--pop-gen-limit-dist', dest='pop_gen_limit_dist',
            type=int, default=None, 
            help='Limit the population inserted into each district for speed')
    parser.add_argument('--pop-fetch-limit-dist', dest='pop_fetch_limit_dist',
            type=int, default = None,
            help='Limit the population fetched from each district for speed')
    parser.add_argument('--profile', dest='profile', action='store_true',
            default=False, help='Profile running time')
    return vars(parser.parse_args())

def avg(x):
    return float(sum(x)/len(x))

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
    
    #Generate the population
    data.populate_district_total(test_district,
            limit = args['pop_gen_limit_dist'])

    #Fetch the population from the database
    population = data.get_population_district(test_district.name,
            limit=args['pop_fetch_limit_dist'])
    print 'Testing population of', len(population), 'people'

    #Create a solution to treat the population
    solution = health.Aravind(treatment_cost = 500)
    #districts = [data.get_district_by_name(district_name) for district_name in solution.get_covered_district_names()] 
    filter_test = util.FilterPopulation(solution.treatment_cost, 1, 1)

    #Treat the population using the solution
    treated_population = [solution.treat(person) if filter_test.filter_all(person) else person for person in population]

    #Perform analytics on the treated population
    print 'Average eye health in original population', avg([person.eye_health for person in population])
    print 'Average eye health in treated population', avg([person.eye_health for person in treated_population])
    
if __name__ == "__main__":
    args = initialize_argument_parser()
    data = io_data.Database(import_data=args['import_data'])
    #Only run the test if we didn't try to recreate the database
    # Not strictly necessary, but helps separate workflow
    if not args['import_data']:
        if args['profile']:
            cProfile.run('test(data, args)')
        else:
            test(data, args)
