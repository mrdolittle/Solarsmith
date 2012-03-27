#!/usr/bin/python

import sunburnt
from storageHandler.Document import Document

# FIXME: can schema be gotten from server directly with sunburnt (pydoc seemed to suggest this)
# interface = sunburnt.SolrInterface("http://localhost:8080", "schema.xml")
# interface = sunburnt.SolrInterface("http://localhost:8080/solr/", "schema.xml") 
interface = sunburnt.SolrInterface("http://xantoz.failar.nu:8080/solr/")

asdf = []
asdf.append(Document("potatismos", [("cat", 34), ("fishing", 22), ("bear grylls", 33)], [("dog", 123), ("bear hunting", 44)]))
asdf.append(Document("motatispos", [("cat", 44), ("bear hunting", 22), ("dog", 33)], [("fishing", 55), ("bear grylls", 33)]))

asdf.append(Document("xantestuser1", [("fear", 1.0*1000), 
                                      ("penguin",0.3*1000),
                                      ("cheese",0.5*1000),
                                      ("catastrophe",0.5*1000),
                                      ("mortal",0.5*1000),
                                      ("lethality",0.5*1000)]))
         
asdf.append(Document("xantestuser2", [("fear",0.3*1000),
                                      ("penguin",0.8*1000),
                                      ("cheese",0.5*1000),
                                      ("catastrophe",0.5*1000),
                                      ("mortal",0.5*1000),
                                      ("lethality",0.5*1000)]))

interface.add(asdf)
interface.commit()
