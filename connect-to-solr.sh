#!/bin/sh

# run this script and then you can connect to solr on
# localhost:8888/solr/ until you CTRL-C this or otherwise kill it.
# send your ssh pubkey to bountyjedi@gmail.com/antonki@kth.se to
# request access (currently granted to MVK group only, if you are not
# please set up your own Solr)


echo "--- Connect to Solr at http://localhost:8888/solr/ ---"

ssh -N -p 22022 -L 8888:localhost:8888 sshguest@xantoz.failar.nu
