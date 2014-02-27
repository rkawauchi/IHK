class Kiosk():
    def __init__(self, location, visit_cost, diabetes_threshold,
            cardio_threshold):
        self.location = location
        self.visit_cost = visit_cost
        self.diabetes_threshold = diabetes_threshold
        self.cardio_threshold = cardio_threshold
        #Initial cost to create kiosk: $5000. We are measuring in rupees
        self.money = -309900
        print 'initializing Kiosk'

    #patient shold be Person
    def visit(self, patient):
        if not patient.location == self.location:
            print 'patient not in correct location'
            return False
        if not patient.money>self.visit_cost:
            print 'patient cannot afford treatment'
        patient.money -= visit_cost
        kiosk.money += visit_cost
        
        #If we diagnose diabetes
        if patient.diabetes<diabetes_threshold:
            #For now, we ignore the details and just improve the patient's
            #health.
            patient.diabetes = diabetes_threshold

        #If we diagnose cardiovascular problems
        if patient.cardio<cardio_threshold:
            #For now, we ignore the details and just improve the patient's
            #health.
            patient.cardio = cardio_threshold

        #The visit was successful
        return True
