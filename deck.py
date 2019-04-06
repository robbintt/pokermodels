''' Standard Card and Deck abstractions
'''
import random

class Card(object):
    '''
    '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return("{}{}".format(self.rank, self.suit))

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
        self.deck = [Card(r, s) for s in self.suits for r in self.ranks]
        if self.shuffled:
            self.shuffle()

    def deal(self):
        return self.deck.pop()

    def shuffle(self):
        random.shuffle(self.deck)
