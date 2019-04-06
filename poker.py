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

    unittest.main(verbosity=2)
    

