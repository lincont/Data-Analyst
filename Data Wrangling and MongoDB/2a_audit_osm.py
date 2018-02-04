#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Audit the OSM file for data issues
Because the OSM file can be large, redirect the output to a file.
    python audit_osm.py > see_it.txt
'''

# import libraries
import xml.etree.ElementTree as ET
from collections import defaultdict
import pprint
import re

# audited file
SAMPLE_FILE = 'NW_Austin.osm'

# regex to bucket different types of keys
# for future handling
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\\?%#$@\,\. \t\r\n]')

# regex to get the last word in a string
# intention is to find values like St., St, Road, Rd
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# the expected list of street types.  This list is manually built as the osm
# file is audited.  The bad ones will be added to the street mapping dictionary
# in the clean up stage.  Added here as they are discovered so we don't continue
# to re-audit them.
expected = [# good ones
            'Street', 'Avenue', 'Boulevard', 'Drive', 'Court', 'Place', 'Square', 'Lane', 'Road',
            'Trail', 'Parkway', 'Commons', 'Circle', 'Loop', 'Cove', 'Park', 'Bend', 'Highway',
            'Pass', 'Point', 'Yard', 'Path', 'Way', 'North', 'East', 'West', 'South', 'View',
            'Hollow', 'Mountain', 'Hill', 'Valley', 'View', 'Oaks', 'Expressway', 'Crossing',
            'Ridge', 'Run', 'Expressway', 'Ramp'

            #bad ones added to mapping
            'St', 'St.',
            'avenue', 'Ave.', 'Ave',
            'Blvd.', 'Blvd',
            'Dr.', 'Dr',
            'W.', 'N.',
            'Rd.', 'Rd',
            'Ln', 'Trl', 'Cir',
            'Cv', 'Ct']


def audit_street_type(street_types, street_name):
    '''
    find the last word in a string, if it is not within the array
    expected than keep track of it in a list

    taken from MondgoDB quiz Improving Street Names, audit.py
    '''
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def street_types(osmfile):
    '''
    audit the streets and names, look at the last word and keep a
    dictionary of the last word and string they appear in.  use this audit as
    a way to build the street mapping dictionary in the clean up phase.

    note:  name was included here, because roads and highways are named here.
    in this case, places like stores would also be audited in the same way.

    take from MondgoDB quiz Improving Street Names, audit.py, and modified
    '''
    osm_file = open(osmfile, 'r')
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=('start',)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if tag.attrib['k'] == 'addr:street' or tag.attrib['k'] == 'name':
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def key_type(element, keys):
    '''
    keep a running count of keys that match the regex expression
    see how many keys belong to each type

    taken from MondgoDB quiz Tag Types, tags.py
    '''
    if element.tag == 'tag':
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    return keys

def show_key_types(filename):
    '''
    take a closer look at each key/regex match
    see if there are any with problem characters, colons, or cases that
    have not been coded for

    taken from the mongoDB quiz Tag Types, tags.py
    '''
    keys = {'lower': 0, 'lower_colon': 0, 'problemchars': 0, 'other': 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

def count_tags(filename):
    '''
    count the number of tags in the sample file
    to get familiar with the contents
    '''
    dict_map = {}
    for event, element in ET.iterparse(filename):
        if element.tag in dict_map.keys():
            dict_map[element.tag] += 1
        else:
            dict_map[element.tag] = 1

    return dict_map


def see_tags(filename):
    '''
    see a list of all the attribute names used in a node or way element
    '''
    attribute_names=set()
    for event, element in ET.iterparse(filename):
        if element.tag == 'node' or element.tag == 'way':
            for tag in element.iter('tag'):
                attribute_names.add(tag.attrib['k'])

    return attribute_names

def see_problem_tags(filename):
    '''
    see a list of all the attribute names used in a node or way element
    '''
    # create a list of inner attribute tag names
    attribute_names=set()

    for event, element in ET.iterparse(filename):
        if element.tag == 'node' or element.tag == 'way':
            for tag in element.iter('tag'):
                if problemchars.search(tag.attrib['k']):
                    attribute_names.add(tag.attrib['k'])

    return attribute_names

def see_values(filename, key_value=None):
    '''
    see a list of all the values associated with a specific attribute
    '''
    attribute_values = defaultdict(set)

    for event, element in ET.iterparse(filename):
        if element.tag == 'node' or element.tag == 'way':
            for tag in element.iter('tag'):
                # if no key was specified add all values
                if key_value == None:
                    attribute_values[tag.attrib['k']].add(tag.attrib['v'])
                # if a key value was specified, than only add those key values
                else:
                    if tag.attrib['k'] == key_value:
                        attribute_values[tag.attrib['k']].add(tag.attrib['v'])

    return attribute_values


if __name__ == '__main__':
    print('Start of count_tags')
    pprint.pprint(count_tags(SAMPLE_FILE))
    print('End of count_tags')
    print('\n')

    print('Start of see_tags')
    pprint.pprint(see_tags(SAMPLE_FILE))
    print('End of see_tags')
    print('\n')

    print('Start of key_types')
    pprint.pprint(show_key_types(SAMPLE_FILE))
    print('End of key_types')
    print('\n')

    print('Start of see_problem_tags')
    pprint.pprint(see_problem_tags(SAMPLE_FILE))
    print('End of see_problem_tags')
    print('\n')

    print('issue with addresses')
    pprint.pprint(street_types(SAMPLE_FILE))
    print('end of addresses')
    print('\n')

    print('Start of see_values')
    pprint.pprint(see_values(SAMPLE_FILE))
    print('End of see_values')
    print('\n')
