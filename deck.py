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


class Card(object):
    '''
    '''
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    

class Deck(object):
    '''
    '''

    def __init__(self, suits, ranks, shuffled=True):
        '''
        '''
        self.suits = suits
        self.ranks = ranks
        self.shuffled = shuffled
        self.deck = [Card(s, r) for s in self.suits for r in self.ranks]
        if self.shuffled:
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
    def suitedness(self):
        if self.card1.suit == self.card2.suit:
            return True
        else: 
            return False


if __name__ == '__main__':
    '''
    '''
    print("Unshuffled", ["{}{}".format(card.suit, card.rank) for card in Deck(SUITS, RANKS, shuffled=False).deck])
    print("Shuffled", ["{}{}".format(card.suit, card.rank) for card in Deck(SUITS, RANKS, shuffled=True).deck])
    unittest.main()
    

