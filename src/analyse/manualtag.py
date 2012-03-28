writefile = open('manual', 'w')
import twitter
api = twitter.Api()
var = raw_input("What would you like to search for?")
searchresults = a.GetSearch(var)
 
for line in searchresults:
    line = line.text()
    print line + "\n"
    var = raw_input("Enter an option: [Positive: '+', Negative: '-', Neutral: '0', Skip: 's']")
    if var == '+':
        par = (line, "positive")
        writefile.write(repr(par))
        writefile.write("\n")
    if var == '-':
        par = (line, "negative")
        writefile.write(repr(par))
        writefile.write("\n")
    if var == '0':
        par = (line, "neutral")
        writefile.write(repr(par))
        writefile.write("\n")

readfile.close()
writefile.close()

        