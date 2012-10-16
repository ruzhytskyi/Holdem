from holdem.diler import Diler
from holdem.player import PlayerAtTable

class Table(object):
    """
    Implementation of table abstraction.
    """
    def __init__(self, name, sbl, bbl, sits_count, max_buyin):
        self.diler = Diler()
        self.sbl = sbl
        self.bbl = bbl
        self.max_buyin = max_buyin
        self.table_history = []
        self.sits = range(1, sits_count + 1)
        self.players = []

    def add_player(self, player):
        """Registers player for current table"""
        tplayer = PlayerAtTable(player)
        tplayer.take_sit(self.__available_sits__())
        tplayer.make_buyin(self.max_buyin)
        self.players.append(tplayer)
        tplayer.become_active()
        
    def remove_player(self, player):
        """Removes player from current table"""
        pass
        

    def __available_sits__(self):
        """Returns list of sits numbers that are avaialble for players"""
        return list(set(self.sits) - set(self.__occupied_sits__()))

    def __occupied_sits__(self):
        """Returns list of sits numbers that are occupied by players"""
        return [player.sit for player in self.players]

