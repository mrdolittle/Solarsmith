'''
Created on Mar 19, 2012

@author: mbernt
'''



def analyseAndAddToDatabase(username,sinceID,remakeProfile):
    '''
    used by update, scrape and request
    
    API: (boolean userUpdatedInDatabase) analyseAndUpdateUser(String username,int sinceid,boolean remakeProfile):
    
    Description:
    if remakeProfile is true then it will disregard sinceID and analyse as many tweets as possible
    and then replace the profile in solr.
    
    if remakeProfile is false it will analyse tweets newer than sinceID and merge the result with the profile in solr
    
    '''
    # maybe check if the user exists on twitter
    
    if(remakeProfile):
        # get all tweeets from twitter API 
        
        # send to analysis
        
        # store result in sunburnt
        
        return True #returns true if added to solr
    else:
        # get tweets newer than sinceID 
        
        # send to analysis
        
        # merge result with the profile in solr
        
        return True # returns true if added to solr
        
    