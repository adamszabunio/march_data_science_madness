#!/usr/bin/env python3
'''
Simulates a 5-card-stud poker game and determines the winning hand(s)
'''
import random

ranks = '23456789TJQKA'
suits = '♥♣◆♠' # add some images for fun 
deck = [r+s for r in ranks for s in suits] 
hand_types = {
    8:"Straight flush!", 7:"4 of a kind!",
    6:"Full house", 5:"Flush", 4:"Straight",
    3:"3 of a kind", 2:"2 pair", 
    1:"1 pair", 0:"High card"
}

def card_ranks(hand):
    '''
    Return a list of the ranks, sorted with the highest first.
    *Unless it is an Ace low straight [5, 4, 3, 2, Ace]
    '''
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse=True)
    if ranks == [14, 5, 4, 3, 2]:
        return [5, 4, 3, 2, 1]  
    else:
        return ranks

def flush(hand):
    '''
    Return True if all the cards have the same suit.
    '''
    suits = [s for r,s in hand]
    return len(set(suits)) == 1

def straight(ranks):
    '''
    Return True if the ranked hand forms a 5-card straight.
    '''
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5

def kind(n, ranks):
    '''
    Return the first rank that hand has exactly n-of-a-kind of. 
    Return None otherwise.
    '''
    for r in ranks:
        if ranks.count(r) == n: 
            return r
    return None

def two_pair(ranks):
    '''
    If there are two-pairs, return a tuple of ranks,
    highest rank first.
    Return None otherwise
    '''
    pairs = [r for r in set(ranks) if ranks.count(r) == 2]
    if len(pairs) < 2:
        return None
    return tuple(sorted(pairs, reverse=True))

def hand_rank(hand):
    '''
    Return a value indicating the ranking of a hand.
    '''
    ranks = card_ranks(hand) # need for straights and comparisons
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)

def poker(hands):
    '''
    Return the best hand(s): poker([hand,...]) => [hand, ...(if ties)]
    *Returns a list regardless of number of winners
    '''
    m = max(map(hand_rank, hands))
    return list(filter(lambda x: hand_rank(x)==m, hands))

def deal(numhands, n=5, deck=deck):
    '''
    Deal `numhands` of `n` cards from a shuffled `deck`
    Return a list of unique hands.
    '''
    # check to see there are enough cards in the deck 
    # to deal `numhands`
    assert len(deck)//n >= numhands
    # shuffle deck in place
    random.shuffle(deck)
    return [deck[i:i+n] for i in range(0, n*numhands, n)]

def test():
    """
    Test cases for the functions in poker program
    """
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    return 'tests pass'

def main():
    """
    Runs tests and two simualtions.
    """
    # Tests to make sure everything is running
    test()

    # Simulate 5 games of 5-card stud with 10 players in each game
    for game in range(1, 5):
        print("Game {}:".format(game))
        hands = deal(10)
        print("Hands Dealt:")
        for hand in hands:
            print(hand)
        winner = poker(hands)
        hand_type = hand_rank(winner[0])[0]
        if len(winner) > 1:
            print("\nWe have a {} way tie Winner! \n{}:\n{}\n".format(
                len(winner), hand_types[hand_type], winner))
        else:       
            print("\nWinner! \n{}:\n{}\n".format(
                hand_types[hand_type], winner))
        print("-"*60)

    # for fun, see how many games it takes to have a tie (limit 10,000 games)
    prnt_statement = False
    for game in range(10_000):
        hands = deal(10)
        winner = poker(hands)
        if len(winner) > 1:
            hand_type = hand_rank(winner[0])[0]
            print("We have a {} way tie! \n{}:\n{}\n".format(
                len(winner), hand_types[hand_type], winner))       
            print("It only took {} games to have a tie!".format(game+1))
            prnt_statement = True
            break

    if not prnt_statement:
        print("No ties for 10,000 iterations!")
        
if __name__ == "__main__":
    main()
        