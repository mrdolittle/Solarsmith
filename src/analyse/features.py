import nltk
from nltk.tag import _POS_TAGGER

def extract_features(text):
    sequence = nltk.pos_tag(nltk.word_tokenize(text))
    grammar='''Adjective: {<RBR>*(<JJ>|<JJS>|<JJT>|<JJR>)+}
               VbVerb: {(<RB>*(<VBN>|<VB>|<VBP>|<VBG>))+}'''
    chunks = nltk.RegexpParser(grammar)
    feat = []
    for t in chunks.parse(sequence).subtrees():
        if t.node == "Adjective":
            if len(t)>1:
                line = reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t))
                feat.append(line)
            else:
                feat.append(t[0][0])  
        elif t.node == "VbVerb":
            if len(t)>1:
                line = reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t))
                line = line.replace("n't","not")
                line = line.replace("'m", "am")
                feat.append(line)
            else:
                feat.append(t[0][0])
            
    return list(set(feat))


#Initialize _POS_TAGGER
nltk.data.load(_POS_TAGGER)
if __name__ == '__main__':
    print extract_features("The mobile web is more important than mobile apps")

