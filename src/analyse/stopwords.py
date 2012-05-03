# -*- coding: utf-8 -*-
'''
Stopwords

Defines a list of words that could be seen as keywords but are too vague
Includes methods: filter_keyword

@author: 0tchii, Xantoz
'''


import re
from common import *

#### TODO: Words that MAYBE should be stopworded or maybe just weighted down due to their commonality
# fail
# post,
# birthday,
# check,
# hope,
# sun(maybe?), (realise this is a former company's name though! (could be supported through explicit_keywords only thought))
# account,
# tomorrow,
# watching (watch?)
# saying
# playing
# version
# word (be VERY careful of Microsoft Word, which is a valid keyword and all)
# help
#### Should probably be just weighted down, not ever completely removed
# watch (people could really like watches for instance)
# read
# tonight (vagueish, though just night seems slightly (just) better)
# season (just for it's vagueness)
# blog
# picture 
# hell
# internet
# tv(true maybe, this is a pretty good keyword overall)
# game
# google(maybe even this: since everybody seems to love it so much)
# talk
# followers
# twitter
# friend
# idea(?)
# wait (should be downweighted quite fiercly though)
# people(?) (CURRENTLY STOPWORDED, should maybe be only downvoted)
# info
# playing
# weekend
# boy
# dad
# mom
# brother
# nice (since it's a city besides being a word)




# This is a huge list, meant to filter out stuff that
# isn't good KEYWORDS, after the extracting has been done.
# TODO: move me outta this file and into some separate file
# (preferrably newline-separated but with support for comments)
# ---
# POSSIBLE OPTIMIZATION: bloom filter (though this is hardly
# speed/memory-critical as of now. Could maybe be memory-critical,
# though probably not)
# ---
# Words marked with a comment of STEM CAUTIOUSLY indicate that these
# words should perhaps not be stemmed by the keyword stemmer as the
# non-stemmed versions might have legitimate interest as
# keywords. E.g. damning, damnation are interesting but damn
# isn't. 'dudes' is possibly interesting (maybe not...) but 'dude'
# almost always isn't.
#
# By having words like these in a list-of-words-to-protect-from-stemming
# we can avoid having them stopworded
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
                 "happening",
                 "happy",
                 "guy",                                     #FIXME?: poor people with the name guy. MAYBE JUST DOWNWEIGHT THIS
                 "account",
                 "wee",     # now while this could be construed as a
                            # keyword (wee == pee == piss etc.) when
                            # we see "wee" in lovekeywords it usually
                            # isn't because the person at hand likes
                            # piss...
                 "yay",
                 "beware",
                 "ima",                                      # lazy people usually write this instead of "i'ma". it's not a keyword. Maybe we should synonym on this though
                 "bye",
                 "yesss",                                   # maybe this should have a regex
                 "love",
                 "lmfao",
                 "hahaha",
                 "hate",
                 "reason",
                 "goal",
                 "dude",                                     # though in the plural this might be a good keyword. TODO: STEM CAUTIOUSLY. make "dudes" exempt from stemming when implementing that
                 "wtf",
                 "wont",                                     # similar to 'ima' this shouldn't really be needed and should instead be sanitized by strip_tweet
                 "saying",
                 "damn",                                     # TODO: STEM CAUTIOUSLY. have caution when stemming "damning" and "damnation"
                 "som",                                      # what is this even doing here? it's like a swedish word!
                 "start",                                    # TODO: STEM CAUTIOUSLY. starting might be very slightly interesting (ok maybe not)
                 "haha",
                 "ahaha",                                     # maybe we should regex for laughing sounds...
                 "tat",
                 "thats",
                 "that",
                 "dis",                                      # similar to ima could be handled in strip_tweet
                 "sucks",
                 "suck",
                 "miss",
                 "list", # TODO: STEM CAUTIOUSLY. the stemmer shoulde maybe actually go backwards and
                         # make list -> lists even. Maybe the keyword extractor should be cautious of
                         # determinants for stuff like "The List" (at least when titlecapsed...) darnit
                         # is NLP difficult BLAH
                 "dang",
                 "darn",
                 "wow",
                 "people", # SHOULD WE HAVE THIS? this is a somwhat valid keyword, but it appears so frequently that it sort of loses any meaning for matching purposes
                 "buy",    # TODO: STEM CAUTIOUSLY. 'buying' might still make good sense as a keyword (though our keyword stemmer oughn't stem VBG to NN anyhow
                 "hmm",
                 "stop",                                # WEE! 'stop' is a stopword
                 "answer",                                   # STEM CAUTIOUSLY. 'answering' might be relevant
                 "free",                                      # probably...
                 "auto",
                 "sigh",                                     # though it is sort of conceivable for somebody to _REALLY_ like sighs...
                 "fine",                                     # though it is conceivable that "a fine" or fines is a keyword of interest... so STEM CAUTIOUSLY
                 "win",                                      # STEM CAUTIOUSLY. 'winning' is a good keyword. and probably something else to
                 "wins",
                 "dear",
                 "please",                                   # STEM CAUTIOUSLY. 'pleasure' for instance
                 "crap",
                 "past",                                      # probably...
                 "hour",
                 "piece",
                 "funny",
                 "view",                                     # STEM CAUTIOUSLY. 'views' like in the youtube sense or so could be an interesting keyword
                 "question",                                  # STEM CAUTIOUSLY. 'questions' and maybe even 'questioning' might be somewhat interesting
                 "cool",                                       # STEM CAUTIOUSLY. 'cooling' is a nice keyt\section{word}
                 "a long time",
                 "episode",                                  # way too common word
                 "lame"
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
TWEET_STOPSMILEYS = set(["-_-", "T_T", "^^", "^_^", ":)", ":(", ":<", ":>", ":-)", ":-(", ":-<", ";-)", ";)", ";(", ";-(", ":D", "D:", ":-D", "D-:",
                         ":3",   # cat
                         ">:3",  # lion
                         "}:3"]) # elk

URL_REGEX = re.compile(r'https?:(?:(//)|(\\\\))+[!\w\d:#@%/;$()~_?\+\-=\\\.,&]*', re.I)
DOTS_REGEX = re.compile(r'\.{2,}')
AT_REGEX = re.compile(r'\s+@\s+')
def strip_tweet(tweet):
    '''Strips tweet of scary features like hashtags at the start or
    end of a tweet as well as some smileys etc. Also canonicalises some words, turning e.g. thanx -> thanks
    '''
    # TODO: * Convert ima -> i'ma, wont -> won't, dis -> this, u -> you, cant -> can't etc. etc. (maybe not the last one, could be "to diss" or something)
    #       * Remove words consisting of only repeated underline (other characters?)
    #       * test whether this approach to hashtags is not insane etc.
    #       * More words to transform?
    #       * DONE keep eventual punctation (or any non-alnum chars really)
    #         at the end of hashtag when removing it, instead of completely nuking it.
    #       * DONE? strip at-sign and maybe even split those names at camelCase
    #       (seems common) (maybe be wholly crazy and get fullname from twitter?)
    #       * Strip URLS completely at the very end or so (like hashtags)

    global TWEET_STOPSMILEYS, URL_REGEX, DOTS_REGEX, AT_REGEX


    def transform(a):                                       # TODO: break this out to become own function or so
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
    
