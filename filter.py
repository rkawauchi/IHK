

"""Kiosk Function Design
Goal: Apply to a subset of population 


Inputs: 
Outputs:

Filter Function
Steps:
	1. Filters = filter by location, filter by income, filter by reason #order it by computationally ascendent
	3. Kiosk limitations (not awareness)
	4. Call the visit function for those visited

Filter by location:
#1 version: patient.region == kiosk.region



"""

"""Filter"""
        if not patient.location == self.location:
            print 'patient not valid attendee'
            return False
        if not patient.money>self.visit_cost:
            print 'patient cannot afford treatment'
            return False