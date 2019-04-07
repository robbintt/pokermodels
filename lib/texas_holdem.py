'''
'''
import random
import logging
import collections

from lib.poker_const import *

class Hand(object):

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


class CommunityCards(object):

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

class Player(object):
    ''' Stub for naming players, for now
    '''
    def __init__(self, name=None, chips=0, cards=None):
        self.name = name
        self.chips = chips
        if cards:
            self.cards = cards
        else:
            self.cards = list()

    def __str__(self):
        return "Player {}: {} chips.".format(self.name, self.chips)

class GameController(object):
    ''' Game controller manages the table, players, and chips

    This multi-Game module isn't on the roadmap at the moment.
    
    I am most interested in using the Game abstraction for stats.

    If I wanted to run strategy simulations, I would use this game controller.

    The controller could be used to play a table for awhile, replay different 
    game scenarios at key branch points, etc.

    The controller could also be the gateway for an API for multiplayer games.
    '''
    pass


class Game(object):
    ''' Play a game of poker with no bets

    This can be used to calculate preflop odds on n-way-hands

    deck is a Deck() object, typically Deck(SUITS, RANKS, shuffled=True)
    give players as a list of  player objects, which is converted for rotate()

    NOTES:
    - This module DOES NOT randomize the players list. Do that separately.
    '''
    def __init__(self, deck, players):
        self.deck = deck
        self.muck = list()
        self.players = collections.deque(players)
        self.button = None

    def select_button(self):
        self.button = self.players[-1]
        logging.debug("Player {} is button.".format(str(self.button.name)))

    def update_button(self):
        self.players.rotate(-1)  # rotate(-1) will rotate player 1 to last position
        self.button = self.players[-1]
        logging.debug("Player {} is button.".format(str(self.button.name)))

    def burn_card(self):
        ''' Add a card to the muck

        This is done before the flop, turn, river for three total burns.
        '''
        self.muck.append(self.deck.deal())

    def deal_hands(self):
        ''' Deal cards to each player in two rounds.

        dealing order is sb->bb->...->button
        
        - The small blind is self.players[0]
        - The big blind is self.players[1]
        - The button is self.players[-1]
        '''
        for player in self.players:
            player.cards.append(self.deck.deal())
        for player in self.players:
            player.cards.append(self.deck.deal())


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

    def order_cards(self):
        self.cards.sort(key=lambda card: RANK_ORDER[card.rank]) 

    def eval_flush(self):
        '''
        '''
        pass

    def eval_royalflush(self):
        pass

    def eval_straightflush(self):
        ''' should royal flush be evaluated here?
        '''
        pass

    def eval_straight(self):
        ''' Use combinatorics to evaluate if there's a straight
        '''
        STRAIGHT_RANKS = ['A'] + list(RANKS)
        STRAIGHT = 5
        has_straight = (False, None)
        possible_straights = [STRAIGHT_RANKS[a:a+STRAIGHT] for a in range(len(STRAIGHT_RANKS)-STRAIGHT+1)]

        self.order_cards()
        hand_ranks = list(set([card.rank for card in self.cards]))
        hand_ranks.sort(key=lambda card: RANK_ORDER[card])
        possible_hands = [hand_ranks[a:a+STRAIGHT] for a in range(len(hand_ranks)-STRAIGHT+1)]

        for s in possible_straights:
            for h in possible_hands:
                if s == h:
                    has_straight = (True, s[-1])

        return has_straight

    def eval_fullhouse(self):
        ''' how does this match up with fullhouse, 4-kind, 3-kind, 2-pair, 2-kind
        '''
        pass

    def eval_4kind(self):
        ''' how does this match up with fullhouse, 4-kind, 3-kind, 2-pair, 2-kind
        '''
        pass

    def eval_3kind(self):
        ''' how does this match up with fullhouse, 4-kind, 3-kind, 2-pair, pair
        '''
        pass

    def eval_2pair(self):
        ''' how does this match up with fullhouse, 4-kind, 3-kind, 2-pair, pair
        '''
        pass

    def eval_pair(self):
        ''' how does this match up with fullhouse, 4-kind, 3-kind, 2-pair, pair
        '''
        pass

    def eval_highcard(self):
        ''' how does this match up with fullhouse, 4-kind, 3-kind, 2-pair, pair
        '''
        pass

    def eval_leftovers(self):
        ''' based on the number of cards in the hand, fill remaining slots with high card

        generally used to solve ties, relevant for 4p and down
        '''

    def __str__(self):
        return " ".join([str(card) for card in self.cards])


def HandCompare(self):
    ''' Given two equal hands, determine who wins

    We need to differentiate between private cards here which is kind of funky in the context of hand construction

    relevant for: 3-kind, 2-pair, pair, highcard
    also matters for: straight, 
    simple for: straightflush (only 2 players will ever have a straightflush, 1 would have highcard, the other lowcard)
    very simple for flush, since highest card in the flush wins (flush consumes all 5 slots)
    '''



