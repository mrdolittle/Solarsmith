'''
Created on Mar 27, 2012

@author: jimmy
'''
from datetime import datetime 

LOG_DIRECTORY = "/tmp/"

def log(source, text):
    global LOG_DIRECTORY
    
    current_time = datetime.now()
    file = LOG_DIRECTORY + source +".log"
    with open(file, 'a+') as log:
        log.write(str(current_time) + ": " + text + "\n")