import twitter
import time
api=twitter.Api()
cph=600
hour=3600
timetosleep=3600/125
f = open('corpus6', 'w')
while 1:
    statuses=api.GetPublicTimeline()
    for s in statuses:
    #print [s.text for s in statuses]
        f.write(s.text)
        f.write("\n")
        #f.writeline(s.text)    
    time.sleep(timetosleep)
    print "sleeping for some time cause of twitter max api calls"
        
    
