#!/usr/bin/python2.7

from sentiment import analyse_sentiment

a = True
while a:
    a = raw_input()
    print analyse_sentiment(a)

