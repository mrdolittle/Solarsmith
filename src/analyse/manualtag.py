import twitter

writefile = open('manual', 'a')
api = twitter.Api()
option = raw_input("What would you like to search for? \n")
while option !="":
    searchresults = api.GetSearch(option)
 
    for line in searchresults:
        line = line.text
        print line
        var = raw_input("Enter an option: [Positive: '+', Negative: '-', Neutral: '0', Skip: 's'] \n")
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
            
    print "DONE!"
    
writefile.close()

        