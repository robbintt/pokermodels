'''
'''
import random
import logging
import collections

from lib.poker_const import *

logging.basicConfig(filename='logs/debug.log',level=logging.DEBUG)

class Hand(object):
    '''
    '''
    def __init__(self, card1=None, card2=None):
        self.card1 = card1
        self.card2 = card2
        
    @property
    def cards(self):
        ''' return a list of cards for evaluation... don't destroy the cards!
        '''
        return [self.card1, self.card2]

    def __str__(self):
        return " ".join([str(card) for card in self.cards])

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


class CommunityCards(object):

    def __init__(self, card1=None, card2=None, card3=None, card4=None, card5=None):
        self.card1 = card1
        self.card2 = card2
        self.card3 = card3
        self.card4 = card4
        self.card5 = card5

    @property
    def cards(self):
        ''' return a list of cards for evaluation... don't destroy the cards!
        '''
        return [self.card1, self.card2, self.card3, self.card4, self.card5]

    def __str__(self):
        return " ".join([str(card) for card in self.cards])

class Player(object):
    '''
    '''
    def __init__(self, name=None, chips=0, hand=None):
        self.name = name
        self.chips = chips
        if hand:
            self.hand = hand 
        else:
            self.hand = Hand()

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
        self.community_cards = CommunityCards()
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
            player.hand.card1 = self.deck.deal()
        for player in self.players:
            player.hand.card2 = self.deck.deal()

    def deal_flop(self):
        self.burn_card()
        self.community_cards.card1 = self.deck.deal()
        self.community_cards.card2 = self.deck.deal()
        self.community_cards.card3 = self.deck.deal()

    def deal_turn(self):
        self.burn_card()
        self.community_cards.card4 = self.deck.deal()

    def deal_river(self):
        self.burn_card()
        self.community_cards.card5 = self.deck.deal()


