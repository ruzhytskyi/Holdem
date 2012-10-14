from random import randint
from different import Decision

class Player(object):
    def __init__(self, name, cash_amount, plid):
        self.name = name
        self.cash_amount = cache_amount
        self.plid = plid

class PlayerAtTable(object):
    def __init__(self, player):
        self.player = player
        self.bankroll = 0
        self.is_active = False

    def make_move(self, game_info):
        r = randint(5)
        if r == 0:
            return Decision(DTYPE.FOLD, 0)
        else:
            return Decision(DTYPE.BET, r)
            
    def take_sit(self, available_sits):
        """Player chooses a sit among available"""
        self.sit = available_sits[randint(len(available_sits))]
                
    def make_buyin(max_buyin):
        """Player makes a buy-in"""
        buyin = max(max_buyin, cash_amount)
        self.player.cash_amount -= buyin
        self.bankroll += buyin

    def receive_surplus(value):
        """Increase players cash amount when player leaves a game"""
        self.player.cash_amount += value
        self.bankroll -= value

    def become_active(self):
        """If active, player joins next game"""
        self.is_active = True

    def become_inactive(self):
        """If inactive, player skips next game"""
        self.is_active = False
