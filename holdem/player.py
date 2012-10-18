from random import randint
from holdem.different import Decision
from holdem.different import DecisionType

class Player(object):
    """
    Implementation of player abstraction.
    """
    def __init__(self, name, cash_amount, plid):
        self.name = name
        self.cash_amount = cash_amount
        self.plid = plid

class PlayerAtTable(object):
    """
    Implementation of player at a table abstraction
    """
    def __init__(self, player):
        self.player = player
        self.plid = player.plid
        self.bankroll = 0
        self.is_active = False
        self.cards = []

    def make_move(self, game_info):
        """
        Implementation of player's strategy.
        """
        r = randint(0, 5)
        if r == 0:
            return {'plid': self.player.plid, 
                    'decision': Decision(DecisionType.FOLD, 0)}
        else:
            return {'plid': self.player.plid,
                    'decision': Decision(DecisionType.BET, r)}
            
    def take_sit(self, available_sits):
        """Player chooses a sit among available"""
        self.sit = available_sits[randint(0, len(available_sits) -1 )]
                
    def make_buyin(self, max_buyin):
        """Player makes a buy-in"""
        buyin = max(max_buyin, self.player.cash_amount)
        self.player.cash_amount -= buyin
        self.bankroll += buyin

    def receive_surplus(self, value):
        """Increase players cash amount when player leaves a game"""
        self.player.cash_amount += value
        self.bankroll -= value

    def become_active(self):
        """If active, player joins next game"""
        self.is_active = True

    def become_inactive(self):
        """If inactive, player skips next game"""
        self.is_active = False
