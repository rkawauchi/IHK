drop table districts;
create table raw_data ("State", "District", "Level", "Name", "TRU", "No of Households", "Total Population Person", "Total Population Male", "Total Population Female", "Population in the age group 0-6 Person", "Population in the age group 0-6 Male", "Population in the age group 0-6 Female", "Scheduled Castes population Person", "Scheduled Castes population Male", "Scheduled Castes populationFemale", "Scheduled Tribes population Person", "Scheduled Tribes population Male", "Scheduled Tribes population Female", "Literates Population Person", "Literates Population Male", "Literates Population Female", "Illiterate Persons", "Illiterate Male", "Illiterate Female", "Total Worker Population Person", "Total Worker Population Male", "Total Worker Population Female", "Main Working Population Person", "Main Working Population Male", "Main Working Population Female", "Main Cultivator Population Person", "Main Cultivator Population Male", "Main Cultivator Population Female", "Main Agricultural Labourers Population Person", "Main Agricultural Labourers Population Male", "Main Agricultural Labourers Population Female", "Main Household Industries Population Person", "Main Household Industries Population Male", "Main Household Industries Population Female", "Main Other Workers Population Person", "Main Other Workers Population Male", "Main Other Workers Population Female", "Marginal Worker Population Person", "Marginal Worker Population Male", "Marginal Worker Population Female", "Marginal Cultivator Population Person", "Marginal Cultivator Population Male", "Marginal Cultivator Population Female", "Marginal Agriculture Labourers Population Person", "Marginal Agriculture Labourers Population Male", "Marginal Agriculture Labourers Population Female", "Marginal Household Industries Population Person", "Marginal Household Industries Population Male", "Marginal Household Industries Population Female", "Marginal Other Workers Population Person", "Marginal Other Workers Population Male", "Marginal Other Workers Population Female", "Marginal Worker Population 3_6 Person", "Marginal Worker Population 3_6 Male", "Marginal Worker Population 3_6 Female", "Marginal Cultivator Population 3_6 Person", "Marginal Cultivator Population 3_6 Male", "Marginal Cultivator Population 3_6 Female", "Marginal Agriculture Labourers Population 3_6 Person", "Marginal Agriculture Labourers Population 3_6 Male", "Marginal Agriculture Labourers Population 3_6 Female", "Marginal Household Industries Population 3_6 Person", "Marginal Household Industries Population 3_6 Male", "Marginal Household Industries Population 3-6 Female", "Marginal Other Workers Population Person 3_6 Person", "Marginal Other Workers Population Person 3_6 Male", "Marginal Other Workers Population Person 3_6 Female", "Marginal Worker Population 0_3 Person", "Marginal Worker Population 0_3 Male", "Marginal Worker Population 0_3_Female", "Marginal Cultivator Population 0_3 Person", "Marginal Cultivator Population 0_3 Male", "Marginal Cultivator Population 0_3_Female", "Marginal Agriculture Labourers Population 0_3 Person", "Marginal Agriculture Labourers Population 0_3 Male", "Marginal Agriculture Labourers Population 0_3 Female", "Marginal Household Industries Population 0_3 Person", "Marginal Household Industries Population 0_3 Male", "Marginal Household Industries Population 0_3 Female", "Marginal Other Workers Population 0_3 Person", "Marginal Other Workers Population 0_3 Male", "Marginal Other Workers Population 0_3 Female", "Non Working Population Person", "Non Working Population Male", "Non Working Population Female");

.mode csv
create table if not exists districts (name TEXT, state TEXT, classification TEXT, household_total INTEGER, population_total INTEGER);
.import "data/Andaman and Nicobar Islands 35.CSV" raw_data
insert or replace into districts select trim(Name), "Andaman and Nicobar Islands", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Andhra Pradesh 28.CSV" raw_data
insert or replace into districts select trim(Name), "Andhra Pradesh", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Arunachal Pradesh 12.CSV" raw_data
insert or replace into districts select trim(Name), "Arunachal Pradesh", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Assam 18.CSV" raw_data
insert or replace into districts select trim(Name), "Assam", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Bihar 10.CSV" raw_data
insert or replace into districts select trim(Name), "Bihar", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Chandigarh (4).CSV" raw_data
insert or replace into districts select trim(Name), "Chandigarh", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Chhattisgarh 22.CSV" raw_data
insert or replace into districts select trim(Name), "Chhattisgarh", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Dadra and Nagar Haveli 26.CSV" raw_data
insert or replace into districts select trim(Name), "Dadra and Nagar Haveli", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Daman and Diu 25.CSV" raw_data
insert or replace into districts select trim(Name), "Daman and Diu", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Goa 30.CSV" raw_data
insert or replace into districts select trim(Name), "Goa", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Gujarat 24.CSV" raw_data
insert or replace into districts select trim(Name), "Gujarat", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Haryana (06).CSV" raw_data
insert or replace into districts select trim(Name), "Haryana", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Himacahl Pradesh (02).CSV" raw_data
insert or replace into districts select trim(Name), "Himacahl Pradesh", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/JAMMU and Kashmir (1).CSV" raw_data
insert or replace into districts select trim(Name), "Jammu and Kashmir", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Jharkhand 20.CSV" raw_data
insert or replace into districts select trim(Name), "Jharkhand", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Karnataka 29.CSV" raw_data
insert or replace into districts select trim(Name), "Karnataka", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Kerala 32.CSV" raw_data
insert or replace into districts select trim(Name), "Kerala", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Lakshadweep 31.CSV" raw_data
insert or replace into districts select trim(Name), "Lakshadweep", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Madhya Pradesh 23.CSV" raw_data
insert or replace into districts select trim(Name), "Madhya Pradesh", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Maharashtra 27.CSV" raw_data
insert or replace into districts select trim(Name), "Maharashtra", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Manipur 14.CSV" raw_data
insert or replace into districts select trim(Name), "Manipur", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Meghalaya 17.CSV" raw_data
insert or replace into districts select trim(Name), "Meghalaya", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Mizoram 15.CSV" raw_data
insert or replace into districts select trim(Name), "Mizoram", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Nagaland 13.CSV" raw_data
insert or replace into districts select trim(Name), "Nagaland", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Nct of Delhi (7).CSV" raw_data
insert or replace into districts select trim(Name), "Delhi", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Odisha 21.CSV" raw_data
insert or replace into districts select trim(Name), "Odisha", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Puducherry 34.CSV" raw_data
insert or replace into districts select trim(Name), "Puducherry", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Punjab (3).CSV" raw_data
insert or replace into districts select trim(Name), "Punjab", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Rajasthan (08).CSV" raw_data
insert or replace into districts select trim(Name), "Rajasthan", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Sikkim 11.CSV" raw_data
insert or replace into districts select trim(Name), "Sikkim", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Tamil Nadu 33.CSV" raw_data
insert or replace into districts select trim(Name), "Tamil Nadu", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Tripura 16.CSV" raw_data
insert or replace into districts select trim(Name), "Tripura", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Uttarakhand (5).CSV" raw_data
insert or replace into districts select trim(Name), "Uttarakhand", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/Utter (09).CSV" raw_data
insert or replace into districts select trim(Name), "Utter", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
.import "data/West Bengal 19.CSV" raw_data
insert or replace into districts select trim(Name), "West Bengal", TRU, "No of households", "Total Population Person" from raw_data where Level='DISTRICT';
drop table raw_data;
