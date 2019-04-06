'''
'''
from __future__ import absolute_import, division, print_function
import unittest
import logging

from lib.const_poker import *
from lib.deck import Deck, Card
from lib.texas_holdem import CommunityCards, Hand, HandEvaluator, Game, Player


class StandardDeckPropertiesTest(unittest.TestCase):

    def setUp(self):
        self.shuffled_deck = Deck(SUITS, RANKS, shuffled=True)
        self.unshuffled_deck = Deck(SUITS, RANKS, shuffled=False)

    def test_count_deck(self):
        self.assertEqual(len(self.shuffled_deck.deck), 52)

    def test_count_kings(self):
        self.assertEqual(len([card for card in self.shuffled_deck.deck if card.rank == 'K']), 4)

    def test_count_spades(self):
        self.assertEqual(len([card for card in self.shuffled_deck.deck if card.suit == 'S']), 13)

class HandEvaluatorTest(unittest.TestCase):

    def setUp(self):
        ''' set up a variety of hands and community cards manually for testing
        '''
        self.deck = Deck(SUITS, RANKS)
        self.hand = Hand(
                self.deck.deal(), 
                self.deck.deal())
        self.community_cards = CommunityCards(
                self.deck.deal(), 
                self.deck.deal(), 
                self.deck.deal(), 
                self.deck.deal(), 
                self.deck.deal())
        self.hand_straight = Hand(
                Card('A', 'S'), 
                Card('K', 'S'))
        self.cc_straight = CommunityCards(
                Card('Q', 'S'), 
                Card('3', 'H'),
                Card('J', 'S'), 
                Card('T', 'S'),
                Card('9', 'S'))

        self.straight_hand_eval = HandEvaluator(self.hand_straight, self.cc_straight)

    def test_is_flush(self):
        pass

    def test_is_straight(self):
        self.assertTrue(self.straight_hand_eval.eval_straight()[0])

    def test_straight_rank(self):
        ''' test report rank of a six or seven card straight correctly
        '''
        self.assertEqual(self.straight_hand_eval.eval_straight(), (True, 'A'))


class PokerGameTest(unittest.TestCase):

    def setUp(self):
        ''' set up a variety of hands and community cards manually for testing
        '''
        deck = Deck(SUITS, RANKS, shuffled=True)

        players = list()
        player_number = 2
        for i in range(player_number):
            players.append(Player(name=str(i), chips=1500))

        self.game = Game(deck, players)

    def test_assign_dealer(self):
        self.assertIsNone(self.game.dealer, None)
        self.game.select_dealer()
        self.assertIsInstance(self.game.dealer, Player)

    '''
    def count_deal(self):
        game.deal
    '''
