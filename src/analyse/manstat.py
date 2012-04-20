#!/usr/bin/python2.7
import sys
import fileinput
import ast

length = 0

pos = 0
neg = 0
neu = 0

for line in fileinput.input():
    length = length + 1
    (_1,stat) = ast.literal_eval(line)
    if stat == "positive":
        pos = pos + 1
    if stat == "negative":
        neg = neg + 1
    if stat == "neutral":
        neu = neu +1
        
print("Positive: " + str(100*pos/length) + "%\n")
print("Negative: " + str(100*neg/length) + "%\n")
print("Neutral: " + str(100*neu/length) + "%\n") 

 



