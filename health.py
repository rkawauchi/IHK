"""
REFERENCE

FILTER STEPS
0 = 
1 = Transport arranged for people
2 = Transport arranged for people
3 = Transport arranged for people
4 = Transport arranged for people
5 = Transport arranged for people
"""

import math
import random

"""FILTER"""
#**** STEP 1 = AWARENESS OF ARAVIND SOLUTION ***
#TO PUT IN PEOPLE.PY
"""
def generate_person():
    #To add to person generation, after classification
    if classification = 'Urban':
        city_center_distance = urban_radius*random.random()
    if classification = 'Rural':
        city_center_distance = (random.random()*(max_radius-urban_radius)+urban_radius
    person = io.Person(classification, )
    return person
"""
#General area variables 
TN_area = 130058 #state.area
TN_urban_area = 4703 #state.urban_area
city_CN_urban_area = 1200
city_CN_urban_radius = 19.55

def eval_urban_radius(urban_area):
    #check urban_area is in sq km, return in km
    return (city_CN_urban_radius*urban_area)/city_CN_urban_area #we use Chennai data, with a 1200 sqkm metro area and a city radius of 19.55km

urban_radius = eval_urban_radius(TN_urban_area)
max_radius = sqrt(Tamil_Nadu_area/math.pi) #calculation: total Tamil Nadu area is 

#Init_split
urb_split, rur_split = 91.5%, 39.7%
# Static variables to store: (assumptions based on Aravind results)
# for urban: percentage of people treated who attend hospitals vs clinics in urban areas (2013 result data by default)
# for urban : percentage of people treated who attend clinics vs hospitals in urban areas (2013 results data by default)
# for rural : percentage of people treated who attend vision centers vs camps in rural areas 
# for rural : percentage of people treated who attend camps vs vision centers in rural areas 
#The idea is to cut in four segments of activy the space, so that the more you're remote the smaller structure you get.
#We use reach rate to provide a refinement to model the idea that even in one of the segment, you might not be aware (they cannot cover everything.
hospital_reach_rate = 100%
clinic_reach_rate = 70%
center_reach_rate = 40%
camp_reach_rate = 10%

#Init Health Structure Dictionnary
dict_structure = {"hospital" = 1, "clinic" = 2, "center" = 3, "camp" = 4}
dict_milestones = {dict_structure('hospital') = 0, dict_structure('clinic') = urb_split*urban_radius, dict_structure('center') = urban_radius, dict_structure('camp') = urban_radius+(max_radius-urban_radius)*rur_split}

def test_awareness(person):
    if person.city_center_distance in range(0, urb_split*urban_radius*hospital_reach_rate):
        person.structure = dict_structure["hospital"]
        return True
    if person.city_center_distance in range(urb_split*urban_radius, urban_radius*clinic_reach_rate):
        person.structure = dict_structure["clinic"]
        return True
    if person.city_center_distance in range(urban_radius, urban_radius+(max_radius-urban_radius)*rur_split*center_reach_rate):
        person.structure = dict_structure["center"]
        return True
    if person.city_center_distance in range(urban_radius+(max_radius-urban_radius)*rur_split, max_radius*camp_reach_rate):
        person.structure = dict_structure["camp"]
        return True
    else:
        return False


#*** STEP 2 = WORRYINESS LEVEL ***
def calculate_worry_threshold():
#worry_threshold calculation: Given that an estimated 9% of the population is considered hypocondriac,
#we calculate in the hypothesis of a Gaussian distribution of worry level in the population that these 9%
#match a -inverse_erf(1-9/50) threshold = -0.95. worry_level of each person is simulated given a Normal distribution N(0,1)
    return -0.95

def test_worry_level(person):
        if person.worry_level > calculate_worry_threshold():
            return True
        else:
            return False


#*** STEP 3 = HEALTH NEED ***
def define_treatment_needed(people):
    # health_status is generated (30% of population nee for eye-related treatment: 20% glasses, 10% surgery), 70% don't need treatment
    # 0 : no need for eye treatment, 1: need for glasses, 2: need for surgeries
    if person.eye_health < 0.10: # 10% population need surgeries : TO CHANGE with 10thQUANTILE OF RIE DISTRIBUTION
        return 2 
    elif person.eye_health < 0.30: # 20% population need glasses TO CHANGE with 30thQUANTILE OF RIE DISTRIBUTION
        return 1
    else: 
        return 0 # 70% population don't need eye treatment TO CHANGE with 70thQUANTILE OF RIE DISTRIBUTION

#*** STEP 4 = PRICE CATEGORISATION
quantile70_avg_money_rural = 30 # TO CALCULATE
quantile20_avg_money_urban = 50 # TO CALCULATE

