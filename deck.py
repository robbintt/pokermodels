'''
'''
import unittest
import random


SUITS = ('S', 'C', 'H', 'D')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

SUIT_NAMES = {
    'S': 'spades',
    'C': 'clubs',
    'H': 'hearts',
    'D': 'diamonds'
}

RANK_NAMES = {
    '2' : 'two',
    '3' : 'three',
    '4' : 'four',
    '5' : 'five',
    '6' : 'six',
    '7' : 'seven',
    '8' : 'eight',
    '9' : 'nine',
    '10' : 'ten',
    'J' : 'jack',
    'Q' : 'queen',
    'K' : 'king',
    'A' : 'ace'
}

HAND_RANKS = (
    'high_card',
    'pair',
    '2_pair',
    '3_kind',
    'straight',
    'flush',
    'full_house',
    '4_kind',
    'straight_flush',
    'royal_flush'
)

class Card(object):
    '''
    '''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    

class Deck(object):
    ''' Deck for dealing cards

    This deck only supports dealing from the top and shuffling.
    For the purposes of this deck, python list.pop() deals from the top.
    '''

    def __init__(self, suits, ranks, shuffled=True):
        '''
        '''
        self.suits = suits
        self.ranks = ranks
        self.shuffled = shuffled
        self.deck = [Card(s, r) for s in self.suits for r in self.ranks]
        if self.shuffled:
            self.shuffle()

    def deal(self):
        return self.deck.pop()

    def shuffle(self):
        random.shuffle(self.deck)

    
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
        self.all_cards = self.hand + self.community_cards

    STRAIGHT_ORDER = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    def eval_flush(self):
        for card in self.all_cards:
            pass

    def order_cards(self):
        sorted(self.all_cards, key=lambda card: card.rank) 


if __name__ == '__main__':
    '''
    '''
    shuffled_deck = Deck(SUITS, RANKS)
    unshuffled_deck = Deck(SUITS, RANKS, shuffled=False)

    print("Unshuffled", ["{}{}".format(card.suit, card.rank) for card in unshuffled_deck.deck])
    print("Shuffled", ["{}{}".format(card.suit, card.rank) for card in shuffled_deck.deck])

    hand = TexasHoldemHand(
            shuffled_deck.deal(), 
            shuffled_deck.deal())
    community_cards = TexasHoldemCommunityCards(
            shuffled_deck.deal(), 
            shuffled_deck.deal(), 
            shuffled_deck.deal(), 
            shuffled_deck.deal(), 
            shuffled_deck.deal())

    print("Hand: {}".format(hand))
    print("Community cards: {}".format(community_cards))

    unittest.main()
    

