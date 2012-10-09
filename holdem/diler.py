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

    def best_combination(self, cards):
        """Returns a list of 5 cards that form best combination"""
        comb = self.__check_straight_flush__(cards)
        if comb != None:
            return comb
        comb = self.__check_four_of_kind__(cards)
        if comb != None:
            return comb
        comb = self.__check_full_house__(cards)
        if comb != None:
            return comb
        comb = self.__check_flush__(cards)
        if comb != None:
            return comb
        comb = self.__check_straight__(cards)
        if comb != None:
            return comb
        comb = self.__check_three_of_kind__(cards)
        if comb != None:
            return comb
        comb = self.__check_two_pair__(cards)
        if comb != None:
            return comb
        comb = self.__check_pair__(cards)
        if comb != None:
            return comb
        comb = self.__check_high_card__(cards)
        if comb != None:
            return comb
        print "Raise error"
        
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
        scards = self.__same_rank__(cards)[0]
        if len(scards) == 4:
            return scards
        else:
            return None

    def __check_full_house__(self, cards):
        """
        Returns a list of 5 cards from given list that form full house
        or None otherwise
        """
        scards = self.__same_rank__(cards)
        fset = scards[0]
        if len(fset) == 3:
            sset = scards[1]
            if len(sset) == 2:
                return fset + sset
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
            return scards[-6:-1]

    def __check_straight__(self, cards):
        """
        Returns a list of 5 cards from given list that form straight
        or None otherwise
        """
        scards = sorted(cards, key = lambda card: card.rank)
        if scards[-1] == Rank.ACE:
            scards.insert(0, scards[-1])
        # Form possible straight combinations
        # (as sublists in __same_suit__() are sorted
        # in ascending order)
        for i in reversed(range(len(scards) - 4)):
            comb = scards[i:(4 - len(scards) + i)]
            if self.__is_straight__(comb) == True:
                return comb

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
            return scards[0] + scards[1] + max(scards[2])

    def __check_pair__(self, cards):
        """
        Returns a list of 5 cards from given list that form pair
        or None otherwise
        """
        scards = self.__same_rank__(cards)
        if len(scards[0]) != 2:
            return None
        else:
            rcards = sorted(list(set(cards) - set(scards)),\
                            key = lambda card: card.rank,\
                            reverse = True) 
            return scards[0] + rcards[:3]

    def __check_high_card__(self, cards):
        """Returns a list of 5 cards from given list that form high card"""
        return sorted(cards, lambda card: card.rank, reverse = True)[:5]

    def __same_suit__(self, cards):
        """
        Returns a sorted list of sublists of cards with same suit. Cards in
        sublists doesn't intersect. Cards in sublists are sorted by ranks in
        ascending order. Resulting list is sorted in decreasing order according
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
