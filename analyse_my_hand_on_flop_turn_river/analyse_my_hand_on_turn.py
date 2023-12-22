from collections import defaultdict
from analyse_my_hand_on_flop import AnalyseMyHandOnFlop

from flop_turn_river_cards import TheTurn
TT = TheTurn()


class AnalyseMyHandOnTurn(AnalyseMyHandOnFlop):

    def __init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                 positions_of_players_to_act_ahead_of_me,
                 pot_size, my_position, num_list, suit_list, big_blind):

        AnalyseMyHandOnFlop.__init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)
        self.positions_of_players_to_act_ahead_of_me = positions_of_players_to_act_ahead_of_me
        self.guy_to_right_bet_size = guy_to_right_bet_size
        self.SPR_tracker = SPR_tracker
        self.pot_size = pot_size
        self.stack_tracker = stack_tracker

        # Commenting out for testing
        self.organise_turn = self.organise_turn()
        self.turn = self.organise_turn[0]   # looks like [[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']] ; it is sorted
        self.turn_num = int(self.organise_turn[1])  # this is the number of the turn card, e.g. 10
        self.turn_suit = self.organise_turn[2]  # this is the suit of the turn card, e.g. 'S'
        # self.turn = [[8, 'C'], [8, 'H'], [6, 'S'], [2, 'C']]
        # self.turn_num = 2
        # self.turn_suit = 'C'

        # This is just to help determine if any obvious straights got there
        self.list_of_two_straight_draw_cards_on_flop = self.list_of_two_straight_draw_cards_on_flop()

        # check if any straights completed on turn
        self.any_straight_completed_on_turn_f = self.any_straight_completed_on_turn()
        # self.any_straight_completed_on_turn_f = False, 'second_third_fourth_card'  # just for testing commenting out line above
        self.did_straight_complete_on_turn = self.any_straight_completed_on_turn_f[0]
        self.which_three_cards_on_turn_make_the_straight = self.any_straight_completed_on_turn_f[1]

        # return True or False and all the straight making combinations IN ORDER starting with nut straight
        self.obvious_or_general_straight_made = self.any_obvious_or_general_straights_complete()
        self.all_two_card_straight_completing_combinations_on_turn = self.obvious_or_general_straight_made[1]
        self.obvious_straight_completed = True if self.obvious_or_general_straight_made[0] == 'obvious' else False
        self.general_straight_completed = True if not self.obvious_straight_completed else False
        self.turn_did_not_change_made_straight_on_flop = True if self.obvious_or_general_straight_made[0] == 'straight_made_on_flop_turn_card_didnt_change_anything' else None

        # check if flush completed on turn, and the suit of the flush if so
        # self.flush_complete_on_turn = self.flush_completed_on_turn()
        self.flush_complete_on_turn = False, 'nothing', 'nothing'
        self.did_flush_completed_on_turn = self.flush_complete_on_turn[0]
        self.nut_flush_nums_turn = self.flush_complete_on_turn[1]  # N.B. This is not the largest nums of the flush on the board; e.g. [14, 13, 10, 2] all hearts; then this would be 12 of hearts.
        self.suit_of_flush_turn = self.flush_complete_on_turn[2]

        # check if a flush hit on turn (and there wasn't one on flop), and return the highest number of that suit in my hand
        self.my_highest_num_of_the_completed_flush_on_turn = self.did_I_hit_flush_on_turn(self.turn_suit)

        # check if I hit the nut straight or any straight on turn
        self.did_I_hit_straight_on_turn_f = self.did_I_hit_straight_on_turn(self.all_two_card_straight_completing_combinations_on_turn)

        # check if the board paired on the turn - this will simply return True or False
        self.did_board_pair_on_turn_f = self.did_board_pair_on_turn()


    def organise_turn(self):
        """
        turn will look like: [[13, 'S'], [10, 'C'], [9, 'S'], [8, 'C']] ; after we sort it.
        """
        turn_generator = TT.add_turn_card_num_and_suit_to_flop(self.flop)
        self.flop = self.organise_flop()  # self.flop gets messed up by the line above and points to self.turn, so need this line to correct it
        turn = turn_generator[0]
        turn_num = turn_generator[1]
        turn_suit = turn_generator[2]
        return turn, turn_num, turn_suit

    def any_straight_completed_on_turn(self):
        """
        Analyse the turn nums and check if any possible straight is present on the turn.

        Do this by checking 3 cards at a time, and since it is sorted we need to check 2 lots of 3, as there are only 4 cards.

        There is only a straight when the gap between the 3 cards is no more than 4.
        e.g. 10, 7, 6 or 10, 8, 6

        self.turn looks like [[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']]

        It's worth returning the 3 cards that make the straight, so that on the river, I can easily check
        if the river card changed the nuts of the straight.
        """
        turn_numbers = [num[0] for num in self.turn]

        if (turn_numbers[0] - turn_numbers[1]) + (turn_numbers[1] - turn_numbers[2]) <= 4:
            if (turn_numbers[1] - turn_numbers[2]) + (turn_numbers[2] - turn_numbers[3]) <= 4:
                # both the first three cards and the second, third, fourth card make a straight
                return True, 'first_three_cards_and_second_third_fourth_card'
            else:
                return True, 'first_three_cards'
        elif (turn_numbers[1] - turn_numbers[2]) + (turn_numbers[2] - turn_numbers[3]) <= 4:
            return True, 'second_third_fourth_card'
        return False, None

    def generate_all_straight_possibilities(self, three_card_straight_possibility):
        """
        When checking if any straights or wraps got there on the turn, you will need to check for all combinations
        of straights, so this function will do exactly that;
        It will take 3 cards as input and generate all possible 2 cards combinations that make a straight.
        The 3 cards will consist of the 2 straight_making cards on the flop and the turn card.

        e.g. 9 7 6 ->> [(10,8), (8,5)]
             9 8 7 ->> [(11,10), (10,6), (6,5)]

        Although some straights are less likely, I do make the distinction in obvious vs. general straight.

        I will generate straights from the highest number going down, so in the list of straights that I return,
        the nut straight will always be the first one in the list.

        At this point I've checked that straights are possible, so just generate the combinations.
        """
        card1, card2, card3 = three_card_straight_possibility
        two_straight_making_card_combis = []

        if card1 - card2 == 2 and card2 - card3 == 2:  # e.g. 9 7 5
            two_straight_making_card_combis.append((card2 + 1, card3 + 1))

        elif card1 - card2 == 2 and card2 - card3 == 1:  # e.g. 9 7 6
            two_straight_making_card_combis.append((card1 + 1, card2 + 1))  # 10 8
            two_straight_making_card_combis.append((card2 + 1, card3 -1 ))  # 8 5

        elif card1 - card2 == 1 and card2 - card3 == 2:  # e.g. 9 8 6
            two_straight_making_card_combis.append((card1 + 1, card3 + 1))  # 10 7
            two_straight_making_card_combis.append((card3 + 1, card3 - 1))  # 7 5

        elif card1 - card2 == 1 and card2 - card3 == 1:  # e.g. 9 8 7
            two_straight_making_card_combis.append((card1 + 2, card1 + 1))  # 11, 10
            two_straight_making_card_combis.append((card1 + 1, card3 - 1))  # 10, 6
            two_straight_making_card_combis.append((card3 - 1, card3 - 2))  # 6, 5

        elif card1 - card2 == 3 and card2 - card3 == 1:  # e.g. 9 6 5
            two_straight_making_card_combis.append((card2 + 2, card2 + 1))  # 8 7

        elif card1 - card2 == 1 and card2 - card3 == 3:  # e.g. 9 8 5
            two_straight_making_card_combis.append((card3 + 2, card3 + 1))  # 7 6

        return two_straight_making_card_combis

    def list_of_two_straight_draw_cards_on_flop(self):
        """
        This function simply looks at what straight making cards there are on the flop.
        This is to determine if any 'obvious' straights got there.
        Reminder:
        self.flop = [[13, 'S'], [10, 'S'], [8, 'C']]
        """
        flop_num = [card[0] for card in self.flop]
        list_of_two_straight_making_cards_on_flop = []

        if flop_num[0] - flop_num[1] <= 4:
            list_of_two_straight_making_cards_on_flop.append([flop_num[0], flop_num[1]])
        if flop_num[1] - flop_num[2] <= 4:
            list_of_two_straight_making_cards_on_flop.append([flop_num[1], flop_num[2]])

        return list_of_two_straight_making_cards_on_flop

    def did_board_pair_on_turn(self):
        """
        This function will return True if the turn card paired the board.
        """
        flop_nums = [card[0] for card in self.flop]
        if self.turn_num in flop_nums:
            return True
        return False

    def any_obvious_or_general_straights_complete(self):
        """
        This function checks if any obvious or general straight completed on the turn, when there is a straight
        draw on the flop.

        It also considers the scenario when there is already a made straight on the flop, and considers if the
        turn card changes the nut straight or creates any more straights.
        If not then do nothing, because on the flop we pass on the two card combinations that make the straight already,
        so nothing has changed.

        When there is just a straight draw, like 13,8,6 then the 9,7 straight is quite obvious. So if the turn card
        is a 10 or 5, then I'll class that as an 'obvious' straight.
        When 13,8,7 then it's slightly less obvious, that's when position would be V IMP.
        As I will act according to the action of the opp.

        I'll classify obvious straights as:
        - 9 7 2 ; if 11 or 6 hit then obvious straight got there
        - 11 7 2 ; if 8, 9, 10 hit then obvious straight got there
        - 8 9 2 ; if 12 or 7 hit then obvious straight got there
        - 10 7 ; if 11 or 6 hit then obvious straight got there

        Note I inherit from FlopHelper, which checks if for straight and wrap draws on the flop.

        This function will return 'obvious' or 'general' for obvious or general straight and will return all 2 cards combos that make a straight.
        The first entry will always be the nut straight and going down in strength.

        The first half of the function builds on the scenario where there is already a straight on the flop.
        The second half considers the scenario when there is a straight draw on the flop and the turn comes in,
        and it checks if any straights are completed.
        """
        all_two_card_straight_completing_combinations = []
        made_straight_on_flop_two_straight_completing_combinations = []
        # Check if a straight was completed on the flop already, and if so, check if the turn makes any difference!
        # it will only make a difference if the turn card num is greater than the smallest flop num.
        if self.made_straight_on_flop_f[1]:
            # N.B. the nuts can only change if it is a gap card, e.g. 9 7 5; nuts chances only if turn is 6 or 8
            flop_nums = [card[0] for card in self.flop]
            # In all scenarios if the turn changes the straight, it will be the first 3 cards that does it.
            # There is a new nut straight if the turn card is larger than the smallest card on the flop;
            # here are what all straights can look like: 9 8 7 ; 9 8 6 ; 9 8 5 ;
            if self.turn_num > flop_nums[2]:
                # if the turn card is higher than the smallest flop card then the nut straight has changed, so generate combinations
                # otherwise do nothing, because if made straight on flop we already generated all combi's of two cards that complete straight.
                if self.turn_num <= flop_nums[2] + 3:
                    # we need to check that the turn card affects the straight, because if we have
                    # 8 6 5 on the flop and the turn card is a 14, then it has no impact!
                    made_straight_on_flop_two_straight_completing_combinations = [[flop_nums[0], flop_nums[1]], [flop_nums[1], flop_nums[2]]]
            else:
                return 'straight_made_on_flop_turn_card_didnt_change_anything', self.two_card_combis_that_complete_the_straight_on_flop

            # generate the straight combinations from the made straight on flop plus the turn card (as the nut straight might change)
            for two_straight_making_cards in made_straight_on_flop_two_straight_completing_combinations:
                three_card_straight_possibility = sorted([int(two_straight_making_cards[0]), int(two_straight_making_cards[1]), int(self.turn_num)])
                # using the two straight draw cards on the flop and the turn card, check if any straights are completed
                all_two_card_straight_completing_combinations = self.generate_all_straight_possibilities(three_card_straight_possibility)
                # check for obvious straights completing
                straight_card1 = two_straight_making_cards[0]
                straight_card2 = two_straight_making_cards[1]
                if straight_card1 - straight_card2 == 1:  # e.g. 10 9
                    if self.turn_num == straight_card2 - 1 or self.turn_num == straight_card1 + 3:
                        return 'obvious', all_two_card_straight_completing_combinations

                elif straight_card1 - straight_card2 == 2:  # e.g. 10 8
                    if self.turn_num == straight_card1 + 2 or self.turn_num == straight_card2 - 1:
                        return 'obvious', all_two_card_straight_completing_combinations

                elif straight_card1 - straight_card2 == 3:  # e.g. 10 7
                    if self.turn_num == straight_card1 + 1 or self.turn_num == straight_card2 - 1:
                        return 'obvious', all_two_card_straight_completing_combinations

                elif straight_card1 - straight_card2 == 4:  # e.g. 10 6
                    if self.turn_num == straight_card1 - 1 or self.turn_num == straight_card1 - 2 or self.turn_num == straight_card1 - 3:
                        return 'obvious', all_two_card_straight_completing_combinations

                else:
                    return 'general', all_two_card_straight_completing_combinations

        # if there is no made straight on the flop, check if the turn made a straight

        # Below I check for any straight draw possibilities on the flop, and I store the combination of two cards that make a straight draw
        # Then I use these two card combinations together with the turn card and gather all the cards that make a straight, even the
        # unusual straights.

        # list_of_two_straight_draw_cards_on_flop holds any two cards on the flop that make a straight draw, can only be at most two things in this list
        if not self.made_straight_on_flop_f[1]:
            for two_straight_making_cards in self.list_of_two_straight_draw_cards_on_flop:
                three_card_straight_possibility = sorted([int(two_straight_making_cards[0]), int(two_straight_making_cards[1]), int(self.turn_num)], reverse=True)
                # using the two straight draw cards on the flop and the turn card, check if any straights are completed
                all_two_card_straight_completing_combinations = self.generate_all_straight_possibilities(three_card_straight_possibility)

                # check for obvious straights completing
                straight_card1 = two_straight_making_cards[0]
                straight_card2 = two_straight_making_cards[1]
                if straight_card1 - straight_card2 == 1:  # e.g. 10 9
                    if self.turn_num == straight_card2 - 1 or self.turn_num == straight_card1 + 3:
                        return 'obvious', all_two_card_straight_completing_combinations

                elif straight_card1 - straight_card2 == 2:  # e.g. 10 8
                    if self.turn_num == straight_card1 + 2 or self.turn_num == straight_card2 - 1:
                        return 'obvious', all_two_card_straight_completing_combinations

                elif straight_card1 - straight_card2 == 3:  # e.g. 10 7
                    if self.turn_num == straight_card1 + 1 or self.turn_num == straight_card2 - 1:
                        return 'obvious', all_two_card_straight_completing_combinations

                elif straight_card1 - straight_card2 == 4:  # e.g. 10 6
                    if self.turn_num == straight_card1 - 1 or self.turn_num == straight_card1 - 2 or self.turn_num == straight_card1 - 3:
                        return 'obvious', all_two_card_straight_completing_combinations

        # check if there is any straight possible using the 2 cards we identified on the flop that can make a straight and the turn card
        if not self.any_straight_completed_on_turn_f:
            return False, None

        # This will be executed if say the flop is 14 6 5 and the turn is a 7.
        return 'general', all_two_card_straight_completing_combinations

    def flush_completed_on_turn(self):
        """
        This function will return True if a flush completed on turn, it will return the suit of the flush, and
        whatever the nut flush nums card is.
        (R)!!! - note that this is NOT the highest num on the board that has that suit.
        e.g. [14, 13, 12, 2] and they are all 'hearts' or whatever suit, then this function will return 11!!
        """
        nut_flush_num = None
        turn_suits = [card[1] for card in self.turn]
        suit_counter = defaultdict(int)

        for suit_card in turn_suits:
            suit_counter[suit_card] += 1

        for suit_card in suit_counter:
            if suit_counter[suit_card] >= 3:
                # N.B. The way to find the nut nums of the flush is simply to iterate from 14 down and the first card that you do not find
                # is the nut flush
                for num in reversed(range(15)):  # iterates from 14
                    if [num, suit_card] not in self.turn:
                        nut_flush_num = num
                return True, nut_flush_num, suit_card
        return False, False, False

    def did_I_hit_flush_on_turn(self, flush_suit):
        """
        This function returns a number indicating how high my flush is, if I don't have the flush it will return False.

        Check that there wasn't a flush already on the flop.
        This is important, because I am passing in the 'turn_suit' into this function, so it would be WRONG
        to do this if there is already a flush on the flop!!
        """
        # check that there wasn't a flush completed on the flop
        if not self.did_flush_completed_on_flop:
            if self.did_flush_completed_on_turn:
                highest_flush_num = None
                for pos, card in enumerate(self.num_list):
                    if self.suit_list[pos] == flush_suit:
                        highest_flush_num = card
                        break  # we want first instance where the card suit matches the flush_suit, as this is the highest num of that suit

                if self.suit_list.count(flush_suit) >= 2:  # check I have at least two cards of the flush suit - otherwise I don't have a flush!
                    return highest_flush_num

        return False

    def did_I_hit_straight_on_turn(self, all_two_card_straight_completing_combinations_on_turn):
        """
        In this function, I will:
        Check all of the straight completing combinations, and see if any are in my hand.
        I'll break it down so that I have either the nut straight, otherwise 'any' other straight.

        Note that if there is a straight on the flop, and the turn card didn't change anything,
        then take the all_two_card_straight_completing_combination from the flop, because on
        the turn I don't generate anything for it - i.e. it will be an empty list.

        Reminder:
        all_two_card_straight_completing_combinations = [ [10, 8], [7, 6], ... ]
        """
        all_two_card_straight_completing_combinations = []
        # Scenario where straight completed on flop and turn card didn't change anything
        if self.straight_completed_on_flop:
            if self.turn_num < self.flop[2][0]:
                all_two_card_straight_completing_combinations = self.two_card_combis_that_complete_the_straight_on_flop

        # If there is a made straight on the flop, check if I have the nut straight or any straight.
        if all_two_card_straight_completing_combinations:
            nut_straight_two_cards = all_two_card_straight_completing_combinations[0]
            for two_cards in all_two_card_straight_completing_combinations:
                if all(card in self.num_list for card in two_cards):
                    # check if I have any straight or nut straight
                    if two_cards == nut_straight_two_cards:
                        return 'I_have_nut_straight'
                    else:
                        return 'I_have_non_nut_straight'
        else:
            # If no made straight on flop, then take the all_two_card_straight_completing_combinations that is passed into
            # this function, which is all the two_card_combinations that completed the straight on the turn
            all_two_card_straight_completing_combinations = all_two_card_straight_completing_combinations_on_turn
            if all_two_card_straight_completing_combinations:
                nut_straight_two_cards = all_two_card_straight_completing_combinations[0]
                for two_cards in all_two_card_straight_completing_combinations:
                    if all(card in self.num_list for card in two_cards):
                        # check if I have any straight or nut straight
                        if two_cards == nut_straight_two_cards:
                            return 'I_have_nut_straight'
                        else:
                            return 'I_have_non_nut_straight'

        return 'I_dont_have_straight'

    def analyse_final_check_on_turn(self, hu, flopped=None):
        """
        final_check_on_turn will do two things:
        1) Continue cases from final_check on flop
        2) Check if we hit any straight or flushes on the turn card, from the main hands on the turn,
        i.e. the main hands on the turn will sometimes directly call on this function to check if I hit the
        weird straight that completed on the turn for example, when I had top set on the flop.

        When I do 2) and call this function from a main hand rather than final_check on the flop,
        I should indicate this in 'flopped' ! - because if no action is returned, I can finish off the action
        in the main hand.
        (R)!!! Inside flopped I will start it with 'ma_...' if I am calling final_check from a main hand.
        And the rest of the string should describe why I am calling this function.
        e.g. 'ma_top_set_on_flop_straight_completed_on_turn'

        (R)!!!
        For the above, it will be mainly straights that will call this function from the main hand.
        If flushes complete or board pairs, it will be dealt with in the main hand.
        TO DO:
        Might be worth splitting it out to an entirely new function that checks if I hit the straight or hit a straight draw
        with whatever I have in the main hand, rather than calling final_check_on_turn

        """
        # comment out all hu for MVP as I haven't coded it yet.
        # if hu:
        #     return self.analyse_heads_up_on_turn_f
        if self.did_board_pair_on_turn_f:
            # This will cover the case if the board was not paired on the flop but paired on the turn
            return self.board_paired_on_turn(hu)

        if self.did_flush_completed_on_turn:
            return self.flush_completed_on_turn_play()

        # I use this check quite a lot so make it a variable for easy reference below
        important_four_SPR_amount = self.SPR_tracker[self.my_position] >= 4 and \
                                    self.guy_to_right_bet_size <= self.stack_tracker[self.my_position] / 4

        # check if straight completed on turn and if I have a straight
        my_straight = None
        if self.any_straight_completed_on_turn_f:
            my_straight = self.did_I_hit_straight_on_turn_f  # my_straight = 'I_have_nut_straight' or 'I_have_non_nut_straight' or 'I_dont_have_straight'

        # Below two scenarios directly below this are me representing the straight/flush in very specific situations;
        # ie. I'm last to act, checked to me, SPR >= 4

        # Scenario 1: This is a general scenario where I will rep the nut flush on turn; I am last to act checked to me on turn
        if self.did_flush_completed_on_turn:
            # Im IP
            if not self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    if self.SPR_tracker[self.my_position] >= 4:
                        return 'BET', 'fc_Im_IP_checked_to_me_flush_completed_I_have_top_set_representing_the_flush_SPR_is_decent', 'place_holder'
        # I should code out every scenario including folding in flush completed, because this renders my straights useless,
        # and below I don't want to keep checking whether flush completed.

        # Scenario 2: This is a general scenario where I will rep the nut straight; I am last to act checked to me
        if self.any_straight_completed_on_turn_f:
            # this is if I have the nut straight and no flush completed so just bet
            if my_straight == 'I_have_nut_straight' and flopped == 'ma_top_set_straight_completed_on_turn' and not self.did_flush_completed_on_turn:
                return 'BET', 'fc_bet_turned_the_nut_straight_and_no_flush_completed', 'place_holder'
            # Im IP
            if not self.positions_of_players_to_act_ahead_of_me:
                # not for MVP, but later you want to add a condition only to do this with weird straights;
                # weird meaning lower cards and gappers, e.g. 7 6 4 - as ppl less likely to have 8 5 then say 8 7
                if not self.guy_to_right_bet_size:
                    if self.SPR_tracker[self.my_position] >= 4:
                        return 'BET', 'fc_Im_IP_checked_to_me_straight_completed_I_have_top_set_representing_the_nut_straight', 'place_holder'

        # I represented the flush on flop I'm IP and checked to me and I BET with top set
        if flopped == 'fc_top_set_made_flush_on_flop_checked_to_me_im_last_to_act':
            # the situation where it's checked to me on turn and I'm last to act and nothing changed on turn; see two scenarios above this
            if self.guy_to_right_bet_size:
                if important_four_SPR_amount:
                    return 'CALL', 'fc_bet_into_me_on_turn_checked_to_me_on_flop_I_have_set_trying_to_hit_river_or_bluff_catch', 'place_holder'

            else:
                # ADD SPR check if highish SPR then bet
                if self.SPR_tracker[self.my_position] >= 3:
                    return 'BET', 'fc_check_to_me_on_flop_and_turn_I_have_top_set_but_made_flush_on_flop_betting_to_rep', 'place_holder'
                else:
                    return 'CALL', 'fc_check_to_me_on_flop_and_turn_I_have_top_set_but_made_flush_on_flop_checking', 'place_holder'

        # I have top set on flop with no straight or flushes made on the flop
        if flopped == 'fc_top_set_no_made_straight_or_flush_on_flop':
            # if flush completed on turn
            if self.did_flush_completed_on_turn:
                if not self.positions_of_players_to_act_ahead_of_me:
                    if self.guy_to_right_bet_size:  # if guy doesn't bet this case is handled at top of this function
                        if self.SPR_tracker[self.my_position] > 5:
                            return 'CALL', 'fc_flush_completed_bet_into_me_SPR_decent_im_calling_w_top_set', 'place_holder'
                # Im OOP
                else:
                    # others ahead of me to act
                    if not self.guy_to_right_bet_size:
                        if len(self.positions_of_players_to_act_ahead_of_me) == 1:  # one person ahead of me
                            if self.SPR_tracker[self.my_position] >= 5:
                                return 'BET', 'fc_betting_top_set_when_flush_got_there_checked_to_me_repping_flush', 'place_holder'
                        else:
                            return 'CALL', 'fc_checking_top_set_many_players_ahead_of_me_flush_comp_on_turn', 'place_holder'
                    else:
                        if self.SPR_tracker[self.my_position] >= 5:
                            return 'CALL', 'fc_bet_into_me_flush_completed_I_have_top_set', 'place_holder'

            # if straight completed on turn
            if self.any_straight_completed_on_turn_f:
                if not self.guy_to_right_bet_size:
                    return 'CALL', 'fc_checking_top_set_with_straight_completing', 'place_holder'
                if not self.obvious_straight_completed:
                    if not self.guy_to_right_bet_size:
                        if self.SPR_tracker[self.my_position] >= 5:
                            return 'BET', 'fc_no_obvious_st8_completed_checked_to_me_Im_betting_top_set', 'place_holder'
                else:
                    # obvious straight completed, check it
                    if not self.guy_to_right_bet_size:
                        return 'CALL', 'fc_checking_obv_straight_completed', 'place_holder'
                    else:
                        # obv str8 completed guy bet and I'll call if SPR is decent hoping for board to pair on river
                        if not self.positions_of_players_to_act_ahead_of_me:
                            if self.SPR_tracker[self.my_position] >= 6:
                                return 'CALL', 'fc_calling_bet_when_obv_str8_got_there', 'place_holder'

            # I have top set and neither straight nor flush completed on turn
            if not self.any_straight_completed_on_turn_f and not self.did_flush_completed_on_turn:
                if self.guy_to_right_bet_size:
                    return 'BET', 'fc_top_set_nothing_completed_on_turn_raise_bet_on_turn', 'place_holder'
                else:
                    if 3 < self.SPR_tracker[self.my_position] < 5:
                        # TO DO: add check if it is multi-toned board, i.e. straight + flush draw possibilities, if one toned, bet to denty equity
                        if self.positions_of_players_to_act_ahead_of_me:
                            return 'CALL', 'fc_checking_on_turn_awkward_SPR', 'place_holder'
                        else:
                            return 'BET', 'fc_awkward_SPR_Im_IP_with_top_set_checked_to_me_nothing_completed', 'place_holder'
                    else:
                        return 'BET', 'fc_top_set_on_turn_nothing_completed', 'place_holder'

        if flopped == 'fc_top_set_made_straight_on_flop_checked_to_me_im_last_to_act_I_bet_on_flop':
            if not self.did_flush_completed_on_turn:
                if not self.guy_to_right_bet_size:
                    if self.SPR_tracker[self.my_position] >= 3:
                        return 'BET', 'fc_top_set_made_straight_on_flop_checked_to_me_im_last_to_act_I_bet_on_flop_checked_to_me_on_turn_I_bet', 'place_holder'
            else:
                # flush hit on turn
                if self.guy_to_right_bet_size:
                    # they probably hit their flush, but maybe not
                    if important_four_SPR_amount:
                        return 'CALL', 'fc_flush_hit_on_turn_SPR_enough_for_me_to_call_to_try_hit_full_house', 'place_holder'
                else:
                    if self.SPR_tracker[self.my_position] >= 4:
                        return 'BET', 'fc_flush_hit_on_turn_bet_into_me_Im_last_to_act_checked_to_me_I_bet', 'place_holder'

        # good chance someone has trip aces and I have middle set, basically check fold, unless I hit straight on turn
        if flopped == 'fc_middle_set_check_someone_three_bet_pre_flop_ace_on_flop':
            if my_straight == 'I_have_nut_straight':
                return 'BET', 'betting_with_nut_straight_and_middle_set_redraw', 'place_holder'
                # TO DO: add one more layer here that if SPR is awkward like 4 then worth going for a check raise
            elif my_straight == 'I_have_non_nut_straight':
                if self.positions_of_players_to_act_ahead_of_me:
                    if self.guy_to_right_bet_size:
                        # check call see what happens on river, if someone has top set likely they will check on river
                        return 'CALL', 'calling_bet_into_me_I_have_non_nut_straight_and_middle_set', 'place_holder'
                else:
                    # not so sure here, randomise, but if someone checks and I suspect they have top set, worth betting if I am in position
                    return 'BET', 'betting_non_nut_straight_middle_set_I_suspect_opp_has_top_set', 'place_holder'

        # Same as directly above but with bottom set
        if flopped == 'fc_bottom_set_check_someone_three_bet_pre_flop_ace_on_flop':
            if my_straight == 'I_have_nut_straight':
                return 'BET', 'betting_with_nut_straight_and_bottom_set_redraw', 'place_holder'
            elif my_straight == 'I_have_non_nut_straight':
                if self.positions_of_players_to_act_ahead_of_me:
                    if self.guy_to_right_bet_size:
                        # check call see what happens on river, if someone has top set likely they will check on river
                        return 'CALL', 'calling_bet_into_me_I_have_non_nut_straight_and_bottom_set', 'place_holder'
                else:
                    # not so sure here, randomise, but if someone checks and I suspect they have top set, worth betting if I am in position
                    return 'BET', 'betting_non_nut_straight_bottom_set_I_suspect_opp_has_top_set', 'place_holder'

        if flopped == 'fc_bet_middle_set_no_made_flush_straight_on_flop':
            # case for flush completing dealt with at the top of this function
            if not self.any_straight_completed_on_turn_f:
                return 'BET', 'fc_bet_flop_turn_no_made_flush_or_straight_middle_set', 'place_holder'
            else:
                # if straight completed on turn
                if my_straight == 'I_have_nut_straight':
                    return 'BET', 'I_have_nut_straight_middle_set', 'place_holder'
                elif not self.obvious_straight_completed and my_straight == 'I_have_non_nut_straight':
                    # unusual straight completed and I have a straight and middle set
                    if not self.guy_to_right_bet_size:
                        return 'CALL', 'fc_I_have_weird_straight_middle_set_im_checking', 'place_holder'
                    else:
                        if important_four_SPR_amount:
                            return 'CALL', 'fc_I_have_weird_straight_middle_set_calling_a_bet_with_important_SPR', 'place_holder'

        if flopped == 'fc_bet_bottom_set_no_made_flush_straight_on_flop':
            # case for flush completing dealt with at the top of this function
            if not self.any_straight_completed_on_turn_f:
                return 'BET', 'fc_bet_flop_turn_no_made_flush_or_straight_bottom_set', 'place_holder'
            else:
                # if straight completed on turn
                if my_straight == 'I_have_nut_straight':
                    return 'BET', 'I_have_nut_straight_bottom_set', 'place_holder'
                elif not self.obvious_straight_completed and my_straight == 'I_have_non_nut_straight':
                    # unusual straight completed and I have a straight and middle set
                    if not self.guy_to_right_bet_size:
                        return 'CALL', 'fc_I_have_weird_straight_bottom_set_im_checking', 'place_holder'
                    else:
                        if important_four_SPR_amount:
                            return 'CALL', 'fc_I_have_weird_straight_middle_set_calling_a_bet_with_important_SPR', 'place_holder'

        if flopped == 'fc_bet_flopped_nut_flush_on_flop':
            # if the board paired it would be covered at the top of this function, so here the board did not pair on turn
            return 'BET', 'fc_flopped_nut_flush_bet_flop_turn_did_not_pair', 'place_holder'

        # Below are cases where I have the nut straight on the turn, and potentially some redraws
        # Write distinction where there was a straight all along on the flop vs. straight was made on turn
        # also make distinction in-position vs. OOP, in some cases, check raise if the SPR is awkward.
        if my_straight == 'I_have_nut_straight':
            if not self.positions_of_players_to_act_ahead_of_me:
                # if I am in position
                if not self.guy_to_right_bet_size:
                    # it is checked to me and I am in position
                    if flopped == 'fc_bet_made_straight_with_house_redraw_on_flop':
                        return 'BET', 'fc_nut_straight_house_redraw_on_turn', 'place_holder'
                    elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw':
                        return 'BET', 'fc_bet_made_straight_with_higher_straight_redraw', 'place_holder'
                    elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw_no_flush_draw':
                        # bet to deny equity to flush draws; if checked to me likely it's what they have
                        return 'BET', 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw', 'place_holder'
                    elif flopped == 'fc_call_bet_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw':
                        # bet to deny equity to flush draws; if checked to me likely it's what they have
                        return 'BET', 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw', 'place_holder'
                    elif flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
                        return 'BET', 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board', 'place_holder'
                else:
                    # I am in position and it is bet into me
                    if flopped == 'fc_bet_made_straight_with_house_redraw_on_flop':
                        return 'BET', 'fc_nut_straight_house_redraw_on_turn_bet_into_me_I_raise', 'place_holder'
                    elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw':
                        return 'CALL', 'fc_nut_straight_higher_st8_redraw_on_turn_bet_into_me_I_call', 'place_holder'
                    elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw_no_flush_draw':
                        # bet to deny equity to flush draws; if checked to me likely it's what they have
                        return 'CALL', 'fc_bet_made_straight_with_higher_straight_redraw_no_flush_draw', 'place_holder'
                    elif flopped == 'fc_call_bet_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw':
                        # bet to deny equity to flush draws; if checked to me likely it's what they have
                        return 'CALL', 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw', 'place_holder'
                    elif flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
                        return 'CALL', 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board', 'place_holder'

            else:
                # if I am out of position
                # if SPR is awkward, go for check raise OOP - I'm assuming something will bet, but if not still have the benefit of
                # my hand being disguised as I checked the nut straight on the turn, so if nothing changes on river can go for value bet.
                if 3 <= self.SPR_tracker[self.my_position] <= 5:
                    # Awkward SPR
                    if not self.guy_to_right_bet_size:
                        # checked to me, with others to act ahead of me
                        if flopped == 'fc_bet_made_straight_with_house_redraw_on_flop':
                            # go for the check raise
                            if not self.guy_to_right_bet_size:
                                return 'CALL', 'fc_nut_straight_house_redraw_on_turn_going_for_check_raise_but_if_flopped_is_this_on_river_it_means_it_was_checked_through', 'place_holder'
                            else:
                                # check raising
                                return 'BET', 'fc_check_raised_my_made_straight_with_house_redraw_on_turn', 'place_holder'
                        elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw':
                            # check/call since I don't have big redraw
                            return 'CALL', 'fc_bet_made_straight_with_higher_straight_redraw', 'place_holder'
                        elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw_no_flush_draw':
                            # check/call since I don't have big redraw
                            return 'CALL', 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw', 'place_holder'
                        elif flopped == 'fc_call_bet_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw':
                            # check/call since I don't have big redraw
                            return 'CALL', 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw', 'place_holder'
                        elif flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
                            return 'CALL', 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board', 'place_holder'
                    else:
                        # bet into me, with others to act ahead of me
                        if flopped == 'fc_bet_made_straight_with_house_redraw_on_flop':
                            # can alternate between checking and betting, I prefer check raise
                            return 'BET', 'fc_nut_straight_house_redraw_on_turn_bet_into_me_and_I_raise_it', 'place_holder'
                        elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw':
                            return 'CALL', 'fc_bet_made_straight_with_higher_straight_redraw', 'place_holder'
                        elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw_no_flush_draw':
                            # bet to deny equity to flush draws; if checked to me likely it's what they have
                            return 'CALL', 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw', 'place_holder'
                        elif flopped == 'fc_call_bet_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw':
                            # bet to deny equity to flush draws; if checked to me likely it's what they have
                            return 'CALL', 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw', 'place_holder'
                        elif flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
                            return 'CALL', 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board', 'place_holder'

                # if SPR is not awkward (i.e. either quite high or very low) then should just bet it to increase size of pot and deny equity
                else:
                    if flopped == 'fc_bet_made_straight_with_house_redraw_on_flop':
                        # case for check raising but I think if someone has straight they will raise me then I'll put it in
                        return 'BET', 'fc_nut_straight_house_redraw_on_turn', 'place_holder'
                    elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw':
                        return 'BET', 'fc_bet_made_straight_with_higher_straight_redraw', 'place_holder'
                    elif flopped == 'fc_bet_made_straight_with_higher_straight_redraw_no_flush_draw':
                        # bet to deny equity to flush draws; if checked to me likely it's what they have
                        return 'BET', 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw', 'place_holder'
                    elif flopped == 'fc_call_bet_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw':
                        # bet to deny equity to flush draws; if checked to me likely it's what they have
                        return 'BET', 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw', 'place_holder'
                    elif flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
                        return 'BET', 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board', 'place_holder'

        if flopped == 'fc_call_SPR_is_quite_low_get_in_on_turn_if_no_flush':
            # going all in - SPR super low
            return 'BET', 'SPR_low_I_had_nut_straight_with_no_flush_draw_on_flop_no_flush_completed_on_turn_this_is_all_in', 'place_holder'

        if flopped == 'fc_bet_on_flop_made_straight_flush_redraw':
            # I AM LEAVING OFF HERE FOR MVP - THERE ARE MORE SCENARIOS TO CODE FROM THE TURN, AND ALSO LOOK AT FLOP - I MISSED OUT SOME TOO
            pass

        # V IMP - TO DO********************************
        # I will be calling final_check_on_turn from some main hand functions, so at the end here,
        # I may have a top set, when a weird straight completed on turn, and I don't want to check fold blindly!

        # So what I do is I pass back to the main hand function, and complete the action there, because there may be
        # more checks that I want to do to decide what action to take.
        if flopped[:3] == 'ma_':
            # end the action in the main hand function, not in this function
            return None  # this is correct to return None - do not change it.

        # I don't have much, check/fold
        if not self.guy_to_right_bet_size:
            return 'CALL', 'I_have_nothing_checking', 'I_have_nothing_I_check'
        else:
            return 'FOLD', 'I_have_nothing_folding', 'I_have_nothing_I_fold'



    def board_paired_on_turn(self, hu):
        """
        If board pairs on turn we deviate from most main hands, as straights and flushes become obsolete.
        But of course there is a chance that neither you nor opp hit trips or a house.
        But I won't play according to my actual hand - it will be more position play and bluffs, and repping in these cases.

        Strategy
        Multi-way should play quite straight forward; i.e. only continue or bet when you have it.
        Or if you are last/second last to act on the turn and were the aggressor on flop, then worth a bet potentially,
        depending on what others do. Otherwise, check/fold.

        I'll assume this function is for multi-way. Because the heads-up function will take care of playing heads up.
        And at the start of every main hand I'll check if I am heads up.

        """
        # Worth keeping track of and passing on your overcards to the paired card on the turn
        paired_card = None
        paired_card_tracker = set()
        turn_nums = [card[0] for card in self.turn]
        for card in turn_nums:
            if card not in paired_card_tracker:
                paired_card_tracker.add(card)
            else:
                paired_card = card
                break

        my_overcards_to_paired_card_on_turn = []
        for my_card in self.num_list:
            if my_card > paired_card:
                my_overcards_to_paired_card_on_turn.append(my_card)

        # If I have top full house, i.e. the absolute coconuts (not quite I lose to quads)
        if self.turn_num == self.flop[0][0]:  # e.g. 10 10 8 5; and I have 10 8 in my hand
            if self.turn[1][0] in self.num_list:
                if self.turn[2][0] in self.num_list:
                    return 'BET', 'bpot_I_have_top_full_house_nuts_currently', my_overcards_to_paired_card_on_turn

                # If I have second nut top full house
                elif self.turn[3][0] in self.num_list:
                    # I'm in position
                    if not self.positions_of_players_to_act_ahead_of_me:
                        # if checked to me
                        if not self.guy_to_right_bet_size:
                            return 'BET', 'bpot_second_top_full_house_checked_to_me_Im_in_position', my_overcards_to_paired_card_on_turn
                        else:
                            if self.SPR_tracker[self.my_position] <= 1:
                                return 'BET', 'bpot_SPR_is_very_low_I_have_second_nut_house', my_overcards_to_paired_card_on_turn
                            # this is a bluff catcher than anything else
                            elif self.SPR_tracker[self.my_position] >= 4:
                                return 'CALL', 'bpot_SPR_medium_I_have_second_nut_house', my_overcards_to_paired_card_on_turn
                            else:
                                overcards_in_my_hand = 0
                                for card in self.num_list:
                                    if card > self.turn[2][0]:
                                        overcards_in_my_hand += 1
                                    else:
                                        break
                                if overcards_in_my_hand >= 3:
                                    return 'CALL', 'bpot_SPR_decent_and_I_have_overcard_outs_and_second_nut_house', my_overcards_to_paired_card_on_turn
                    # I'm OOP with second nut top full house
                    else:
                        if not self.guy_to_right_bet_size:
                            return 'CALL', 'bpot_second_nut_full_house_bet_into_me_I_call_checking', my_overcards_to_paired_card_on_turn
                            # TO DO: Add extra layer to see if opp bet on flop, because likely top two pair if they did
                        else:
                            # Here I must have checked to him and he bet
                            if self.SPR_tracker[self.my_position] >= 4:
                                return 'CALL', 'bpot_second_nut_full_house_bet_into_me_I_call', my_overcards_to_paired_card_on_turn
                            else:
                                # check how many overcards I have
                                overcards_in_my_hand = 0
                                for card in self.num_list:
                                    if card > self.turn[2][0]:
                                        overcards_in_my_hand += 1
                                    else:
                                        break
                                if overcards_in_my_hand >= 3:
                                    return 'CALL', 'bpot_SPR_decent_and_I_have_outs_and_second_nut_house', my_overcards_to_paired_card_on_turn

            # I have TOP TRIPS, no house; play passively if I'm OOP
            if not self.turn[2][0] in self.num_list:
                if not self.turn[3][0] in self.num_list:
                    # I'm IP
                    if not self.positions_of_players_to_act_ahead_of_me:
                        if not self.guy_to_right_bet_size:
                            if self.SPR_tracker[self.my_position] >= 4:
                                return 'BET', 'bpot_bet_high_SPR_checked_to_me_with_top_trips_I_am_in_position', my_overcards_to_paired_card_on_turn
                        else:
                            # I have top trips in position and it is bet into me
                            # check how many overcards I have
                            overcards_in_my_hand = 0
                            for card in self.num_list:
                                if card > self.turn[2][0]:
                                    overcards_in_my_hand += 1
                                else:
                                    break
                            if overcards_in_my_hand >= 3:
                                if self.guy_to_right_bet_size <= 4 * self.stack_tracker[self.my_position]:
                                    return 'CALL', 'bpot_three_or_more_overcards_with_top_trips', my_overcards_to_paired_card_on_turn
                    # I'm OOP
                    else:
                        if not self.guy_to_right_bet_size:
                            return 'CALL', 'bpot_checking_top_trips_with_others_to_act_ahead_of_me', my_overcards_to_paired_card_on_turn
                        else:
                            # I have top trips out of position, I checked and they bet
                            # check how many overcards I have
                            overcards_in_my_hand = 0
                            for card in self.num_list:
                                if card > self.turn[2][0]:
                                    overcards_in_my_hand += 1
                                else:
                                    break
                            if overcards_in_my_hand >= 3:
                                if self.guy_to_right_bet_size <= 4 * self.stack_tracker[self.my_position]:
                                    return 'CALL', 'bpot_three_or_more_overcards_with_top_trips', my_overcards_to_paired_card_on_turn
                            else:
                                # call once see what opp wants to do on river
                                if self.guy_to_right_bet_size <= 4 * self.stack_tracker[self.my_position]:
                                    return 'CALL', 'bpot_I_have_trips_only_calling_to_see_what_opp_wants_to_do_on_river_bluff_catching', my_overcards_to_paired_card_on_turn

        # Any smaller house - I'll treat them all the same ; e.g. 10 9 9 8, and I have 9 8 or 9 10
        # At this point I know the board has paired and it hasn't paired the top card
        else:
            # check if I have normal full house, e.g. 10 9 9 8, and I have 9 8 or 9 10
            if paired_card in self.num_list:
                turn_nums_excluding_paired_card = [card for card in turn_nums if card != paired_card]
                if turn_nums_excluding_paired_card[0] in self.num_list:
                    # Here I have the biggest full house that is not an overfull house, i.e. thr 10 9 in the example above

                    # I'm IP
                    if not self.positions_of_players_to_act_ahead_of_me:
                        # checked to me
                        if not self.guy_to_right_bet_size:
                            # only lose to over_full house
                            if self.SPR_tracker[self.my_position] <= 1:
                                return 'BET', 'bpot_very_low_SPR_I_have_house', my_overcards_to_paired_card_on_turn
                            elif self.SPR_tracker[self.my_position] > 4:
                                return 'BET', 'bpot_highish_SPR_I_have_house', my_overcards_to_paired_card_on_turn
                            else:
                                return 'BET', 'bpot_awkward_SPR_check_call_river', my_overcards_to_paired_card_on_turn
                        # if it's bet into me
                        else:
                            if self.SPR_tracker[self.my_position] <= 1:
                                return 'BET', 'bpot_SPR_very_low_I_have_house', my_overcards_to_paired_card_on_turn
                            elif self.SPR_tracker[self.my_position] >= 4:
                                return 'CALL', 'bpot_SPR_high_enough_for_a_call_bet_into_me', my_overcards_to_paired_card_on_turn

                    # I'm OOP
                    else:
                        if not self.guy_to_right_bet_size:
                            return 'BET', 'bpot_betting_full_house_only_over_full_house_beats_me', my_overcards_to_paired_card_on_turn
                        else:
                            if self.SPR_tracker[self.my_position] >= 4:
                                # If opponent bets full pot on the river when nothing changed, then you can consider foldering,
                                # because they will be scared of overfull house too if they did not have it
                                return 'BET', 'bpot_betting_full_house_only_over_full_house_beats_me', my_overcards_to_paired_card_on_turn

                elif any(card in turn_nums_excluding_paired_card for card in self.num_list):
                    # I have a smaller full house
                    # I'm IP
                    if not self.positions_of_players_to_act_ahead_of_me:
                        # checked to me
                        if not self.guy_to_right_bet_size:
                            # only lose to over_full house
                            if self.SPR_tracker[self.my_position] <= 1:
                                return 'BET', 'bpot_very_low_SPR_I_have_smaller_house', my_overcards_to_paired_card_on_turn
                            elif self.SPR_tracker[self.my_position] > 4:
                                return 'BET', 'bpot_highish_SPR_I_have_smaller_house', my_overcards_to_paired_card_on_turn
                            else:
                                return 'CALL', 'bpot_awkward_SPR_checking_with_smaller_full_house', my_overcards_to_paired_card_on_turn
                        # if it's bet into me
                        else:
                            if self.SPR_tracker[self.my_position] <= 1:
                                return 'BET', 'bpot_SPR_very_low_I_have_house', my_overcards_to_paired_card_on_turn
                            elif self.SPR_tracker[self.my_position] >= 4:
                                return 'CALL', 'bpot_SPR_high_enough_for_a_call_bet_into_me', my_overcards_to_paired_card_on_turn

                    # I'm OOP
                    else:
                        if not self.guy_to_right_bet_size:
                            return 'CALL', 'bpot_checking_with_smaller_full_house', my_overcards_to_paired_card_on_turn
                        else:
                            if self.SPR_tracker[self.my_position] >= 4:
                                # If opponent bets full pot on the river when nothing changed, then you can consider foldering,
                                # because they will be scared of overfull house too if they did not have it
                                return 'BET', 'bpot_calling_bet_small_full_house_decent_SPR_bluff_catcher', my_overcards_to_paired_card_on_turn

                else:
                    # I rushed the below come back later to add more information
                    # I have trips
                    if self.SPR_tracker[self.my_position] >= 3:
                        # I am IP
                        if not self.positions_of_players_to_act_ahead_of_me:
                            if not self.guy_to_right_bet_size:
                                return 'BET', 'bpot_betting_my_trips_checked_to_me_decent_SPR', my_overcards_to_paired_card_on_turn
                            else:
                                # TO DO: worth adding a check how many overcards, may be worth one call or as a bluff catcher.
                                return 'FOLD', 'bpot_folding_trips_as_raised_or_bet_into_me', my_overcards_to_paired_card_on_turn
                        # I am OOP
                        else:
                            if self.guy_to_right_bet_size:
                                # Think twice about this call - I don't like calling in general but maybe once if SPR is decent here as bluff catcher
                                return 'CALL', 'bpot_calling_bet_out_of_position_I_have_trips', my_overcards_to_paired_card_on_turn
                            else:
                                # N.B. THERE IS A DIFFERENCE BETWEEN THIS SCENARIO AND THE ABOVE ONE - IF THIS flopped='bpot_checking_my_trips_I_am_OOP'
                                # gets passed to the river that means that the opp checked back, but if the above flopped == 'bpot_calling_bet_out_of_position_I_have_trips'
                                # gets passed to the river it means that the opp bet and i called!
                                return 'CALL', 'bpot_checking_my_trips_I_am_OOP', my_overcards_to_paired_card_on_turn

                    else:
                        # TO DO: add code here if SPR is higher cba for MVP
                        if not self.guy_to_right_bet_size:
                            return 'CALL', 'bpot_checking_trips', my_overcards_to_paired_card_on_turn



                    # TO DO: Worth adding a scenario here where OPP's SPR is low like < 1, the just shove on him.

        # 'Top' full house, e.g. 10 9 9 8 or 10 9 8 8, and I have 10 10 or 9 9  in my hand
        num_cards_flop = [self.flop[1][0], self.flop[2][0]]
        if self.turn_num in num_cards_flop:
            if self.num_list.count(self.flop[0][0]) >= 2 or self.num_list.count(self.flop[1][0]) >= 2:
                return 'BET', 'bpot_top_full_house_bet_half_pot', my_overcards_to_paired_card_on_turn

        trip_card = self.turn_num
        # quads
        trips_counter = 0
        for card in self.num_list:
            if card == trip_card:
                trips_counter += 1
        if trips_counter == 2:
            return 'CALL', 'bpot_checking_quads_to_bet_on_river', my_overcards_to_paired_card_on_turn

        # Check if I have hit any bottom full houses
        bottom_full_house = False
        bottom_full_house2 = False
        # 'Bottom' full house, e.g. turn 10 10 9 8, and I have 9 9 or 8 8 in my hand ;
        if trip_card == self.flop[0][0]:
            num_cards_for_bottom_full_house = [self.flop[1][0], self.flop[2][0]]
            if self.num_list.count(num_cards_for_bottom_full_house[0]) >= 2 or self.num_list.count(num_cards_for_bottom_full_house[1]) >= 2:
                bottom_full_house = True
        elif trip_card == self.flop[1][0]:  # 10 9 9 8, and I have 8 8 in my hand
            num_card_for_bottom_full_house = self.flop[2][0]
            bottom_full_house2 = True if self.num_list.count(num_card_for_bottom_full_house) >= 2 else False

        if bottom_full_house or bottom_full_house2:
            # I'm IP
            # TO DO: Need to add who was aggressor on previous street - pretty important.
            # This will play a huge roll in terms of deciding whether or not to continue firing.
            if not self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    if self.SPR_tracker[self.my_position] >= 4:
                        return 'BET', 'bpot_betting_bottom_full_house_IP_checked_to_me', my_overcards_to_paired_card_on_turn

                    return 'CALL', 'bpot_checking_bottom_full_house_no_value_in_betting', my_overcards_to_paired_card_on_turn
                else:
                    # bluff catcher; bottom full house guy bet into me - they could be betting with trips and I remove house outs
                    if self.guy_to_right_bet_size <= 4 * self.stack_tracker[self.my_position]:
                        return 'CALL', 'bpot_calling_with_bottom_full_house_IP_bet_into_me', my_overcards_to_paired_card_on_turn

                    if self.stack_tracker[self.my_position] <= 1:
                        # Careful, this could be a big bet, and if opp was aggressor on prebious street he could have
                        # top full house - especially if it was 3-bet or more.
                        return 'CALL', 'bpot_calling_with_bottom_full_house_very_low_SPR', my_overcards_to_paired_card_on_turn

            # I'm OOP
            else:
                if not self.guy_to_right_bet_size:
                    return 'CALL', 'bpot_checking_bottom_full_house_Im_OOP', my_overcards_to_paired_card_on_turn
                else:
                    if self.guy_to_right_bet_size <= 4 * self.stack_tracker[self.my_position]:
                        # this is a bluff catcher, see what opp does on river
                        return 'CALL', 'bpot_calling_a_bet_OOP_bottom_full_house', my_overcards_to_paired_card_on_turn

        # If I have nothing but checked to me and I am in position and aggressor on flop, and a
        # lower card (not highest card) paired
        if not self.positions_of_players_to_act_ahead_of_me and not self.guy_to_right_bet_size:
            # TO DO: add a check here to see if I was the aggressor on flop, only do below if I was aggressor.
            if self.SPR_tracker[self.my_position] >= 3:
                return 'BET', 'bpot_I_have_nothing_but_checked_to_me_Im_in_position', my_overcards_to_paired_card_on_turn

        # if hu:
        #     return self.analyse_heads_up_on_turn()

        # I don't have much, check/fold
        if not self.guy_to_right_bet_size:
            return 'CALL', 'checking_not_strong_enough_to_bet', 'checking_not_strong_enough_to_bet'
        else:
            return 'FOLD', 'I_have_nothing_folding', 'I_have_nothing_I_fold'

    def flush_completed_on_turn_play(self):
         # if I have the nut flush; simply bet
        for card_index in range(len(self.num_list)):
            if (self.nut_flush_nums_turn, self.suit_of_flush_turn) == (self.num_list[card_index], self.suit_list[card_index]):
                return 'BET', 'fcot_betting_my_nut_flush_on_the_turn', 'place_holder'

        # if I have some flush but not the nut flush
        if self.my_highest_num_of_the_completed_flush_on_turn:
            # I am out of position
            if self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    return 'CALL', 'fcot_checking_my_flush_on_the_turn', 'place_holder'
                else:
                    # add check here that if it is the guy in absolute position that bet and my flush is highish then call - randomiser
                    return 'FOLD', 'fcot_folding_my_flush_to_a_bet_on_the_turn', 'place_holder'
            # I am in position
            else:
                if not self.guy_to_right_bet_size:
                    # If I have a highish flush, worth betting for some value
                    # TO DO: check how high my flush is to bet here, but checking for now for MVP
                    return 'CALL', 'fcot_checking_my_flush_on_the_turn', 'place_holder'
                else:
                    # worth adding some calls here.
                    return 'FOLD', 'fcot_folding_my_flush_to_a_bet', 'place_holder'

        # I do not have the flush
        if not self.guy_to_right_bet_size and not self.positions_of_players_to_act_ahead_of_me:
            return 'BET', 'representing_the_nut_flush_but_I_have_no_flush', 'place_holder'






    def flush_completed_on_turn_play_turn_exploit(self, flopped, card_helper):
        """
        EXPLOIT
        """
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            if not self.positions_of_players_to_act_ahead_of_me:
                if lowest_spr >= 2:
                    return 'BET', 'fcot_flush_completed_on_turn_checked_to_me_I_am_betting_in_position', 'bet_turn'
            else:
                if lowest_spr >= 2:
                    return 'BET', 'fcot_flush_completed_on_turn_checked_to_me_I_am_betting_one_person_ahead_to_act', 'bet_turn'

    def flush_completed_on_flop_turn_play(self, flopped, card_helper):
        """
        EXPLOIT
        """
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            if not self.positions_of_players_to_act_ahead_of_me:
                if lowest_spr >= 2:
                    return 'BET', 'fcof_I_bet_on_flop_it_was_called_I_am_in_position_betting_turn', 'bet_flop_betting_turn'
            else:
                if lowest_spr >= 2:
                    return 'BET', 'fcof_I_bet_on_flop_it_was_called_one_guy_to_act_ahead_betting_turn', 'bet_flop_betting_turn'

    def straight_completed_on_flop_turn_play(self, flopped, card_helper):
        """
        EXPLOIT

        At this point I've checked that no flush got there and board did not pair,
        so don't need to worry about those here.

        One thing worth considering later is if a higher straight got there.
        """
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if flopped == 'scof_checked_to_me_in_position_closed_straight_competed_on_flop':
            if lowest_spr >= 2:
                return 'BET', 'scof_checked_to_me_on_flop_and_turn_I_am_in_position_betting', 'bet_flop_betting_turn'
            else:
                return 'CALL', 'scof_SPR_is_low_checking_to_maybe_bet_on_river_if_opp_checks_again', 'bet_flop_check_turn'

        if flopped == 'scof_checked_to_me_one_guy_to_act_closed_straight_competed_on_flop_at_least_two_gapper':
            if not self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    if lowest_spr >= 2:
                        return 'BET', 'scof_betting_turn_checked_to_me_in_position_closed_straight_at_least_two_gapper', 'bet_flop_betting_turn'
            else:
                # not so sure if someone is in position of me, I think still bet and maybe give up on river
                if not self.guy_to_right_bet_size:
                    if lowest_spr >= 2:
                        return 'BET', 'scof_betting_turn_checked_to_me_one_guy_ahead_to_act_closed_straight', 'bet_flop_betting_turn'

        if flopped == 'scof_checking_open_straight_in_position':
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'scof_betting_open_straight_from_flop_checked_to_me_on_flop_and_turn', 'check_flop_bet_turn'

        if flopped == 'scof_checking_open_straight_one_guy_ahead_to_act':
            if not self.guy_to_right_bet_size:
                return 'CALL', 'scof_checking_open_straight_from_flop_one_guy_to_act_ahead_of_me', 'check_flop_check_turn'

    def board_paired_on_turn_play_turn_exploit(self, flopped, card_helper):
        """
        EXPLOIT

        this is if the board paired on the turn - it is to help the straight completed on flop function.

        In this case either someone has it or they don't, and it would be hard for them to continue with just a straight.
        SO I think bet it on turn if they call give up on river.
        """
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            # I thought about splitting it out into whether someone ahead of me to act, but even if there is I would play it like this
            # where I bet on turn and if called I would check give up on river.
            # Though on river there is a case to randomise it, in case someone did call with just a straight.
            if lowest_spr >= 2:
                return 'BET', 'bpot_representing_straight_on_flop_board_paired_on_turn_checked_to_me_I_am_betting', 'bet_turn'

    def dry_board_on_flop_turn_play(self, flopped, card_helper):
        """
        EXPLOIT

        Need to add straight completed on turn check, so if we are here no straight completed on turn
        """
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            if lowest_spr >= 2:
                return 'BET', 'dbof_dry_board_on_flop_nothing_changed_on_turn_checked_to_me_betting_again', 'bet_flop_turn'



    def board_paired_on_flop_turn_play(self, flopped, card_helper):
        """
        EXPLOIT
        """

        # TO DO: verify that checking the SPR in this way is okay, when running against real thing
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        # low_paired_card_high_non_paired_card
        if flopped == 'bpof_calling_bet_on_flop_low_paired_high_non_paired':
            if not self.guy_to_right_bet_size:
                return 'BET', 'bpof_opp_bet_on_flop_checked_on_turn_I_am_betting_low_paired_high_non_paired', 'opp_bet_on_flop_checked_on_turn'
            else:
                if self.stack_tracker[self.guy_to_right_bet_position] >= 2 * self.guy_to_right_bet_size:
                    return 'CALL', 'bpof_opp_bet_on_flop_bet_on_turn_I_call_to_see_river', 'opp_bet_flop_and_turn'
                else:
                    return 'FOLD', 'bpof_opp_bet_on_flop_bet_on_turn_folding_SPR_not_enough_to_catch_him_on_river', 'opp_bet_flop_and_turn'

        if flopped == 'bpof_betting_on_flop_checked_to_me_in_position_low_paired_high_non_paired' or \
                flopped == 'bpof_betting_on_flop_checked_to_me_one_guy_ahead_of_me_to_act_low_paired_high_non_paired':
            # may be worth checking if the guy who called is in position to you; but I think I will bet either way in SPR is enough

            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_opp_called_flop_bet_and_checked_turn_again_I_am_betting_low_paired_high_non_paired_and_low_paired_high_non_paired', 'opp_called_my_flop_bet_I_am_betting_turn'

        # high_paired_card_low_non_paired_card
        if flopped == 'bpof_betting_flop_checked_to_me_in_position_high_pair_low_non_pair':
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_opp_checked_to_me_twice_on_flop_and_turn_I_am_betting_high_pair_low_non_pair', 'betting_flop_and_turn'
                else:
                    # Not so sure about this play - the story is a bit off here; i.e. bet check bet.
                    return 'CALL', 'bpof_SPR_less_than_2_on_turn_planning_to_pot_river_if_checked_to_me_then', 'I_bet_on_flop_checked_on_turn'
            else:
                if lowest_spr >= 2:
                    return 'CALL', 'opp_story_does_not_make_sense_checking_flop_to_bet_turn_I_am_calling_to_bet_on_river_if_he_checks', 'I_bet_on_flop_call_on_turn'

        if flopped == 'bpof_calling_bet_on_flop_high_paired_low_non_paired':
            # I'll leave this case out, but need to check if the turn nums is higher than the non-paired card from the flop
            # if so and checked to you then bet.
            pass

        if flopped == 'bpof_betting_flop_checked_to_me_one_guy_to_act_ahead_of_me_high_pair_low_non_pair':
            # if we are here check if the guy who called is the one in position to us.
            # because then our check of self.guy_to_right_bet_size could be meaningless if it is heads up and just us 2
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_betting_turn_my_flop_bet_was_called_and_then_checked_to_me_on_turn_high_pair_low_non_pair', 'I_bet_flop_bet_turn'

        # high_paired_card_high_non_paired_card
        if flopped == 'bpof_betting_flop_checked_to_me_in_position_high_pair_high_non_pair' \
            or flopped == 'bpof_betting_flop_checked_to_me_one_guy_to_act_ahead_of_me_high_pair_high_non_pair':
            # TO DO: worth checking if the guy who called is in position to me
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_bet_flop_was_called_betting_turn_high_pair_high_non_pair', 'I_bet_flop_and_turn'
                else:
                    return 'CALL', 'bpof_SPR_is_low_checking_turn_to_bet_river_potentially_high_pair_high_non_pair', 'I_bet_flop_checked_turn'

        # low_paired_card_low_non_paired_card
        if flopped == 'bpof_betting_flop_checked_to_me_in_position_low_pair_low_non_pair' \
                or flopped == 'bpof_betting_flop_checked_to_me_one_guy_to_act_ahead_of_me_low_pair_low_non_pair':
            # TO DO: worth checking if opp is guy in position of us
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_bet_flop_was_called_betting_turn_low_pair_low_non_pair', 'I_bet_flop_and_turn'

        if flopped == 'bpof_calling_bet_on_flop_in_position_low_paired_low_non_paired':
            # TO DO: add check here if turn card is higher than non-paired flop card
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_bet_flop_was_called_betting_turn_low_paired_low_non_paired', 'I_bet_flop_and_turn'
                else:
                    return 'CALL', 'bpof_SPR_is_low_checking_turn_to_bet_river_potentially_low_paired_low_non_paired', 'I_bet_flop_checked_turn'

        # adding a catch all where if I am in position, checked to me and SPR is high enough I will just bet and see what happens
        if not self.positions_of_players_to_act_ahead_of_me:
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_default_hit_where_its_checked_to_me_in_position_and_spr_greater_than_2_low_pair_low_non_pair', 'betting_turn_default_play_was_hit'


        # I don't have much, check/fold
        if not self.guy_to_right_bet_size:
            return 'CALL', 'sh1_I_have_nothing_checking', 'I_have_nothing_I_check'
        else:
            return 'FOLD', 'sh1_I_have_nothing_folding', 'I_have_nothing_I_fold'

    def straight_completed_on_turn_turn_play(self, flopped, card_helper):
        """
        EXPLOIT

        """
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            if lowest_spr >= 2:
                return 'BET', 'scot_checked_to_me_on_turn_straight_completed_betting', 'bet_turn'


    def analyse_my_hand_against_turn(self, action_on_flop, extra_information):
        """
        flop_action will be 'BET' or 'CALL' - tells us what we did on the flop

        card_helper is a dict() that holds what we flopped as the key, and helper cards as the values.
        e.g. ... card_helper('flopped_straight_draw': (9,7), 'flopped_wrap': (10,9,7), 'flopped_set': 'flopped_top_set', 'SPR_low': True)

        All possible keys for card_helper:
        1. flopped_straight_draw
        2. flopped_wrap
        3. flopped_set
        4. SPR_low
        5. flopped_nut_flush_draw
        6. flopped_nut_flush
        ---------------------------------------------------------

        It's quite important to know on the turn in general the SPR of the person who bet and anyone who called.
        Because if it is small, then a fold should be a call many times.

        Assumption: I'll buy in for the max (60) and I'll make decisions based on this.

        SPR = 1 : 30 in pot (30 in my stack)
        SPR = 2 : 20 in pot (40 in my stack)
        SPR = 3 : 15 in pot (45 in my stack)
        SPR = 4 : 12 in pot (48 in my stack)
        SPR = 5 : 10 in pot (50 in my stack)
        SPR = 7 : 7.5 in pot (52.5 in my stack)
        SPR = 9 : 6 in pot (54 in my stack)
        SPR = 11 : 5 in pot (55 in my stack)
        SPR = 19 : 3 in pot (57 in my stack)
        """


        # EXPLOIT plays from flop
        if flopped[:6] == 'bpof_':
            print('board paired on flop detected, so running board paired on turn')
            return self.board_paired_on_flop_turn_play(flopped, card_helper)

        if flopped[:6] == 'fcof_':
            return self.flush_completed_on_flop_turn_play(flopped, card_helper)

        # EXPLOIT if we were representing completed straight on flop but flush or board paired on turn
        # Specifically if from flop we were representing a completed straight but flush got there or board paired
        if self.did_board_pair_on_turn_f:
            return self.board_paired_on_turn_play_turn_exploit(flopped, card_helper)

        if self.did_flush_completed_on_turn:
            return self.flush_completed_on_turn_play_turn_exploit(flopped, card_helper)

        if flopped[:6] == 'scof_':
            return self.straight_completed_on_flop_turn_play(flopped, card_helper)

        # Add a check if straight completed on turn; this will impact dry_board on flop play
        if self.did_straight_complete_on_turn:
            return self.straight_completed_on_turn_turn_play(flopped, card_helper)

        if flopped[:5] == 'dbof_':
            return self.dry_board_on_flop_turn_play(flopped, card_helper)
