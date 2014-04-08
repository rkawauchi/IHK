import random

'''I PUT IN COMMENTS THE FILTER PART AS THIBAULT ALREADY UPDATED IT'''

# """FILTER"""

# def define_treatment_needed(people):
# 	# health_status is generated (30% of population nee for eye-related treatment: 20% glasses, 10% surgery), 70% don't need treatment
# 	# 0 : no need for eye treatment, 1: need for glasses, 2: need for surgeries
# 	if people.eye_health < 0.10: # 10% population need surgeries : TO CHANGE with 10thQUANTILE OF RIE DISTRIBUTION
# 		treatment_needed = 2 
# 	elif people.eye_health < 0.30: # 20% population need glasses TO CHANGE with 30thQUANTILE OF RIE DISTRIBUTION
# 		treatment_needed = 1
# 	else: 
# 		treatment_needed = 0 # 70% population don't need eye treatment TO CHANGE with 70thQUANTILE OF RIE DISTRIBUTION
# 	return treatment_needed # (0, 1 or 2)

# # function geo location Duch to integrate 

# def bool_want_consult(people, treatment): # returns boolean to consult according to eye_health and worry_level
# 	# mutliply worry level by eye.health? # complete DUCH with geolocation
# 	var = treatment
# 	if var == 0 # no need treatment
# 		if people.worry_level > 0.9: # need to feel very worry about your health to consult without need
# 			return True
# 		else: 
# 			return False
# 	if var == 1: # need glasses
# 		if people.worry_level > 0.6: # people with need and medium worry will consult
# 			return True
# 		else: 
# 			return False
# 	if var == 2: # need surgery
# 		if people.worry_level > 0.2: # only people with very low worried won't consult
# 			return True
# 		else:
# 			return False


# quantile70_avg_income_rural = 30 # TO CALCULATE
# quantile20_avg_incom_urban = 50 # TO CALCULATE

# def pricing_category(people): 
# 	# in "rural": camps are free, vision centers are 20 Rs if lowest_income
# 	if people.area == "rural":
# 		if people.income < quantile70_avg_incom_rural: # 70 % free consultations in rural areas --> approximation with quantile
# 			return "Free consultation"
# 		else:
# 			return "Paying consultation"
# 	elif people.area = "urban":
# 		if people.income < quantile20_avg_incom_urban: # 20% free consultations in urban areas
# 			return "Free consultation"
# 		else: 
# 			return "Paying consultation"

# pricing_cat = pricing_category(people)

# rural_consult_price = 20
# min_income_rural = 7* rural_consult_price # to define more accurately
# urban_consult_price = 20
# min_income_urban = 7* urban_consult_price # to define more accurately

# def check_price(people, pricing_cat): # returns boolean (True if they can afford)
# # to define and store as static variables : min_income_rural and min_income_urban
# 	if people.area == "rural": 
# 		if pricing_cat == "Free consultation":
# 			return True
# 		elif pricing_cat == "Paying consultation"
# 			if people.income < min_income_rural: # people who are not poor enough to get free consultation and in the same time cannot afford Full price
# 				return False
# 			else:
# 				return True
# 	elif people.area == "urban": 
# 		if pricing_cat == "Free consultation":
# 			return True
# 		elif pricing_cat == "Paying consultation":
# 			if people.income < min_income_urban: # people who are not poor enough to get free consultation and in the same time cannot afford Full price
# 				return False
# 			else:
# 				return True

# # Main function filter:
# def filter(people):
# 	treatment = define_treatment_needed(people)
# 	pricing_cat = pricing_category(people)
# 	if bool_want_consult(people, treatment) and check_price(people, pricing_cat):
# 		return True
# 	else:
# 		return False







""" MATCH + CHANGE_PEOPLE --> ONLY ACTIVATED IF FILTER TRUE"""

'''VARIABLES AND INITIALIZATION to put outside of functions '''
# TO DO: Initialize a dictionary patient_treated ["treatment_district"]['structure_type'] to 0. Will be incremented by 1 each time a patient is treated.
# And will be used to check capacity before treating a patient.
patient_treated = {"Madurai": {'vision_center': , 'hospital': , "eye_clinic": , "camp": }...} # TO DO
# 
# TO DO: Initialize a static dictionary patient_treated_max with max capacities per structure_type per district 
# --> equal to (number entities in district for a specific structure type * max capacity per entity): data available in database_solutions in Google doc 
patient_treated_max = {"Madurai": {'vision_center_max': , 'hospital_max': , "eye_clinic_max": , "camp_max": }...}} #TO DO
# 
# Static variables to store: (assumptions based on Aravind results)
rate_hospital = 0.91 # for urban: percentage of people treated who attend hospitals vs clinics in urban areas (2013 result data by default)
rate_community_clinic = 0.09 # for urban : percentage of people treated who attend clinics vs hospitals in urban areas (2013 results data by default)
rate_vision_center = 0.40 # for rural : percentage of people treated who attend vision centers vs camps in rural areas 
rate_camp = 0.60 # for rural : percentage of people treated who attend camps vs vision centers in rural areas 
# number of structures of the four types in each hospital_district (ex: 4 vision centers in Madurai)

