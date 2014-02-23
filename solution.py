
worryLevel = 0.8

def symptomToDiagnosis(input):
    if input in ('hasHeadache', 'isTired'):
        return ('glcmeter','premeter')
    # implement link to backend
    #return list(
    #   SELECT *
    #   FROM symptoms S
    #   INNER JOIN diagnosis D ON S.symptomID = D.symptomID
    #   WHERE S.symptomName = "input")

class Person():
    def __init__(self, money, symptoms, location, selfAwareness):
        self.money = money
        self.symptoms = symptoms
        self.disease = disease
        self.location = location
        self.selfAwareness = selfAwareness

class Kiosk():
    def __init__(self, visit_cost, location):
        self.visit_cost = visit_cost
        self.location = location
        self.expertise = expertise #each kiosk has ability to cure some diseases
        self.diagnosis = diagnosis #each kiosk has ability to measure some symptoms
        print 'initializing Kiosk'

    #patient should be Person
    def visit(self, patient):
        if not patient.disease in self.expertise:
            print "patient cannot be cured by the kiosk"
            return False
        patient.money -= visit_cost
        #improve patient.diabetes
        #improve patient.cardio
        return True

        #Patient should be from class Person
    def filter(self, patient):
        if patient.selfAwareness < worryLevel:
            print "patient don't think cure is needed"
        if not patient.location == self.location:
            print "patient not at proper location"
            return False
        if not symptomToDiagnosis(patient.symptoms) in self.diagnosis: #filter under-equipped kiosks or structure. step possibly 
            print "kiosk doesn't have proper equipment"
            #patient should visit hospital
        if not patient.money>self.visit_cost:
            print "patient cannot afford treatment"
            return False
        else:
            visit(self,patient)

