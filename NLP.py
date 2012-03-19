# lite kladdig testkod bara



import nltk

##FUNKTIONER##



def Hi():
  print"supz!"
  return


def test(tweet):
  tokens=nltk.word_tokenize(tweet)
  test=nltk.pos_tag(tokens)
  for token in test:
    print token
      




##SLUTFUNKTIONER##

# main
pos_tweets = [('I love this car', 'positive'),
              ('This view is amazing', 'positive'),
              ('I feel great this morning', 'positive'),
              ('I am so excited about the concert', 'positive'),
              ('He is my best friend', 'positive')]

neg_tweets = [('I do not like this car', 'negative'),
              ('This view is horrible', 'negative'),
              ('I feel tired this morning', 'negative'),
              ('I am not looking forward to the concert', 'negative'),
              ('He is my enemy', 'negative')]


Hi()
hello="Hello, World!"


print hello

goodTweet ="I LIKE DOGS"

badTweet ="I Hate DOGS"

tweet2=nltk.word_tokenize(badTweet)
tweet1=nltk.word_tokenize(goodTweet)
print nltk.pos_tag(tweet1)
print nltk.pos_tag(tweet2)

test(goodTweet)
test(badTweet)

-

-

