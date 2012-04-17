"""
@package tweet_features
Convert tweet to feature vector.

These routines help convert arbitrary tweets in to feature vectors.

"""
import numpy


# search patterns for features
testFeatures = \
    [('hasAddict',     (' addict',)), \
     ('hasAmazing',     (' amazing,amazingly',)), \
     ('hasAwesome',    ('awesome',)), \
     ('hasBroken',     ('broke',)), \
     ('hasBetter',     ('better',)), \
     ('hasBest',     ('best',)), \
     ('hasBad',        (' bad',)), \
     ('hasBug',        (' bug',)), \
     ('hasCant',       ('cant','can\'t')), \
     ('hasCrash',      ('crash',)), \
     ('hasCool',       ('cool',)), \
     ('hasCute',        ('cute',)), \
     ('hasDifficult',  ('difficult',)), \
     ('hasDisaster',   ('disaster',)), \
     ('hasDown',       (' down',)), \
     ('hasDont',       ('dont','don\'t','do not','does not','doesn\'t')), \
     ('hasEasy',       (' easy',)), \
     ('hasExclaim',    ('!',)), \
     ('hasExcite',     (' excite',)), \
     ('hasExpense',    ('expense','expensive')), \
     ('hasFail',       (' fail',)), \
     ('hasFew',       (' few',)), \
     ('hasFast',       (' fast',)), \
     ('hasFix',        (' fix',)), \
     ('hasFine',        (' fine',)), \
     ('hasFree',       (' free',)), \
     #('hasFrowny',     (':(', '):')), \
     ('hasFuck',       ('fuck',)), \
     ('hasGood',       ('good','great')), \
     ('hasHappy',      (' happy',' happi')), \
     ('hasHate',       ('hate',)), \
     ('hasHeart',      ('heart', '<3')), \
     ('hasHonest',     ('honest',)), \
     ('hasIssue',      (' issue',)), \
     ('hasIncredible', ('incredible',)), \
     ('hasInterest',   ('interest',)), \
     ('hasLike',       (' like',)), \
     ('hasLol',        (' lol',)), \
     ('hasLove',       ('love','loving')), \
     ('hasLose',       (' lose',)), \
     ('hasNeat',       ('neat',)), \
     ('hasNever',      (' never',)), \
     ('hasNice',       (' nice',)), \
     ('hasPoor',       ('poor',)), \
     ('hasPerfect',    ('perfect',)), \
     ('hasPlease',     ('please',)), \
     ('hasPretty',        ('pretty',)), \
     ('hasReliable',       ('reliable',)), \
     ('hasSerious',    ('serious',)), \
     ('hasSecure',     ('secure',)), \
     ('hasStable',     ('stable',)), \
     ('hasSuperior',     ('superior',)), \
     ('hasShit',       ('shit',)), \
     ('hasSlow',       (' simple',)), \
     ('hasSimple',       (' slow','simplicity')), \
     #('hasSmiley',     (':)', ':D', '(:')), \
     ('hasSuck',       ('suck',)), \
     ('hasTerrible',   ('terrible',)), \
     ('hasThanks',     ('thank',)), \
     ('hasTrouble',    ('trouble',)), \
     ('hasUnhappy',    ('unhapp',)), \
     ('hasUse',        ('use',)), \
     ('hasWin',        (' win ','winner','winning')), \
     #('hasWinky',      (';)',)), \
     ('hasWorse',      ('worse','worst')), \
     ('hasWow',        ('wow','omg')) ]


def make_tweet_nparr( txt ):
    """ 
    Extract tweet feature vector as NumPy array. 
    """
    # result storage
    fvec = numpy.empty( len(testFeatures) )

    # search for each feature
    txtLow = ' ' + txt.lower() + ' '
    for i in range( 0, len(testFeatures) ):

        key = testFeatures[i][0]

        fvec[i] = False
        for tstr in testFeatures[i][1]:
            fvec[i] = fvec[i] or (txtLow.find(tstr) != -1)

    return fvec


def make_tweet_dict( txt ):
    """ 
    Extract tweet feature vector as dictionary. 
    """
    txtLow = ' ' + txt.lower() + ' '

    # result storage
    fvec = {}

    # search for each feature
    for test in testFeatures:

        key = test[0]

        fvec[key] = False;
        for tstr in test[1]:
            fvec[key] = fvec[key] or (txtLow.find(tstr) != -1)

    return fvec


def tweet_dict_to_nparr( dict ):
    """
    Convert dictionary feature vector to numpy array
    """
    fvec = numpy.empty( len(testFeatures) )

    for i in range( 0, len(testFeatures) ):
        fvec[i] = dict[ testFeatures[i][0] ]

    return fvec


def tweet_nparr_to_dict( nparr, use_standard_features=False ):
    """
    Convert NumPy array to dictionary
    """
    fvec = {}

    if use_standard_features:
        assert len(nparr) == len(testFeatures)
        fvec = {}
        for i in range( 0, len(nparr) ):
            fvec[ testFeatures[i][0] ] = nparr[i]

    else:
        for i in range( 0, len(nparr) ):
            fvec[ str(i) ] = nparr[i]

    return fvec


def is_zero_dict( dict ):
    """
    Identifies empty feature vectors
    """
    has_any_features = False
    for key in dict:
        has_any_features = has_any_features or dict[key]

    return not has_any_features
