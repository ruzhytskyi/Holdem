from holdem.diler import *
from holdem.different import *
import unittest

class TestDilerMethods(unittest.TestCase):

    def setUp(self):
        self._deck = Deck() 
        self._diler = Diler(self._deck) 

    def test___is_straight__valid_comb(self):
        comb = []
        comb.append(Card(Rank.TWO, Suit.HEARTS))
        comb.append(Card(Rank.SIX, Suit.DIAMONDS))
        comb.append(Card(Rank.THREE, Suit.DIAMONDS))
        comb.append(Card(Rank.FOUR, Suit.DIAMONDS))
        comb.append(Card(Rank.FIVE, Suit.DIAMONDS))
        self.assertTrue(self._diler.__is_straight__(comb))


    def test___is_straight__valid_comb_wth_ace(self):
        comb = []
        comb.append(Card(Rank.TWO, Suit.HEARTS))
        comb.append(Card(Rank.ACE, Suit.DIAMONDS))
        comb.append(Card(Rank.THREE, Suit.DIAMONDS))
        comb.append(Card(Rank.FOUR, Suit.DIAMONDS))
        comb.append(Card(Rank.FIVE, Suit.DIAMONDS))
        self.assertTrue(self._diler.__is_straight__(comb))

    def test__is_straight__inv_comb(self):
        comb = []
        comb.append(Card(Rank.THREE, Suit.HEARTS))
        comb.append(Card(Rank.ACE, Suit.DIAMONDS))
        comb.append(Card(Rank.THREE, Suit.DIAMONDS))
        comb.append(Card(Rank.FOUR, Suit.DIAMONDS))
        comb.append(Card(Rank.FIVE, Suit.DIAMONDS))
        self.assertFalse(self._diler.__is_straight__(comb))

if __name__ == '__main__':
    unittest.main()
