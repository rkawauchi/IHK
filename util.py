#http://www.gefeg.com/edifact/d03a/s3/codes/cl1h.htm
#This is a terrible method, but it works for now
state_names = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
state_abbreviations = ['AP', 'AR', 'AS', 'BR', 'CT', 'DL', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OR', 'PB', 'RJ', 'SK', 'TN', 'TR', 'UP', 'UT', 'WB']

#Other utility methods (that aren't input/output) which multiple 
#files might need go here

class FilterPopulation(object):
    
    def __init__(self, cost, diabetes, cardio):
        self.cost = cost
        self.diabetes = diabetes
        self.cardio = cardio

    def filter_all(self, person):
        return self.filter_health(person) and self.filter_money(person)

    def filter_health(self, person):
        return self.filter_diabetes(person) or self.filter_cardio(person)

    def filter_diabetes(self, person):
        return person.diabetes >= self.diabetes

    def filter_cardio(self, person):
        return person.cardio >= self.cardio

    def filter_money(self, person):
        return person.money>=self.cost
