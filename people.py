import io_data
from sqlalchemy import func
import scipy.stats as stats
import numpy as np
from array import *
from math import log10, log
import random
import util

#generate a dict of values corresponding to the attributes of a Person
def generate_person_dict(state, state_total, district, mpce, mpce_total):
    person = generate_person(state, state_total, district, mpce, mpce_total)
    return person.to_dict()

def generate_person(state, state_total, district, mpce, mpce_total):
    #This is where math and statistics comes in
    gender = generate_gender()
    age = generate_age(district.classification)
    money = generate_money(age, state, state_total, mpce, mpce_total)
    #Just a number in a uniform distribution from 0-1
    #Obviously needs to be changed later
    health_utility = generate_health_utility(age)
    health_problems = generate_health_problems()
    perceived_health = generate_perceived_health(state)
    classification = district.classification
    """
    if classification = 'Urban':
        city_center_distance = urban_radius*random.random()
    if classification = 'Rural':
        city_center_distance = (random.random()*(max_radius-urban_radius)+urban_radius
    """
    person = io_data.Person(money, gender, age, health_utility, health_problems,
            perceived_health, district.name, state.name, classification)
    #Other variables to potentially add: worry_level, pricing_class, structure, city_center_distance
    return person

    #We need to find a way to store those variables to person
    #pricing_class = None
    #structure = None
    #type_visit = None
    #area = None #area following Aravind's cut where the person is attached to

######################## below by RieK #########################

def exp_percentile(mpce):
    #return mpce.get_d_all(add_zero = False)
    return mpce.get_d_all(add_zero = False)

def generate_expense_log(mpce):
    listPercentile = exp_percentile(mpce)
    logPercentile = []
    # http://stackoverflow.com/questions/4561113/python-list-conversion
    logPercentile[:] = [log(x) for x in listPercentile]
    return np.random.lognormal(mean=np.mean(logPercentile), sigma=np.std(logPercentile))

def generate_income(state, state_total, mpce, mpce_total):
    # get meanMPCE and % of classMPCE in meanMPCE
    classPercent = float(mpce.mpce_average) / mpce_total.mpce_average
    # multiply GSP (in Rs.10M) by % to get modified GSP for given class
    meanGSP = state_total.gsp * 10000000
    classGSP = int(classPercent * meanGSP)
    classPop = state.population_total
    # get mean
    meanIncome_person = classGSP / classPop / 10000
    # get sd (I manually calculated from raw data, and made adj,
    # calculation refer to R3.r file: "2. Distribution of Income")
    poorMean = 17097.05 - 2000
    richMean = 171282.9 - 7000
    if classGSP < (60000 * 10000000):
        sdIncome_person = poorMean * 10000000 / state.population_total / 10000
    else:
        sdIncome_person = richMean * 10000000 / state.population_total / 10000
    return np.random.lognormal(log(meanIncome_person),log(sdIncome_person)) * 10000 / 12

def generate_money(age, state, state_total, mpce, mpce_total):
    income = generate_income(state, state_total, mpce, mpce_total)
    expense = generate_expense_log(mpce)
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
    MaleLifeExp = {"0":63.8, "5":62.7, "10":58.1, "15":53.4, "20":52.9, "25":44.2, "30":39.7, "35":35.3, "40":31.1, "45":26.9, "50":23, "55":19.3, "60":15.7, "65":12.7, "70":10.2, "75":8.3, "80":6.7,"85":5.2, "90":3.9, "95":2.8, "100":2.0}
    FemaleLifeExp = {"0":67.3, "5":66.8, "10":62.2, "15":57.5, "20":52.9, "25":48.4, "30":43.8, "35":39.2, "40":34.7, "45":30.2, "50":25.8, "55":25.8, "60":17.7, "65":14.3, "70":11.3, "75":9.0, "80":7.0,"85":5.3, "90":3.9, "95":2.8, "100":2.0}
    if gender == 'F':
        return FemaleLifeExp(age)
    else:
        return MaleLifeExp(age)

#Needs to change to average of 0.85
def generate_health_utility(age):
    # assumption that people over 50 years old would have lower health condition
    lower = 0
    upper = 1
    sigma = 0.35
    if age >= 50:
        mu = 0.6
    else: 
        mu = 0.8
    health_utility = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    return health_utility.rvs()

#Return a comma-separated list of health problems
#This is HORRIBLE database practice. Don't do this. But we have a deadline, yo
def generate_health_problems():
    problems = list()
    #FROM DATA 
    cataract_probability = 0.1
    if random.random() <= cataract_probability:
        problems.append('cataract')
    #FROM DATA
    glasses_probability = 0.3
    if random.random() <= glasses_probability:
        problems.append('glasses')
    return ','.join(problems)
    
def generate_perceived_health(state):
    # Human Development Index: HDI
    # Gender Inequality Index: GII
    # http://wcd.nic.in/publication/GDIGEReport/Part2.pdf
    # Per analysis in R3.r, there is a strong correlation between gender
    # development and health level
    lower = 0
    upper = 1
    sigma = 1
    topList = ('Kerala', 'Goa', 'Manipur')
    lowList = ('Haryana','Jammu and Kashmir','Gujarat','Jharkhand','Andhra Pradesh',	'Meghalaya','Bihar','Rajasthan','Chhattisgarh','Assam','Uttar Pradesh','Odisha','Madhya Pradesh')
    if state.name in topList:
        mu = 0.800
    elif state.name in lowList:
        mu = 0.543
    else:
        mu = 0.62
    health = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    return health.rvs()

if __name__ == '__main__':
    print generate_health()
    print generate_expense_log(mpce)

