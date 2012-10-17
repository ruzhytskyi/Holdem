from holdem.different import *

class Diler(object):
    def __init__(self, deck):
        self.deck = deck    

    def give_card(self):
        """Returns Card object taken from a Deck"""
        return self.deck.pop_card() 
    
    def give_two_cards(self):
        """Returns a list of two Card objects"""
        return [self.deck.pop_card() for i in range(2)]
        
    def give_three_cards(self):
        """Returns a list of three Card objects"""
        return [self.deck.pop_card() for i in range(3)]
    
    def verify_move(self, move, history):
        """
        Verifies player's move according to given game history.
        Returns 0 if move is correct and 1 otherwise.
        """ 
        pass
    
    def compare_combs(self, comb1, comb2):
        """
        Compares two given combinations. Combination should be passed
        as a tuple with comb type and comb as list of cards.
        """
        c1type, c1cards = comb1
        c2type, c2cards = comb2
        if c1type != c2type:
            return c1type - c2type

        elif c1type == CombType.STRAIGHT_FLUSH:
            return self.__second_highest_rank__(c1cards)\
                   - self.__second_highest_rank__(c2cards)

        elif c1type == CombType.FOUR_OF_KIND:
            srank1 = self.__same_rank__(c1cards)
            srank2 = self.__same_rank__(c2cards)
            if srank1[0][0].rank == srank2[0][0].rank:
                return srank1[1][0].rank - srank2[1][0].rank
            else:
                return srank1[0][0].rank - srank2[0][0].rank

        elif c1type == CombType.FULL_HOUSE:
            srank1 = self.__same_rank__(c1cards)
            srank2 = self.__same_rank__(c2cards)
            if srank1[0][0].rank == srank2[0][0].rank:
                return srank1[1][0].rank - srank2[1][0].rank
            else:
                return srank1[0][0].rank - srank2[0][0].rank
        
        elif c1type == CombType.FLUSH:
            return self.__second_highest_rank__(c1cards)\
                   - self.__second_highest_rank__(c2cards)

        elif c1type == CombType.STRAIGHT:
            return self.__second_highest_rank__(c1cards)\
                   - self.__second_highest_rank__(c2cards)

        elif c1type == CombType.THREE_OF_KIND:
            srank1 = self.__same_rank__(c1cards)
            srank2 = self.__same_rank__(c2cards)
            if srank1[0][0].rank == srank2[0][0].rank:
                # Make a list of cards excluding "three of a kind" combination
                rcards1 = list(set(c1cards) - set(srank1[0]))
                rcards1.sort(key = lambda card: card.rank, reverse = True)
                rcards2 = list(set(c2cards) - set(srank2[0]))
                rcards2.sort(key = lambda card: card.rank, reverse = True)
                for card1, card2 in zip(rcards1, rcards2):
                    if card1.rank != card2.rank:
                        return card1.rank - card2.rank
                return 0
            else:
                return srank1[0][0].rank - srank2[0][0].rank
 
        elif c1type == CombType.TWO_PAIR:
            srank1 = self.__same_rank__(c1cards)
            srank2 = self.__same_rank__(c2cards)
            for clist1, clist2 in zip(srank1, srank2):
                if clist1[0].rank != clist2[0].rank:
                    return clist1[0].rank - clist2[0].rank
            return 0

        elif c1type == CombType.PAIR:
            srank1 = self.__same_rank__(c1cards)
            srank2 = self.__same_rank__(c2cards)
            if srank1[0][0].rank == srank2[0][0].rank:
                # Make a list of cards excluding "three of a kind" combination
                rcards1 = list(set(c1cards) - set(srank1[0]))
                rcards1.sort(key = lambda card: card.rank, reverse = True)
                rcards2 = list(set(c2cards) - set(srank2[0]))
                rcards2.sort(key = lambda card: card.rank, reverse = True)
                for card1, card2 in zip(rcards1, rcards2):
                    if card1.rank != card2.rank:
                        return card1.rank - card2.rank
                return 0
            else:
                return srank1[0][0].rank - srank2[0][0].rank
           
        elif c1type == CombType.HIGH_CARD:
            scards1 = sorted(c1cards, key = lambda card: card.rank,\
                             reverse = True)
            scards2 = sorted(c2cards, key = lambda card: card.rank,\
                             reverse = True)
            for card1, card2 in zip(scards1, scards2):
                if card1.rank != card2.rank:
                    return card1.rank - card2.rank
            return 0
    
        else:
            return 'Error'

    def best_comb(self, cards):
        """
        Returns a tuple with combination type as a first element and
        list of 5 cards that form best combination as a second element.
        """
        comb = self.__check_straight_flush__(cards)
        if comb != None:
            return (CombType.STRAIGHT_FLUSH, comb)
        comb = self.__check_four_of_kind__(cards)
        if comb != None:
            return (CombType.FOUR_OF_KIND, comb)
        comb = self.__check_full_house__(cards)
        if comb != None:
            return (CombType.FULL_HOUSE, comb)
        comb = self.__check_flush__(cards)
        if comb != None:
            return (CombType.FLUSH, comb)
        comb = self.__check_straight__(cards)
        if comb != None:
            return (CombType.STRAIGHT, comb)
        comb = self.__check_three_of_kind__(cards)
        if comb != None:
            return (CombType.THREE_OF_KIND, comb)
        comb = self.__check_two_pair__(cards)
        if comb != None:
            return (CombType.TWO_PAIR, comb)
        comb = self.__check_pair__(cards)
        if comb != None:
            return (CombType.PAIR, comb)
        comb = self.__check_high_card__(cards)
        if comb != None:
            return (CombType.HIGH_CARD, comb)
        return 'Error'
        
    def __check_straight_flush__(self, cards):
        """
        Returns a list of 5 cards from given list that form straight flush
        or None otherwise
        """
        scards = self.__same_suit__(cards)[0]
        if len(scards) < 5:
            return None
        else:
            return self.__check_straight__(scards)

    def __check_four_of_kind__(self, cards):
        """
        Returns a list of 5 cards from given list that form four of a kind
        or None otherwise
        """
        scards = self.__same_rank__(cards)
        fset = scards[0]
        if len(fset) != 4:
            return None 
        else:
            return fset + [scards[1][0]]

    def __check_full_house__(self, cards):
        """
        Returns a list of 5 cards from given list that form full house
        or None otherwise
        """
        scards = self.__same_rank__(cards)
        fset = scards[0]
        if len(fset) == 3:
            sset = scards[1]
            if len(sset) >= 2:
                return fset + sset[:2]
            else: return None
        else: return None

    def __check_flush__(self, cards):
        """
        Returns a list of 5 cards from given list that form flush
        or None otherwise
        """
        scards = self.__same_suit__(cards)[0]
        if len(scards) < 5:
            return None
        else:
            return scards[-5:]

    def __check_straight__(self, cards):
        """
        Returns a list of 5 cards from given list that form straight
        or None otherwise
        """
        scards = sorted(cards, key = lambda card: card.rank)
        if scards[-1].rank == Rank.ACE:
            scards.insert(0, scards[-1])
        # Form possible straight combinations
        # (as sublists in __same_suit__() are sorted
        # in ascending order)
        for i in reversed(range(len(scards) - 4)):
            comb = scards[i:5 + i]
            if self.__is_straight__(comb) == True:
                return comb

        return None

    def __check_three_of_kind__(self, cards):
        """
        Returns a list of 5 cards from given list that form three of a kind
        or None otherwise
        """
        scards = self.__same_rank__(cards)[0]
        if len(scards) != 3:
            return None
        else:
            rcards = sorted(list(set(cards) - set(scards)),\
                            key = lambda card: card.rank,\
                            reverse = True) 
            return scards + rcards[:2]

    def __check_two_pair__(self, cards):
        """
        Returns a list of 5 cards from given list that form two pair
        or None otherwise
        """
        scards = self.__same_rank__(cards)
        if len(scards[0]) != 2:
            return None
        elif len(scards[1]) != 2:
            return None
        else:
            return scards[0] + scards[1] + [scards[2][0]]

    def __check_pair__(self, cards):
        """
        Returns a list of 5 cards from given list that form pair
        or None otherwise
        """
        scards = self.__same_rank__(cards)
        if len(scards[0]) != 2:
            return None
        else:
            rcards = sorted(list(set(cards) - set(scards[0])),\
                            key = lambda card: card.rank,\
                            reverse = True) 
            return scards[0] + rcards[:3]

    def __check_high_card__(self, cards):
        """Returns a list of 5 cards from given list that form high card"""
        return sorted(cards, key = lambda card: card.rank, reverse = True)[:5]

    def __same_suit__(self, cards):
        """
        Returns a sorted list of sublists of cards with same suit. Cards in
        sublists doesn't intersect. Cards in sublists are sorted by ranks in
        ascending order. Resulting list is sorted in descending order according
        to the count of cards with same suit. Sublist with higher card rank is
        greater than sublist with same cards count, but lower card rank.
        """
        # Make a dictionary with suit and corredponding lists of cards of this 
        # suit
        d = {}
        for card in cards:
            if d.has_key(card.suit) == False:
                d[card.suit] = [card]
            else:
                d[card.suit].append(card)
        
        # Make a function that returns highest rank if dict item is given
        lfunc = lambda el: self.__highest_rank__(list(el)[1])
        # Sort a dictionary by highest rank
        sd = sorted(d.items(), key = lfunc , reverse = True)
        # Make a list of sublists from a dictionary
        l = [y for x, y in sd]
        
        # Make a list of sublists sorted by elements count in sublists.
        # As sorted() preserves original order if two elements are equal,
        # equal sublists will be sorted according to highest rank
        l = sorted(l, key = len, reverse = True)

        # Sort sublists according to card rank  
        for subl in l:
            subl.sort(key = lambda card: card.rank)
    
        return l

    def __same_rank__(self, cards):
        """
        Returns a sorted list of sublists of cards with same rank. Cards in
        sublists doesn't intersect. Cards in sublists are sorted by rank in
        ascending order. Resulting list is sorted in descending order according
        to the count of cards with same rank. Sublist with higher card rank is
        greater than sublist with same cards count, but lower card rank.
        """
        # Make a dictionary with ranks and corredponding lists of cards of this
        # rank
        d = {}
        for card in cards:
            if d.has_key(card.rank) == False:
                d[card.rank] = [card]
            else:
                d[card.rank].append(card)

        # Make a function that returns highest rank if dict item is given
        lfunc = lambda el: self.__highest_rank__(list(el)[1])
        # Sort a dictionary by highest rank
        sd = sorted(d.items(), key = lfunc , reverse = True)
        # Make a list of sublists from a dictionary
        l = [y for x, y in sd]
        
        # Make a list of sublists sorted by elements count in sublists.
        # As sorted() preserves original order if two elements are equal,
        # equal sublists will be sorted according to highest rank
        l = sorted(l, key = len, reverse = True)

        # Sort sublists according to card rank  
        for subl in l:
            subl.sort(key = lambda card: card.rank)
    
        return l

    def __highest_rank__(self, cards):
        """Returns a highest rank among given cards"""
        return sorted(cards, key = lambda card: card.rank)[-1].rank

    def __second_highest_rank__(self, cards):
        """Returns a second highest rank among given cards"""
        return sorted(cards, key = lambda card: card.rank)[-2].rank

    def __is_straight__(self, cards):
        """
        Returns True if cards in given list form straight combination.
        Raises an error if len(cards) doesn't equal to 5
        """
        scards = sorted(cards, key = lambda card: card.rank)
        for i in range(len(scards) - 2):
            if scards[i].rank + 1 != scards[i + 1].rank:
                return False

        if scards[-1].rank == scards[-2].rank + 1:
            return True
        elif scards[-1].rank == Rank.ACE and scards[0].rank == Rank.TWO:
            return True
        else:
            return False
