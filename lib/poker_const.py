''' Constants for Poker
'''

SUITS = ('S', 'C', 'H', 'D')
RANKS = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')

WINNING_HANDS = (
    'HighCard',
    'Pair',
    'TwoPair',
    'ThreeofaKind',
    'Straight',
    'Flush',
    'FullHouse',
    'FourofaKind',
    'StraightFlush',
    'RoyalFlush'
)


RANK_ORDER = {rank: score for score, rank in enumerate(RANKS)}
WINNING_HAND_ORDER = {hand: score for score, hand in enumerate(WINNING_HANDS)}


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
    'T' : 'ten',
    'J' : 'jack',
    'Q' : 'queen',
    'K' : 'king',
    'A' : 'ace'
}
