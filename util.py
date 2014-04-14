import re
import random
import bisect
import numpy as np

#http://www.gefeg.com/edifact/d03a/s3/codes/cl1h.htm
#This is a terrible method, but it works for now
state_names = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
state_abbreviations = ['AP', 'AR', 'AS', 'BR', 'CT', 'DL', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OR', 'PB', 'RJ', 'SK', 'TN', 'TR', 'UP', 'UT', 'WB']

#Other utility methods (that aren't input/output) which multiple 
#files might need go here

def clean_state_filename(filename):
    #The name is the first thing in the filename
    #it is always followed by a non-word character
    #sometimes & is in the name, so allow that 
    state = re.sub(r'\.CSV', '', filename)
    state = re.sub(r'\([A-Z&]*\)', '', state)
    state = re.sub(r'[()\d]', '', state)
    return clean_state_name(state)

def clean_state_name(state):
    state = re.sub('Nct of Delhi', 'Delhi', state)
    state = re.sub('JAMMU', 'Jammu', state)
    state = re.sub('Utter', 'Uttar Pradesh', state)
    state = re.sub('Himacahl', 'Himachal', state)
    state = re.sub('&', 'and', state)
    state = state.strip()
    if state not in state_names:
        print 'Warning: state name not found while cleaning:', state
    return state

def avg(x):
    return float(sum(x)/len(x))

class FilterPopulation(object):
    
    def __init__(self, cost_threshold):
        self.cost_threshold = cost_threshold
        self.eye_health_treatment_thresholds = eye_health_treatment_thresholds

    def filter_all(self, person):
        return self.filter_health(person) and self.filter_money(person)

    def filter_health(self, person):
        return self.filter_eye_health(person)

    def filter_eye_health(self, person):
        #We only care about the largest treatment threshold
        return person.eye_health <= max(
                self.eye_health_treatment_thresholds.values())

    """
    def filter_eye_health_surgery(self, person):
        # filter for those who need surgery who is about 10 % of the population
        return person.eye_health <= self.eye_health_threshold_surgery

    def filter_eye_health_glasses(self, person):
        # filter for those who need glasses who is about 30 % of the population
        return person.eye_health <= self.eye_health_threshold_glasses
    """

    def filter_money(self, person):
        return person.money>=self.cost_threshold

class Location(object):
    def __init__(self, state_name, district_name, classification):
        self.state_name = state_name
        self.district_name = district_name
        self.classification = classification

    def is_in(self, location):
        if not self.district_name == location.district_name:
            return False
        if not self.state_name == location.state:
            return False
        if location.classification == 'total' or self.classification == location.classification:
            return True

def calc_eye_health_treatment_thresholds(population):
    eye_health_treatment_thresholds = dict()
    # thresholds for surgery and glasses in filtering the people
    eye_health_treatment_thresholds['surgery'] = np.percentile(
            [person.eye_health for person in population], 10)
    eye_health_treatment_thresholds['glasses'] = np.percentile(
            [person.eye_health for person in population], 30)
    return eye_health_treatment_thresholds

#http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
#Given a set of choices and corresponding weights, choose a random option
#using the appropriate weight
def weighted_choice(choices, weights):
    #Convert the weights into cumulative weights
    cumulative_weights = []
    total = 0
    for weight in weights:
        total += weight
        cumulative_weights.append(total)
    #total should 1 if weights is a proper distribution
    rnd = random.random() * total
    i = bisect.bisect(cumulative_weights, rnd) #faster search
    return choices[i]

def init_life_expectancy_distribution():
    #One per five years of life
    life_expectancy = dict()
    life_expectancy_anchor_points_male = [63.8, 62.7, 58.1, 53.4, 52.9, 44.2,
            39.7, 35.3, 31.1, 26.9, 23, 19.3, 15.7, 12.7, 10.2, 8.3, 6.7,5.2,
            3.9, 2.8, 2.0]
    life_expectancy['M'] = list()
    for i in xrange(20):
        current_spread = np.linspace(life_expectancy_anchor_points_male[i],
                life_expectancy_anchor_points_male[i+1], num=5)
        for life_expectancy_at_age in current_spread:
            life_expectancy['M'].append(life_expectancy_at_age)
    life_expectancy['M'].append(life_expectancy_anchor_points_male[-1])

    life_expectancy_anchor_points_female = [67.3, 66.8, 62.2, 57.5, 52.9, 48.4,
            43.8, 39.2, 34.7, 30.2, 25.8, 25.8, 17.7, 14.3, 11.3, 9.0, 7.0, 5.3,
            3.9, 2.8, 2.0]
    life_expectancy['F'] = list()
    for i in xrange(20):
        current_spread = np.linspace(life_expectancy_anchor_points_female[i],
                life_expectancy_anchor_points_female[i+1], num=5)
        for life_expectancy_at_age in current_spread:
            life_expectancy['F'].append(life_expectancy_at_age)
    life_expectancy['F'].append(life_expectancy_anchor_points_female[-1])

    return life_expectancy

life_expectancy = init_life_expectancy_distribution()

def calculate_life_exp(gender, age):
    # life-expectancy data from 
    # http://www.worldlifeexpectancy.com/country-health-profile/india
    return life_expectancy[gender][age]

def calculate_qaly(person):
    age = person.age
    life_exp = calculate_life_exp(person.gender, age)
    util = person.health_utility
    return life_exp * util

#Perform analytics on the treated population
def analyze_populations(population, treated_population):
    print 'Average health utility in original population', avg(
            [person.health_utility for person in population])
    print 'Average health utility in treated population', avg(
            [person.health_utility for person in treated_population])
    print 'Average age of original population:', avg(
            [person.age for person in population])
    print 'average age of treated population:', avg(
            [person.age for person in treated_population])

    ##### QALY for Glasses #####

    # generate before and after population
    glasses_problem = Problem.from_problem_name('glasses')
    glasses_population_before = [person for person in population if 
            person.has_problem(glasses_problem)]
    glasses_population_after = [person for person in treated_population if 
            person.has_problem(glasses_problem)]
    print 'No. of patients - Glasses: ', len(glasses_population_before)
    # QALY_before
    glasses_untreated_qaly = 0
    for person in glasses_population_before:
        glasses_untreated_qaly += calculate_qaly(person)
    glasses_average_untreated_qaly = glasses_untreated_qaly/len(glasses_population_before)
    print 'QALY-Glasses: untreated:', glasses_average_untreated_qaly

    # QALY_after
    glasses_treated_qaly = 0
    for person in glasses_population_after:
        glasses_treated_qaly += calculate_qaly(person)
    glasses_average_treated_qaly = glasses_treated_qaly/len(glasses_population_after)
    print 'QALY-Glasses: treated:', glasses_average_treated_qaly

    print '* QALY-Glasses: change by:', glasses_average_treated_qaly - glasses_average_untreated_qaly

     ##### QALY for Cataracts #####

    # generate before and after population
    cataracts_problem = Problem.from_problem_name('cataracts')
    cataracts_population_before = [person for person in population if 
            person.has_problem(cataracts_problem)]
    cataracts_population_after = [person for person in treated_population if 
            person.has_problem(cataracts_problem)]
    print 'No. of patients - Cataracts: ', len(cataracts_population_before)
    # QALY_before
    cataracts_untreated_qaly = 0
    for person in cataracts_population_before:
        cataracts_untreated_qaly += calculate_qaly(person)
    cataracts_average_untreated_qaly = cataracts_untreated_qaly/len(cataracts_population_before)
    print 'QALY-Cataracts: untreated:', cataracts_average_untreated_qaly

    # QALY_after
    cataracts_treated_qaly = 0
    for person in cataracts_population_after:
        cataracts_treated_qaly += calculate_qaly(person)
    cataracts_average_treated_qaly = cataracts_treated_qaly/len(cataracts_population_after)
    print 'QALY-Cataracts: treated:', cataracts_average_treated_qaly
    
    print '* QALY-Cataracts: change by:', cataracts_average_treated_qaly - cataracts_average_untreated_qaly

def old_qaly_calc(population, treated_population):
    # generate before and after population
    glasses_problem = Problem.from_problem_name('glasses')
    glasses_population_before = [person for person in population if 
            person.has_problem(glasses_problem)]
    glasses_population_after = [person for person in treated_population if 
            person.has_problem(glasses_problem)]
    # calculate ave_age
    glasses_age_before = avg([person.age for person in glasses_population_before])
    glasses_age_after = avg([person.age for person in glasses_population_after])
    # calculate life_exp
    glasses_life_expectancy_before = 68
    glasses_life_expectancy_after = 72
    glasses_utility_before = avg([person.health_utility for person in glasses_population_before])
    glasses_utility_after = avg([person.health_utility for person in glasses_population_after])
    glasses_utility_change = glasses_utility_after - glasses_utility_before
    qaly_glasses_before = glasses_life_expectancy_before + glasses_utility_before
    qaly_glasses_after = glasses_life_expectancy_after + glasses_utility_after
    qaly_change_glasses = qaly_glasses_after - qaly_glasses_before
    print 'QALY_Glasses: before treatment', qaly_glasses_before
    print 'QALY_Glasses: after treatment', qaly_glasses_after
    print 'QALY Glasses: increased by', qaly_change_glasses
    ##### QALY for cataracts #####
    # generate before and after population
    cataracts_problem = Problem.from_problem_name('cataracts')
    cataracts_population_before = [person for person in population if 
            person.has_problem(cataracts_problem)]
    cataracts_population_after = [person for person in treated_population if 
            person.has_problem(cataracts_problem)]
    # calculate ave_age, ave_life_expectancy, and average utility
    cataracts_age_before = avg([person.age for person in cataracts_population_before])
    cataracts_age_after = avg([person.age for person in cataracts_population_after])
    cataracts_life_expectancy_before = 64
    cataracts_life_expectancy_after = 78
    cataracts_utility_before = avg([person.health_utility for person in cataracts_population_before])
    cataracts_utility_after = avg([person.health_utility for person in cataracts_population_after])
    cataracts_utility_change = cataracts_utility_after - cataracts_utility_before
    qaly_cataracts_before = cataracts_life_expectancy_before + cataracts_utility_before
    qaly_cataracts_after = cataracts_life_expectancy_after + cataracts_utility_after
    qaly_change_cataracts = qaly_cataracts_after - qaly_cataracts_before
    print 'QALY_Cataracts: before treatment', qaly_cataracts_before
    print 'QALY_Cataracts: after treatment', qaly_cataracts_after
    print 'QALY Cataracts: increased by', qaly_change_cataracts
    print 'Average health_utility increase:', (glasses_utility_change + cataracts_utility_change)/2
     

class Problem(object):
    def __init__(self, problem_name, health_utility, cost_full, cost_subsidized):
        self.name = problem_name
        self.health_utility = health_utility
        self.cost_full = cost_full
        self.cost_subsidized = cost_subsidized

    def equals(self, problem):
        return self.name == problem.name
       
    @classmethod #[health_utility, cost_full, cost_subsidized]
    def from_problem_name(cls, problem_name):
        attributes  = {
                'cataracts': [0.14, 4750, 750], #FROM DATA
                'glasses': [0.07, 120, 120]     #ASSUMPTION
                }[problem_name]
        return cls(problem_name, attributes[0], attributes[1], attributes[2])
    
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

        
