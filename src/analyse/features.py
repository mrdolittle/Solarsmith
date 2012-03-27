import nltk
from nltk.tag import _POS_TAGGER

def extract_features(text):
    sequence = nltk.pos_tag(nltk.word_tokenize(text))
    grammar='''Adjective: {<RBR>*(<JJ>|<JJS>|<JJT>|<JJR>)+}
               RbVerb: {(<RB>*(<VBN>|<VB>|<VBP>|<VBG>))+}'''
    chunks = nltk.RegexpParser(grammar)
    feat = []
    print chunks.parse(sequence)
    for t in chunks.parse(sequence).subtrees():
        if t.node == "Adjective":
            if len(t)>1:
                line = reduce(lambda x,y: x + " " + y, map(lambda (x,_1): x, t))
                feat.append(line)
            else:
                feat.append(t[0][0])  
        elif t.node == "RbVerb":
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
    print extract_features("Disarming The Playground: Training Video One [VHS]: Disarming the Playground presents a movement-based curriculu... http://t.co/rc9qLCfg")

