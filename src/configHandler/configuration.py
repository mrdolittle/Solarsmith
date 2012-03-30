'''
Created on Mar 28, 2012

@author: jimmy
'''

'''Documentation goes here!!!!!!!!'''  

class Config():
    
    def __init__(self, conf_file="../../configuration_file.conf"):
        #Global variables
        self.READ_FROM_FILE = conf_file
        self.SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/" 
#        self.REQUEST_SERVER = "130.229.142.114"
        # self.REQUEST_SERVER = "130.229.185.90"
        # self.TALL_SERVER = "130.229.185.90"
        self.REQUEST_SERVER="localhost"
        self.TALL_SERVER="localhost"
        #self.set_locations()
        
    def set_locations(self):
        '''This method will read the file given in the __init__ and set the variables.'''
        
        file = open(self.READ_FROM_FILE)
        for current_line in file:
            if not current_line.startswith('#', 0, 1):    #The line is not a comment.
                #Remove newline
                current_line = current_line.replace('\n', '')
                
                #If the line starts with SOLR then set the solr variable
                if current_line.startswith("SOLR"):
                    location = current_line.rpartition('=')
                    location_as_string = str(location[2])
                    location_as_string = location_as_string.lstrip()                
                    self.SOLR_SERVER = location_as_string
                    
                #If the line starts with REQUEST then set the request_server variable
                elif current_line.startswith("REQUEST"):
                    location = current_line.rpartition('=')
                    location_as_string = str(location[2])
                    location_as_string = location_as_string.lstrip()
                    self.REQUEST_SERVER = location_as_string
                
                #If the line starts with TALL then set the tall variable
                elif current_line.startswith("TALL"):
                    location = current_line.rpartition('=')
                    location_as_string = str(location[2])
                    location_as_string = location_as_string.lstrip()
                    self.TALL_SERVER = location_as_string
                
    def get_solr_server(self):
        '''Will return the location of the Solr Server given in the configuration_file.conf
        @return: The location of the Solr Server'''
        
        return self.SOLR_SERVER
    
    def get_request_server(self):
        '''Will return the location of the Request Server given in the configuration_file.conf
        @return: The location of the Request Server'''
        
        return self.REQUEST_SERVER
    
    def get_tall_server(self):
        '''Will return the location of the Tall Server given in the configuration_file.conf
        @return: The location of the Tall Server'''
        
        return self.TALL_SERVER
