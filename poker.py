'''
'''
from __future__ import absolute_import, division, print_function
import unittest
import logging

from lib.poker_const import *
from lib.deck import Deck, Card
from lib.texas_holdem import CommunityCards, Hand, HandConstructor, Game, Player


logging.basicConfig(filename='logs/debug.log',level=logging.DEBUG)
    

if __name__ == '__main__':
    '''
    '''
    from tests.poker_tests import HandConstructorTest, StandardDeckPropertiesTest, PokerGameTest, KindHandConstructorTest

    unittest.main(verbosity=2)
    

