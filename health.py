import random
import util

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
        self.district_names = Aravind.covered_district_mapping.keys()
        self.treatment_costs = {
                'hospital': 500,
                'clinic': 200,
                'vision_center': 100,
                'camp': 20}
        #FROM DATA
        self.urban_hospital_probability = 0.915
        self.urban_clinic_probability = 1 - self.urban_hospital_probability
        self.rural_vision_center_probability = 0.397
        self.rural_camp_probability = 1 - self.rural_vision_center_probability
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
        treatable_problems = ['cataracts', 'glasses']
        capacity = 1000000
        #FROM DATA
        visit_fee = 50
        for district_name in self.district_names:
            self.hospitals.append(Hospital(district_name, treatable_problems,
                capacity, visit_fee))

    def _init_clinics(self):
        treatable_problems = ['glasses']
        capacity = 1000000
        #FROM DATA
        visit_fee = 20
        for district_name in self.district_names:
            self.clinics.append(Clinic(district_name, treatable_problems,
                capacity, visit_fee))

    def _init_vision_centers(self):
        treatable_problems = ['glasses']
        capacity = 1000000
        #FROM DATA
        visit_fee = 20
        for district_name in self.district_names:
            self.vision_centers.append(VisionCenter(district_name,
                treatable_problems, capacity, visit_fee))

    def _init_camps(self):
        treatable_problems = ['glasses']
        capacity = 1000000
        #FROM DATA
        visit_fee = 0
        for district_name in self.district_names:
            self.camps.append(Camp(district_name, treatable_problems,
                capacity, visit_fee))

    #True if treatment was done, False otherwise
    def treat(self, person):
        #Assign the person to a type of facility randomly
        rnd = random.random()
        if person.classification == 'urban':
            if rnd <= self.urban_hospital_probability:
                treatment_facility = 'hospitals'
            else:
                treatment_facility = 'clinics'
        elif person.classification == 'rural':
            if rnd <= self.rural_vision_center_probability:
                treatment_facility = 'vision_centers'
            else:
                treatment_facility = 'camps'
        return self.treat_with_facility(treatment_facility, person)

    #True if treatment was done, False otherwise
    def treat_with_facility(self, treatment_facility, person):
        #Now that we know the type of facility
        #Find a facility that can cover the patient and have it treat them
        facility_list = getattr(self, treatment_facility)
        for facility in facility_list:
            if facility.can_see(person):
                return facility.treat(person)
        return False

#Generic class which includes Hospital, EyeClinic, and VisionCamp
class AravindFacility(object):

    #Paying, subsidized, free
    #FROM DATA
    surgery_fee_proportions_by_state = {
            'Madurai': [69298, 41637, 25647],
            'Thenia': [6507, 3292, 3360],
            'Tirunelveli': [26956, 12227, 13470],
            'Coimbatore': [41418, 25566, 19071],
            'Pundicherry': [25478, 12974, 16943],
            'Tirupur': [1934, 381, 87],
            'Dingipul': [2952, 0, 0],
            'Salem': [7763, 8, 1423]}
    #Turn those numbers into actual proportions
    for state_name, proportions in surgery_fee_proportions_by_state.items():
        total = float(sum(proportions))
        surgery_fee_proportions_by_state[state_name] = [x/total for x in proportions]

    def __init__(self, district_name, treatable_problems,
            capacity, visit_fee):
        self.district_name = district_name
        self.treatable_problems = treatable_problems
        self.capacity = capacity
        self.visit_fee = visit_fee
        self.treated_patient_count = 0
        self._init_covered_districts()

    def _init_covered_districts(self):
        #Use Python version of "switch statement"
        self.covered_districts = Aravind.covered_district_mapping[
                self.district_name]

    #True if the district is in the list of districts this hospital covers
    def can_see(self, person):
        #First, check whether this facility is already at capacity
        if self.treated_patient_count > self.capacity:
            return False
        #Next, check whether the person is in the right district 
        if not person.district in self.covered_districts:
            return False
        return True

    def treat(self, person):
        self.charge_visit_fee(person)
        for problem in person.get_health_problem_list():
            treatment_performed = self.treat_problem(problem, person)
            if treatment_performed:
                self.charge_problem_fee(problem, person)
        self.treated_patient_count += 1
        return True

    #problem is a util.Problem
    def treat_problem(self, problem, person):
        person.health_utility += problem.health_utility
        return True

    def charge_visit_fee(self, person):
        person.money -= self.visit_fee

    def charge_problem_fee(self, problem, person):
        if problem.name == 'cataracts':
            fee_options = [problem.cost_full, problem.cost_subsidized, 0]
            fee = util.weighted_choice(fee_options, 
                    Hospital.surgery_fee_proportions_by_state[self.state_name])
        elif problem.name == 'glasses':
            #FROM DATA
            fee = 120
        else:
            print 'Warning: unrecognized problem', problem.name
        person.money -= fee

class Hospital(AravindFacility):
    def __init__(self, district_name, treatable_problems,
            capacity, visit_fee):
        super(Hospital, self).__init__(district_name, treatable_problems,
                capacity, visit_fee)
    pass

class Clinic(AravindFacility):
    pass

class VisionCenter(AravindFacility):
    pass

class Camp(AravindFacility):

    #Camps are free
    def charge_problem_fee(self, problem, person):
        pass

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
