
from xml.sax.saxutils import unescape
'''really an uncessary python classed that we used earlienr to clean 
    corpuses that was not correctly cleansed, now it serves no purpose since
    the logic is put in the scraper instead  now
'''



def cleaner(inputf,output):
    ''' METHOd that cleans a file from bad format and turns for example &lt to < etc...'''
    inputfile=open(inputf,'r')
    outputfile=open(output,'w')
    for line in inputfile:
        outputfile.write(unescape(line))
        outputfile.write('\n')
            
            
cleaner("corpusnew2","corpusnew")
