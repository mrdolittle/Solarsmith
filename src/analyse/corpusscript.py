import twitter
import time

import ast

    
api=twitter.Api()
positive =[':-)', ':)',':)', ':D', '=D', '=)', 'C:', ':]',':>', ';)', ';D', ';-)','^^', '^.^', 'xD','XD', '(:', '(-:', '(=', '^.~', '<3', 'c"']
negative =[':-(', ':(', '=(', ":'(", 'D:', 'DX', 'D=', '-.-', "-.-'", ':<', ':[', 'X(', 'x(', '><', '>.<', '>_<', '<.<', '>.>']
hour=3600
timetosleep=hour/600

sentimentcorpus = open('corpusnew2', 'w')
manualtagging = open('manualtagging', 'w')
page=1
while 1:
    posstatuses=api.GetSearch(term=":-)",per_page=100,lang="en")
    negstatuses=api.GetSearch(term=":-(",per_page=100,lang="en",page=page)
    page=page+1
    for s in posstatuses:
       
                
                par=(s.text,"positive");
                sentimentcorpus.write(repr(par))
                sentimentcorpus.write('\n')
    for s in negstatuses:

                par=(s.text,"negative");
                sentimentcorpus.write(repr(par))
                sentimentcorpus.write('\n')
                   
    time.sleep(timetosleep)
    print "sleeping for some time cause of twitter max api calls"
        