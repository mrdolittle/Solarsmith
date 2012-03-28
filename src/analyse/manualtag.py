readfile = open('manualtagging', 'r')
writefile = open('manual', 'w')

 
for line in readfile:
    print line + "\n"
    var = raw_input("Enter an option: [Positive: '+', Negative: '-', Neutral: '0', Skip: 's']")
    if var == '+':
        par = (var, "positive")
        writefile.write(repr(par))
        writefile.write("\n")
    if var == '-':
        par = (var, "negative")
        writefile.write(repr(par))
        writefile.write("\n")
    if var == '0':
        par = (var, "neutral")
        writefile.write(repr(par))
        writefile.write("\n")

readfile.close()
writefile.close()

        