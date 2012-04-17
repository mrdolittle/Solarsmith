import twitter
import sys
from xml.sax.saxutils import unescape
writefile = open('manual', 'a')
api = twitter.Api()
option = raw_input("What would you like to search for? To stop, press enter\n")
page = 1;
while option !="":
    searchresults = api.GetSearch(term=option, per_page=100, lang="en",page=page)
    page = page+1
    for line in searchresults:
        line = unescape(line.text)
        print line
        var = raw_input("Enter an option: [Positive: '+', Negative: '-', Neutral: '0', Skip: 's', Quit: 'q'] \n")
        if var == '+':
            a = (line, "positive")
            writefile.write(repr(a))
            writefile.write("\n")
        if var == '-':
            a = (line, "negative")
            writefile.write(repr(a))
            writefile.write("\n")
        if var == '0':
            a = (line, "neutral")
            writefile.write(repr(a))
            writefile.write("\n")
        if var == 'q':
            print "DONE!"
            sys.exit
print "DONE!"    
writefile.close()

        