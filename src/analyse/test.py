#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8
'''test script for fast and convienient test of alot of data
'''

from compiler import analyse


tweet=[u"Google is fast, reliable, easy to use and user friendly. It relies on a simplicity that many other search engines lack. Need I say more? "]
print analyse(tweet)

tweet=[u"Google is the best search engine"]
print analyse(tweet)

tweet=[u"Let’s be honest, folks. Google Chrome is amazingly superior to IE."]
print analyse(tweet)

tweet=[u"Can’t get any better browser than Chrome, can you?"]
print analyse(tweet)

tweet=[u"Google Chrome is by far the most secure browser I’ve used."]
print analyse(tweet)

tweet=[u"Google Chrome is the most stable browser I have ever used. There are very, very few crashes in Chrome."]
print analyse(tweet)

tweet=[u"Google Chrome definitely has the fastest webpage rendering of any browser I have EVER used"]
print analyse(tweet)

tweet=[u"Google Chrome is the best web browser in the world"]
print analyse(tweet)
tweet=[u"I HATE GOOGLE"]
print analyse(tweet)
tweet=[u"I dislike google"]
print analyse(tweet)
tweet=[u"I dont like justin bieber"]
print analyse(tweet)
tweet=[u"I dont like google"]
print analyse(tweet)
