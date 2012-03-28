import twitter
import time
api=twitter.Api()
hour=3600
timetosleep=3600/60
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
        
    
