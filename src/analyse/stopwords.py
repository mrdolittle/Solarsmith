# -*- coding: utf-8 -*-
'''
Stopwords

Defines a list of words that could be seen as keywords but are too vague
Includes methods: filter_keyword

@author: 0tchii, Xantoz
'''

import re

STOPWORDS = set(["something",
                 "nothing",
                 "loving",       # ex: "just got my iphone in the mail, loving it!". This might somehow be appropriate as a keyword though...
                 "hating",        # same as above applies. Strange idea: extract_keywords without filtering then use some extracted keywords for sentiment analysis?
                 "everything",
                 "anything",
                 "fun",
                 "lol",
                 "LOL",
                 "ROFL",
                 "ROFLMAO",
                 "ROLFMAO",     # rolling on lava fucking my ass of. The variant ROLF, rolling on laughing floor, is not added since it is a name
                 "rolfmao",
                 "roflmao",
                 "urlyburlysmurlypurly", # this one is inserted for URL's by word_tokenize, so we filter it (it tends to be tagged as NNP and considered a keyword)
                 "ve",                  # weird keyword when using "I've"
                 "t",                   # weird keyword when using "can't"
                 "s",
                 "a",
                "about",
                "above",
                "across",
                "after",
                "again",
                "against",
                "all",
                "almost",
                "alone",
                "along",
                "already",
                "also",
                "although",
                "always",
                "among",
                "an",
                "and",
                "another",
                "any",
                "anybody",
                "anyone",
                "anything",
                "anywhere",
                "are",
                "area",
                "areas",
                "around",
                "as",
                "ask",
                "asked",
                "asking",
                "asks",
                "at",
                "away",
                "b",
                "back",
                "backed",
                "backing",
                "backs",
                "be",
                "became",
                "because",
                "become",
                "becomes",
                "been",
                "before",
                "began",
                "behind",
                "being",
                "beings",
                "best",
                "better",
                "between",
                "big",
                "both",
                "but",
                "by",
                "c",
                "came",
                "can",
                "cannot",
                "case",
                "cases",
                "certain",
                "certainly",
                "clear",
                "clearly",
                "come",
                "could",
                "d",
                "did",
                "differ",
                "different",
                "differently",
                "do",
                "does",
                "done",
                "down",
                "down",
                "downed",
                "downing",
                "downs",
                "during",
                "e",
                "each",
                "early",
                "either",
                "end",
                "ended",
                "ending",
                "ends",
                "enough",
                "even",
                "evenly",
                "ever",
                "every",
                "everybody",
                "everyone",
                "everything",
                "everywhere",
                "f",
                "face",
                "faces",
                "fact",
                "facts",
                "far",
                "felt",
                "few",
                "find",
                "finds",
                "first",
                "for",
                "four",
                "from",
                "full",
                "fully",
                "further",
                "furthered",
                "furthering",
                "furthers",
                "g",
                "gave",
                "general",
                "generally",
                "get",
                "gets",
                "give",
                "given",
                "gives",
                "go",
                "going",
                "good",
                "goods",
                "got",
                "great",
                "greater",
                "greatest",
                "group",
                "grouped",
                "grouping",
                "groups",
                "h",
                "had",
                "has",
                "have",
                "having",
                "he",
                "her",
                "here",
                "herself",
                "high",
                "high",
                "high",
                "higher",
                "highest",
                "him",
                "himself",
                "his",
                "how",
                "however",
                "i",
                "if",
                "important",
                "in",
                "interest",
                "interested",
                "interesting",
                "interests",
                "into",
                "is",
                "it",
                "its",
                "itself",
                "j",
                "just",
                "k",
                "keep",
                "keeps",
                "kind",
                "knew",
                "know",
                "known",
                "knows",
                "l",
                "large",
                "largely",
                "last",
                "later",
                "latest",
                "least",
                "less",
                "let",
                "lets",
                "like",
                "likely",
                "long",
                "longer",
                "longest",
                "m",
                "made",
                "make",
                "making",
                "man",
                "many",
                "may",
                "me",
                "member",
                "members",
                "men",
                "might",
                "more",
                "most",
                "mostly",
                "mr",
                "mrs",
                "much",
                "must",
                "my",
                "myself",
                "n",
                "necessary",
                "need",
                "needed",
                "needing",
                "needs",
                "never",
                "new",
                "new",
                "newer",
                "newest",
                "next",
                "no",
                "nobody",
                "non",
                "noone",
                "not",
                "nothing",
                "now",
                "nowhere",
                "number",
                "numbers",
                "o",
                "of",
                "off",
                "often",
                "old",
                "older",
                "oldest",
                "on",
                "once",
                "one",
                "only",
                "open",
                "opened",
                "opening",
                "opens",
                "or",
                "order",
                "ordered",
                "ordering",
                "orders",
                "other",
                "others",
                "our",
                "out",
                "over",
                "p",
                "part",
                "parted",
                "parting",
                "parts",
                "per",
                "perhaps",
                "place",
                "places",
                "point",
                "pointed",
                "pointing",
                "points",
                "possible",
                "present",
                "presented",
                "presenting",
                "presents",
                "problem",
                "problems",
                "put",
                "puts",
                "q",
                "quite",
                "r",
                "rather",
                "really",
                "right",
                "right",
                "room",
                "rooms",
                "s",
                "said",
                "same",
                "saw",
                "say",
                "says",
                "second",
                "seconds",
                "see",
                "seem",
                "seemed",
                "seeming",
                "seems",
                "sees",
                "several",
                "shall",
                "she",
                "should",
                "show",
                "showed",
                "showing",
                "shows",
                "side",
                "sides",
                "since",
                "small",
                "smaller",
                "smallest",
                "so",
                "some",
                "somebody",
                "someone",
                "something",
                "somewhere",
                "state",
                "states",
                "still",
                "still",
                "such",
                "sure",
                "t",
                "take",
                "taken",
                "than",
                "that",
                "the",
                "their",
                "them",
                "then",
                "there",
                "therefore",
                "these",
                "they",
                "thing",
                "things",
                "think",
                "thinks",
                "this",
                "those",
                "though",
                "thought",
                "thoughts",
                "three",
                "through",
                "thus",
                "to",
                "today",
                "together",
                "too",
                "took",
                "toward",
                "turn",
                "turned",
                "turning",
                "turns",
                "two",
                "u",
                "under",
                "until",
                "up",
                "upon",
                "us",
                "use",
                "used",
                "uses",
                "v",
                "very",
                "w",
                "want",
                "wanted",
                "wanting",
                "wants",
                "was",
                "way",
                "ways",
                "we",
                "well",
                "wells",
                "went",
                "were",
                "what",
                "when",
                "where",
                "whether",
                "which",
                "while",
                "who",
                "whole",
                "whose",
                "why",
                "will",
                "with",
                "within",
                "without",
                "work",
                "worked",
                "working",
                "works",
                "would",
                "x",
                "y",
                "year",
                "years",
                "yet",
                "you",
                "young",
                "younger",
                "youngest",
                "your",
                "yours",
                "z",
                # weird keyword when using "let's"
                "let",
                "stunning",
                "half",
                "annoying",
                "inspiring",
                "amazing",
                "warming",
                "week",
                "quote"])

