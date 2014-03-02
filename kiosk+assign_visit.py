class Kiosk():
    def __init__(self, visit_cost, location):
        self.visit_cost = visit_cost
        self.location = location
        print 'initializing Kiosk'

    #patient in class Person
    def visit_or_not(self, patient):
        if not patient.money>self.visit_cost:
            print 'patient cannot afford treatment'
            return False
        if patient.diabetes > threshold_diabetes and patient.cardio > threshold_cardio:
            print "patient in good health, no need to consult"
            return False
        return True





def assign_visit(people, kiosks): # list of patients from class Person and list of kiosks in class Kiosk
# (already selected in the district?)
    visits = {}
    for j in kiosks:
        visits[j] = []# initialize dict with "kiosk":[list of patients who will visit]
    for i in people:
        # We assume patient's choice is only motivated by the location
        kiosk_selected = min_distance_to_kiosk(i) # takes kiosks as input and returns [min_distance, kiosk_selected] TO DEFINE
        if visit_or_not(kiosk_selected, i) == True:
            visits[kiosk_selected[1].append(i)
            # ? person_change(i, consultation_type, kiosk_selected.visit_cost, health_benefit)
    return visits #return the dict with kiosks as keys and list of patients as values
