'''
'''
from __future__ import absolute_import, division, print_function
import unittest
import logging

from lib.poker_const import *
from lib.deck import Deck, Card
from lib.texas_holdem import CommunityCards, Hand, HandConstructor, Game, Player


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

class KindHandConstructorTest(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = None
        pass

    def test_kindhand_4kind(self):
        self.hand = Hand(
                Card('5', 'S'), 
                Card('5', 'C'))
        self.cc = CommunityCards(
                Card('K', 'S'), 
                Card('5', 'H'),
                Card('J', 'D'), 
                Card('5', 'D'),
                Card('2', 'S'))

        self.hand_eval = HandConstructor(self.hand, self.cc)
        self.hand_eval.eval_kinds()
        the_best_hand = [
                Card('5', 'H'), 
                Card('5', 'D'),
                Card('5', 'S'), 
                Card('5', 'C'),
                Card('K', 'S')]

        logging.debug([str(card) for card in self.hand_eval.best_hand])
        self.assertItemsEqual(self.hand_eval.best_hand, the_best_hand)


    def test_kindhand_highcard(self):
        self.hand = Hand(
                Card('5', 'S'), 
                Card('6', 'C'))
        self.cc = CommunityCards(
                Card('K', 'S'), 
                Card('9', 'H'),
                Card('J', 'D'), 
                Card('T', 'D'),
                Card('2', 'S'))

        self.hand_eval = HandConstructor(self.hand, self.cc)
        self.hand_eval.eval_kinds()
        the_best_hand = [
                Card('K', 'S'), 
                Card('J', 'D'),
                Card('T', 'D'), 
                Card('9', 'H'),
                Card('6', 'C')]

        logging.debug([str(card) for card in self.hand_eval.best_hand])
        self.assertItemsEqual(self.hand_eval.best_hand, the_best_hand)


    def test_kindhand_2p(self):
        self.hand = Hand(
                Card('5', 'S'), 
                Card('K', 'C'))
        self.cc = CommunityCards(
                Card('K', 'S'), 
                Card('5', 'H'),
                Card('J', 'D'), 
                Card('T', 'C'),
                Card('8', 'S'))

        self.hand_eval = HandConstructor(self.hand, self.cc)
        self.hand_eval.eval_kinds()
        the_best_hand = [
                Card('5', 'S'), 
                Card('K', 'C'),
                Card('K', 'S'), 
                Card('5', 'H'),
                Card('J', 'D')]
        self.assertItemsEqual(self.hand_eval.best_hand, the_best_hand)
        logging.debug([str(card) for card in self.hand_eval.best_hand])

    def test_kindhand_3(self):
        self.hand = Hand(
                Card('5', 'S'), 
                Card('5', 'C'))
        self.cc = CommunityCards(
                Card('K', 'S'), 
                Card('5', 'H'),
                Card('J', 'D'), 
                Card('T', 'C'),
                Card('8', 'S'))

        self.hand_eval = HandConstructor(self.hand, self.cc)
        self.hand_eval.eval_kinds()
        the_best_hand = [
                Card('5', 'S'), 
                Card('5', 'C'),
                Card('K', 'S'), 
                Card('5', 'H'),
                Card('J', 'D')]
        self.assertItemsEqual(self.hand_eval.best_hand, the_best_hand)
        logging.debug([str(card) for card in self.hand_eval.best_hand])

class HandConstructorTest(unittest.TestCase):

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
        self.hand_flush = Hand(
                Card('T', 'S'), 
                Card('3', 'S'))
        self.cc_flush = CommunityCards(
                Card('4', 'S'), 
                Card('7', 'H'),
                Card('9', 'S'), 
                Card('J', 'S'),
                Card('K', 'S'))

        self.straight_hand_eval = HandConstructor(self.hand_straight, self.cc_straight)
        self.flush_hand_eval = HandConstructor(self.hand_flush, self.cc_flush)

    def test_is_flush(self):
        ''' no test yet
        '''
        pass

    def test_order_suits(self):
        ''' no test yet
        '''
        self.flush_hand_eval.order_suits()

    def test_tally_ranks(self):
        ''' no test yet
        '''
        self.flush_hand_eval.tally_ranks()

    def test_eval_3kind(self):
        '''
        '''
        self.flush_hand_eval.eval_kinds()

    def test_is_straight(self):
        self.assertTrue(self.straight_hand_eval.eval_straight()[0])

    def test_straight_rank(self):
        ''' test report rank of a six or seven card straight correctly
        '''
        # TODO: i may have changed the input data and screwed this up... when verified remove this comment 
        self.assertEqual(self.straight_hand_eval.eval_straight(), (True, 'A'))


class PokerGameTest(unittest.TestCase):

    def setUp(self):
        ''' set up a variety of hands and community cards manually for testing
        '''
        deck = Deck(SUITS, RANKS, shuffled=True)
        players = list()
        self.player_number = 2
        for i in range(self.player_number):
            players.append(Player(name=str(i), chips=1500))

        self.player_1 = players[0]
        self.player_2 = players[1]  # initially the button, aka players[-1]

        self.game = Game(deck, players)
        self.cards_left_in_deck = len(self.game.deck.deck)

    def test_select_button(self):
        self.assertIsNone(self.game.button, None)
        self.game.select_button()
        #self.assertIsInstance(self.game.button, Player)
        self.assertEqual(self.game.button, self.player_2)

    def test_update_button(self):
        self.game.update_button()
        self.assertEqual(self.game.button, self.player_1)

    def test_deal_hands(self):
        self.game.deal_hands()
        self.cards_left_in_deck -= 2 * len(self.game.players)
        self.assertEqual(len(self.game.deck.deck), self.cards_left_in_deck)

    def test_burn_card(self):
        self.game.burn_card()
        self.cards_left_in_deck -= 1
        self.assertEqual(len(self.game.deck.deck), self.cards_left_in_deck)

    def test_deal_flop(self):
        self.game.deal_flop()
        self.cards_left_in_deck -= 4
        self.assertEqual(len(self.game.deck.deck), self.cards_left_in_deck)
        self.assertIs(self.game.community_cards.card1, self.game.community_cards.cards[0])
        self.assertIs(self.game.community_cards.card2, self.game.community_cards.cards[1])
        self.assertIs(self.game.community_cards.card3, self.game.community_cards.cards[2])
        self.assertIsNone(self.game.community_cards.card4)
        self.assertIsNone(self.game.community_cards.card5)

    def test_deal_turn(self):
        self.game.deal_turn()
        self.cards_left_in_deck -= 2
        self.assertEqual(len(self.game.deck.deck), self.cards_left_in_deck)
        self.assertIs(self.game.community_cards.card1, self.game.community_cards.cards[0])
        self.assertIs(self.game.community_cards.card2, self.game.community_cards.cards[1])
        self.assertIs(self.game.community_cards.card3, self.game.community_cards.cards[2])
        self.assertIs(self.game.community_cards.card4, self.game.community_cards.cards[3])
        self.assertIsNone(self.game.community_cards.card5)

    def test_deal_river(self):
        self.game.deal_river()
        self.cards_left_in_deck -= 2
        self.assertEqual(len(self.game.deck.deck), self.cards_left_in_deck)
        self.assertIs(self.game.community_cards.card1, self.game.community_cards.cards[0])
        self.assertIs(self.game.community_cards.card2, self.game.community_cards.cards[1])
        self.assertIs(self.game.community_cards.card3, self.game.community_cards.cards[2])
        self.assertIs(self.game.community_cards.card4, self.game.community_cards.cards[3])
        self.assertIs(self.game.community_cards.card5, self.game.community_cards.cards[4])
