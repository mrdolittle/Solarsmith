'''
Created on Mar 19, 2012

@author: mbernt
'''

def get_all_user_for_update():
    '''
    used by update
    
    returns: (int sinceid,int updatecount, String username)[] tuples
    '''
    # get profiles from sunburnt with only the needed info
    # I don't know the format but maybe it's xml
    #xml_res=sunburnt.get...
    
    # change xml to tuple list
    #list=to_tuple_list(xml_res)

    # test return
    updatecount=30
    sinceid=7
    username="name"
    return [(sinceid,updatecount,username)]
    #return list 

#placeholder
def get_all_user_names():
    '''
    used by scrape and...
    
    returns String[] names
    '''
    return ["name"]