def pricing_category(person): 
    # in "rural": camps are free, vision centers are 20 Rs if lowest_income
    if person.classification == "rural":
        if person.money < quantile70_avg_money_rural: # 70 % free consultations in rural areas --> approximation with quantile
            person.pricing_class = "Free"
        else:
            person.pricing_class = "Paying"
    elif people.classification = "urban":
        if people.money < quantile20_avg_money_urban: # 20% free consultations in urban areas
            person.pricing_class = "Free"
        else: 
            person.pricing_class = "Paying"


#*** STEP 5 = PRICE IS OK FOR THEM
#definition of the acceptability of a consultation WTP
rural_consult_price = 20
urban_consult_price = 20

def transit_cost(distance):
    #http://www.delhitourism.gov.in/delhitourism/transport/autos.jsp
    return distance*

def get_transit_cost(person):
    distance = abs(person.city_center_distance - dict_milestones(person.structure))
    return transit_cost(distance)

def test_price(person): # returns boolean (True if they can afford)
# to define and store as static variables : min_income_rural and min_income_urban
    if person.classification == "Rural": 
        if person.pricing_class == "Free":
            return True
        elif person.pricing_class  == "Paying"
            if person.money < 7*rural_consult_price: # people who are not poor enough to get free consultation and in the same time cannot afford Full price
                return False
            else:
                return True
    elif person.classification == "urban": 
        if person.pricing_class == "Free":
            return True
        elif person.pricing_class == "Paying":
            if people.money < 7*urban_consult_price: # people who are not poor enough to get free consultation and in the same time cannot afford Full price
                return False
            else:
                return True



# Main function filter:
def filter(person):
    eval_urban_radius(TN_urban_area)
    if test_awareness(person):
        if test_worry_level(person):
            if define_treatment_needed(person) == 1 or define_treatment_needed(person) == 2 or define_treatment_needed(person) == 0: #review to see if we really exclude some people
                pricing_category(person)
                if test_price(person):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
        return False

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
# Health improvements for each treatment category (1 and 2 only, nothing for 0)
health_improvement_1 = 0.7 # ASSUMPTION --> TO DEFINE (QALY/10)?
health_improvement_2 = 0.2 # ASSUMPTION --> TO DEFINE

# Static variables stored in a dictionary prices 
# Assumptions for price of glasses, paying surgeries (we took info from Aravind but prices  differ with more granularity in real)
# Also some high-level surgeries are 20000Rs--> make weighted average for paying surgery?
# Also we didn"t have the consultation price for eye_clinic and took the same as vision center
prices = {"consultation": {"vision_center": 20, "eye_clinic": 20, "hospital": 50}, "surgery": {"subsidized": 750, "paying": 4750, "free": 0}, "glasses": 120}

def attach_treatment_district(person):
    # TO DO
    person.area = # call function that look at people district and attach the corresponding hospital district it is rattached to.

def capacity_check (person, patient_treated, patient_treated_max): # check capacity of the structure_type in hospital_district of the patient
    # check if capacity of the structure attanding is full (ex: capacity of all vision centers in a district) --> capacity = capacity/unit * #units in district
    if patient_treated[person.area][person.structure] < patient_treated_max[person.area][person.structure]:
        return True
    else:
        return False

"""functions only if capacity_check True"""
def increment(person, patient_treated):
    patient_treated[person.area][person.structure]+=1 # updates the dictionary



### IMPROVE "person.type_visit, it doesn't exist yet" ### 
def change_consultation(person):
    # Following statements modified people money, health (for glasses only) 
    # and reassign variables correponding to transfer to surgery (tpe_visit, structure hospital and price_cat)
    if define_treatment_needed(person) == 0 and person.pricing_class = "Paying": # (no need and paying)
        person.money-= prices[person.type_visit][person.structure] # people pays for consultation and looses money

    if define_treatment_needed(person) ==1 and person.pricing_class = "Paying": # (need glasses and paying)
        person.money-= prices[person.type_visit][person.structure] # people pays for consultation and looses money
        person.money-=prices[glasses] # people who do not have free consultation buys glasses (assumption)
        person.eye_health+=health_improvement_1 # improvement related to wearing glasses benefit

    if define_treatment_needed(person) ==1 and person.pricing_class = "Free": # (need glasses and free)
        person.eye_health+=health_improvement_1

    # ASSUMPTION: To determine subsidies/free/full price for surgeries:
    # free surgery for people who got free consultation, 
    # full price for those who got paying consultation in urban area, 
    # subsidized for others (paying consultation in rural)
    # We also assume that determined pricing category will satisfy people --> they will accept
    if define_treatment_needed(person) ==2 and person.pricing_class = "Paying": # (need surgery and paying)
        person.money-= prices[person.type_visit][person.structure] # people pays for consultation and looses money
        person.type_visit = "surgery" # will be transfered for surgery --> reassign variable
        person.structure = "hospital" # attach new structure hospital --> reassign variable
        if person.classification =="rural":
            person.pricing_class = "subsidized" # only people paying with RURAL consultation will have subsidized surgery (assumption)
        elif person.classification =='urban':
            person.pricing_class = "paying"   

    if person.treatment ==2 and person.pricing_class = "Free consultation": # (need surgery and paying)
            person.type_visit = "surgery" # will be transfered for surgery --> reassign variable
            person.structure = "hospital" # attach new structure hospital --> reassign variable
            person.pricing_class = "free" 

