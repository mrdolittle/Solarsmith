import compiler

tweetlist=["one tweet is good but two is better", "I don't like apples!","I like reading books about apples","tweeting is boring","I've bought an apple computer"]
print compiler.analyse_sentences_var_2(tweetlist)


tweet="i dislike this apple"
print compiler.analyse_sentence(tweet)

tweet="i hate this computer"
print compiler.analyse_sentence(tweet)

tweet="i like this orange"
print compiler.analyse_sentence(tweet)

tweet="i thanks thanks happy love this phone"
print compiler.analyse_sentence(tweet)

tweet="this computer is so terrible"
print compiler.analyse_sentence(tweet)