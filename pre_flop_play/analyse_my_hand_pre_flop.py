"""
EXTRA NOTES:

- Note the 'raise'/'bet' button always says 'bet' after the flop and 'raise' before the flop; but they represent the same thing.
- Note that hands are always dealt with the HIGHEST CARD to the far left and the LOWEST CARD to the far right, this should
  help a lot with indexing;
  e.g. nums_list = [13,12,12,7,5,3] , suit_list = ['D','D','C','H','S','S']
"""
from collections import defaultdict
from all_the_steps_with_coordinates.step_7_detect_whos_turn_to_act.whos_turn_to_act import IsItMyTurnToAct


class PreFlopHandCombinations:
    """
    This class defined all the general functions that helps to build up the type of hand;
    e.g. singleSuitedAce, TwoPairedHighCard, etc.

    These should just return True or False.
    Because on the flop I consider what I have already compared to the flop, so no need to
    do such work here twice.
    """

    def __init__(self, my_position, empty_seat_tracker, num_list, suit_list):
        self.my_position = my_position
        self.empty_seat_tracker = empty_seat_tracker
        self.num_list = num_list
        self.suit_list = suit_list

        # high card
        self.at_least_five_high_cards = self.count_high_cards()
        # suited
        self.single_suited_ace_f = self.single_suited_ace()
        self.single_suited_king_f = self.single_suited_king()
        self.double_suited_aces_f = self.double_suited_ace()
        self.double_suited_f = self.double_suited()
        # pair
        self.high_pair_in_my_hand_f = self.high_pairs_in_my_hand()  # returns an integer
        # running
        self.check_for_wrap_and_wrap_plus_pair_generator = self.check_for_wrap_and_wrap_plus_pair()
        self.wrap_no_pair = self.check_for_wrap_and_wrap_plus_pair_generator[0]
        self.wrap_plus_pair = self.check_for_wrap_and_wrap_plus_pair_generator[1]

    def count_high_cards(self):
        num_high_cards_in_my_hand = 0
        for card in self.num_list:
            if card >= 10:
                num_high_cards_in_my_hand += 1
        return num_high_cards_in_my_hand >= 5

    def single_suited_ace(self):
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

    def single_suited_king(self):
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

    def double_suited_ace(self):
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

    def high_pairs_in_my_hand(self):
        """
        I consider a high pair to be a pair that is 10 or above.
        """
        count_of_num = defaultdict(int)
        for i in self.num_list:
            count_of_num[i] += 1  # {'A': 2, 10: 1, 5: 1, 2: 2}
        number_of_high_pairs = 0
        for num in count_of_num:
            if int(num) >= 10 and count_of_num[num] > 1:
                number_of_high_pairs += 1
        if number_of_high_pairs == 1:
            return True
        else:
            return False

    def check_for_wrap_and_wrap_plus_pair(self):
        """
        nums_list = [13,12,12,7,5,3]

        The only wraps I consider playing: [9, 8, 7], [9, 8, 6], [9, 7, 6], [9, 8, 5], [9, 6, 5]

        Will only consider wraps higher than 5.

        One caveat, if there is a pair inbetween, we want to filter it out first at the start.
        e.g. 10 9 9 8 4 3 -> 10 9 8 4 3
        """
        # remove all pairs from num_list before checking for wraps
        filtered_num_list_take_out_pairs = [self.num_list[0]]
        for i in range(1, 5):
            if self.num_list[i] == self.num_list[i-1] or self.num_list[i] == self.num_list[i+1]:
                pass
            else:
                filtered_num_list_take_out_pairs.append(self.num_list[i])
        if self.num_list[-1] != filtered_num_list_take_out_pairs[-1]:
            filtered_num_list_take_out_pairs.append(self.num_list[-1])
        if len(filtered_num_list_take_out_pairs) < 3:
            return False
        # split num_list into combo of 3 cards
        all_combo_of_three = []
        for i in range(len(filtered_num_list_take_out_pairs)):
            all_combo_of_three.append(filtered_num_list_take_out_pairs[i:i+3])
            if len(filtered_num_list_take_out_pairs) - i == 3:
                break
        # look if I have wrap and/or wrap plus pair in my hand
        any_wrap_in_my_hand = False
        is_wrap_plus_pair_in_my_hand = False
        for combo in all_combo_of_three:
            is_wrap_in_my_hand = False
            difference_first_two_cards = combo[0] - combo[1]
            difference_second_two_cards = combo[1] - combo[2]
            if difference_second_two_cards == 1 and difference_second_two_cards == 1:  # 9 8 7
                is_wrap_in_my_hand = True
            if difference_first_two_cards == 2 and difference_second_two_cards == 1:  # 9 7 6
                is_wrap_in_my_hand = True
            if difference_first_two_cards == 1 and difference_second_two_cards == 2:  # 9 8 6
                is_wrap_in_my_hand = True
            if difference_first_two_cards == 3 and difference_second_two_cards == 1:  # 9 6 5
                is_wrap_in_my_hand = True
            if difference_first_two_cards == 1 and difference_second_two_cards == 3:  # 9 8 5
                is_wrap_in_my_hand = True
            if is_wrap_in_my_hand:
                any_wrap_in_my_hand = True
                for num in combo:
                    if self.num_list.count(num) >=2:
                        is_wrap_plus_pair_in_my_hand = True

        return any_wrap_in_my_hand, is_wrap_plus_pair_in_my_hand


