'''
'''
from __future__ import absolute_import, division, print_function
import unittest
import logging

from lib.const_poker import *
from lib.deck import Deck, Card
from lib.texas_holdem import CommunityCards, Hand, HandEvaluator


logging.basicConfig(filename='debug.log',level=logging.DEBUG)
    

if __name__ == '__main__':
    '''
    '''
    from tests.poker_tests import HandEvaluatorTest, StandardDeckPropertiesTest

    shuffled_deck = Deck(SUITS, RANKS)
    unshuffled_deck = Deck(SUITS, RANKS, shuffled=False)

    hand = Hand(
            shuffled_deck.deal(), 
            shuffled_deck.deal())
    community_cards = CommunityCards(
            shuffled_deck.deal(), 
            shuffled_deck.deal(), 
            shuffled_deck.deal(), 
            shuffled_deck.deal(), 
            shuffled_deck.deal())
    hand_evaluator_object = HandEvaluator(hand, community_cards)

    print("Hand: {}".format(hand))
    print("Community Cards: {}".format(community_cards))
    print("Hand Evaluator Cards: {}".format(hand_evaluator_object))

    hand_evaluator_object.order_cards()
    print("Hand Evaluator Cards: {}".format(hand_evaluator_object))
    print("The hand has a straight? {}".format(hand_evaluator_object.eval_straight()))

    hand_evaluator_object.eval_straight()

    unittest.main(verbosity=2)
    

