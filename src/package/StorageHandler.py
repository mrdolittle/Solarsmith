'''
Created on Mar 19, 2012

@author: mbernt
'''

def getAllUserUpdate():
    '''
    used by update
    
    returns: (int sinceid,int updatecount, String username)[] tuples
    '''
    
    #test, replace with real code
    list=[]
    updatecount=30
    sinceid=7
    username="name"
    list.append((sinceid,updatecount,username))
    return list

#placeholder
def getAllUserNames():
    '''
    used by scrape and...
    
    returns String[] names
    '''
    return ["name"]