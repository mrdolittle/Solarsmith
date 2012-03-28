'''
Created on Mar 21, 2012

@author: jonas
'''


def get_common_keywords(userskeywords, otherkeywords):
    commonkeywords = []
    for key in otherkeywords:
        if key in userskeywords:
            commonkeywords = commonkeywords + [key]
    return commonkeywords

first = ["hej", "da","knasboll"]
sec = ["jag", "heter", "knasboll", "da"]
test = get_common_keywords(first, sec)
print test
