import io
from sqlalchemy import func
import numpy as np
from array import *
from math import log10, log
import random
import util

#generate a dict of values corresponding to the attributes of a Person
def generate_person_dict(data, state, district, mpce):
    person = generate_person(data, state, district, mpce)
    return person.to_dict()

def generate_person(data, state, district, mpce):
    #This is where math and statistics comes in
    gender = generate_gender()
    age = generate_age(district.classification)
    money = generate_money(data, age, state, mpce)
    #Just a number in a uniform distribution from 0-1
    #Obviously needs to be changed later
    eye_health = random.random()
    cardio = random.random()
    classification = district.classification
    """
    worry_level = generate_worry_level() ### to create
    pricing_class = None
    structure = None
    type_visit = None
    area = None #area following Aravind's cut where the person is attached to
    if classification = 'Urban':
        city_center_distance = urban_radius*random.random()
    if classification = 'Rural':
        city_center_distance = (random.random()*(max_radius-urban_radius)+urban_radius
    """
    person = io.Person(money, gender, age, eye_health, cardio, district.name,
            state.name, classification, """worry_level, pricing_class, structure, city_center_distance""")
    return person


#Note that this is merely a demonstration of how to randomly generate money
# for a Person. This will be rewritten later!
def randomize_money(mpce):
    #generate random value between 0 and double the MPCE average
    #The mean is therefore the MPCE average
    return random.random()*mpce.mpce_average*2

######################## below by RieK #########################

def exp_percentile(mpce):
    #return mpce.get_d_all(add_zero = False)
    return mpce.get_d_all(add_zero = False)

def generate_expense(state, mpce):
    # Currently not in use
    # For testing, only generating 100,000th of population
    pop = 0.1 * (state.population_total)/100000
    listPercentile = exp_percentile(mpce)
    expenseList=[]
    for i in xrange(len(listPercentile)-1):
        genUniform = np.random.uniform(listPercentile[i], listPercentile[i+1],
                pop)
        expenseList.append(genUniform)
    return expenseList

def generate_expense_log(state, mpce):
    listPercentile = exp_percentile(mpce)
    logPercentile = []
    # http://stackoverflow.com/questions/4561113/python-list-conversion
    logPercentile[:] = [log(x) for x in listPercentile]
    return np.random.lognormal(mean=np.mean(logPercentile), sigma=np.std(logPercentile))

def generate_income(data, state_name, class_type):
    # get meanMPCE and % of classMPCE in meanMPCE
    ruralMPCE = data.meanMpce_by_state_name(state_name, "rural")
    urbanMPCE = data.meanMpce_by_state_name(state_name, "urban")
    meanMPCE = (ruralMPCE + urbanMPCE)/2
    classMPCE = data.meanMpce_by_state_name(state_name, class_type)
    classPercent = float(classMPCE) / meanMPCE
    # multiply GSP (in Rs.10M) by % to get modified GSP for given class
    meanGSP = data.get_gsp_by_state_name(state_name, "total").gsp * 10000000
    classGSP = int(classPercent * meanGSP)
    classPop = data.pop_by_state_name(state_name, class_type)
    # get mean
    meanIncome_person = classGSP / classPop / 10000
    # get sd (I manually calculated from raw data, and made adj,
    # calculation refer to R3.r file: "2. Distribution of Income")
    poorMean = 17097.05 - 2000
    richMean = 171282.9 - 7000
    if classGSP < (60000 * 10000000):
        sdIncome_person = poorMean * 10000000 / data.pop_by_state_name(state_name, "total")/ 10000
    else:
        sdIncome_person = richMean * 10000000 / data.pop_by_state_name(state_name, "total")/ 10000
    return np.random.lognormal(log(meanIncome_person),log(sdIncome_person)) * 10000 / 12

def generate_money(data, age, state, mpce):
    state_name = state.name
    income = generate_income(data, state_name, state.classification)
    expense = generate_expense_log(state, mpce)
    if age <= 20:
        return (income / 5) - (expense / 2)
    money = income - expense
    return money

def generate_gender():
    # mean prob of M = 0.5117376, F = 0.4882624
    # (I manually calculated from raw data,
    # calculation refer to R3.r file: "3. Distribution of Age")
    if random.random() >= 0.4882624:
        return "M"
    else:
        return "F"

age_ranges = [[0,9], [10,19], [20,39], [40,59], [60,79], [80,102]]
age_weights = {'urban': [x/100 for x in [16.4, 18.3, 35.9, 21.5, 7.3, 0.7]],
        'rural': [x/100 for x in [19.1, 20.7, 33.1, 18.8, 7.6, 0.8]]}
def generate_age(classification):
    # age distribution at last tab "17.Population by Age-Group"
    # http://rural.nic.in/sites/downloads/IRDR/1.%20Demographic%20Profile.xls
    # does this need to go to database? or shall we use the average
    # but this needs to have the total number: pop ***!!!
    # my current idea idea is to simulate age dist and bootstrap
    age_range = util.weighted_choice(age_ranges, age_weights[classification])
    return random.randint(age_range[0], age_range[1])

def generate_life_exp(gender, age):
    # life-expectancy data from 
    # http://www.worldlifeexpectancy.com/country-health-profile/india
    # we could make database or make dicitonary
    MaleLifeExp = {"0":63.8, "5":62.7, "10":58.1, "15":53.4, "20":52.9, "25":44.2, "30":39.7, "35":35.3, "40":31.1, "45":26.9, "50":23, "55":19.3, "60":15.7, "65":12.7, "70":10.2, "75":8.3, "80":6.7,"85":5.2, "90":3.9, "95":2.8, "100":2.0}
    FemaleLifeExp = {"0":67.3, "5":66.8, "10":62.2, "15":57.5, "20":52.9, "25":48.4, "30":43.8, "35":39.2, "40":34.7, "45":30.2, "50":25.8, "55":25.8, "60":17.7, "65":14.3, "70":11.3, "75":9.0, "80":7.0,"85":5.3, "90":3.9, "95":2.8, "100":2.0}
    if gender == 'F':
        return FemaleLifeExp(age)
    else:
        return MaleLifeExp(age)

def generate_eye_health(age):
    return random.random()

def generate_2ndHealth(state_name, class_type, gender, age):
    return random.random()

if __name__ == '__main__':
    data = io.Database()
    test_state_name = "Tamil Nadu"
    test_classif = "urban"
    state_name = data.get_mpce_by_state_name(test_state_name, test_classif).state
    print state_name, test_classif
    print 'pop_by_state_name', data.pop_by_state_name(state_name, test_classif)
    print 'meanMpce_by_state_name', data.meanMpce_by_state_name(state_name, test_classif)
    print 'exp_percentile', exp_percentile(state_name, test_classif)
    print 'Income: urban', generate_income(state_name, test_classif)
    print 'Income: rural', generate_income(state_name, test_classif)
    print 'Gender:', generate_gender()
    print 'Age:', generate_age(test_classif)
