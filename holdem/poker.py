from holdem.table import *
from holdem.player import *
from holdem.game import *

table = Table('tT', 1, 2, 4, 50)
player1 = Player('p1', 300, 1)
player2 = Player('p2', 300, 2)
player3 = Player('p3', 300, 3)
table.add_player(player1)
table.add_player(player2)
table.add_player(player3)
game = Game(table) 
game.play_game()
