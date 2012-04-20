# -*- coding: utf-8 -*-
'''
Stopwords

Defines a list of words that could be seen as keywords but are too vague
Includes methods: filter_keyword

@author: 0tchii, Xantoz
'''

import re
from common import *

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
                 "quote",
                 "awesome",
                 "time",
                 "okay",
                 "doing",
                 "coming",
                 "using",
                 "crappy",
                 "lot",
                 "anymore",
                 "look",
                 "looking",
                 "yup",
                 "'ve", # stupid keyword coming from whatever
                 "disgusting",
                 "cause",
                 "day", "days",  # really really fuzzy (second one not needed if we stem plurals in future)
                 "life",         # fuzzy
                 "getting",
                 "trying",      # hmm
                 "name",
                 "yes",
                 "sorry",        # WUT?
                 "fascinating",
                 "talkin",
                 "thanks",
                 "row",
                 "yeah",
                 "etc",
                 "join",
                 "omg",
                 "shit",
                 "fucking",
                 "stuff",
                 "fuck",
                 "thank",
                 "excited",
                 "times",
                 "holding",
                 "rule",
                 "feel",
                 "worst",
                 "pay",
                 "stupid",
                 "taking",
                 "happening"
                 ])

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
TWEET_STOPSMILEYS = set(["T_T", "^^", "^_^", ":)", ":(", ":<", ":>", ":-)", ":-(", ":-<", ";-)", ";)", ";(", ";-(", ":D", "D:", ":-D", "D-:",
                         ":3",   # cat
                         ">:3",  # lion
                         "}:3"]) # elk

URL_REGEX = re.compile(r'https?:(?:(//)|(\\\\))+[!\w\d:#@%/;$()~_?\+\-=\\\.,&]*', re.I)
DOTS_REGEX = re.compile(r'\.{2,}')
AT_REGEX = re.compile(r'\s+@\s+')
def strip_tweet(tweet):
    '''Strips tweet of scary features like hashtags at the start or
    end of a tweet as well as some smileys etc.

    TODO: * Remove words consisting of only repeated underline (other characters?)
          * test whether this approach to hashtags is not insane etc.
          * More words to transform?
          * DONE keep eventual punctation (or any non-alnum chars really)
            at the end of hashtag when removing it, instead of completely nuking it.
          * DONE? strip at-sign and maybe even split those names at camelCase
          (seems common) (maybe be wholly crazy and get fullname from twitter?)
          * Strip URLS completely at the very end or so (like hashtags)
          '''
    global TWEET_STOPSMILEYS, URL_REGEX, DOTS_REGEX, AT_REGEX


    def transform(a):
        if a[0:2] == '<3':
            # convert hearts to: love 
            return u'love ' + a[2:]
        if a[0] == u'\u2665':   # unicode heart !
            return u'love' + a[1:]
        if a == "thanx":        # correct an internet spelling (TODO: more of these :/)
            return "thanks"
        else:
            return a

    words = split_tweet(AT_REGEX.sub(" at ",
                                     URL_REGEX.sub("URLYBURLYSMURLYPURLY",
                                                   DOTS_REGEX.sub(" ... ",
                                                                  tweet.replace(u'\u2026', "...")))))

    # # strip leading hashtags
    # while words != [] and words[0][0] == '#':
    #     del words[0]

    # strip leading @Usage (fetching these is handled separately
    # anyhow, so less confusion for the POS tagger is good. Albeit
    # names in the middle of the tweet will thus be prioritated.)
    while words != [] and words[0][0] == '@':
        del words[0]

    # strip trailing hashtags
    while words != [] and words[-1][0] == '#':
        del words[-1]

    words = map(lambda x: x[1:] if x[0] in ('#','@')  else x, words) # strip the hashes out of hashtags in the middle, as well as stripping @
    words = map(transform, words) 
    words = filter(lambda x: x not in TWEET_STOPSMILEYS, words) # strip the smileys etc. out of the tweet

    result = ' '.join(words)
    # print "strip_tweet():", tweet, "=>", result
    return result
    