class ShouldWePlayThisPreFlopHand(PreFlopHandCombinations):
    """
    This class will define all the types of hands I will play pre_flop_play.

    It will use functions from the above PreFlopHandCombinations, which is a helper functions
    where the functions define useful things about my hand construct like two paired high cards,
    or ace high flush, so that in this class I can refer to it without needing to write code to
    check if I have it.
    """

    def __init__(self, my_position, num_list, suit_list, empty_seat_tracker=None):
        PreFlopHandCombinations.__init__(self, my_position, empty_seat_tracker, num_list, suit_list)

    """
    Keep in mind I will play 99% of hands from positions 5 and 6.
    I think the most important thing is that the hand uses all 6 cards! - this constructs a high hand
    when we flop something. Of course a strong hand can miss the board completely too, but 
    when it hits you want ALL or most of the cards to play a part in the hand.
    
    Also remember I read that in Omaha, hands are made on the straight - so running cards are quite important - VERY! 
    
    I write these with DOMINATION in mind. 
    Having redraws to the nuts, and set over set, etc. 
    
    (R)!!! 
    Keep in mind what I read about being in position and playing less nutted hand because 
    you have the benefit of position, whereas if you play any hands OOP, you'll want to be nutted. 
    i.e. drawing to nut flush draw, as you don't have benefit of position and don't know as well 
    where you are vs. your opponent.
    
    IF I play hands in position 5 or 6 ALWAYS raise (it if hasn't been raised behind you).
    IF I play hands OOP ALWAYS call. 
    (unless SPR is low and you have double suited aces - so some caveats but not many)
    
    (R)!!!! 
    Position should play a part in determining if a hand is premium, so A 8 7 6 5 4 would be 
    premium hand if you are in position 6 but in position 1 it is a call hand.  
    (That's because IP you can bluff a lot more! - but OOP you need to play more straight forward, since 
    you lack opponent information).
    """

    def my_turn_to_act(self):
        is_it_my_turn_to_act = IsItMyTurnToAct()
        return is_it_my_turn_to_act.is_it_my_turn_to_act()

    def does_my_hand_meet_at_least_three_pillars(self):
        """
        STRATEGY:

        I will only play a hand if it meets the following criteria:
        1) at least 5 of the 6 cards are connected
        2) By connected I mean connect in some ways according to the 4 pillars: high, paired, suited, running
        - At least 3 of the pillars must be met for me to play the hand.
        So for example if he had three high paired in my hand but they're not suited or running then I won't play.

        (On second thought as long as 3/4 pillars are met I'll play the hand;
        because if you think about it as long as 3/4 pillars are met, can you think of a weak hand
        that meets 3/4 pillars, if so then change the strategy but if not, which I think not, then
        keep it like this)

        I think it's worth making a distinction between a very strong and a strong hand.
        Because I can think of hands where I would want to 3-bet that meet 3 pillars but others that I would not.
        For now leave it, to play safer even super storng hands don't three bet pre_flop, just go nuts when
        you hit something strong on flop. SOMETHING TO CONSIDER LATER ONCE THINGS ARE RUNNING.

        # high card
        self.at_least_five_high_cards = self.count_high_cards()  # True or False
        # suited
        self.single_suited_ace_f = self.single_suited_ace()
        self.single_suited_king_f = self.single_suited_king()
        self.double_suited_aces_f = self.double_suited_ace()
        self.double_suited_f = self.double_suited()
        # pair
        self.how_many_high_pair_in_my_hand_f = self.how_many_high_pairs_in_my_hand()  # returns an integer
        # running
        self.check_for_wrap_and_wrap_plus_pair_generator = self.check_for_wrap_and_wrap_plus_pair()
        self.wrap_no_pair = self.check_for_wrap_and_wrap_plus_pair_generator[0]
        self.wrap_plus_pair = self.check_for_wrap_and_wrap_plus_pair_generator[1]

        Initially I thought it might be worth keeping track of the pillars that I have, but I don't think it's
        necessary, just return 'bet' or 'fold' or 'call'.
        Look at notepad and see what the considerations are to decide, call, bet or fold.
        On the flop I check what I have already so no point doing the work here too.
        """
        pillars_of_a_strong_starting_hand = dict()
        pillars_of_a_strong_starting_hand['high_cards'] = self.at_least_five_high_cards
        pillars_of_a_strong_starting_hand['suited'] = [self.single_suited_ace_f, self.single_suited_king_f]
        pillars_of_a_strong_starting_hand['pair'] = self.high_pair_in_my_hand_f
        pillars_of_a_strong_starting_hand['running'] = [self.wrap_no_pair, self.wrap_plus_pair]
        number_of_pillars_met = 0
        for pillar in pillars_of_a_strong_starting_hand.values():
            if isinstance(pillar, list):
                if any(pillar):
                    number_of_pillars_met += 1
            else:
                if pillar:
                    number_of_pillars_met += 1
        if number_of_pillars_met < 3:
            return False

        return True

    def double_suited_aces(self):
        pass

    def all_six_cards_connected(self):
        """
        This is where we have running + paired + suited.

        Not as important if the cards or suits are high, because this is powerful if you hit the right flop.
        i.e. you can be flopping the opp dead.
        """
        pass