# Health improvements for each treatment category (1 and 2 only, nothing for 0)
# Treatment categories: 0 is none, 1 is glasses, 2 is surgery
health_improvement_1 = 0.7 # ASSUMPTION --> TO DEFINE (QALY/10)?
health_improvement_2 = 0.2 # ASSUMPTION --> TO DEFINE

# Static variables stored in a dictionary prices 
# Assumptions for price of glasses, paying surgeries (we took info from Aravind but prices  differ with more granularity in real)
# Also some high-level surgeries are 20000Rs--> make weighted average for paying surgery?
# Also we didn"t have the consultation price for eye_clinic and took the same as vision center
prices = {"consultation": {"vision_center": 20, "eye_clinic": 20, "hospital": 50}, "surgery": {"subsidized": 750, "paying": 4750, "free": 0}, "glasses": 120}



def attach_structure(person): 
# attach a structure type to people (among 4 types) according to their area (rural/urban) and effective proportion
# of people treated in each type of structure (Aravind results by default)
	rand = random.uniform (0,1) # random number uniformely between 0 and 1 to dispatch people in accurate proportions (according to Aravind proportion results)
	if people.area == "rural":
		if rand < rate_vision_center:
			person.structure = "vision_center" # knowing the district of people, we know what structure he matches
		else:
			return "camp"
	elif people_area == "urban":
		if rand < rate_hospital:
			person.structure = "hospital"
		else:
			person.structure = "community_clinic"


def attach_treatment_district(person):
	# TO DO
	person.treatment_district = # call function that look at people district and attach the corresponding hospital district it is rattached to.


def capacity_check (person, patient_treated, patient_treated_max): # check capacity of the structure_type in hospital_district of the patient
	# check if capacity of the structure attanding is full (ex: capacity of all vision centers in a district) --> capacity = capacity/unit * #units in district
	if patient_treated[person.treatment_district][person.structure] < patient_treated_max[person.treatment_district][person.structure]:
		return True
	else:
	 	return False



"""functions only if capacity_check True"""

def increment(person, patient_treated):
	patient_treated[person.treatment_district][person.structure]+=1 # updates the dictionary


def change_consultation(person):

	# Following statements modified people money, health (for glasses only) 
	# and reassign variables correponding to transfer to surgery (tpe_visit, structure hospital and price_cat)
	if person.treatment ==0 and person.pricing_cat = "Paying consultation": # (no need and paying)
		person.money-= prices[person.type_visit][person.structure] # people pays for consultation and looses money

	if person.treatment ==1 and person.pricing_cat = "Paying consultation": # (need glasses and paying)
		person.money-= prices[person.type_visit][person.structure] # people pays for consultation and looses money
		person.money-=prices[glasses] # people who do not have free consultation buys glasses (assumption)
		person.eye_health+=health_improvement_1 # improvement related to wearing glasses benefit

	if person.treatment ==1 and person.pricing_cat = "Free consultation": # (need glasses and free)
		person.eye_health+=health_improvement_1

	# ASSUMPTION: To determine subsidies/free/full price for surgeries:
	# free surgery for people who got free consultation, 
	# full price for those who got paying consultation in urban area, 
	# subsidized for others (paying consultation in rural)
	# We also assume that determined pricing category will satisfy people --> they will accept
	if person.treatment ==2 and person.pricing_cat = "Paying consultation": # (need surgery and paying)
		person.money-= prices[person.type_visit][person.structure] # people pays for consultation and looses money
		person.type_visit = "surgery" # will be transfered for surgery --> reassign variable
		person.structure = "hospital" # attach new structure hospital --> reassign variable
		if person..area =="rural":
			person.pricing_cat = "subsidized" # only people paying with RURAL consultation will have subsidized surgery (assumption)
		elif person..area =='urban':
			person.pricing_cat = "paying"	

	if person.treatment ==2 and person.pricing_cat = "Free consultation": # (need surgery and paying)
			person.type_visit = "surgery" # will be transfered for surgery --> reassign variable
			person.structure = "hospital" # attach new structure hospital --> reassign variable
			person.pricing_cat = "free" 


def change_surgery(person): # called if capacity_check True
	person.money-= prices[person.type_visit][person.pricing_cat] # will remove amount related to pricing cat (0, 750 or 4750)
	person.eye_health+=health_improvement_2 # improvement related to surgery benefits



"""PEOPLE CHANGE"""


'''Main function in health.py'''

def people_change(person): # called only if filter True
	#person.type_visit = "consultation" # ALREADY DONE IN FILTER? always consultation at first (by default)that can convert in "surgery" if necessary.
	#define_treatment_needed(person) --> ALREADY DONE IN FILTER?
	#pricing_category(people) # ALREADY DONE IN FILTER?
	attach_treatment_district(person)
	attach_structure(person)
	
	if capacity_check(person, patient_treated, patient_treated_max):
		if person.type_visit == "consultation":
			increment(person, patient_treated) # updates dictionary of people treated/consulted
			change_consultation(person)
	
	if person.type_visit == "surgery": # will be activated only if change_consultation changed type_visit to surgery (ie people.eye_health ==2)
		if capacity_check(person, patient_treated, patient_treated_max): # check capacity of hospital (because structure associated with type_visit =surgery is necessarily hospital)
			increment(person, patient_treated) # updates dictionary of people treated/consulted
			change_surgery(person)








