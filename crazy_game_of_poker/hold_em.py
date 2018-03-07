#!/usr/bin/env python3
'''
Texas Hold em
'''
import random
from utils7card import *

hand_types = {
    9:"Straight flush!", 7:"4 of a kind!",
    6:"Full house", 5:"Flush", 4:"Straight",
    3:"3 of a kind", 2:"2 pair", 
    1:"1 pair", 0:"High card"
}

def communal_cards(remaining_deck):
    flop = remaining_deck[1:4]
    # burn = [remaining_deck[0]] + remaining_deck[4:7:2]
    turn = remaining_deck[5:8:2] 
    return flop + turn 

def deal_holdem(numhands, n=2, deck=deck):
    '''
    Deal `numhands` of `n` cards from a shuffled `deck`
    Return a list of unique hands, and list of the communal cards.
    '''
    # check to see there are enough cards in the deck 
    # to deal `numhands` 
    # for hold_em, 8 extra cards needed for flop, burn & turn
    assert (len(deck)//n + 8) >= numhands
    # shuffle deck in place
    random.shuffle(deck)
    hands = [deck[i:i+n] for i in range(0, n*numhands, n)]
    communal = communal_cards(deck[n*numhands:])
    return hands, communal

def games(n_games=5, n_players=10, n_cards=2):
    '''
    Simulate `n_games` of `n_card` stud with `n_players` in each game
    '''
    for game in range(1, n_games+1):
        print("Game {}:".format(game))
        hands, communal = deal_holdem(n_players, n_cards)
        print("Communal Cards: {} \n".format(communal))
        print("Hold-em Hands:" + " "*15 + "Best 5-Card Combo:")
        best_combos = []
        for hand in hands:
            best_combo = best_hand(hand + communal)
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
    # Simulate 5 games of Texas hold-em with 10 players in each game
    games()
    
if __name__ == "__main__":
    main()
