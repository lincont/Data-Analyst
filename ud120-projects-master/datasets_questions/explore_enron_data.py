#!/usr/bin/python

"""
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000

"""

import pickle
import re
import pprint

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

#need
#for key in enron_data.iterkeys():
#    print key
#    print enron_data[key]
#    print "--------------"

#find out how many people are in enron_data
enron_length = len(enron_data)
print(enron_length)

#find out the max number of features given to each person
for person in enron_data.iterkeys():
    feature_length = len(enron_data[person])
print(feature_length)

#the number of poi's in dataset
poi_count = 0
for person in enron_data.iterkeys():
    if enron_data[person]["poi"] == 1:
        poi_count += 1
print(poi_count)

poi_txt = open('../final_project/poi_names.txt').readlines()
pois = [txt.strip() for txt in poi_txt]
#print(pois)
print len(pois) - 2

print(enron_data["PRENTICE JAMES"]["total_stock_value"])

for person in enron_data:
    if "JAMES" in person:
        print person

for person in enron_data:
    if "WESLEY" in person:
        print person

for person in enron_data:
    if "LAY" in person:
        print person

for person in enron_data:
    if "FASTOW" in person:
        print person

print(enron_data["COLWELL WESLEY"]["from_this_person_to_poi"])

for person in enron_data:
    if "SKILLING" in person:
        print person

pprint.pprint(enron_data["SKILLING JEFFREY K"])

pprint.pprint(enron_data["SKILLING JEFFREY K"]['total_payments'])
pprint.pprint(enron_data["LAY KENNETH L"]['total_payments'])
pprint.pprint(enron_data["FASTOW ANDREW S"]['total_payments'])

valid_email_count = 0
valid_salary_count = 0
invalid_total_payments_count = 0

for person in enron_data:
    if enron_data[person]['email_address'] != 'NaN':
        valid_email_count += 1
    if enron_data[person]['salary'] != 'NaN':
        valid_salary_count += 1
    if enron_data[person]['total_payments'] == 'NaN':
        invalid_total_payments_count += 1
print valid_email_count
print valid_salary_count
print invalid_total_payments_count
print enron_length
damnit = float(invalid_total_payments_count)/enron_length
print "%.2f" % (damnit)
    #if enron_data[person]['']:

    #    print person
