import re
import random
import bisect

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

class FilterPopulation(object):
    
    def __init__(self, cost, eye_health, cardio):
        self.cost = cost
        self.eye_health = eye_health
        self.cardio = cardio

    def filter_all(self, person):
        return self.filter_health(person) and self.filter_money(person)

    def filter_health(self, person):
        return self.filter_eye_health(person) or self.filter_cardio(person)

    def filter_eye_health(self, person):
        return person.eye_health <= self.eye_health

    def filter_cardio(self, person):
        return person.cardio <= self.cardio

    def filter_money(self, person):
        return person.money>=self.cost

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
