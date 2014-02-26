# Simulation of India

from people import Person
#import pandas
from random import normalvariate


# Supposing we have 
# Simulate the population of the entire area around the kiosk, with their specific characteristics

# Parameters: money, location


# array = DataFrame.from_csv(‘data.csv’, header=0, sep=', ', index_col=0, parse_dates=True, encoding=None, tupleize_cols=False, infer_datetime_format=False)

# class Person():
#     def __init__(self, money, diabetes, cardio, location):
#         self.money = money
#         self.diabetes = diabetes
#         self.cardio = cardio
#         self.location = location

class Person2():
    def __init__(self, money, location):
        self.money = money
        self.location = location


# Ideally mean and std for each parameter is picked in a dataframe containing on raw for each Indian area. The function should take 
# a dataframe as input (to update later)
def people_generation(area, population_size, income_mean, income_std, distance_mean_to_kiosk, distance_std_kiosk):
	sample = []
	for i in range(population_size):
		income_generator = normalvariate(income_mean, income_std)
		distance_generator = normalvariate(distance_mean_to_kiosk, distance_std_kiosk)

		newperson = Person2(income_generator, distance_generator)
		sample.append(newperson)
	return sample

print people_generation (1, 3, 4, 1, 300, 20, 38, 2)