class HandConstructor(object):
    ''' Construct the best hand

    If there's a flush, flag it as available so you can skip some lower evaluation
    ==========================================
        - check just the flush cards for a straight to improve the hand
        - check if any straight flushes are royal flush (technically named differently)
        - check for straights if there is no flush

    If it's '4 of a kind', stop evaluating (nothing else fits)
        - select 1 kicker
    ==========================================

    Flow down from full house to high card...
    ==========================================
    If three of a kind
        - check remainder for a pair - that's a full house
        - else get 2 kickers
    if two of a kind, 
        - check remainder for a pair - that's two pair
            - get the kicker to fill the hand
        - else get 3 kickers
    finally select high card
        - select 4 kickers to construct the hand

    ===

    There is a degenerate nomenclature for hands

    Royal Flush
    Straight Flush, 
        - King High
    4 of a kind Aces
        - King Kicker
    Full House, Tens over Twos, Tens over Threes, Aces over Tens
        - compare three of a kind
        - compare two of a kind
    Flush
        - compare down the flush
    Straight, 5 High
        - compare down the straight
    Three of a Kind, Aces
        - two kickers!!
    Two pair, Aces over threes, kicker
        - high pair
        - then low pair
        - then kicker
    Pair
        - three kickers
    High Card
        - Four kickers

    community_cards = a container of 5 cards
    hand = a container of 2 cards

    get the class of hand and rank of class
    e.g. ('flush', '13') - ace high flush
    write a little scoring matrix from low to high that can be enumerated
    identify each score that can be made from the five cards and keep the highest
    or test each from the top and keep the first one you get

    FUTURE:
    - evaluate all possible hands then use a comparison tool to select the best
    - evaluate potential hands from an incomplete community_cards
    '''
    def __init__(self, hand, community_cards):
        self.hand = hand
        self.community_cards = community_cards
        self.cards = self.hand.cards + self.community_cards.cards

        self.best_hand = list()
        self.best_hand_name = None #  see WINNING_HANDS

        self.rank_tally = list()
        self.suit_tally = list()

    def order_ranks(self):
        self.cards.sort(key=lambda card: RANK_ORDER[card.rank]) 
        logging.debug('by rank: {}'.format(str(self)))

    def order_suits(self):
        self.cards.sort(key=lambda card: card.suit) 
        #logging.debug(str(self))

    def tally_ranks(self):
        ''' reset rank_tally and perform tally
        '''
        self.rank_tally = {rank: 0 for rank in RANKS}
        for card in self.cards:
            self.rank_tally[card.rank] += 1
        #logging.debug(str(self))
        #logging.debug('rank tally: {}'.format(self.rank_tally))

    def tally_suits(self):
        ''' reset suit_tally and perform tally
        '''
        self.suit_tally = {suit: 0 for suit in SUIT}
        for card in self.cards:
            self.suit_tally[card.suit] += 1
        logging.debug(str(self))
        logging.debug('suit tally: {}'.format(self.suit_tally))

    def eval_hand(self):
        ''' Run each evaluation in order

        1. eval_flush
            a. run eval_straight if there are 5-7 cards in 1 suit
        2. eval_straight
        3. eval_kinds

        After each eval is run, if best_hand is populated then no further evals are run.
        This is a cascading system and I'm not a huge fan.
        I would like to replace this with a DSL for evaluation using a parser.
        '''
        self.eval_flush()  # does eval for straightflush
        if not self.best_hand:
            self.eval_straight()
        if not self.best_hand:
            self.eval_kinds()
        if not self.best_hand:
            logging.debug("How did you get here?")
            raise

    def eval_flush(self):
        ''' Evaluate if there's a flush.

        This method also evaluates for straight flush inside the superset of flush cards (5 to 7 suited cards)
        '''
        self.tally_suits()
        for suit, tally in self.suit_tally:
            if tally >= 5:
                flush_cards = [card for card in self.cards if card.suit == suit]
            if len(flush_cards) > 5:
                flush_cards.sort(key=lambda card: RANK_ORDER[card.rank]) 
                flush_cards.reverse()  # higher ranks go first

                # this is tricky, because eval_straight goes to the parent object by default
                # can either give those as default kwargs in eval_straight and
                # could have eval_straight return its result and do assignment in another controller...
                # what will the overall controller look like?
                if eval_straight(flush_cards):
                    # TODO this could be cleaner... i don't think i will be assigning these here? not sure...
                    # ideally the hand names are generated from the best hands with a parser...
                    self.best_hand_name = 'StraightFlush'  # needs corrected from eval_straight
                else:
                    self.best_hand_name = 'Flush'
                    self.best_hand = flush_cards[:5]  # use the top 5
                # evaluate if it's a straight, if so return as straight flush...
                # if not, return it as flush
                # this will miss if there's a lower straightflush and a higher non-straight flush...
                # FIX ME: what if we evaluate the long flush for straights?
                # this affects my control flow, as the eval_straight is not made to be reused currently

    def eval_straight(self, cards=None):
        ''' Use combinatorics to evaluate if there's a straight

        This could be used on the full hand or just the flush containing subset...
        Then straightflush is just a natural outcome of eval_straight on the result of eval_flush

        Sets the best_hand to the highest straight
        '''
        if not cards:
            cards = self.cards
        STRAIGHT_RANKS = ['A'] + list(RANKS)
        STRAIGHT = 5
        has_straight = False
        possible_straights = [STRAIGHT_RANKS[a:a+STRAIGHT] for a in range(len(STRAIGHT_RANKS)-STRAIGHT+1)]

        self.order_ranks()
        hand_ranks = list(set([card.rank for card in cards]))
        hand_ranks.sort(key=lambda card: RANK_ORDER[card])
        possible_hands = [hand_ranks[a:a+STRAIGHT] for a in range(len(hand_ranks)-STRAIGHT+1)]

        # TODO we just need to compare this once, but this checks every hand in possible_hands against 
        #     every straight in possible straights
        # but it doesn't break the logic as long as the highest hand is tested last in possible_hands
        for s in possible_straights:
            # keeps the last tested self.best_hand, relies on order of possible_hands
            for h in possible_hands:
                if s == h:
                    has_straight = True
                    self.best_hand_name = 'Straight'
                    self.best_hand = h
        return has_straight  # logic used by flush_eval()

    def get_high_card(self, remaining_cards):
        remaining_cards.sort(key=lambda card: RANK_ORDER[card.rank])
        remaining_cards.reverse()
        logging.debug('remaining by rank: {}'.format([str(card) for card in remaining_cards]))
        return remaining_cards[0], remaining_cards[1:]

    def eval_kinds(self):
        ''' evaluate kinds including full house, flow through complete hand construction

        all non-kind hands are complete hands and do not need 'rounding off' with kickers
        although the high card selection process for a suited group forming a flush
        or a long straight are analogous...
        '''
        self.tally_ranks()
        rank_tally_list = [(tally, rank) for rank, tally in self.rank_tally.iteritems()]
        logging.debug(rank_tally_list)
        remaining_cards = list()
        # sort by rank and then by instance, so 3 aces will always occur after 3 kings
        # this will allow a full house to be properly ordered as AAAKK or "aces full of kings"
        rank_tally_list.sort(key=lambda vals: (vals[0], RANK_ORDER[vals[1]]))
        rank_tally_list.reverse() # traverse higher kinds first
        logging.debug(rank_tally_list)

        for tally, rank in rank_tally_list:
            if tally == 4:
                for card in self.cards:
                    if card.rank == rank and len(self.best_hand) < 5:
                        self.best_hand.append(card)
                    else:
                        remaining_cards.append(card)
                    self.best_hand_name = 'FourofaKind'

                logging.debug(remaining_cards)
                high_card, remaining_cards = self.get_high_card(remaining_cards)
                self.best_hand.append(high_card)  # result is stored in self.best_hand
                return

            if tally == 3:
                # this catches a AAATTT or similar situation to ensure the tally is AAATT
                # it will not fail in the fail case AAATTTQQ since that's 1 too many cards for holdem
                self.best_hand_name = 'ThreeofaKind'  # TODO hacky... FH overrides on best_hand completion
                for card in self.cards:
                    if card.rank == rank and len(self.best_hand) < 5:
                        self.best_hand.append(card)
                        if len(self.best_hand) == 5:
                            self.best_hand_name = 'FullHouse' # TODO this is pretty ugly detection
                    else:
                        remaining_cards.append(card)
                if len(self.best_hand) == 5:
                    # i guess you can get here if you've got AAAKTTT
                    return

            if tally == 2:
                # will tally == 2 catch a AATT66K situation? The best hand is AATTK
                # to do so it must back off after 4 cards
                if len(self.best_hand) < 4:
                    self.best_hand_name = 'Pair' # TODO this works since FH would be 5 cards
                    for card in self.cards:
                        if card.rank == rank:
                            self.best_hand.append(card)
                            if len(self.best_hand) == 4:
                                self.best_hand_name = 'TwoPair' # TODO this works since FH would be 5 cards
                            elif len(self.best_hand) == 5:
                                self.best_hand_name = 'FullHouse' # TODO this works since FH would be 5 cards
                        else:
                            remaining_cards.append(card)
                # kicker is part of a third, smaller pair
                elif len(self.best_hand) == 4:
                    # don't change self.best_hand_name here, it's already been assigned
                    high_card, remaining_cards = self.get_high_card(remaining_cards)
                    self.best_hand.append(high_card)  # result is self.best_hand
                    return

            # this shouldn't be necessary, all higher hands should have a return above
            # in general this style of flowing exits is trash, but it's quick too
            if not self.best_hand_name:
                self.best_hand_name = 'HighCard'  # TODO only assign high card if its empty
            if tally == 1:
                if len(self.best_hand) < 5:
                    # guaranteed to be the highest card left
                    for card in self.cards:
                        if card.rank == rank:
                            self.best_hand.append(card)
                            if len(self.best_hand) == 5:
                                return
                        else:
                            pass # continue loop
                # shouldn't get here with a full hand anyways
                else:
                    logging.debug("How did you get here?")
                    raise
                    return # raise should not be handled anyways

    def __str__(self):
        return " ".join([str(card) for card in self.cards])


def HandCompare(self):
    ''' Given a list of equal hands, determine who wins

    Will this re-evaluate each player's best_hand or will it take the best_hand_name and kickers?

    We need to differentiate between private cards here which is kind of funky in the context of hand construction

    relevant for: 3-kind, 2-pair, pair, highcard
    also matters for: straight, 
    simple for: straightflush (only 2 players will ever have a straightflush, 1 would have highcard, the other lowcard)
    very simple for flush, since highest card in the flush wins (flush consumes all 5 slots)
    '''



