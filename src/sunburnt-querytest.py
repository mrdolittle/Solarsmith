

import sunburnt

# interface = sunburnt.SolrInterface("http://localhost:8080", "schema.xml")
si = sunburnt.SolrInterface("http://localhost:8080/solr/")

# ?!?!?!  Don't do like this, sunburnt doesn't do native solr syntax stuff: 
# si.query("lovekeywords:cat^2.3 OR lovekeywords:fish^1.2")

# like this
si.query(si.Q(lovekeywords='cat')**2.3 | si.Q(lovekeywords='fish')**1.2)
