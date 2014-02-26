class Kiosk():
    def __init__(self, visit_cost, location):
        self.visit_cost = visit_cost
        self.location = location
        print 'initializing Kiosk'

    #patient shold be Person
    def visit(self, patient):
        if not patient.location == self.location:
            print 'patient not in correct location'
            return False
        if not patient.money>self.visit_cost:
            print 'patient cannot afford treatment'

    #patient should be Person
    def visit(self, patient):
        patient.money -= visit_cost
        #improve patient.diabetes
        #improve patient.cardio
        return True

    #Patient should be from class Person
    def filter(self, patient):
        if not patient.location == self.location:
            print "patient not at proper location"
            return False
        if not patient.money>self.visit_cost:
            print "patient cannot afford treatment"
            return False
        visit(self,patient)
