"""
Continue this once I have coded some of the other main hands on the river, because I get the feeling
that I will cover things like flushes and straights in the main hand - particularly at the start of each main
hand.

The below is a helper for the river, it is to determine what the nuts is on the river.

I don't think I'll need to cover straight and flushes, because I will cover that anyway in certain hands.

Here is where I found the code: https://github.com/annaymj/Python-Code/blob/master/Poker.py
"""


    def isRoyal (self):
        """
        It's a weird one to check whether a royal is possible, because if you think about it, it only
        requires 3 cards on the flop, because the other 2 cards will be in someone's hand.

        The function will return True if there is a possible royal flush.
        It will also return the two cards that make the royal flush.
        """
        diamonds_royal_flush = [[14, 'D'], [13, 'D'], [12, 'D'], [11, 'D'], [10, 'D']]
        hearts_royal_flush = [[14, 'H'], [13, 'H'], [12, 'H'], [11, 'H'], [10, 'H']]
        clubs_royal_flush = [[14, 'C'], [13, 'C'], [12, 'C'], [11, 'C'], [10, 'C']]
        spades_royal_flush = [[14, 'S'], [13, 'S'], [12, 'S'], [11, 'S'], [10, 'S']]

        all_the_royal_possibilities = [diamonds_royal_flush, hearts_royal_flush, clubs_royal_flush, spades_royal_flush]

        three_cards_on_board_that_make_the_royal = []
        royal_flush_potential_count = 0
        for royal_flush in all_the_royal_possibilities:
            for card in self.river:
                if card in royal_flush:
                    royal_flush_potential_count += 1
                    three_cards_on_board_that_make_the_royal.append(card)

            if royal_flush_potential_count == 3:
                two_card_that_complete_the_royal_flush = list(set(royal_flush) - set(three_cards_on_board_that_make_the_royal))
                return True, two_card_that_complete_the_royal_flush
            royal_flush_potential_count = 0

        return False, 'royal_flush_not_possible'


    def isStraightFlush(self):
        """
        Way to check for straight flush is to check whether there are at least 3 of the same suit on the baard first.
        Then check if they are running (in particular if their total difference is no more than 4)
        From there you can calculate what the two cards are that complete the straight flush.

        One thing to note is that there can only be one straight flush, and only one possible 3 card suit that is
        the same on the board.
        """

        # get the suit of the potential straight flush
        suit_counter = dict()
        suit_counter['D'] = self.river.count('D')
        suit_counter['C'] = self.river.count('C')
        suit_counter['S'] = self.river.count('S')
        suit_counter['H'] = self.river.count('H')
        all_suit_count = ['D', 'C', 'S', 'H']

        suit_of_potential_straight_flush = None
        for suit in all_suit_count:
            if suit_counter[suit] >= 3:
                suit_of_potential_straight_flush = suit

        if not suit_of_potential_straight_flush:
          return False

        # gather all the nums with the potential straight flush suit
        nums_of_potential_straight_flush = []
        for card in self.river:
            if card[1] == suit_of_potential_straight_flush:
                nums_of_potential_straight_flush.append(card[0])

        # check if those with the potential suit are 'running' enough to make a straight flush
        # N.B. since I had the excellent foresight to sort the river, you can check three cards at a time
        curr_three_cards = []
        potential_straight_flushes = []  # note that there can be more than one straight flush
        for i in range(3):
            curr_three_cards = nums_of_potential_straight_flush[i:i+3]
            total_diff_of_curr_three_cards = 0
            total_diff_of_curr_three_cards += curr_three_cards[0] - curr_three_cards[1]
            total_diff_of_curr_three_cards += curr_three_cards[1] - curr_three_cards[2]

            if


        return False




  def isFour (self, hand):                  #returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=8
    Currank=sortedHand[1].rank               #since it has 4 identical ranks,the 2nd one in the sorted listmust be the identical rank
    count=0
    total_point=h*13**5+self.point(sortedHand)
    for card in sortedHand:
      if card.rank==Currank:
        count+=1
    if not count<4:
      flag=True
      print('Four of a Kind')
      self.tlist.append(total_point)

    else:
      self.isFull(sortedHand)

  def isFull (self, hand):                     #returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=7
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                 #create a list to store ranks
    for card in sortedHand:
      mylist.append(card.rank)
    rank1=sortedHand[0].rank                  #The 1st rank and the last rank should be different in a sorted list
    rank2=sortedHand[-1].rank
    num_rank1=mylist.count(rank1)
    num_rank2=mylist.count(rank2)
    if (num_rank1==2 and num_rank2==3)or (num_rank1==3 and num_rank2==2):
      flag=True
      print ('Full House')
      self.tlist.append(total_point)

    else:
      flag=False
      self.isFlush(sortedHand)

  def isFlush (self, hand):                         #returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=6
    total_point=h*13**5+self.point(sortedHand)
    Cursuit=sortedHand[0].suit
    for card in sortedHand:
      if not(card.suit==Cursuit):
        flag=False
        break
    if flag:
      print ('Flush')
      self.tlist.append(total_point)

    else:
      self.isStraight(sortedHand)

  def isStraight (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=5
    total_point=h*13**5+self.point(sortedHand)
    Currank=sortedHand[0].rank                        #this should be the highest rank
    for card in sortedHand:
      if card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
      print('Straight')
      self.tlist.append(total_point)

    else:
      self.isThree(sortedHand)

  def isThree (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=4
    total_point=h*13**5+self.point(sortedHand)
    Currank=sortedHand[2].rank                    #In a sorted rank, the middle one should have 3 counts if flag=True
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
    if mylist.count(Currank)==3:
      flag=True
      print ("Three of a Kind")
      self.tlist.append(total_point)

    else:
      flag=False
      self.isTwo(sortedHand)

  def isTwo (self, hand):                           #returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=3
    total_point=h*13**5+self.point(sortedHand)
    rank1=sortedHand[1].rank                        #in a five cards sorted group, if isTwo(), the 2nd and 4th card should have another identical rank
    rank2=sortedHand[3].rank
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
    if mylist.count(rank1)==2 and mylist.count(rank2)==2:
      flag=True
      print ("Two Pair")
      self.tlist.append(total_point)

    else:
      flag=False
      self.isOne(sortedHand)

  def isOne (self, hand):                            #returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=2
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                       #create an empty list to store ranks
    mycount=[]                                      #create an empty list to store number of count of each rank
    for card in sortedHand:
      mylist.append(card.rank)
    for each in mylist:
      count=mylist.count(each)
      mycount.append(count)
    if mycount.count(2)==2 and mycount.count(1)==3:  #There should be only 2 identical numbers and the rest are all different
      flag=True
      print ("One Pair")
      self.tlist.append(total_point)

    else:
      flag=False
      self.isHigh(sortedHand)

  def isHigh (self, hand):                          #returns the total_point and prints out 'High Card'
    sortedHand=sorted(hand,reverse=True)
    flag=True
    h=1
    total_point=h*13**5+self.point(sortedHand)
    mylist=[]                                       #create a list to store ranks
    for card in sortedHand:
      mylist.append(card.rank)
    print ("High Card")
    self.tlist.append(total_point)

def main ():
  numHands = eval (input ('Enter number of hands to play: '))
  while (numHands < 2 or numHands > 6):
    numHands = eval( input ('Enter number of hands to play: ') )
  game = Poker (numHands)
  game.play()

  print('\n')
  for i in range(numHands):
    curHand=game.hands[i]
    print ("Hand "+ str(i+1) + ": " , end="")
    game.isRoyal(curHand)

  maxpoint=max(game.tlist)
  maxindex=game.tlist.index(maxpoint)

  print ('\nHand %d wins'% (maxindex+1))
