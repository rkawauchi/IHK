import io

class Person():
    def __init__(self, money, diabetes, cardio, location):
        self.money = money
        self.diabetes = diabetes
        self.cardio = cardio
        self.location = location
# connect to extract data

data = io.Database()
#delhi = data.get_state_by_name("Mizoram")
#print delhi
# a = data.get_all_states()
#    print a

def state_name(state_name):
    return data.session.query(io.State).filter(io.State.name == state_name).all()

def rural_pop(state_name, cl):
    return data.session.query(io.District.state, io.District.name, io.District.classification, io.District.population_total).filter(io.District.state == state_name).filter(io.District.classification == cl).all()

print rural_pop("Tamil Nadu", "Rural")

