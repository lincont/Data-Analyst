#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Clean the OSM file and create a json document to be inserted
into MongoDB.
'''

# import libraries
import xml.etree.ElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json
import phonenumbers

# audited file
#SAMPLE_FILE = 'NW_Austin_Sample.osm'
#SAMPLE_FILE = 'small.osm'
SAMPLE_FILE = 'NW_Austin.osm'

#regex to see if a colon exists
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')

# array of keys for the created dictionary
CREATED = [
    'version', 'changeset', 'timestamp', 'user', 'uid'
]

# array of keys that are prefixed, so they can be handled differently
PREFIX_ARRAY = [
    'addr', 'coa', 'gnis', 'name', 'tiger', 'turn'
]

IGNORE = []#'coa', 'name']

# array of the keys to include in the road dictionary
ROADWAY = [
    'foot', 'bicycle', 'cycleway', 'sidewalk',
    'lanes', 'lanes:backward', 'lanes:forward',
    'turn:lanes', 'turn:lanes:forward', 'turn:lanes:backward',
    'turn:lanes:both_ways', 'lanes:both_ways',
    'highway', 'maxspeed', 'oneway', 'surface', 'toll', 'access'
]

# the mapping used to clean up street values
# all defined as upper case, the audit keys will also be uppercase
street_mapping = {
    'ST' : 'Street',
    'ST.' : 'Street',
    'AVE.' : 'Avenue',
    'AVE' : 'Avenue',
    'AVENUE' : 'Avenue',
    'BLVD.' : 'Boulevard',
    'BLVD' : 'Boulevard',
    'DR.' : 'Drive',
    'DR' : 'Drive',
    'W.' : 'West',
    'N.' : 'North',
    'RD' : 'Road',
    'RD.' : 'Road',
    'LN' : 'Lane',
    'TRL' : 'Trail',
    'CIR' : 'Circle',
    'CV' : 'Cove',
    'CT' : 'Court',
    'HWY' : 'Highway'
}

# the mapping used to clean up state values
# all defined as upper case, the audit keys will also be uppercase
state_mapping = {
    'TEXAS' : 'TX',
    'TX' : 'TX',
    'TEX' : 'TX'
}

# create a mapping to clean up the lane keys
lane_mapping = {
    'lanes' : 'total',
    'lanes:backward' : 'backward',
    'lanes:forward' : 'forward',
    'turn:lanes' : 'total_turn',
    'turn:lanes:forward' : 'forward_turn',
    'turn:lanes:backward' : 'backward_turn',
    'turn:lanes:both_ways' : 'both_ways_turn',
    'lanes:both_ways' : 'both_ways'
}

def split_keys (key):
    '''
    split a string by colon
    '''
    return key.split(':')

def split_key_length(key):
    '''
    find the length of a string that was split
    '''
    return len(split_keys(key))

def prefix_part(key):
    '''
    split the array and check if the first split
    is in PREFIX_ARRAY.  This means we will want to
    shape it differently:  redefine values, keys, or make a sub-document.
    '''
    prefix = split_keys(key)[0]
    if prefix in PREFIX_ARRAY:
        return prefix
    else:
        return None

#def new_key (key):
#    if split_key_length(key) <= 2:
#        return split_keys(key)[1]

def update_value_with_mapping(value, mapping):
    '''
    search for each string part in the mapping dictionary
    to perform clean up of certain words (streets, states)
    '''
    dictionary = {}
    dictionary = value.split(' ')
    for part in dictionary:
        # check the string part in uppercase
        if part.upper() in mapping:
            dictionary[dictionary.index(part)] = mapping[part.upper()]
    # put all the parts back together for a complete string
    value = ' '.join(dictionary)
    return value

def update_key_with_mapping(key, mapping):
    '''
    return a new key based on a mapping dictionary
    '''
    if key in mapping:
        return mapping[key]

def shape_address(key, value):
    '''
    fix address by updating the state and street name
    '''
    if key == 'state':
        return update_value_with_mapping(value, state_mapping)
    elif key == 'street':
        return update_value_with_mapping(value, street_mapping)
    else:
        return value

def shape_roadway(key, value):
    road={}
    lanes={}
    mode=[]

    if key == 'maxspeed':
        if 'mph' not in value:
            value = value + ' mph'
        road[key] = value
    elif key in lane_mapping:
        key = update_key_with_mapping(key, lane_mapping)
        lanes[key] = value
    elif key in ('foot', 'sidewalk'):
        mode.append('sidewalk')
    elif key in ('cycleway', 'bicycle'):
        mode.append('cycleway')
    else:
        road[key] = value

    if lanes:
        road['lanes'] = lanes

    if mode:
        road['mode'] = mode

    return road

def shape_element(element):
    node = {}
    address = {}
    created = {}
    road = {}
    pos = []
    node_refs = []
    gnis={}
    tiger={}

    if element.tag == 'node' or element.tag == 'way' :
        node['type'] = element.tag
        for key in element.attrib:
            if key in CREATED:
                created[key] = element.attrib[key]
            elif key == 'id':
                node['id'] = element.attrib[key]
            elif key == 'visible':
                node['visible'] = element.attrib[key]
            elif key == 'lat':
                pos.append(element.attrib[key])
            elif key =='lon':
                pos.append(element.attrib[key])
            else:
                node[key] = element.attrib[key]

            # loop through the children of the element
            for child in element:
                # if the child element is a tag
                if child.tag == 'tag':
                    # create some short-hand variables since these will be used often
                    # replace the underscores with spaces in the value to make it for readability
                    child_key = child.attrib['k']
                    child_value = re.sub(r'_+', ' ', child.attrib['v'])

                    # contains a colon, need to handle cases based on the prefix
                    # and use a new key value
                    if lower_colon.search(child_key):
                        prefix = prefix_part(child_key)
                        if prefix not in IGNORE or child_key not in IGNORE:
                            if prefix == 'addr':
                                # per instructions, if the original key has more than
                                # two colon parts, ignore it.
                                if split_key_length(child_key) <= 2:
                                    new_key = split_keys(child_key)[1]
                                    address[new_key] = shape_address(new_key, child_value)
                            elif prefix == 'tiger':
                                new_key = split_keys(child_key)[1]
                                tiger[new_key] = child_value
                            elif prefix == 'gnis':
                                new_key = split_keys(child_key)[1]
                                gnis[new_key] = child_value
                    # doesn't contain a colon, use the regular child_key
                    else:
                        if child_key == 'name':
                            node['name'] = update_value_with_mapping(child_value, street_mapping)
                        elif child_key == 'phone':
                            node['phone'] = phonenumbers.format_number(phonenumbers.parse(child_value, 'US'), \
                                phonenumbers.PhoneNumberFormat.NATIONAL)
                        elif child_key in ROADWAY:
                            road = shape_roadway(child_key, child_value)
                        else:
                            node[child_key] = child_value
                # if child element is a nd
                elif child.tag == 'nd':
                    if child.get('ref'):
                        node_refs.append(child.attrib['ref'])
                # else we missed something, print it out so we can add it
                else:
                    print child.tag

    # all elements have been parsed
    # check to see if the following have been populated
    # if yes, add it to node
    if created:
        node['created'] = created
    if pos:
        node['pos'] = pos
    if address:
        node['address'] = address
    if node_refs:
        node['node_ref'] = node_refs
    if road:
        node['road'] = road
    if tiger:
        node['tiger'] = tiger
    if gnis:
        node['gnis'] = gnis

    # if node exists, return it
    if node:
        return node
    else:
        return None

def process_map(filename, pretty = False):
    '''
    Takes the xml file and reshapes the data into json format
    with the help of helper funciton shape_element to clean the data.
    Taken from quiz Preparting for Database - MongoDB, data.py
    '''
    # You do not need to change this file
    file_out = '{0}.json'.format(filename)
    data = []
    with codecs.open(file_out, 'w') as fo:
        for _, element in ET.iterparse(filename):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+'\n')
                else:
                    fo.write(json.dumps(el) + '\n')
    return data

if __name__ == '__main__':
    process_map(SAMPLE_FILE, True)
