from __future__ import print_function
import os
import re

#http://stackoverflow.com/questions/3964681/find-all-files-in-directory-with-extension-txt-with-python
create_table_file = open('create_raw_data_table.sql', 'r')
output_file = open('import_data.sql', 'w')
print('drop table districts;', file=output_file)
print('drop table states;', file=output_file)
for line in create_table_file:
    print(line, file=output_file)
print('.mode csv', file=output_file)
print('create table if not exists districts (name TEXT, state TEXT, classification TEXT, household_total INTEGER, population_total INTEGER);', file=output_file)
print('create table if not exists states (name TEXT, state TEXT, household_poor INTEGER, household_middle INTEGER, household_rich INTEGER);', file=output_file)

def import_from_file(filename):
    print('.import "data/'+filename+'" raw_data', file=output_file)

#Use standardized names for states
def clean_state(state):
    state = re.sub(r'\([A-Z&]*\)', '', state)
    state = re.sub(r'[()\d]', '', state)
    state = re.sub('Nct of Delhi', 'Delhi', state)
    state = re.sub('JAMMU', 'Jammu', state)
    state = re.sub('Utter', 'Uttar Pradesh', state)
    state = re.sub('&', 'and', state)
    state = state.strip()
    return state

for filename in os.listdir("data/"):
    if filename.endswith('.CSV'):
        import_from_file(filename)
        state_name = re.sub(r'.CSV', '', filename)
        print('insert or replace into districts select trim(Name), "'+clean_state(state_name)+'", TRU, "No of households", "Total Population Person" from raw_data where Level=\'DISTRICT\';', file=output_file)
        print('drop table raw_data;', file=output_file)
    if filename.endswith('household_income.csv'):
        
