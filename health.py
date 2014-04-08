class Aravind(object):
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

    def __init__(self):
        self.district_names = ['Madurai', 'Theni', 'Tirunelveli', 
                'Coimbatore', 'Pondicherry', 'Dindigul', 'Tiruppur', 'Salem',
                'Tuticorin', 'Udumalaipet']
        self.treatment_costs = {
                'hospital': 500,
                'clinic': 200,
                'vision_center': 100,
                'camp': 20}
        self._init_facilities()

    def _init_facilities(self):
        self.hospitals = list()
        self.clinics = list()
        self.vision_centers = list()
        self.camps = list()
        self._init_hospitals()
        self._init_clinics()
        self._init_vision_centers()
        self._init_camps()

    def _init_hospitals(self):
        treatment_cost = self.treatment_costs['hospital']
        treatable_symptoms = ['eye_health']
        for district_name in self.district_names:
            self.hospitals.append(Hospital(district_name, 
                treatment_cost, treatable_symptoms))

    def _init_clinics(self):
        treatment_cost = self.treatment_costs['clinic']
        treatable_symptoms = ['eye_health']
        for district_name in self.district_names:
            self.clinics.append(Clinic(district_name,
                treatment_cost, treatable_symptoms))

    def _init_vision_centers(self):
        treatment_cost = self.treatment_costs['vision_center']
        treatable_symptoms = ['eye_health']
        for district_name in self.district_names:
            self.vision_centers.append(VisionCenter(district_name,
                treatment_cost, treatable_symptoms))

    def _init_camps(self):
        treatment_cost = self.treatment_costs['camp']
        treatable_symptoms = ['eye_health']
        for district_name in self.district_names:
            self.vision_centers.append(Camp(district_name,
                treatment_cost, treatable_symptoms))

    def treat(self, person):
        for hospital in self.hospitals:
            if hospital.covers_district_name(person.district):
                hospital.treat(person)
        #If patient is not covered, the patient is unchanged
        return person

#Generic class which includes Hospital, EyeClinic, and VisionCamp
class AravindFacility(object):
    def __init__(self, district_name, treatment_cost, treatable_symptoms):
        self.district_name = district_name
        self.treatment_cost = treatment_cost
        self.treatable_symptoms = treatable_symptoms
        self._init_covered_districts()

    def _init_covered_districts(self):
        #Use Python version of "switch statement"
        self.covered_districts = Aravind.covered_district_mapping[
                self.district_name]

    #True if the district is in the list of districts this hospital covers
    def covers_district_name(self, district_name):
        return district_name in self.covered_districts

    def treat(self, person):
        for symptom in self.treatable_symptoms:
            self.treat_symptom(symptom, person)
        self.charge_fee(person)

    #symptom is a string containing the name of the
    # attribute: "eye_health", for example
    def treat_symptom(self, symptom, person):
        #This is overwritten by each of the subclasses
        pass 

    #Also overwritten by subclasses
    def charge_fee(self, person):
        pass

class Hospital(AravindFacility):

    def treat_symptom(self, symptom, person):
        if symptom=='eye_health':
            #Any patient treated by this hospital has their symptoms increased
            # to a minimum of 0.5
            #This is obviously a placeholder for a more nuanced approach
            improved_symptom = max(getattr(person, symptom), 0.5)
            #Change the patient's symptom so it is improved by the hospital
            setattr(person, symptom, improved_symptom)

    def charge_fee(self, person):
        person.money -= self.treatment_cost

class Clinic(AravindFacility):
    
    def treat_symptom(self, symptom, person):
        if symptom=='eye_health':
            #Any patient treated by this clinic has eye health improved to 0.4
            improved_symptom = max(getattr(person, symptom), 0.4)
            #Change the patient's symptom so it is improved by the clinic
            setattr(person, symptom, improved_symptom)
            person.money -= self.treatment_cost

    def charge_fee(self, person):
        person.money -= self.treatment_cost

class VisionCenter(AravindFacility):
    def treat_symptom(self, symptom, person):
        if symptom=='eye_health':
            #Any patient treated by this clinic has eye health improved to 0.3
            improved_symptom = max(getattr(person, symptom), 0.3)
            #Change the patient's symptom so it is improved by the vision center
            setattr(person, symptom, improved_symptom)
            person.money -= self.treatment_cost

    def charge_fee(self, person):
        person.money -= self.treatment_cost

class Camp(AravindFacility):
    def treat_symptom(self, symptom, person):
        if symptom=='eye_health':
            #Any patient treated by this clinic has eye health improved to 0.2
            improved_symptom = max(getattr(person, symptom), 0.2)
            #Change the patient's symptom so it is improved by the camp
            setattr(person, symptom, improved_symptom)
            person.money -= self.treatment_cost

    def charge_fee(self, person):
        person.money -= self.treatment_cost

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