def change_surgery(person): # called if capacity_check True
    person.money-= prices[person.type_visit][person.pricing_class] # will remove amount related to pricing cat (0, 750 or 4750)
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


#store number of people people rejected by filter/accepted by filter


class Aravind(object):

    def __init__(self, treatment_cost = 100):
        self.hospital_district_names = ['Madurai', 'Theni', 'Tirunelveli', 
                'Coimbatore', 'Pondicherry', 'Dindigul', 'Tiruppur', 'Salem',
                'Tuticorin', 'Udumalaipet']
        self.treatment_cost = treatment_cost
        self._init_hospitals()

    def _init_hospitals(self):
        self.hospitals = list()
        treatable_symptoms = ['eye_health']
        for district_name in self.hospital_district_names:
            self.hospitals.append(Hospital(district_name, 
                    treatable_symptoms, self.treatment_cost))


""" THINK ABOUT HOW TO INITIATE THE HOSPITALS
    def _init_structures(self):
        self.structure = dict('hospital' = 0, 'clinic' = 0, 'center' = 0, 'camp' = 0)
        #create the areas
"""
    def get_covered_district_names(self):
        return self.covered_district_names

    def treat(self, person):
        for hospital in self.hospitals:
            if hospital.covers_district_name(person.district):
                return hospital.treat(person)
        #If patient is not covered, return the untreated patient
        return person

    def get_structure(self):
        return self.hospitals

