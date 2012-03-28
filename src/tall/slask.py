'''
Created on Mar 21, 2012

@author: jonas
'''
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring
import sys
import re, string

st = 'hej 89&lt"%\/ a sd'
pattern = re.compile('[^\w_\s]+')
test = pattern.sub('', st)
print test

