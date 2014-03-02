import people.py
import assign_visit

def person_change (person, consultation_type, price, health_benefit): # to call if visit_or_not for the patient returns True and after
# determining which kiosk he attends (function assign_visit)
# takes an object in class Person as input
# consultation_type = 'type1' or 'type2' --> depends of the nature of consultation (treatment, diagnosis...) can be extended
	person.money-=price[consultation_type] # we assume the person have enough money if bool_visit ==True (checked in a previous function)
	person.diabetes+=health_benefit[consultation_type]['diabete']
	person.cardio+=health_benefit[consultation_type]['cardio']


Emilie = Person(300, 23, 15, 'Bengal')


# Hopefully the following input parameters values already match the location specificities (picked up from the database)
# For example in Bengal (and considering other parameters to define):
price = {'type1':20, 'type2':5 }
health_benefit = {'type1':{"diabete": 10, "cardio": 0}, 'type2':{"diabete": 10, "cardio": 0} } # dictionary with classes equal to different 

person.change(Emilie, 'type1', health_benefit) 






