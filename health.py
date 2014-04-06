"""
REFERENCE

Hospital::equipmentLevel information
0 = Transport arranged for people
1 = Transport arranged for people
2 = Transport arranged for people
3 = Transport arranged for people
4 = Transport arranged for people
5 = Transport arranged for people
"""

import math

#worry_threshold calculation: Given that an estimated 9% of the population is considered hypocondriac,
#we calculate in the hypothesis of a Gaussian distribution of worry level in the population that these 9%
#match a -inverse_erf(1-9/50) threshold = -0.95. worry_level of each person is simulated given a Normal distribution N(0,1)
worry_threshold = -0.95



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

#geo_scale calculation:
def generate_person():
    #To add to person generation, after classification
    if classification = 'Urban':
        city_center_distance = urban_radius*random.random()
    if classification = 'Rural':
        city_center_distance = (random.random()*(max_radius-urban_radius)+urban_radius
    
    person = io.Person(classification, )

    return person


class Solution(object):
    def __init__(self, location, expertise, start_date, end_date, is_operating):
        self.location = location
        self.expertise = expertise
        self.start_date = start_date
        self.end_date = end_date
        self.is_operating = is_operating

        """
        self.location = "KA" #modify to match: reach only Karnataka state
        self.treatmentRatePerYear = 2646000 #number of people treated per year by the whole system. Treatment definition = "went into Aravind System and met with one personel"
        self.expertise = "Eyecare" #Aravind System will only treat the patients that have problem related to Eyecare
        self.beginDate = 01-01-1976 #convert in the most common date format. By default if no month/day, first january
        self.endDate = "N/A" #system is still operating
        self.operatingStatus = 'Y'
        """

class Aravind(object):

    def __init__(self, treatment_cost = 100):
        self.district_names = ['Madurai', 'Theni', 'Tirunelveli', 
                'Coimbatore', 'Pondicherry', 'Dindigul', 'Tiripur', 'Salem',
                'Tuticorin', 'Udumalaipet']
        self.treatment_cost = treatment_cost
        self._init_hospitals()

    def _init_hospitals(self):
        self.hospitals = dict()
        treatable_symptoms = ['diabetes']
        for district_name in self.district_names:
            self.hospitals[district_name] = Hospital(district_name, 
                    treatable_symptoms, self.treatment_cost)

    def get_district_names(self):
        return self.district_names

    def get_hospitals(self):
        return self.hospitals

class Hospital(object):

    def __init__(self, location, treatable_symptoms, treatment_cost, 
            equipment_level = None):
        self.location = location
        #treatable_symptoms is a list of symptoms the hospital can treat
        self.treatable_symptoms = treatable_symptoms
        self.equipment_level = equipment_level #cf. equipment_level index
        self.treatment_cost = treatment_cost

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

    def testAwareness(self, person):
        if city_center_distance in range(0, urb_split*urban_radius):

        if city_center_distance in range(urb_split*urban_radius, urban_radius):
        if city_center_distance in range(urban_radius, urban_radius*rur_split):
        if city_center_distance in range(urban_radius*rur_split, max_radius):



    def testWorryLevel(self, person):
        if person.worry_level > worry_threshold:
            return 1
        else:
            return 0






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

'''
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

"""
Surgery (only Hospital)
        - Free 
        - Subsidized
        - Pay

OutPatient
        - Free (Hospital, Camps)
        - Paying (Hospital, VisionCenter(10Rpee), CommunityEyeClinic (10 Rpee)
"""

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

class HumanResources: """#number of personel per structure
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
class 

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

class 
"""
'''

if __name__ == "__main__":
    #This is very bad right now because the Solution __init__ method isn't
    #fully developed yet. But this is an example of how to work with a class
    aravind = Solution(location = 'Karnataka', expertise = 'eyecare',
            start_date = 'TODO', end_date = None, is_operating = True)
