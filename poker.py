'''
'''
import unittest
import random
import logging

from poker_constants import SUITS, RANKS, WINNING_HANDS, RANK_ORDER, WINNING_HAND_ORDER, SUIT_NAMES, RANK_NAMES
from deck import Deck, Card

logging.basicConfig(filename='debug.log',level=logging.DEBUG)



    
class TexasHoldemHand(object):

    def __init__(self, card1=None, card2=None):
        self.card1 = card1
        self.card2 = card2

    @property
    def suited(self):
        if self.card1.suit == self.card2.suit:
            return True
        else: 
            return False

    @property
    def suited_str(self):
        if self.card1.suit == self.card2.suit:
            return 's'
        else: 
            return 'o'

    @property
    def cards(self):
        ''' return a list of cards for evaluation... don't destroy the cards!
        '''
        return [self.card1, self.card2]

    def __str__(self):
        return("{}{}-{}{} : {}{}{}".format(
            self.card1.rank, self.card1.suit, 
            self.card2.rank, self.card2.suit,
            self.card1.rank, self.card2.rank, self.suited_str))


class TexasHoldemCommunityCards(object):

    def __init__(self, card1=None, card2=None, card3=None, card4=None, card5=None):
        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
        self.card4 = card4
        self.card5 = card5

    @property
    def suitedness(self):
        if self.card1.suit == self.card2.suit:
            return True
        else: 
            return False

    @property
    def cards(self):
        ''' return a list of cards for evaluation... don't destroy the cards!
        '''
        return [self.card1, self.card2, self.card3, self.card4, self.card5]

    def __str__(self):
        card_string_template = "{}{} " * 5
        return(card_string_template.format(
            self.card1.rank, self.card1.suit, 
            self.card2.rank, self.card2.suit,
            self.card3.rank, self.card3.suit,
            self.card4.rank, self.card4.suit,
            self.card5.rank, self.card5.suit))

class HandEvaluator(object):
    ''' Build and evaluate a hand, and score it

    community_cards = a container of 5 cards
    hand = a container of 2 cards

    get the class of hand and rank of class
    e.g. ('flush', '13') - ace high flush
    write a little scoring matrix from low to high that can be enumerated
    identify each score that can be made from the five cards and keep the highest
    or test each from the top and keep the first one you get
    '''
    def __init__(self, hand, community_cards):
        self.hand = hand
        self.community_cards = community_cards
        self.cards = self.hand.cards + self.community_cards.cards

    def eval_flush(self):
        for card in self.cards:
            pass

    def order_cards(self):
        self.cards.sort(key=lambda card: RANK_ORDER[card.rank]) 

    def eval_straight(self):
        ''' Use combinatorics to evaluate if there's a straight
        '''
        STRAIGHT_RANKS = ['A'] + list(RANKS)
        STRAIGHT = 5
        has_straight = (False, None)
        possible_straights = [STRAIGHT_RANKS[a:a+STRAIGHT] for a in range(len(STRAIGHT_RANKS)-STRAIGHT+1)]
        logging.debug(possible_straights)

        logging.debug(str(self))
        self.order_cards()
        logging.debug(str(self))
        hand_ranks = list(set([card.rank for card in self.cards]))
        hand_ranks.sort(key=lambda card: RANK_ORDER[card])
        possible_hands = [hand_ranks[a:a+STRAIGHT] for a in range(len(hand_ranks)-STRAIGHT+1)]

        logging.debug("Asking if there is a straight in {}".format(possible_hands))
        for s in possible_straights:
            logging.debug("test if we have each straight: {}".format(s))
            for h in possible_hands:
                if s == h:
                    has_straight = (True, s[-1])
                    logging.debug("straight found; {} high: {} is in {}".format(has_straight[1], s, possible_hands))

        return has_straight


    def __str__(self):
        return " ".join([str(card) for card in self.cards])


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
        # random
        self.deck = Deck(SUITS, RANKS)
        self.hand = TexasHoldemHand(
                self.deck.deal(), 
                self.deck.deal())
        self.community_cards = TexasHoldemCommunityCards(
                self.deck.deal(), 
                self.deck.deal(), 
                self.deck.deal(), 
                self.deck.deal(), 
                self.deck.deal())
        self.hand_straight = TexasHoldemHand(
                Card('A', 'S'), 
                Card('K', 'S'))
        self.cc_straight = TexasHoldemCommunityCards(
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



if __name__ == '__main__':
    '''
    '''
    shuffled_deck = Deck(SUITS, RANKS)
    unshuffled_deck = Deck(SUITS, RANKS, shuffled=False)

    hand = TexasHoldemHand(
            shuffled_deck.deal(), 
            shuffled_deck.deal())
    community_cards = TexasHoldemCommunityCards(
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
    

