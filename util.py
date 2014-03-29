#http://www.gefeg.com/edifact/d03a/s3/codes/cl1h.htm
#This is a terrible method, but it works for now
state_names = ['Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
state_abbreviations = ['AP', 'AR', 'AS', 'BR', 'CT', 'DL', 'GA', 'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML', 'MZ', 'NL', 'OR', 'PB', 'RJ', 'SK', 'TN', 'TR', 'UP', 'UT', 'WB']

#Other utility methods (that aren't input/output) which multiple 
#files might need go here

#thresholds is a dict containing relevant thresholds
def filter_by_all(population, thresholds = None):
    if thresholds is None:
        thresholds = default_thresholds()
    filtered_population = list()
    for person in population:
        if health_filter(person, thresholds):
            filtered_population.append(person)
    return filtered_population

def default_thresholds():
    return {'diabetes': 0.1,
            'cardio': 0.1}

def diabetes_filter(person, thresholds):
    return person.diabetes >= thresholds['diabetes']
    
def cardio_filter(person, thresholds):
    return person.cardio >= thresholds['cardio']

def health_filter(person, thresholds):
    return diabetes_filter(person, thresholds) or cardio_filter(person, thresholds)
