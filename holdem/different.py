class DecisionType(object):
    FOLD = 0
    BET = 1

class Decision(object):
    def __init__(self, dec_type, value):
        self.dec_type = dec_type
        self.value = value

class Rank(object):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def elements(self):
        """Returns list of all elements of enum Rank"""
        return [x for x in range(2, 15)]

class Suit(object):
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

    def elements(self):
        """Returns list of all elements of enum Suit"""
        return [x for x in range(1, 5)]

class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

from random import randint
class Deck(object):
    def __init__(self, cards_count = 52):
        self.deck = []
        for i in range(1, cards_count + 1):
            self.deck.append(i)
    
    def pop_card(self):
        """Returns Card object taken randomly from a Deck"""
        card_no = randint(1, cards_count)
        card = self.deck[card_no]
        self.deck.remove(self.deck[card_no])
        cards_count -= 1
        rank = card % 14 + 1
        suit = card / 14 + 1
        return Card(rank, suit)







