class Hospital(object):
    #Use this to assign each hospital to cover surrounding districts
    #Based on Aravind's data
    #A more robust approach would be to define adjacencies for all districts
    covered_district_mapping = {
                'Coimbatore': ['Coimbatore', 'Nilgiris', 'Kollam'],
                'Dindigul': ['Dindigul'],
                'Madurai': ['Ariyalur', 'Dharmapuri', 'Karur', 'Madurai', 
                    'Nagapattinam', 'Namakkal', 'Perambalur', 'Pudukkottai',
                    'Ramanathapuram', 'Siviganga', 'Thanjavur', 'Thiruvarur',
                    'Tiruchirappalli', 'Virudhunagar'],
                'Pondicherry': ['Chennai', 'Cuddalore', 'Kanchipuram',
                    'Krishnagiri', 'Thiruvallur', 'Tiruvannamalai',
                    'Vellore', 'Villupuram'],
                'Salem': ['Erode', 'Salem'],
                'Theni': ['Theni', 'Kottayam', 'Iduki'],
                'Tirunelveli': ['Kanniyakumari', 'Thoothukudi', 'Tirunelveli'],
                'Tiruppur': ['Tiruppur'],
                #These are not from the google drive
                'Tuticorin': ['Tuticorin'],
                'Udumalaipet': ['Udumalaipet']}
                

    def __init__(self, district_name, treatable_symptoms, treatment_cost, 
            equipment_level = None):
        self.district_name = district_name
        #treatable_symptoms is a list of symptoms the hospital can treat
        self.treatable_symptoms = treatable_symptoms
        self.equipment_level = equipment_level #cf. equipment_level index
        self.treatment_cost = treatment_cost
        self._init_covered_districts()

    def _init_covered_districts(self):
        #Use Python version of "switch statement"
        self.covered_districts = Hospital.covered_district_mapping[
                self.district_name]
            

    #True if the district is in the list of districts this hospital covers
    def covers_district_name(self, district_name):
        return district_name in self.covered_districts

    def treat(self, person):
        for symptom in self.treatable_symptoms:
            #Any patient treated by this hospital has their symptoms increased
            # to a minimum of 0.5
            #This is obviously a placeholder for a more nuanced approach
            improved_symptom = max(getattr(person, symptom), 0.5)
            #Change the patient's symptom so it is improved by the hospital
            setattr(person, symptom, improved_symptom)
            person.money -= self.treatment_cost
        return person

    def get_transit_cost(person)
        distance = abs(person.city_center_distance - 

    

    def WillingnessScore




"""
class Solution(object):
    def __init__(self, location, expertise, start_date, end_date, is_operating):
        self.location = location
        self.expertise = expertise
        self.start_date = start_date
        self.end_date = end_date
        self.is_operating = is_operating
"""
"""
        self.location = "KA" #modify to match: reach only Karnataka state
        self.treatmentRatePerYear = 2646000 #number of people treated per year by the whole system. Treatment definition = "went into Aravind System and met with one personel"
        self.expertise = "Eyecare" #Aravind System will only treat the patients that have problem related to Eyecare
        self.beginDate = 01-01-1976 #convert in the most common date format. By default if no month/day, first january
        self.endDate = "N/A" #system is still operating
        self.operatingStatus = 'Y'
"""


        """
        self.nbOutpatientsFree
        self.nbOutpatientPaying = nbPopPaying
        self.nbSurgeryFree =
        self.nbSurgerySubsidized =
        self.nbSurgeryPay =
        self.priceSurgeryPay = 
        self.priceSurgerySubsidized = 900 #750*88%+2000*12% (balance between ICCE and ECCE)
        self.priceSurgeryFree = 0
        self.nbPopFree = nbPopFree #check sum free + paid = Screened
        """

"""
#possible merge 
class CommunityEye:
    def __init__()
        self.nbOutpatients
        self.costRegistration = 10

class VisionCenter:
    def __init__()
        self.nbOutpatients
        self.costRegistration = 10

class OutreachCamp:
    def __init__()
        self.nbOutpatients
        self.costRegistration = 0

Surgery (only Hospital)
        - Free 
        - Subsidized
        - Pay

OutPatient
        - Free (Hospital, Camps)
        - Paying (Hospital, VisionCenter(10Rpee), CommunityEyeClinic (10 Rpee)

class Cost:
    def __init__(self, Operation, Salary, Asset)
        self.Operation = 20 #info for cataract operation, in US $, can be converted in Ruppees, we will research it later
        self.Salary = 000
        self.Asset = 99

    class Cost.Operation:
        def __init__(self, diagnosticTest)
            self.costSurgery = '1000'
            self.costDiagnosisTest = '1000' #could be expanded in level1, level2, etc.
            self.cost = 1000 #tofinish

    class Cost.Salary:
        def __init__(self, salaryParamed, salarySurgeon)
            self.salaryParamed = '1000'
            self.salarySurgeon = '1000'

    class Cost.Activity:
        def __init__(costAssetsYearly, costEquipment)
            self.costAssetsYearly = '1000' #find in Aravind financials
            self.costEquipment = '1000'

class HumanResources: #number of personel per structure
    def __init__(self)
        self.Personel = 999
        self.TrainingLevel = 999

    class HumanResources.Personel:
        def __init__(self, numberSurgeonStructure1, numberParamedStructure2):
            numberSurgeonStructure1 = '1000' #Not sure exactly how to cross: structure type (whether Aravind System or Aravind Hospital or Eye camp center etc. with the level of competencies)
            numberParamedStructure2 = '1000'

    class HumanResources.TrainingLevel:
        def __init__(self, programEmployeeFormation, programEmployeeWelfare, programSelfDevelopment, programMotherInclusion)
            self.programEmployeeFormation = 1 #general method: Binary level for presence of the program. 0 if no, 1 if yes. Final score as a float between 0 and 1 as # of Yes / # of total programs
            self.programSelfDevelopment = 1
            self.programEmployeeWelfare = 1
            self.programMotherInclusion = 1

        def levelScore(self):
            return (programMotherInclusion + programEmployeeWelfare + programSelfDevelopment + programEmployeeFormation) /(4)

        print 'initializing Aravind System'
#Parent

    #patient in class Person
    def visit_or_not(self, patient):
        if not patient.money>self.visit_cost:
            print 'patient cannot afford treatment'
            return False
        if patient.diabetes > threshold_diabetes and patient.cardio > threshold_cardio:
            print "patient in good health, no need to consult"
            return False
        return True

    solution_id = 1
    location = #Karnataka
    treatment_rate = 
"""


if __name__ == "__main__":
    #This is very bad right now because the Solution __init__ method isn't
    #fully developed yet. But this is an example of how to work with a class
    aravind = Solution(location = 'Karnataka', expertise = 'eyecare',
            start_date = 'TODO', end_date = None, is_operating = True)