def nop(a):
    '''The identity function'''
    
    return a

def filter_keywords(keywords, key=nop):
    """Receives the keywords and filters out words from the set 'words'.

    Takes an optional key argument for usage like:
        filter_keywords([('hej', 2), ('potatis', 3)], key=lambda x: x[0])"""
    global STOPWORDS
    
    # matches lowercaseish
    return [x for x in keywords if len(key(x)) > 2 and key(x).lower() not in STOPWORDS]

# smileys and other words that shouldn't be left intact as to not confuse the keyword-exrctracty shit
# TODO: generate this in some function or something instead, so many combinations!
#       lotsa more smileys and other words that are wierd and stuff.
TWEET_STOPSMILEYS = set([":)", ":(", ":<", ":>", ":-)", ":-(", ":-<", ";-)", ";)", ";(", ";-(",
                         ":3",   # cat
                         ">:3",  # lion
                         "}:3"]) # elk

def split_tweet(text):
    '''Splits tweets neater than regular splitting at whitespace (for
    instance whenever we encounter a hashtag or @-notation we split
    away any punctuation at the end. Doesn't split punctuation from
    words outside of hashtags/@-notation however.'''

    def split_tag(tag):
        [(a, b)] = re.findall(r'([#@]\w+)(.*)', tag) # this will blow up if more than one match (but it won't due to the regex...)
        return [a] if b == '' else [a,b]

    wordsplit = text.split()
    result = []
    for i in wordsplit:
        if i[0] in ('#','@'):
            result = result + split_tag(i)
        else:
            result.append(i)
    return result

URL_REGEX = re.compile(r'https?:(?:(//)|(\\\\))+[!\w\d:#@%/;$()~_?\+\-=\\\.,&]*', re.I)
def strip_tweet(tweet):
    '''Strips tweet of scary features like hashtags at the start or
    end of a tweet as well as some smileys etc.

    TODO: * test whether this approach to hashtags is not insane etc.
          * More words to transform?
          * DONE keep eventual punctation (or any non-alnum chars really)
            at the end of hashtag when removing it, instead of completely nuking it.
          * DONE? strip at-sign and maybe even split those names at camelCase
          (seems common) (maybe be wholly crazy and get fullname from twitter?)
          * Strip URLS at the very end or so (like hashtags)
          '''
    global TWEET_STOPSMILEYS, URL_REGEX


    def transform(a):
        if a[0:2] == '<3':
            # convert hearts to: love 
            return "love " + a[2:]
        else:
            return a

    urlless_tweet = URL_REGEX.sub("URLYBURLYSMURLYPURLY", tweet)
    words = split_tweet(urlless_tweet)

    # # strip leading hashtags
    # while words != [] and words[0][0] == '#':
    #     del words[0]

    # strip trailing hashtags
    while words != [] and words[-1][0] == '#':
        del words[-1]

    words = map(lambda x: x[1:] if x[0] in ('#','@')  else x, words) # strip the hashes out of hashtags in the middle, as well as stripping @
    words = map(transform, words) 
    words = filter(lambda x: x not in TWEET_STOPSMILEYS, words) # strip the smileys etc. out of the tweet

    return ' '.join(words)
