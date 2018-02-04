#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Create a sample OSM file from a starter file.
Use every k element that belongs to a node, way, or relation.
Change the k value to get other elements to audit and clean.
'''

# import libraries
import xml.etree.ElementTree as ET
import re

# orignal, larger file used
OSM_FILE = 'NW_Austin.osm'

# smaller file, with every k tag-lines created
SAMPLE_FILE = 'NW_Austin_Sample.osm'

# parameter:  take every k-th top level element
k = 215

def get_element (osm_file, tags = ('node', 'way', 'relation')):
    '''
    Iterate through the xml element tree using iterpase.
    Yield element if it is the right type of tags

    REFERENCE:     http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    '''
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

if __name__ == '__main__':
    with open(SAMPLE_FILE, 'wb') as output:
        # write the opening and closing tags for the file
        # since they will get skipped while taking only the kth element

        # opening tags
        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<osm>\n  ')

        # every kth top level element
        for i, element in enumerate(get_element(OSM_FILE)):
            if i % k == 0:
                output.write(ET.tostring(element, encoding='utf-8'))

        # closing tag
        output.write('</osm>')
