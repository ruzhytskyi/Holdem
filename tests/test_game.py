import unittest
from holdem.game import *
from holdem.table import *
from holdem.diler import *
from holdem.player import *
from holdem.different import *

class TestGameMethods(unittest.TestCase):

    def setUp(self):
        self.table = Table('tT', 1, 2, 4, 100)
        player1 = Player('p1', 300, 1)
        player2 = Player('p2', 300, 2)
        player3 = Player('p3', 300, 3)
        self.table.add_player(player1)
        self.table.add_player(player2)
        self.game = Game(self.table) 

    def test___remove_folds__(self):
        move1 = {
            'decision': Decision(DecisionType.BET, 10),
            'plid': 1
        }
        move2 = {
            'decision': Decision(DecisionType.FOLD, 0),
            'plid': 2
        }
        move3 = {
            'decision': Decision(DecisionType.FOLD, 0),
            'plid': 3
        }

        lap = [move1, move2, move3]
        rlap = self.game.__remove_folds__(lap)
        self.assertListEqual(rlap, [move1])

if __name__ == '__main__':
    unittest.main()
