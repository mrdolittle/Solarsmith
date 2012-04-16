'''
Created on Apr 16, 2012

@author: mbernt
'''

def get_words_list(sentence, tuple_length):
    sentences=sentence.lower().split()
    tuple_length=min(tuple_length,len(sentences))
    list=[]
    i=1
    while i<=tuple_length:
        start=0
        end=start+i
        while end<=len(sentences):
            list.append(" ".join(sentences[start:end]))
            start=start+1
            end=start+i
        i=i+1
    return list
        
print get_words_list("hej pa lilla dej", 1)
print get_words_list("hej pa lilla dej", 2)
print get_words_list("hej pa lilla dej", 3)