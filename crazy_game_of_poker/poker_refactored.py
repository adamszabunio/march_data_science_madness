#!/usr/bin/env python3
'''
Simulates a 5-card-stud poker game and determines the winning hand(s)
'''
import random

ranks = '23456789TJQKA'
suits = '♥♣◆♠' # Hearts, Clubs, Diamonds, Spades 
deck = [r+s for r in ranks for s in suits] 
hand_types = { # need to bump the value of straight flush to 9
    9:"Straight flush!", 7:"4 of a kind!",
    6:"Full house", 5:"Flush", 4:"Straight",
    3:"3 of a kind", 2:"2 pair", 
    1:"1 pair", 0:"High card"
}
              # 4-of-a-kind, fh,     3-of-a-kind
count_rankings = {(4,1):7,  (3,2):6, (3,1,1):3, 
                 (2,2,1):2, (2,1,1,1):1, (1,1,1,1,1):0}
                # two_pair,  one_pair,    high_card
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
    '''
    Test cases for the functions in poker program
    '''
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House
    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert hand_rank(sf) == (9, (10, 9, 8, 7, 6))
    assert hand_rank(fk) == (7, (9, 7))
    assert hand_rank(fh) == (6, (10, 7))
    return 'tests pass'

def games(n_games=5, n_players=10):
    '''
    Simulate `n_games` of 5-card stud with `n_players` in each game
    '''
    for game in range(1, n_games+1):
        print("Game {}:".format(game))
        hands = deal(n_players)
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

def to_tie_or_not_to_tie(n_sim=10_000, n_players=10):
    '''
    Simulate `n_sim` games of 5-card-stud with `n_players` in each game.
    Print how many games required to find a tie, and the winners
    * if one is found in `n_sim` games.
    '''
    prnt_statement = False
    for game in range(n_sim):
        hands = deal(n_players)
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

def main():
    '''
    Runs tests and two simualtions.
    '''
    # Tests to make sure everything is running
    test()
    # Simulate 5 games of 5-card stud with 10 players in each game
    games()
    # for fun, see how many games it take to have a tie (limit 10,000 games)
    to_tie_or_not_to_tie()
    
if __name__ == "__main__":
    main()
