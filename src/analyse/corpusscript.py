import twitter
import time
from xml.sax.saxutils import unescape
'''
Basic twitter corpuss script that gather tweets based on smileys and 
tags them correspondely to negative and positive and put them in our corpus
so they can later be used by our machine learning algorithm 
'''
CORPUS="corpusnew3"    
api=twitter.Api()
#determins sleeptime based on how many calls (to not exceed twitters calllimit)
#max ammount for unautherized twitter api gathering is 1500 tweets per hour
#or 125calls
hour=3600
calls_per_hour=6
timetosleep=hour/calls_per_hour

sentimentcorpus = open(CORPUS, 'a')
page=1


# the loop which runs indefinatly to gather data
while 1:
    posstatuses=api.GetSearch(term=":-)",per_page=100,lang="en")
    negstatuses=api.GetSearch(term=":-(",per_page=100,lang="en",page=page)
    page=page+1
    for s in posstatuses:
                par=(unescape(s.text),"positive");
                sentimentcorpus.write(repr(par))
                sentimentcorpus.write('\n')
    for s in negstatuses:
                par=(unescape(s.text),"negative");
                sentimentcorpus.write(repr(par))
                sentimentcorpus.write('\n')
                   
    time.sleep(timetosleep)
    print "sleeping for some time cause of twitter max api calls"
        