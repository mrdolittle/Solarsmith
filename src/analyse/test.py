# -*- coding: utf-8 -*-
import compiler

tweetlist=["one tweet is good but two is better", "I don't like apples!","I like reading books about apples","tweeting is boring","I've bought an apple computer"]
print compiler.analyse_sentences_var_2(tweetlist)


tweet="i dislike this apple"
print compiler.analyse_sentence(tweet)

tweet="Google is fast, reliable, easy to use and user friendly. It relies on a simplicity that many other search engines lack. Need I say more? "
print compiler.analyse_sentence(tweet)

tweet="Google is the best search engine"
print compiler.analyse_sentence(tweet)

tweet="Let’s be honest, folks. Google Chrome is amazingly superior to IE."
print compiler.analyse_sentence(tweet)

tweet="Can’t get any better browser than Chrome, can you?"
print compiler.analyse_sentence(tweet)

tweet="Google Chrome is by far the most secure browser I’ve used."
print compiler.analyse_sentence(tweet)

tweet="Google Chrome is the most stable browser I have ever used. There are very, very few crashes in Chrome."
print compiler.analyse_sentence(tweet)

tweet="Google Chrome definitely has the fastest webpage rendering of any browser I have EVER used"
print compiler.analyse_sentence(tweet)

tweet="Google Chrome is the best web browser in the world"
print compiler.analyse_sentence(tweet)