"""
EXTRA NOTES:

- Note the 'raise'/'bet' button always says 'bet' after the flop and 'raise' before the flop; but they represent the same thing.
- Note that hands are always dealt with the HIGHEST CARD to the far left and the LOWEST CARD to the far right, this should
  help a lot with indexing;
  e.g. nums_list = [13,12,12,7,5,3] , suit_list = ['D','D','C','H','S','S']
"""
from collections import defaultdict
from all_the_steps_with_coordinates.step_6_number_of_players_in_pot.num_of_players_in_pot import PlayersLeftInPot
from all_the_steps_with_coordinates.step_7_detect_whos_turn_to_act.whos_turn_to_act import IsItMyTurnToAct


class PreFlopHandCombinations:
    """
    This class defined all the general functions that helps to build up the type of hand;
    e.g. singleSuitedAce, TwoPairedHighCard, etc.
    """

    def __init__(self, my_position, empty_seat_tracker, num_list, suit_list):
        self.my_position = my_position
        self.empty_seat_tracker = empty_seat_tracker
        self.num_list = num_list
        self.suit_list = suit_list

        # N.B. Rather than calling the below functions multiple times - which is what I would do if I
        # didn't make them class attributes; here it makes a lot more sense to call them one time
        # since the data is static and won't change.
        self.singlesuitedAce_f = self.singlesuitedAce()
        self.singlesuitedKing_f = self.singlesuitedKing()
        self.double_suited_aces_f = self.doublesuitedAce()
        self.oneHighPair_f = self.onehighPair()
        self.twoHighPair_f = self.twohighPair()
        self.wrap_f = self.Wrap()
        self.double_suited_f = self.double_suited()
        self.aces_f = self.aces()
        self.super_wrap_f = self.super_wrap()
        self.wrap_plus_pair_f = self.wrap_plus_pair()

    def singlesuitedAce(self):
        if self.num_list[0] == 14:
            first_ace_suit = self.suit_list[0]
            if any(suit == first_ace_suit for suit in self.suit_list[1:]):
                return True

        if self.num_list[1] == 14:
            second_ace_suit = self.suit_list[1]
            if any(suit == second_ace_suit for suit in self.suit_list[2:]):
                return True

        if self.num_list[2] == 14:
            second_ace_suit = self.suit_list[2]
            if any(suit == second_ace_suit for suit in self.suit_list[3:]):
                return True

        return False

    def singlesuitedKing(self):
        if self.num_list[0] == 13:
            first_ace_suit = self.suit_list[0]
            if any(suit == first_ace_suit for suit in self.suit_list[1:]):
                return True

        if self.num_list[1] == 13:
            second_ace_suit = self.suit_list[1]
            if any(suit == second_ace_suit for suit in self.suit_list[2:]):
                return True

        if self.num_list[2] == 13:
            second_ace_suit = self.suit_list[2]
            if any(suit == second_ace_suit for suit in self.suit_list[3:]):
                return True

        if self.num_list[3] == 13:
            second_ace_suit = self.suit_list[3]
            if any(suit == second_ace_suit for suit in self.suit_list[4:]):
                return True

        return False

    def doublesuitedAce(self):
        number_of_suited_aces = 0
        if self.num_list[0] == 14:
            first_ace_suit = self.suit_list[0]
            if any(suit == first_ace_suit for suit in self.suit_list[1:]):
                number_of_suited_aces += 1
        if self.num_list[1] == 14:
            second_ace_suit = self.suit_list[1]
            if any(suit == second_ace_suit for suit in self.suit_list[2:]):
                number_of_suited_aces += 1
        if self.num_list[2] == 14:
            third_ace_suit = self.suit_list[2]
            if any(suit == third_ace_suit for suit in self.suit_list[3:]):
                number_of_suited_aces += 1

        return True if number_of_suited_aces >= 2 else False

    def onehighPair(self):
        """
        I consider a high pair to be a pair that is Q or above.
        """
        count_of_num = defaultdict(int)
        for i in self.num_list:
            count_of_num[i] += 1  # {'A': 2, 10: 1, 5: 1, 2: 2}

        number_of_high_pairs = 0
        for num in count_of_num:
            if int(num) >= 12 and count_of_num[num] > 1:
                number_of_high_pairs += 1

        if number_of_high_pairs == 1:
            return True
        else:
            return False

    def Wrap(self):
        """
        nums_list = [13,12,12,7,5,3]

        Wraps I consider playing: [9, 8, 7], [9, 8, 6], [9, 7, 6]
        All can flop full wraps. Even if the gap is at the top end.
        """
        temp = []
        all_combo_of_three = []
        for i in range(4):
            k = i
            while k < len(self.num_list):
                temp.append(self.num_list[k])
                if len(set(temp)) == 3:
                    all_combo_of_three.append(temp)
                    temp = []
                    break
                k += 1
        for combi in all_combo_of_three:
            for num in range(len(combi)):
                combi[num] = int(combi[num])

        for i in range(len(all_combo_of_three)):
            all_combo_of_three[i] = sorted(list(set(all_combo_of_three[i])), reverse=True)

        total_gap = 0
        final_combo_of_three = []
        for current_three in all_combo_of_three:  # Calculate if we have a potential full-wrap; can only be one gap between any three cards
            total_gap += current_three[0] - current_three[1]
            total_gap += current_three[1] - current_three[2]

            if total_gap <= 3:
                final_combo_of_three.append(current_three)
            total_gap = 0

        if final_combo_of_three:
            return True, final_combo_of_three
        else:
            return False

    def wrap_plus_pair(self):
        current_three = []
        for i in range(len(self.num_list)-3):
            if self.num_list[i] < 5:  #Avoid playing wraps that start smaller than 5
                break
            current_three.append(self.num_list[i])
            current_three.append(self.num_list[i+1])
            current_three.append(self.num_list[i+2])

            #if pair in current three, then there's no wrap in this three combo
            if len(set(current_three)) < 3:
                continue

            #Calculate if we have a potential full-wrap; can only be one gap between all three cards
            total_gap = 0
            total_gap += current_three[0] - current_three[1]
            total_gap += current_three[1] - current_three[2]

            if total_gap <= 3:
                for num in current_three:
                    if self.num_list.count(num) >= 2:
                        return True

            current_three = []

    def double_suited(self):
        count_of_suits = defaultdict(int)
        for i in self.suit_list:
            count_of_suits[i] += 1

        double_suited_count = 0

        for suit_count in count_of_suits.values():
            if suit_count > 1:
                double_suited_count += 1

        if double_suited_count > 1:
            return True

    def aces(self):
        if self.num_list[0] == 14 and self.num_list[1] == 14:
            return True

    def super_wrap(self):
        """
        This will be the helper function for the 5/6 connected cards hand.

        This function checks that at least 4 cars are 'running', with at most one gap.
        It will also return the 4 running cards; there could be more than one combination.
        """
        three_combo_of_fours = [self.num_list[:4], self.num_list[1:5], self.num_list[2:6]]
        running_cards_with_at_most_one_gap = []

        for four_cards in three_combo_of_fours:
            total_gap = 0
            for i in range(len(four_cards)-1):
                total_gap += four_cards[i] - four_cards[i+1]
            if total_gap == 4 or total_gap == 5:
                pass
            else:
                running_cards_with_at_most_one_gap.append(four_cards)

        if running_cards_with_at_most_one_gap:
            return True, running_cards_with_at_most_one_gap

        return False, []


