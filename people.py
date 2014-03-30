import io
from sqlalchemy import func
import numpy as np
from array import *
from math import log10, log
import random

#generate a dict of values corresponding to the attributes of a Person
def generate_person_dict(data, state, district, mpce):
    person = generate_person(data, state, district, mpce)
    return person.to_dict()

def generate_person(data, state, district, mpce):
    #This is where math and statistics comes in
    money = generate_expense_log(mpce, district.classification)
    #Just a number in a uniform distribution from 0-1
    #Obviously needs to be changed later
    diabetes = random.random()
    cardio = random.random()
    classification = district.classification
    person = io.Person(money, diabetes, cardio, district.name, state.name,
            classification)
    return person

#Note that this is merely a demonstration of how to randomly generate money
# for a Person. This will be rewritten later!
def randomize_money(mpce):
    #generate random value between 0 and double the MPCE average
    #The mean is therefore the MPCE average
    return random.random()*mpce.mpce_average*2

######################## below by RieK #########################

def pop_by_state(state_name, class_type):
    return data.session.query(io.District.state, io.District.name, io.District.classification, func.sum(io.District.population_total)).filter(io.District.state == state_name).filter(io.District.classification == class_type).group_by(io.District.state).all()

def exp_by_state(state_name, class_type):
    return data.session.query(io.Mpce.state, io.Mpce.mpce_type, io.Mpce.classification, io.Mpce.mpce_average).filter(io.Mpce.state == state_name).filter(io.Mpce.mpce_type == "mmrp").filter(io.Mpce.classification == class_type).all()

def exp_percentile(mpce, class_type):
    return mpce.get_d_all(add_zero = False)

def generate_expense(mpce, class_type):
    # mean = exp_by_state(mpce, class_type)[0][3]
    # For testing, only generating 100,000th of population
    pop = 0.1 * (pop_by_state(mpce, "rural")[0][3])/100000
    listPercentile = exp_percentile(mpce, class_type)
    expenseList=[]
    for i in xrange(len(listPercentile)-1):
        genUniform = np.random.uniform(listPercentile[i], listPercentile[i+1], pop)
        expenseList.append(genUniform)
    return expenseList

def generate_expense_log(mpce, class_type):
    # For testing, only generating 100,000th of population
    #pop = (pop_by_state(mpce, "rural")[0][3])/100000
    listPercentile = exp_percentile(mpce, class_type)
    logPercentile = []
    # http://stackoverflow.com/questions/4561113/python-list-conversion
    logPercentile[:] = [log(x) for x in listPercentile]
    return np.random.lognormal(mean=np.mean(logPercentile), sigma=np.std(logPercentile))   

def test(state_name):
    return data.session.query(io.Person).filter(io.Person.state == state_name).all()

if __name__ == '__main__':
    data = io.Database()
    test_state_name = "Tamil Nadu"
    mpce = data.get_mpce_by_state_name(test_state_name)
    print 'pop_by_state', pop_by_state(mpce, "rural")[0][3]
    print 'exp_by_state', exp_by_state(mpce, "rural")[0][3]
    print 'exp_percentile', exp_percentile(mpce, "rural")
    #print 'expense', generate_expense_log(mpce, "rural")
