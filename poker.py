'''
'''
from __future__ import absolute_import, division, print_function
import unittest
import logging

from lib.poker_const import *
from lib.deck import Deck, Card
from lib.texas_holdem import CommunityCards, Hand, HandEvaluator, Game, Player


logging.basicConfig(filename='logs/debug.log',level=logging.DEBUG)
    

if __name__ == '__main__':
    '''
    '''
    from tests.poker_tests import HandEvaluatorTest, StandardDeckPropertiesTest, PokerGameTest

    unittest.main(verbosity=2)
    

