#!/usr/bin/env python3
'''
CS 212, hw1-1: 7-card stud
'''

import random
from utils7card import *

hand_types = {
    9:"Straight flush!", 7:"4 of a kind!",
    6:"Full house", 5:"Flush", 4:"Straight",
    3:"3 of a kind", 2:"2 pair", 
    1:"1 pair", 0:"High card"
}

def test_best_hand():
    '''
    Test cases for best combination in 7-card-stud
    '''
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('tests passed\n')

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

def games(n_games=5, n_players=7, n_cards=7):
    '''
    Simulate `n_games` of `n_card` stud with `n_players` in each game
    '''
    for game in range(1, n_games+1):
        print("Game {}:".format(game))
        hands = deal(n_players, n_cards)
        print("7-Card Hands Dealt:" + " "*30 +"Best 5-Card Combo:")
        best_combos = []
        for hand in hands:
            best_combo = best_hand(hand)
            print(hand, " ==> ", best_combo)
            best_combos.append(best_combo)
        winner = poker(best_combos)
        hand_type = hand_rank(winner[0])[0]
        if len(winner) > 1:
            print("\nWe have a {} way tie Winner! \n{}:\n{}\n".format(
                len(winner), hand_types[hand_type], winner))
        else:       
            print("\nWinner! \n{}:\n{}\n".format(
                hand_types[hand_type], winner))
        print("-"*60)

def main():
    '''
    Runs tests and simulate 5 card games.
    '''
    # Test cases for best combination in 7-card-stud
    test_best_hand()
    # Simulate 5 games of 7-card stud with 7 players in each game
    games()
    
if __name__ == "__main__":
    main()
