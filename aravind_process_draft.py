import random


"""FILTER"""

def define_treatment_needed(people):
	# health_status is generated (30% of population nee for eye-related treatment: 20% glasses, 10% surgery), 70% don't need treatment
	# 0 : no need for eye treatment, 1: need for glasses, 2: need for surgeries
	if people.eye_health < 0.10: # 10% population need surgeries : TO CHANGE with 10thQUANTILE OF RIE DISTRIBUTION
		treatment_needed == 2 
	elif people.eye_health < 0.30: # 20% population need glasses TO CHANGE with 30thQUANTILE OF RIE DISTRIBUTION
		treatment_needed == 1
	else: 
		treatment_needed == 0 # 70% population don't need eye treatment TO CHANGE with 70thQUANTILE OF RIE DISTRIBUTION
	return treatment_needed # (0, 1 or 2)

# function geo location Duch to integrate 

def bool_want_consult(people, treatment): # returns boolean to consult according to eye_health and worry_level
	# mutliply worry level by eye.health? # complete DUCH with geolocation
	var = treatment
	if var == 0 # no need treatment
		if people.worry_level > 0.9: # need to feel very worry about your health to consult without need
			return True
		else: 
			return False
	if var == 1: # need glasses
		if people.worry_level > 0.6: # people with need and medium worry will consult
			return True
		else: 
			return False
	if var == 2: # need surgery
		if people.worry_level > 0.2: # only people with very low worried won't consult
			return True
		else:
			return False


quantile70_avg_income_rural = 30 # TO CALCULATE
quantile20_avg_incom_urban = 50 # TO CALCULATE

def pricing_category(people): 
	# in "rural": camps are free, vision centers are 20 Rs if lowest_income
	if people.area == "rural":
		if people.income < quantile70_avg_incom_rural: # 70 % free consultations in rural areas --> approximation with quantile
			return "Free consultation"
		else:
			return "Paying consultation"
	elif people.area = "urban":
		if people.income < quantile20_avg_incom_urban: # 20% free consultations in urban areas
			return "Free consultation"
		else: 
			return "Paying consultation"

pricing_cat = pricing_category(people)

rural_consult_price = 20
min_income_rural = 7* rural_consult_price # to define more accurately
urban_consult_price = 20
min_income_urban = 7* urban_consult_price # to define more accurately

def check_price(people, pricing_cat): # returns boolean (True if they can afford)
# to define and store as static variables : min_income_rural and min_income_urban
	if people.area == "rural": 
		if pricing_cat == "Free consultation":
			return True
		elif pricing_cat == "Paying consultation"
			if people.income < min_income_rural: # people who are not poor enough to get free consultation and in the same time cannot afford Full price
				return False
			else:
				return True
	elif people.area == "urban": 
		if pricing_cat == "Free consultation":
			return True
		elif pricing_cat == "Paying consultation":
			if people.income < min_income_urban: # people who are not poor enough to get free consultation and in the same time cannot afford Full price
				return False
			else:
				return True

# Main function filter:
def filter(people):
	treatment = define_treatment_needed(people)
	pricing_cat = pricing_category(people)
	if bool_want_consult(people, treatment) and check_price(people, pricing_cat):
		return True
	else:
		return False

# store number of people people rejected by filter/accepted by filter







""" MATCH WITH STRUCTURE (if bool_want_consult and check_price --> filter True)"""
# Initialize number patient treated ["treatment_district"]['structure_type'] to 0. Will be incremented by 1 each time a patient is treated.
# And will be used to check capacity before treating a patient.
#dict = {"Madurai": {'vision center': , 'hospital': , "eye clinic": , "camp": }...}


# Static variables to store:
rate_hospital = 0.91 # for urban: percentage of people treated who attend hospitals vs clinics in urban areas (2013 result data by default)
rate_community_clinic = 0.09 # for urban : percentage of people treated who attend clinics vs hospitals in urban areas (2013 results data by default)
rate_vision_center = 0.40 # for rural : percentage of people treated who attend vision centers vs camps in rural areas 
rate_camp = 0.60 # for rural : percentage of people treated who attend camps vs vision centers in rural areas 
# number of structures of the four types in each hospital_district (ex: 4 vision centers in Madurai)

def attach_structure(people): """ attach a structure type to people (among 4 types) according to their area (rural/urban) and effective proportion
of people treated in each type of structure (Aravind results by default)"""
	rand = random.uniform (0,1) # random number uniformely between 0 and 1 to 
	if people.area == "rural":
		if rand < rate_vision_center:
			return "vision_center" # knowing the district of people, we know what structure he matches
		else:
			return "camp"
	elif people_area == "urban":
		if rand < rate_hospital:
			return "hospital"
		else:
			return "community_clinic"

def attach_treatment_district(people):
	treatment_district = # look at people district and attach the corresponding hospital district the district is rattached to.
	return treatment_district


def capacity_check (people, treatment_district, structure):
	# check if capacity of the structure attanding is full (ex: capacity of all vision centers in a district) --> capacity = capacity/unit * #units in district
	if total_patient[district][structure] < number_entities[district][structure]

	# returns boolean


"""if capacity_check True"""

def transfer_to_surgery(people):
	if people.area = "rural" and treatment == 2:
		people.cause = "Surgery"
		return True





"""PEOPLE CHANGE"""
# Static variables to store:
price_consult_rural = 20
price_consult_hospital = 50
price_glasses = 120 # =2-4 Rs --> make a weighted average to consider people who get free glasses (no info on the number...)?
price_surgery_subsidized = 750
price_surgery = 4750 # make weighted average with high-level operations at 20000 Rs ?



def people_change(people):
type_visit = "consultation" # define how to integrate it. Always a consultation at first (by default)that can convert in "surgery" if necessary.
treatment_district = attach_treatment_district(people)
structure = attach_structure(people)
pricing_cat = pricing_category(people) # already called in filter --> find a way not to call it again

# change money (price determined by pricing_category(people) and structure attended): ex vision center + "Paying consultation" --> 20 Rs (=price_consut_rural)
	# and also if treatment_need == 1 (need glasses), remove price_glasses
# health status (improved only if glasses during consultation, othewise  will increase after with surgery). If no treatment, no change.
	if transfer_to_surgery(people): # second step of change after consultation
		# attach structure hospital of the district
		# check capacity of hospital
		# determine subsidies/free/full price (free for people who got free consultation, full price for those who got paying consultation at hospital, subsidized for others)
				#--> we assume that determined pricing category will satisfy people --> they will accept
		# increase number patients treated in hospital in the year (we assume a patient, if comes, only comes once a year)
		# decrease money (with structure)
		#and improve health of patient






