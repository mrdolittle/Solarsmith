'''
Created on Mar 26, 2012

@author: zorgie
'''
from mx import DateTime as mxDateTime

early = mxDateTime.DateTime(2012, 1, 1, 0, 0, 0.0)
late = mxDateTime.DateTime(2013, 1, 1, 0, 0, 0.0)

print (late-early).days