class ShouldWePlayThisPreFlopHand(PreFlopHandCombinations):
    """
    This class will define all the types of hands I will play _1_pre_flop.

    It will use functions from the above PreFlopHandCombinations, which is a helper functions
    where the functions define useful things about my hand construct like two paired high cards,
    or ace high flush, so that in this class I can refer to it without needing to write code to
    check if I have it.
    """

    def __init__(self, my_position, num_list, suit_list, empty_seat_tracker=None):
        PreFlopHandCombinations.__init__(self, my_position, empty_seat_tracker, num_list, suit_list)
        self.my_hand = self.should_we_play_this_hand_pre_flop()  # will either be a string or False

        self.my_position = my_position
        self.empty_seat_tracker = empty_seat_tracker
        self.num_list = num_list
        self.suit_list = suit_list

    """
    Keep in mind I will play 99% of hands from positions 5 and 6.
    I think the most important thing is that the hand uses all 6 cards! - this constructs a high hand
    when we flop something. Of course a strong hand can miss the board completely too, but 
    when it hits you want ALL or most of the cards to play a part in the hand.
    
    Also remember I read that in Omaha, hands are made on the straight - so running cards are quite important - VERY! 
    
    I write these with DOMINATION in mind. 
    Having redraws to the nuts, and set over set, etc. 
    
    1) High pair with high flushes; top set + nut flush draw 
    2) Running smaller cards or running high cards with high suit; straight with flush redraw
    3) Running cards with pair (any pair that is not top pair) straight with house redraw
    4) If all 6 cards connect (or 5 cards); like double suited + running + paired 
    - I thought of a few other combinations, but they fall into one of the categories above anyway, so I'll end up 
    playing them. Every time you think of a new hand, think whether it's already covered below firt before adding it.
    
    (R)!!! 
    Also keep in mind what I read about being in position and playing less nutted hand because 
    you have the benefit of position, whereas if you play any hands OOP, you'll want to be nutted. 
    i.e. drawing to nut flush draw, as you don't have benefit of position and don't know as well 
    where you are vs. your opponent.
    
    IF I play hands in position 5 or 6 ALWAYS raise. 
    IF I play hands OOP ALWAYS call. 
    (unless SPR is low and you have double suited aces - so some caveats but not many)
    
    Rather than thinking about hands in terms of 'premium' and 'call' hands - I think a better way is to 
    Write out the generic hands I will play - then class them into hands I will only play IP and the ones I will play OOP.

    (R)!!!! 
    But position should play a part in determining if a hand is premium, so A 8 7 6 5 4 would be 
    premium hand if you are in position 6 but in position 1 it is a call hand.  
    (That's because IP you can bluff a lot more! - but OOP you need to play more straight forward, since 
    you lack opponent information).
    
    Write out your main hands and final_check will take care of the rest, if you hit something that is not part 
    of your main hand.
    
    N.B. 
    Something genius I just thought of. If I structure my hands the way I have below, I don't need a separate function 
    for each hand - I can handle them all in final_check! 
    This is very clever; the _1_pre_flop hands that you construct IS SOLELY to make sure that hand that I play is good enough 
    and to proceed in terms of whether I am in position or OOP. 
    Final_check in later rounds can take care of the rest! GENIUS!  
    """

    # STEP7
    def my_turn_to_act(self):
        is_it_my_turn_to_act = IsItMyTurnToAct()
        return is_it_my_turn_to_act.is_it_my_turn_to_act(self.my_position)

    def premium_hand1(self):
        if self.double_suited_aces_f:
            return True
        else:
            return False

    def high_pair_with_high_flush(self):
        """
        High pair I mean Q+ and high flush I mean King flush or higher.
        """
        # Do I have a pair that is Queen or higher?
        if not self.oneHighPair_f:
            return False

        # Do I have a high flush?
        if not self.singlesuitedKing_f and not self.singlesuitedAce_f:
            return False
        return True

    def running_cards_high_suit(self):
        """
        Running (i.e. wrap) where the smallest card is at least a 5.

        And suit is at least a K.
        """
        if not self.wrap_f:
            return False

        if not self.singlesuitedKing_f and not self.singlesuitedAce_f:
            return False
        return True

    def running_cards_high_pair(self):
        """
        Running where the smallest card is at least a 5.
        Running as in at least 3 cards are consecutively running; 7 6 5 for example.

        High pair is Q+

        This can be of two forms:
        1) Q Q 7 6 5 (in this function)
        2) 7 6 5 5 (in function below this one- not strong enough on its own)

        i.e. we hit top set with straight draw in 1).
        or We hit a made straight/draw with set.
        This is quite weak on it's own, so I woudn't wat to play it on it's own, if it is double suited for example
        with a high suit, then it makes the hand much more attractive.

        """
        # Scenario where I have running cards with one big pair (Q+)
        if not self.wrap_f:
            return False
        if not self.oneHighPair_f:
            return False
        return True

    def running_cards_any_pair(self):
        """
        As described above this will be something like 7 6 5 5.
        But as it's not strong enough on it's own - meaning I won't hit anything most of the time and
        I won't win the hand.
        So I want something else with it like a flush draw or high pair.
        """
        back_up = [self.singlesuitedKing_f, self.singlesuitedAce_f, self.double_suited_f]

        if not self.wrap_f:
            return False
        if not any(back_up):
            return False
        return True

    def all_five_or_six_cards_connected(self):
        """
        This is where we have running + paired + suited.

        Not as important if the cards or suits are high, because this is powerful if you hit the right flop.
        i.e. you can be flopping the opp dead.
        """
        # Check that cards are running
        if not self.super_wrap_f[0]:
            return False

        # Check that there is at least one pair
        running_four_card_combi = self.super_wrap_f[1]
        found_one_pair_in_running_four = False
        for combi in running_four_card_combi:
            if any(self.num_list.count(card) >= 2 for card in combi):
                found_one_pair_in_running_four = True
                break

        if not found_one_pair_in_running_four:
            return False

        # Check that it is suited (double preferably)
        if not self.double_suited_f and not self.singlesuitedKing_f and not self.singlesuitedAce_f:
            return False

        return True

    def should_we_play_this_hand_pre_flop(self):
        """
        Just a reminder that the _1_pre_flop hands I code is ONLY to ensure I play solid hands - it serves nothing else!
        All of the hands will lead into final_check().

        Read my comment in the function below about differentiating super-premium hands _1_pre_flop.
        """
        list_of_pre_flop_hands_to_play = [self.premium_hand1(), self.all_five_or_six_cards_connected(), self.running_cards_high_pair(),
                                  self.running_cards_high_suit(), self.high_pair_with_high_flush(),
                                  self.running_cards_any_pair()]  # THIS IS A LIST OF TRUE OR FALSE ONLY

        if any(list_of_pre_flop_hands_to_play):
            # We don't need to pass what the hand is on - since we will run final_check regardless of the hand!
            return True

        return False


