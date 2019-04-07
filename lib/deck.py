''' Standard Card and Deck abstractions
'''
import random

class Card(object):
    '''

    equality operators from StackOverflow: 
    https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes
    '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return("{}{}".format(self.rank, self.suit))

    def __eq__(self, other_card):
        if isinstance(self, type(other_card)):
            return self.__dict__ == other_card.__dict__
        return NotImplemented

    def __ne__(self, other_card):
        ''' deprecated in python 3, because this is the default python3 __ne__ behavior
        '''
        res = self.__eq__(other_card)
        if res is NotImplemented:
            return res
        else:
            return not res

    def __hash__(self):
        ''' supports set operations
        '''
        return hash(tuple(sorted(self.__dict__.items())))
        

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
