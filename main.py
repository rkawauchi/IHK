import argparse
import matplotlib.pyplot as pyplot
import cPickle
import io_data
import util
import health
import cProfile
import copy
import os

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
    parser.add_argument('-t', '--trials', dest='trials', type=int,
            default=1, help='Number of simulation trials to run')
    parser.add_argument('--district-index', dest='district_index', type=int,
            default = 0, help='Select a district in a state by its index')
    parser.add_argument('-l', '--pop-gen-limit-dist', dest='pop_gen_limit_dist',
            type=int, default=None, 
            help='Limit the population inserted into each district for speed')
    parser.add_argument('--pop-fetch-limit-dist', dest='pop_fetch_limit_dist',
            type=int, default = None,
            help='Limit the population fetched from each district for speed')
    parser.add_argument('--profile', dest='profile', action='store_true',
            default=False, help='Profile running time')
    return vars(parser.parse_args())

#Put test code here so it doesn't clutter up the main method
def test(data, args, force_population = False):
    test_state_name = args['test_state']
    test_state = data.get_state_by_name(test_state_name)
    print 'test_state', test_state
    if args['test_district']:
        test_district = data.get_district_by_name(args['test_district'])
    else:
        test_district = data.get_districts_by_state_name(
                test_state_name)[args['district_index']]
    print 'test:', test_district.name, 'in', test_state.name
    
    #Generate the population
    data.populate_district_total(test_district,
            limit = args['pop_gen_limit_dist'], force = force_population)

    #Fetch the population from the database
    population = data.get_population_district(test_district.name,
            limit=args['pop_fetch_limit_dist'])
    print 'Testing population of', len(population), 'people'
    #eye_health_treatment_thresholds = util.calc_eye_health_treatment_thresholds( population)

    #Create a solution to treat the population
    solution = health.Aravind()
    #districts = [data.get_district_by_name(district_name) for district_name in solution.get_covered_district_names()] 
    #Need to use all treatment costs for more intelligent filtering
    #filter_test = util.FilterPopulation(max(solution.treatment_costs.values()),
    #        eye_health_treatment_thresholds)

    #Treat the population using the solution
    treated_population = list()
    for person in population:
        treated_person = copy.copy(person)
        if solution.treat(treated_person):
            treated_person.set_treated(True)
        treated_population.append(treated_person)

    qaly_improvement = util.analyze_populations(population, treated_population)
    return qaly_improvement

def iterated_test(data, args):
    qaly_improvement = list()
    output_file = open('qaly_improvement.csv', 'w')
    for i in xrange(args['trials']):
        #If we're doing multiple tests, need to refresh the database
        if i>0:
            data = io_data.Database()
        qaly_improvement.append(test(data, args, force_population = True))
        #Safe the qaly improvement to file so we can manipulate it later
        output_file.write('{0},{1}\n'.format(i, qaly_improvement[i]))
    print qaly_improvement
    pyplot.hist(qaly_improvement)
    pyplot.xlabel('QALY Improvement')
    pyplot.ylabel('Trial Count')
    pyplot.show()

if __name__ == "__main__":
    args = initialize_argument_parser()
    if args['import_data']:
        try:
            os.remove('database.sqlite3')
        except:
            pass
    data = io_data.Database(import_data=args['import_data'])
    #Only run the test if we didn't try to recreate the database
    # Not strictly necessary, but helps separate workflow
    if not args['import_data']:
        if args['profile']:
            cProfile.run('iterated_test(data, args)')
        else:
            iterated_test(data, args)
