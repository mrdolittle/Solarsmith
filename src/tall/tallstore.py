'''
Created on Mar 22, 2012

@author: jonas
'''
import sunburnt
import ast


class SolrUser:
    def __init__(self, id, lovekeywords_list, hatekeywords_list, **other_kwargs):
        self.lovekeywords_list = lovekeywords_list
        self.id = id
        self.hatekeywords_list = hatekeywords_list
        self.other_kwargs = other_kwargs

    def __repr__(self):
        return 'Id: %s Lovekeywords: %s Hatekeywords: %s' % (self.id, self.lovekeywords_list, self.hatekeywords_list)

    def getKeywords(self):
        lovekeywords = "<lovekeywords>"
        lovelist = ast.literal_eval(self.lovekeywords_list)
        for key,w in lovelist:
            print "key: " + key
            lovekeywords = lovekeywords + key + ","

        lovekeywords = lovekeywords[:-1]
        lovekeywords = lovekeywords + "</lovekeywords>"

        hatekeywords = "<hatekeywords>"
        hatelist = ast.literal_eval(self.lovekeywords_list)
        for key, w in hatelist:
            print "key: " + key
            hatekeywords = hatekeywords + key + ","

        hatekeywords = hatekeywords[:-1]
        hatekeywords = hatekeywords + "</hatekeywords>"
        print lovekeywords
        print hatekeywords
        return lovekeywords, hatekeywords

    def getId(self):
        return self.id


def getUserid(username):
    SOLR_SERVER = "http://xantoz.failar.nu:8080/solr/"

    interface = sunburnt.SolrInterface(SOLR_SERVER)

    ans = interface.query(id=username)

    for result in ans.execute(constructor=SolrUser):
        print result
    result.getKeywords()

    return result

getUserid("xantestuser2")
#friends = interface.query(lovekeywords='Fear')
#for fres in friends.execute(constructor=SolrUser):
#    print fres
