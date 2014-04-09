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
    i = bisect.bisect(cumulative_weights, rnd)
    return choices[i]

#Perform analytics on the treated population
def analyze_populations(population, treated_population):
    print 'Average health utility in original population', avg(
            [person.health_utility for person in population])
    print 'Average health utility in treated population', avg(
            [person.health_utility for person in treated_population])

class Problem(object):
    def __init__(self, problem_name, health_utility, cost_full, cost_subsidized):
        self.name = problem_name
        self.health_utility = health_utility
        self.cost_full = cost_full
        self.cost_subsidized = cost_subsidized
       
    @classmethod
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

        
