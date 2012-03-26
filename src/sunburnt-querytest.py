

import sunburnt

# interface = sunburnt.SolrInterface("http://localhost:8080", "schema.xml")
# si = sunburnt.SolrInterface("http://localhost:8080/solr/")
si = sunburnt.SolrInterface("http://xantoz.failar.nu:8080/solr/")


# ?!?!?!  Don't do like this, sunburnt doesn't do native solr syntax stuff: 
# si.query("lovekeywords:cat^2.3 OR lovekeywords:fish^1.2")

# like this
print si.query(si.Q(lovekeywords='cat')**2.3 | si.Q(lovekeywords='fish')**1.2).execute()

lst = [("cat", 44), ("bear hunting", 22), ("dog", 33)]

if lst == []:
    print "NEEEEJ"
    
a = si.Q(lovekeywords=lst[0][0])**lst[0][1]
for (x,y) in lst[1:]:
    a = a | si.Q(lovekeywords=x)**y
print si.query(a).field_limit('id', score=True).execute()

