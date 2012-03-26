import nltk
from nltk.tag import _POS_TAGGER

def extract_features(text):
    sequence = nltk.pos_tag(nltk.word_tokenize(text))
    grammar='''Adjective: {<JJ>}
               VbVerb: {(<RB>*(<VBN>|<VB>|<VBP>|<VBG>))+}'''
    chunks = nltk.RegexpParser(grammar)
    feat = []
    for t in chunks.parse(sequence).subtrees():
        if t.node == "Adjective":
            feat.append(t[0][0])          
        elif t.node == "VbVerb":
            if len(t)>1:
                line = reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t))
                line = line.replace("n't","not")
                feat.append(line)
            else:
                feat.append(t[0][0])
              
    return feat


#Initialize _POS_TAGGER
nltk.data.load(_POS_TAGGER)

print extract_features("I really don't like this awful lamp")  