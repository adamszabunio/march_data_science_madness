#!/usr/bin/env python3
import itertools

ranks = '23456789TJQKA'
suits = '♥♣◆♠' # Hearts, Clubs, Diamonds, Spades 
deck = [r+s for r in ranks for s in suits] 
count_rankings = {(4,1):7, (3,2):6, (3,1,1):3, 
                 (2,2,1):2, (2,1,1,1):1, (1,1,1,1,1):0}

def group(items):
    '''
    Returns sorted tuples of (count, item), a reverse Counter.
    '''
    groups = [(items.count(i), i) for i in set(items)]
    return sorted(groups, reverse=True)

def hand_rank(hand):
    '''
    Return a value indicating the ranking of a hand.
    '''
    groups = group(["--23456789TJQKA".index(r) for r,s in hand])
    counts, ranks = zip(*groups) # unpack
    if ranks == (14, 5, 4, 3, 2): # catch Ace low straights
        ranks = (5, 4, 3, 2, 1)
        
    flush = len(set([s for r,s in hand])) == 1
    straight = (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5
    
    return max(count_rankings[counts], 5*flush + 4*straight), ranks

def best_hand(hand):
    '''
    From a 7-card hand, return the best 5 card hand.
    *Ties can exist, but are ignored, i.e. only first winner is chosen
    '''
    return max(itertools.combinations(hand, 5), key=hand_rank)

def poker(hands):
    '''
    Return the best hand(s): poker([hand,...]) => [hand, ...(if ties)]
    *Returns a list regardless of number of winners
    '''
    m = max(map(hand_rank, hands))
    return list(filter(lambda x: hand_rank(x)==m, hands))    