"""
Wworth starting by checking what the nuts is at the start of the river analiysis!
- quads
- house
- flush
- straight
- set
"""
from collections import defaultdict

from analyse_my_hand_on_turn import AnalyseMyHandOnTurn
from flop_turn_river_cards import TheRiver
TR = TheRiver()


class AnalyseMyHandOnRiver(AnalyseMyHandOnTurn):
    def __init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                 positions_of_players_to_act_ahead_of_me,
                 pot_size, my_position, num_list, suit_list, big_blind):
        # As a learning point, the order of the below matters, so if you initialize self.special_hand1 before self.flop - you will get an error
        # since self.special_hand1 uses self.flop in it's function - makes perfect sense.
        AnalyseMyHandOnTurn.__init__(self, stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                     positions_of_players_to_act_ahead_of_me,
                                     pot_size, my_position, num_list, suit_list, big_blind)

        self.organise_river_f = self.organise_river()
        self.river = self.organise_river_f[0]
        self.river_num = self.organise_river_f[1]
        self.river_suit = self.organise_river_f[2]
        self.positions_of_players_to_act_ahead_of_me_f = positions_of_players_to_act_ahead_of_me

        # self.river = [[10, 'S'], [8, 'C'], [8, 'H'], [6, 'S'], [2, 'C']]
        # self.river_num = 10
        # self.river_suit = 'S'

        # check if there are any completed straights on the river - simple check
        self.any_straight_completed_on_river_f = self.any_straight_completed_on_river()
        self.did_any_straight_complete_on_river = self.any_straight_completed_on_river_f[0]
        self.three_cards_combis_that_make_straight_on_river = self.any_straight_completed_on_river_f[1]

        # Considers if straight is made on turn if river changes nuts or if no straight on turn if river completed any straights
        # and it returns all the 2 card combinations that complete those straights.
        self.all_two_card_combis_completing_straights_on_river = self.did_river_complete_any_straights_or_change_nuts_of_completed_straights()

        # check if flush completed on river, and the suit of the flush if so
        self.flush_complete_on_river = self.flush_completed_on_river()
        self.did_flush_complete_on_river = self.flush_complete_on_river[0]
        self.nut_flush_nums_river = self.flush_complete_on_river[1]  # N.B. This is not the largest nums of the flush on the board; e.g. [14, 13, 10, 2] all hearts; then this would be 12 of hearts.
        self.suit_of_flush_river = self.flush_complete_on_river[2]

        # check if I hit a flush on river; if I did, return the number of the highest flush card otherwise return False if I do not have the flush
        self.my_highest_num_of_the_completed_flush_on_river = self.did_I_hit_flush_on_river(self.river_suit)

        # check if I hit the nut straight or any straight on river
        self.did_I_hit_straight_on_river_f = self.did_I_hit_straight_on_river()

        # check if the board paired on the river - this will simply return True or False
        self.did_board_pair_on_river_f = self.did_board_pair_on_river()


    def any_straight_completed_on_river(self):
        """
        Analyse the river nums and check if any possible straight is present on the turn.

        Do this by checking 3 cards at a time, and since it is sorted we need to check 3 lots of 3.

        There is only a straight when the gap between the 3 cards is no more than 4.
        e.g. 10, 7, 6 or 10, 8, 6

        self.turn looks like [[13, 'S'], [10, 'C'] [9, 'S'], [8, 'C']]
        """
        river_nums = [num[0] for num in self.river]
        three_card_combis_that_complete_straight_on_river = []
        if (river_nums[0] - river_nums[1]) + (river_nums[1] - river_nums[2]) <= 4:
            if river_nums[0] != river_nums[1] and river_nums[1] != river_nums[2]:
                three_card_combis_that_complete_straight_on_river.append(river_nums[:3])
        if (river_nums[1] - river_nums[2]) + (river_nums[2] - river_nums[3]) <= 4:
            if river_nums[1] != river_nums[2] and river_nums[2] != river_nums[3]:
                three_card_combis_that_complete_straight_on_river.append(river_nums[1:4])
        if (river_nums[2] - river_nums[3]) + (river_nums[3] - river_nums[4]) <= 4:
            if river_nums[2] != river_nums[3] and river_nums[3] != river_nums[4]:
                three_card_combis_that_complete_straight_on_river.append(river_nums[2:5])
        if three_card_combis_that_complete_straight_on_river:
            return True, three_card_combis_that_complete_straight_on_river
        return False, []

    def did_river_complete_any_straights_or_change_nuts_of_completed_straights(self):
        """
        ***The first half of the function builds on the scenario where there is already a straight on the turn.
        The second half considers the scenario when there is a straight draw on the flop and the turn comes in,
        and it checks if any straights are completed.

        N.B. To check if the river changed the nuts of the straight that is completed on the turn, you first need to
        grab the three straight making cards from the turn.
        It will either be the first three cards or the second/third/fourth card,
        e.g. for 9 8 7 6 ; 9 8 7 and 8 7 6
             for 10 5 4 3 ; 5 4 3
             for 10 9 8 2 ; 10 9 8

        Cases to cover:
        1) There was a made straight on the turn (doesn't matter to us if the straight was completed on the flop or turn)
                - check if river changed the nuts
                - check if river did not change the nuts
        2) No straight on turn but straight made with the river card.

        - (One edge case to consider, if we have something like 10 9 5 4 ; and the 7 hits on the river;
        this is not the case often but often enough to consider, as it completes the top and bottom straight).
        So it makes sense to always return the nut straight then consider lower straights- both are useful info to have.

        Definitely worth looking at the obvious straight draws on turn if there are any.
        This will determine a lot of thing for me.
        (TO DO FOR LATER - MAYBE NOT FOR MVP - CONSIDERATION IS QUITE DEEP)
        For MVP I'll just consider the above two main cases.
        """
        river_nums = [card[0] for card in self.river]
        all_two_card_straight_completing_combinations = []
        three_card_straight_possibility = []

        # not sure how this fits, but if board pairs, just return False, because straight doesn't matter
        # having this check simplifies the logic below by a lot so don't remove
        # N.B. only one other function calls this function - none of my hands call this function directly.
        # the function that calls this function is called a lot though.
        turn_nums = [card[0] for card in self.turn]
        if self.river_num in turn_nums:
            return False

        # straight already completed on the turn
        if self.did_straight_complete_on_turn:
             # if straight completed on turn, check which cards on the river made the straight;
             # first three or second,third,fourth or both
            if self.which_three_cards_on_turn_make_the_straight == 'first_three_cards_and_second_third_fourth_card' or self.which_three_cards_on_turn_make_the_straight == 'first_three_cards':
                # if both make the straight, then the nut straight only changes if the river card is larger than
                # the third card, but is still within the straight range.
                if river_nums[0] + 3 >= self.river_num > self.turn[2][0]:
                    # can reuse the generate_all_straight_possibilities from the turn
                    if self.which_three_cards_on_turn_make_the_straight == 'first_three_cards_and_second_third_fourth_card':
                        three_card_straight_possibility = [river_nums[:3], river_nums[1:4], river_nums[2:5]]
                    elif self.which_three_cards_on_turn_make_the_straight == 'first_three_cards':
                        three_card_straight_possibility = [river_nums[:3], river_nums[1:4]]
                else:
                    # if its not within the 'range' to change the nut straight then just return the nut straight two card combi
                    # from the turn
                    return True, self.all_two_card_straight_completing_combinations_on_turn

            elif self.which_three_cards_on_turn_make_the_straight == 'second_third_fourth_card':
                # if the straight on the turn is made with the second, third and fourth card on the board
                # then the river will change the nuts of the straight if it is larger than the last turn card
                # but still within range of the straight, i.e. no larger than 3 of the second card on the board
                if self.river_num > self.turn[3][0]:
                    if self.river_num <= river_nums[1] + 3:
                        three_card_straight_possibility = [river_nums[1:4], river_nums[2:5]]

            if not three_card_straight_possibility:
                print('something went wrong with straight calculation')
                breakpoint()
            for three_cards in three_card_straight_possibility:
                all_two_card_straight_completing_combinations.append(self.generate_all_straight_possibilities(three_cards))

            # sometimes all_two_card_straight_completing_combinations above is two lists like this: [[(11, 9), (9, 6)], [(10, 9), (9, 5), (5, 4)]]
            # but we want it to be one list, so join the lists into one
            if len(all_two_card_straight_completing_combinations) > 1:
                all_two_card_straight_completing_combinations = [y for x in all_two_card_straight_completing_combinations for y in x]

            return all_two_card_straight_completing_combinations

        else:
            # if no straight on turn but straight completed on the river
            # Check if straight is present on river
            # Then grab all the 3 card combis that make a straight and generate all the 2 card combis that complete the straight
            if self.did_any_straight_complete_on_river:
                for three_cards in self.three_cards_combis_that_make_straight_on_river:
                    all_two_card_straight_completing_combinations.append(self.generate_all_straight_possibilities(three_cards))

            # Since there is straight, there must be 3 cards that make the straight
            if self.did_any_straight_complete_on_river and not self.three_cards_combis_that_make_straight_on_river:
                print('something went wrong with straight calculation')
                breakpoint()

            return all_two_card_straight_completing_combinations

    def did_I_hit_straight_on_river(self):
        """
        This function looks at all of the potential straights on the river, and by calling on
        self.did_river_complete_any_straights_or_change_nuts_of_completed_straights; it returns all
        two card combinations that complete the straights; it is in nutted order, so the first item in the
        list will be the nut straight.
        """
        all_two_card_straight_completing_combinations = []

        all_two_card_straight_completing_combinations = self.did_river_complete_any_straights_or_change_nuts_of_completed_straights()
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

    def did_board_pair_on_river(self):
        """
        This function will return True if the river card paired the board.
        """
        turn_nums = [card[0] for card in self.turn]
        if self.river_num in turn_nums:
            return True
        return False

    def organise_river(self):
        """
        turn will look like: [[13, 'S'], [10, 'C'], [9, 'S'], [8, 'C']] ; after we sort it.
        """
        river_generator = TR.add_river_card_num_and_suit_to_turn(self.turn)  # all we need to do here is to sort by number as we want the turn nums to still be in descending order
        river = river_generator[0]
        river_num = river_generator[1]
        river_suit = river_generator[2]

        return river, river_num, river_suit

    def nuts_on_the_river(self):
        """
        This function is to check what the nuts is on the river - doesn't mean I have it.
        This is good to know because if I do have it, then I can go nuts.

        But for 99% of time, this will be useful as a quick check in the main hand whether I have the nuts,
        in particular the nut straight, because straights can change so easily.

        Then 1%, but a very important 1% is to check things like a straight flush and other more
        obscure hands, which I haven't really factored into my main hands.
        This can come in handy, when you are facing a weird raise on the river when I think I have the nuts,
        but there is a straight flush out there, then I can assume quite safely what the other person has.

        See the_nuts.py; will code this fully last, because I think I'll cover a lot of things like flushes
        and straights in other hands, so no need to code it twice.
        """
        return

    def flush_completed_on_river(self):
        """
        This function will return True if a flush completed on river, it will return the suit of the flush, and
        whatever the nut flush nums card is.
        (R)!!! - note that nut flush nums is NOT the highest num on the board that has that suit.
        e.g. [14, 13, 12, 2] and they are all 'hearts' or whatever suit, then this function will return 11!!

        TO DO: wondering if I should just check self.did_flush_complete_on_turn and if so just check that
        the river card did not change the nut flush nums, and if not then just return the same thing on the river.
        """

        nut_flush_num = None
        river_suits = [card[1] for card in self.river]
        suit_counter = defaultdict(int)

        for suit_card in river_suits:
            suit_counter[suit_card] += 1

        for suit_card in suit_counter:
            if suit_counter[suit_card] >= 3:
                # N.B. The way to find the nut nums of the flush is simply to iterate from 14 down
                # and the first card that you do not find of that suit on the board is the nut flush
                for num in reversed(range(15)):  # iterates from 14
                    if [num, suit_card] not in self.river:
                        nut_flush_num = num
                        break
                return True, nut_flush_num, suit_card
        return False, False, False

    def did_I_hit_flush_on_river(self, flush_suit):
        """
        This function returns a number indicating how high my flush is, if I don't have the flush it will return False.

        Check that there wasn't a flush already on the flop or turn.
        This is important, because I am passing in the 'turn_suit' into this function, so it would be WRONG
        to do this if there is already a flush on the flop!!
        N.B. if flush completed on turn I would NOT be here, because if flush completes on turn it goes off
        into its own function and it returns some action there and on the river it takes over from there.

        HOWEVER, on the flop, I didn't introduce this idea of checking board pairing/flush completing/straight completing
        at the start of every hand - but this is something that I think wioll be very beneficial.
        """
        # check that there wasn't a flush completed on the flop
        if not self.did_flush_completed_on_flop and not self.did_flush_completed_on_turn:
            if self.did_flush_complete_on_river:
                highest_flush_num = None
                for pos, card in enumerate(self.num_list):
                    if self.suit_list[pos] == flush_suit:
                        highest_flush_num = card
                        break  # we want first instance where the card suit matches the flush_suit, as this is the highest num of that suit

                # check I have at least two cards of the flush suit - otherwise I don't have a flush!
                if self.suit_list.count(flush_suit) >= 2:
                    return highest_flush_num
        return False

    def flush_completed_on_river_play(self):
        """
        This is when the river card completes the flush, and there wasn't a flush completed on previous streets.
        Then this function is called - it is called at the start of every main hand, including final_check.
        (N.B. we have a separate path if flush completed on flop or turn - or at least turn)

        I think if the flush gets there on the river, in any main hand (and the board is not paired) -
        board pair is always checked first in any hand so no need to check in this function.
        then it is a separate play, and the correct thing to do is consider what happened in previous
        streets, and play accordingly.
        If I have the nut flush then it's easy, but if not then should consider what happened previously.

        I should code this for the turn as well (ADDED for final_check, need to add for others too)

        Strategy is quite simply I think:
        - if I have nuts, then bet; can worth in other special scenarios after MVP
        - if I do not have nut flush;
            - if I have some flush;
                - check and call, especially if there was no flush draw on flop
                - randomise if I am in position and it is bet into me and the flush draw was not on flop
            - if I have no flush;
                - if I am in position and checked to me, randomiser to bet like 60% of the time (this strat works better if flush got there on turn)
                  as there is more fear that another bet is coming on river so ppl fold and play honestly.
                - if it is heads up increase the odds of the randomiser above to bet

        After MVP can add other checks like if there was a completed straight on the turn, etc.

        And other cases like if I have the nut flush blocker.
        (though again this is not as effective on the river as on the flop or turn since people will call down easier)
        """
        # note: no need to check if there is a flush on board - everywhere I call this function
        # I first check that there is a flush completed.

        # if I have the nut flush; simply check if I have the nut flush card and a flush
        for card_index in range(len(self.num_list)):
            if (self.nut_flush_nums_river, self.suit_of_flush_river) == (self.num_list[card_index], self.suit_list[card_index]):
                return 'BET', 'betting my nut flush on the river',

        # if I have some flush but not the nut flush
        if self.my_highest_num_of_the_completed_flush_on_river:
            # I am out of position
            if self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    return 'CALL', 'checking my flush on the river',
                else:
                    # add check here that if it is the guy in absolute position that bet and my flush is highish then call - randomiser
                    return 'FOLD', 'folding my flush to a bet on the river',
            # I am in position
            else:
                if not self.guy_to_right_bet_size:
                    # If I have a highish flush, worth betting for some value
                    return 'CALL', 'checking my flush on the river',
                else:
                    # worth adding some calls here.
                    return 'FOLD', 'folding my flush to a bet',

        # I do not have the flush
        if not self.guy_to_right_bet_size and not self.positions_of_players_to_act_ahead_of_me:
            return 'BET', 'representing the nut flush but I have no flush',

    def NOT_USED_ATM_helper_for_board_pair_function(self, card_helper, was_I_aggro_on_turn=False):
        """
        One thing that I refernce quite often on the river is if an overcard hits on the river and i have
        either hit the river card or missed it.
        Either case, I normally do the same thing, so code it once here so that I don't need to include it
        over and over again in the code.

        For now I won't use 'was_I_aggro_on_turn' but this can be quite important to decide what to do
        depending on what I did on turn.

        Not sure if I will incorporate this yet because some scenarios are slightly different.
        I haven'y added it to the code; if I do then delete this note.
        """
        # nuts changed on the river - i.e. it is overcards to the paired card OR it is lower than paired card
        # and it is the third card, i.e. a new nut house is available on the river.
        nuts_changed_on_river = False
        if self.river_num >= self.turn[0][0]:
            nuts_changed_on_river = True
        if self.river_num > self.turn_num:
            if self.river_num == self.turn[2][0]:
                nuts_changed_on_river = True

        # one deviation is whether I was the one who was aggresive on the turn, or I checked called (i.e. was more passive)
        # I'm in position
        if not self.positions_of_players_to_act_ahead_of_me:
            if not self.guy_to_right_bet_size:
                if nuts_changed_on_river:
                    if self.river_num in card_helper:
                        # e.g. 9 9 7 5 11 ; and I have 9 and 11 in my hand
                        return 'BET', 'I hit an overcard house on the river',
                else:
                    return 'CALL', 'checking down my non nut house',
            else:
                if nuts_changed_on_river:
                    if self.river_num in card_helper:
                        if not self.guy_to_right_bet_size:
                            return 'BET', 'I hit an overcard on the river; call ',
                        else:
                            # add check here - in case someone is raising with an over full house
                            return 'CALL', 'calling a check raised',
                    else:
                        # nut sure about this fold, think about it.
                        return 'FOLD', 'folding my third nut house',

    def main_check_flush_completed_on_turn_(self, flopped, card_helper):
        """
        This function is for when the flush completed on the turn - if flush completed on the turn
        then the board is 'locked up' so the way to play it will be similar/same every time.
        """
        if flopped == 'fcot_betting_my_nut_flush_on_the_turn':
            if not self.did_board_pair_on_river_f:
                # I have the nut flush still, should check for straight flush possibility if I get check raised
                if self.guy_to_right_bet_size:
                    if self.guy_to_right_bet_size > self.pot_size:  # this is if it is 3-bet
                        return 'FOLD', 'folding my nutish flush to what I suspect is a straight flush'
                    else:
                        return 'CALL', 'calling a bet, after I have coded to check no straight flush possible then can raise here',
                else:
                    return 'BET', 'betting my nut flush on the river',

        if flopped == 'fcot_checking_my_flush_on_the_turn' or flopped == 'fcot_checking_my_flush_on_the_turn':
            # I checked the turn with a flush and it was checked through
            if not self.guy_to_right_bet_size:
                return 'CALL', 'checking my non nut flush',
            else:
                if self.guy_to_right_bet_size > self.pot_size:  # this is if it is 3-bet
                    return 'FOLD', 'folding my nutish flush to what I suspect is a straight flush'
                else:
                    # can fold this sometimes to play tighter
                    return 'CALL', 'calling a bet, opp checked on the turn so I am calling as a bluff catcher',

        if flopped == 'representing_the_nut_flush_but_I_have_no_flush':
            # if here it means that I am in position and bet on the turn to rep the nut flush but it was called
            if self.guy_to_right_bet_size:
                return 'FOLD', 'tried to rep the nut flush by betting on the turn after it was checked to me and I am in position but it was called'
            else:
                # sometimes can give up here
                return 'BET', 'it was called on the turn when flush got there and I am in position and I bet, betting on the river to try and get fold'

    def analyse_final_check_on_river(self, flopped, card_helper):
        """
        This final check will as usual check the 3 main things that all main hands will check;
        1) did the board pair on river
        2) did a flush draw complete on the river
        3) did a straight complete and do I have the nut straight
        ** TO DO: when I write more main hands - consider just doing a function where the above 3 are checked
        rather than writing it out at the start of every hand.
        For MVP never mind, stick with this.

        Then it will continue all the hand from final_check on the turn.
        """
        # check if board paired as this renders wraps and straights useless for most part
        if self.did_board_pair_on_river_f:
            return self.board_paired_on_river(flopped, card_helper)

        # check if flush got there, as this renders wraps and straights useless for most part
        if self.did_flush_complete_on_river:
            return self.flush_completed_on_river_play()

        # check if straight got there, and if I have the nut straight, if so then bet
        if self.any_straight_completed_on_river_f:
            # checking this right at the start makes life much easier in the main hand.
            if self.did_I_hit_straight_on_river_f == 'I_have_nut_straight':
                return 'BET', 'betting my nut straight on the river',

        # This is a general scenario where I will rep the nut flush on turn; I am last to act checked to me on turn
        if flopped == 'fc_Im_IP_checked_to_me_flush_completed_I_have_top_set_representing_the_flush_SPR_is_decent':
            if not self.guy_to_right_bet_size:
                # if we are here it means that someone called the bet
                # add a check that if the bet amount is small, then raise - as this is what weaker hands would do
                return 'BET', 'betting to rep nut flush that completed on turn but I dont have it',

        # This is a general scenario where I will rep the nut straight; I am last to act checked to me
        if flopped == 'fc_Im_IP_checked_to_me_straight_completed_I_have_top_set_representing_the_nut_straight':
            # if we are here it means that someone called us on the turn when I am in position checked to me
            # I bet to rep the nut straight
            if not self.did_flush_complete_on_river:
                if not self.guy_to_right_bet_size:
                    return 'BET', 'representing the nut straight but I dont have it, in position checked to me',

        # on the flop I represented the flush on flop I'm IP and checked to me and I BET with top set on, I bet on turn
        if flopped == 'fc_bet_into_me_on_turn_checked_to_me_on_flop_I_have_set_trying_to_hit_river_or_bluff_catch':
            # if here it means board did not pair, so check fold
            if self.guy_to_right_bet_size:
                return 'FOLD', 'folding to a likely flush that opp hit or is representing',

        if flopped == 'fc_check_to_me_on_flop_and_turn_I_have_top_set_but_made_flush_on_flop_betting_to_rep':
            # randomiser here
            return 'BET', 'betting final street to rep the flush',

        # I have top set on flop with no straight or flushes made on the flop

            # remember paired board and flush completed taken care of at top of funtion
            # so here only need to check if straight completed and what to do in each scenario

            # e.g. if flopped = fc_flush_completed_bet_into_me_SPR_decent_im_calling_w_top_set
            # there is nothing to code here because we called on the flop hoping for board to pair
            # and if we are here it means it didn't pair! - so can leave it as we check/fold by default
        if flopped == 'fc_betting_top_set_when_flush_got_there_checked_to_me_repping_flush':
            # I was repping flush on turn when it got there
            if not self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    return 'BET', 'representing flush when it got there on turn and I bet on turn',

        # similarly for flopped == 'fc_checking_top_set_many_players_ahead_of_me_flush_comp_on_turn'
        # nothing to code because if board paired we would not be here, and we would check/fold, which is the default


        # if straight completed on turn
        if flopped == 'fc_checking_top_set_with_straight_completing':
            if not self.guy_to_right_bet_size:
                return 'CALL', 'checking my top set when straight complete don turn',

        if flopped == 'fc_no_obvious_st8_completed_checked_to_me_Im_betting_top_set':
            if not self.did_any_straight_complete_on_river:
                if not self.positions_of_players_to_act_ahead_of_me:
                    if not self.guy_to_right_bet_size:
                        return 'BET', 'betting my top set when straight got there on turn and checked to me on turn and river',

        # if flopped == 'fc_checking_obv_straight_completed':
        # nothing to code, I am check folding or checking on the river with this hand.
        # not sure if I would check/call, but if I do then can add it here
        # if flopped == 'fc_calling_bet_when_obv_str8_got_there
        # same as above situation; I will check fold if I am here as I was hoping for board to pair on river

        # I have top set on flop with no straight or flushes made on the turn
        if flopped == 'fc_top_set_nothing_completed_on_turn_raise_bet_on_turn' or flopped == 'fc_checking_on_turn_awkward_SPR' \
                or flopped == 'fc_awkward_SPR_Im_IP_with_top_set_checked_to_me_nothing_completed' or flopped == 'fc_top_set_on_turn_nothing_completed':
            # if here it means board did not pair on river and flush did not get there so only need to check for straights
            # also means that I did not hit nut straight
            if not self.did_any_straight_complete_on_river:
                return 'BET', 'betting my top set, which shoudl be the nuts',
            else:
                if not self.positions_of_players_to_act_ahead_of_me:
                    if not self.guy_to_right_bet_size:
                        # not 100% sure whether to bet or check - bet for now
                        # I get other straights that are choping to fold most likely
                        # but then I am value owning myself if someone with nut straight check raises
                        # but most would bet the nut straight on the river
                        if self.did_I_hit_straight_on_river_f == 'I_have_non_nut_straight':
                            return 'BET', 'betting non nut straight I am in position checked to me',
                        # if I don't have straight then just check it, which is the default
                    # if someone bets, then I will fold which is the default
                else:
                    if self.guy_to_right_bet_size:
                        # this is only possible if I checked and someone ahead of me bet
                        # TO DO: for more complex check if an obvious straight completed, or not
                        # if non-obvious straight then worth calling sometimes with non-nut striaght

                        # need to run randomiser to decide whether to call.
                        return 'FOLD', 'folding non nut straight',

        if flopped == 'fc_top_set_made_straight_on_flop_checked_to_me_im_last_to_act_I_bet_on_flop_checked_to_me_on_turn_I_bet':
            # if we are here it means the board didn't pair and nor did any flush complete
            # I have been repping the straight since flop, so why not continue; fold out weaker straights
            if not self.guy_to_right_bet_size:
                # sometimes just check it - run randomiser
                return 'BET', 'betting to rep straight',

        # flopped == 'fc_flush_hit_on_turn_SPR_enough_for_me_to_call_to_try_hit_full_house'
        # nothing to do, just run the default, because if we are here it means that the board di not pair

        if flopped == 'fc_flush_hit_on_turn_bet_into_me_Im_last_to_act_checked_to_me_I_bet':
            if not self.guy_to_right_bet_size:
                return 'BET', 'betting to rep the flush that hit on the turn, as I bet on turn',
            # TO DO: after MVP add one check here if someone bets small, then sometimes worth raising,
            # because if they checked on the turn, and then bet small on the river likley they are
            # trying to get to a cheap showdown with non-nuts

        # I had nut straight on the turn, but if we are here that means I don't have nut straight on river; as this is covered at top of this function
        if flopped == 'betting_with_nut_straight_and_middle_set_redraw' or flopped == 'betting_with_nut_straight_and_bottom_set_redraw':
            # TO DO: after MVP if I am here it means that I do not have the nut straight as that is checked at the start of this function
            # add check here that if it is 3-bet then fold
            # and if any obvious straights got there from turn to river then worth folding too
            return 'CALL', 'calling_with_non_nut_straight',

        # flopped == 'calling_bet_into_me_I_have_non_nut_straight_and_middle_set' I will check/fold which is default so no need to code

        if flopped == 'betting_non_nut_straight_middle_set_I_suspect_opp_has_top_set' or flopped == 'betting_non_nut_straight_bottom_set_I_suspect_opp_has_top_set':
            # on the turn I bet with non nut straight and I suspect opp has top set, I am in position checked to me
            if not self.guy_to_right_bet_size:
                return 'CALL', 'not worth betting non nut straight if you suspect opp has top set unlikely they will call',

        if flopped == 'fc_bet_flop_turn_no_made_flush_or_straight_middle_set':
            # if we are here it means that flush didn't hit on river and board did not pair
            # so only need to consider straights
            if not self.did_any_straight_complete_on_river:
                if not self.guy_to_right_bet_size:
                    return 'BET', 'I have middle set flush and straight missed',
                else:
                    # add a check here that if it is check raised to me then fold as someone could have top set
                    return 'CALL', 'I am calling a bet with middle set no straight or flush on river',

            # if straight completed on river
            else:
                # I am in position
                if not self.positions_of_players_to_act_ahead_of_me:
                    if not self.guy_to_right_bet_size:
                        return 'CALL', 'checking down I have middle set at least, didnt check non-nut straight because I would check anyway',
                    else:
                        # TO DO: consider more detail after MVP, as I should defo call sometimes
                        return 'FOLD', 'folding middle set when straight got there',
                # I am out of position
                # I think I would default to check/folding all cases here

        if flopped == 'I_have_nut_straight_middle_set' or flopped == 'fc_I_have_weird_straight_middle_set_im_checking' \
                or flopped == 'fc_I_have_weird_straight_middle_set_calling_a_bet_with_important_SPR' \
                or flopped == 'I_have_nut_straight_bottom_set' or flopped == 'fc_I_have_weird_straight_bottom_set_im_checking' \
                or flopped == 'fc_I_have_weird_straight_middle_set_calling_a_bet_with_important_SPR':
            # only way I can abe here is that if a higher straight became available on the river that I don't have
            # and I had nut straight on the turn
            if self.guy_to_right_bet_size:
                # randomiser to decide whether to call.
                # also worth seeing if any obvious straight got there or a weird one; just like I did on turn
                return 'CALL', 'calling bet with non nut straight when opp checked on the turn',

        if flopped == 'fc_bet_flop_turn_no_made_flush_or_straight_bottom_set':
            if not self.did_any_straight_complete_on_river:
                if not self.guy_to_right_bet_size:
                    return 'BET', 'betting bottom set no flush or straight got there',
                else:
                    # add check that if check raise or three bet then fold
                    return 'CALL', 'calling a bet',
            # if a straight got there
            else:
                if self.did_I_hit_straight_on_river_f == 'I_have_non_nut_straight':
                    if not self.positions_of_players_to_act_ahead_of_me:
                        if not self.guy_to_right_bet_size:
                            return 'BET', 'betting my non nut straight on the river',
                        else:
                            # worth adding a check if weird straight then I might call here
                            return 'FOLD', 'folding non nut straight',
                    else:
                        if not self.guy_to_right_bet_size:
                            return 'CALL', 'checking my non not straight',
                        else:
                            # sometimes worth a call - if weird straight or last guy to act bet
                            return 'FOLD', 'folding my non nut straight',

        # all of the following is where on the turn I had the nut straight with some redraw like trips redraw
        # so if we are here it means that the board didn't pair and a new straight is available and I do not have the
        # nut straight any longer, because I would have bet it at the top of this function otherwise
        # so can treat all these scenarios the same on the river

        # for these I AM IN POSITION SO NOT NEED TO CHECK THAT
        if flopped == 'fc_nut_straight_house_redraw_on_turn' \
            or flopped == 'fc_bet_made_straight_with_higher_straight_redraw' \
                or flopped == 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw' \
                or flopped == 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw' \
                or flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board' \
                or flopped == 'fc_nut_straight_house_redraw_on_turn_bet_into_me_I_raise':
            if not self.guy_to_right_bet_size:
                return 'BET', 'betting my non nut straight on the river',
            else:
                if self.guy_to_right_bet_size > self.pot_size:  # this is how to check if I was check raised, because max one can bet on any street is the pot!
                    return 'FOLD', 'folding to a check raise'
                else:
                    return 'CALL', 'calling opponents bet',

        # for these same as above; I am still in position but it was bet into me
        if flopped == 'fc_nut_straight_higher_st8_redraw_on_turn_bet_into_me_I_call' or flopped == 'fc_bet_made_straight_with_higher_straight_redraw_no_flush_draw' or flopped == 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw' or flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
            if not self.guy_to_right_bet_size:
                return 'BET', 'betting my non nut straight on the river',
            else:
                if self.guy_to_right_bet_size > self.pot_size:  # this is how to check if I was check raised, because max one can bet on any street is the pot!
                    return 'FOLD', 'folding to a check raise'
                else:
                    return 'CALL', 'calling bet with my non nut straight where opp bet on the turn when I had nut straight most likely chopping',

        # I AM OUT OF POSITION HERE; same situation as above (had nut straight on turn with redraw)
        if flopped == 'fc_nut_straight_house_redraw_on_turn_going_for_check_raise_but_if_flopped_is_this_on_river_it_means_it_was_checked_through':
            # I was planning on check raising but it was checked around
            # if here it means board did not pair and no flush completed and I do not have the nut straight on the river,
            # but I had nut straight on the turn
            if self.guy_to_right_bet_size:
                # not 100% whether to call or fold
                return 'FOLD', 'folding_my_non_nut_straight_playing_tighter_strat',

        if flopped == 'fc_check_raised_my_made_straight_with_house_redraw_on_turn':
            # I checked raised the turn with nut straight house redraw but river introduced a higher straight
            # so I will go with default check if no one bets, but if someone bets, I'd consider calling, for for MVP
            if self.guy_to_right_bet_size:
                return 'FOLD', 'folding_my_non_nut_straight_playing_tighter_strat',

        if flopped == 'fc_bet_made_straight_with_higher_straight_redraw' or flopped == 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw' \
                or flopped == 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw' or flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
            # I don't think it is possible to be here, because I have the higher straight redraw but I'm adding this scenario in case I missed something
            print('not sure how this is possible analyse the situation that brought us here')
            pass

        # continuation as per above but here I am OOP and it is bet into me with others to act ahead of me
        if flopped == 'fc_nut_straight_house_redraw_on_turn_bet_into_me_and_I_raise_it':
            # I raised the turn with nut straight and house redraw, if here it means a higher house is possible on river and I do not have it!
            if self.guy_to_right_bet_size:
                # not sure, sometimes called
                return 'FOLD', 'folding my non nut straight',

        if flopped == 'fc_bet_made_straight_with_higher_straight_redraw' or flopped == 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw' \
                or flopped == 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw' \
                or flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
            # as per above I don't think this scenario is possible; to be here because I have the higher straight redraw on the turn
            # also if the flush hit it would be taken care of at the start of this function
            # but I'm adding it in case I missed something
            print('not sure how this is possible analyse the situation that brought us here')
            pass

        # continuation of above but SPR is not awkward - so either very high or low on turn
        if flopped == 'fc_nut_straight_house_redraw_on_turn':
            # I bet or raised the turn with nut straight and house redraw, if here it means a higher house is possible on river and I do not have it!
            if self.guy_to_right_bet_size:
                # not sure, sometimes called
                return 'FOLD', 'folding my non nut straight',

        if flopped == 'fc_bet_made_straight_with_higher_straight_redraw' or flopped == 'fc_call_flop_bet_with_made_straight_with_higher_straight_redraw' \
                or flopped == 'fc_call_bet_on_flop_with_made_straight_higher_straight_redraw_flush_draw_on_board_I_dont_have_flush_draw' \
                or flopped == 'fc_call_three_bet_with_made_straight_higher_straight_redraw_no_flush_draw_on_board':
            print('not sure how this is possible analyse the situation that brought us here')
            pass

        # LOOK AT ON TURN I DIDN'T CODE ALL THE SCENARIOS FROM FLOP THIS IS WHERE I LEFT OFF - ENOUGH FOR MVP BUT LATER COME BACK

        # I don't have much, check/fold
        if not self.guy_to_right_bet_size:
            return 'CALL', 'I_have_nothing_checking', 'I_have_nothing_I_check'
        else:
            return 'FOLD', 'I_have_nothing_folding', 'I_have_nothing_I_fold'

    def analyse_special_hand1_river(self, flopped, card_helper):
        """
        N.B. with trips, I don't think it's smart to overplay them - sure you can fold out better hands like
        flushes and straights, but I'd rather be the one having flushes or straight and call down trips.
        So unless there is a lot of weakness, play trips cautiously, because then you also mitigate the
        big loss when it comes to facing someone that has a house.
        i.e. play by the mantra, bet if you have it and check if you don't.
        """
        # nuts changed on the river - i.e. it is overcards to the paired card OR it is lower than paired card
        # and it is the third card, i.e. a new nut house is available on the river.
        nuts_changed_on_river = False
        if self.river_num >= self.turn[0]:
            nuts_changed_on_river = True
        if self.river_num > self.turn_num:
            if self.river_num == self.turn[2]:
                nuts_changed_on_river = True

        if flopped == 'sh1_nut_house':
            if self.river_num in card_helper:
                return 'BET', 'I_have_nut_house',
            if self.river_num <= self.turn[0]:
                # if I have nut house on turn and river is smaller than the largest turn card, then I still have nut house
                return 'BET', 'I_have_nut_house',
            else:
                # I am IP
                if not self.positions_of_players_to_act_ahead_of_me:
                    if not self.guy_to_right_bet_size:
                        return 'BET', 'I_have_second_nut_house_checked_to_me_in_position',
                    else:
                        return 'FOLD', 'folding_second_nut_house_someone_bet_into_us_when_overcard_hit_on_river'
                # I am OOP
                else:
                    if not self.guy_to_right_bet_size:
                         # TO DO: check whether I called on the turn or bet into the player - as this defo makes a difference
                        return 'BET', 'overcard_hit_to_my_house_Im_OOP_betting_to_see_where_Im_at',
                    else:
                        # scenario where I checked and opp bets and I'm OOP; don't need to code this as FOLD is the default if nothing hits
                        return 'FOLD', 'I_bet_someone_raised_fold_they_have_the_nut_house_I_have_second_nut_house',

        if flopped == 'sh1_checking_quads_bet_on_river':
            return 'BET', 'betting_quads',

        if flopped == 'sh1_second_nut_house_checked_to_me_on_turn_and_I_bet':
            if not self.guy_to_right_bet_size:
                if not nuts_changed_on_river:
                    return 'BET', 'betting_the_river_with_second_nut_house',
                else:
                    return 'CALL', 'checking_the_river_with_third_nut_house',
            else:
                if not nuts_changed_on_river:
                    return 'CALL', 'calling_with_second_nut_house',
                else:
                    return 'FOLD', 'nuts_changed_on_river_bet_into_me_they_likely_have_it',

        if flopped == 'sh1_second_nut_house_called_with_four_or_more_overcards':
            if self.river_num in card_helper:
                if self.river_num <= self.num_list[0] and self.turn_num <= self.num_list[0]:
                    if nuts_changed_on_river:
                        return 'BET', 'bet_the_nut_house_on_the_river',
                else:
                    # e.g. 7 7 5 3 10 ; and I have the 7 and 10 in my hand
                    # TO DO: add a check that if not heads up and it is three_bet likely someone has overhouse,
                    # so should fold instead of call.
                    return 'CALL', 'I_have_nut_house_but_overcard_to_paired_board'

        if flopped == 'sh1_second_nut_house_called_OOP':
            if self.river_num in card_helper:
                return 'CALL', 'I_have_nut_house_but_overcard_to_paired_board',

        if flopped == 'sh1_second_nut_house_I_checked_with_others_to_act':
            # if we are here it means that it was checked around and I had second nut house on turn
            # TO DO: add a check that if the person in absolute position suddenly bets, you should call it off
            # will call for now - add check that if it is 3-bet at any point, I fold as someone has nuts for sure
            return 'CALL', 'I_have_second_nut_house_on_turn_and_it_was_checked_arounnd',

        if flopped == 'sh1_second_nut_house_called_with_four_or_more_overcards':
            if self.river_num in card_helper:
                if self.river_num <= self.num_list[0] and self.turn_num <= self.num_list[0]:
                    if nuts_changed_on_river:
                        return 'BET', 'bet_the_nut_house_on_the_river',
                else:
                    # e.g. 7 7 5 3 10 ; and I have the 7 and 10 in my hand
                    # TO DO: add a check that if not heads up and it is three_bet likely someone has overhouse,
                    # so should fold instead of call.
                    return 'CALL', 'I_have_nut_house_but_overcard_to_paired_board'

        # I had trips on the turn
        if flopped == 'sh1_betting_trips_checked_to_me_im_last_to_act':
            # I have absolute position
            if not self.guy_to_right_bet_size:
                if self.river_num in card_helper and nuts_changed_on_river:
                    return 'BET', 'I_hit_nut_house_getting_value_from_smaller_houses_or_trips',
                else:
                    # there is an argument to bet this, because you could fold out straights, etc.
                    return 'CALL', 'checking_my_trips_I_have_showdown_value',
            else:
                if self.river_num in card_helper and nuts_changed_on_river:
                    # e.g. 9 9 11 ; and I have 9 11 in my hand, don't raise because someone might have 11 11 in their hand
                    return 'CALL', 'calling_a_bet_I_hit_nut_house_but_overcard_Im_in_position',
                else:
                    return 'FOLD', 'someone_likely_had_house_and_I_have_trips',

        if flopped == 'sh1_checking_trips_because_of_less_than_three_overcards':
            # at this point it was checked around and I had trips on flop with less than 3 overcards, I have absolute position
            if not self.guy_to_right_bet_size:
                if self.river_num in card_helper and nuts_changed_on_river:
                    return 'BET', 'I_hit_nut_house_getting_value_from_smaller_houses_or_trips',
                else:
                    # there is an argument to bet this, because you could fold out straights, etc.
                    return 'CALL', 'checking_my_trips_I_have_showdown_value',
            else:
                if self.river_num in card_helper and nuts_changed_on_river:
                    return 'BET', 'I_hit_nut_house_getting_value_from_smaller_houses_or_trips',
                else:
                    # there is an argument to bet this, because you could fold out straights, etc.
                    return 'FOLD', 'likely_someone_has_a_house_or_something_better_than_my_trips',

        if flopped == 'sh1_checking_with_others_to_act_ahead_of_me':
            # if it got to this point it checked around on the turn and I had trips
            if self.river_num in card_helper and nuts_changed_on_river:
                if not self.guy_to_right_bet_size:
                    return 'BET', 'I_hit_nut_house_it_was_checked_to_me_betting',
                else:
                    return 'CALL', 'I_hit_nut_house_calling_a_bet_on_river',

        if flopped == 'sh1_calling_bet_with_trips_with_four_or_more_overcards':
            # at this point I called the turn with trips and 4 or more overcards and it was bet into me
            # I'm in position
            if not self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    return 'BET', 'I_hit_nut_house_it_was_bet_into_me_on_turn_and_I_rivered_top_full_house',
                else:
                    return 'CALL', 'I_hit_nut_house_it_was_bet_into_me_on_turn_and_river_and_I_rivered_top_full_house',






    def straight_completed_on_flop_river_play(self, flopped, card_helper):
        """
        EXPLOIT

        At this point I checked that the river did not pair the board or complete any flush.
        """
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            if lowest_spr >= 1:
                return 'BET', 'checked to me on the river I am betting to rep the straight', 'bet river'

    def board_paired_on_turn_exploit_river_play(self, flopped, card_helper):
        """
        EXPLOIT

        if here it means I bet on the turn when the board paired, after I bet on the flop when there was a straight on baord.
        """
        if not self.guy_to_right_bet_size:
            # I am giving up for now, but I think there is a strong case for betting to get straights to fold, especially if I
            # can bet big.
            return 'CALL', 'giving up for now but come back to see if worth betting on the river', 'checking river'

    def board_paired_on_flop_river_play(self, flopped, card_helper):
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

        # low_paired_card_high_non_paired_card
        if flopped == 'bpof_opp_bet_on_flop_checked_on_turn_I_am_betting_low_paired_high_non_paired':
            if not self.guy_to_right_bet_size:
                return 'betting_river_opp_story_doesnt_make_sense', 'bet_river'

        if flopped == 'bpof_opp_bet_on_flop_bet_on_turn_I_call_to_see_river':
            if not self.guy_to_right_bet_size:
                return 'betting_river_opp_bet_flop_and_turn_but_checked_river', 'bet_river'

        if flopped == 'bpof_opp_called_flop_bet_and_checked_turn_again_I_am_betting_low_paired_high_non_paired_and_low_paired_high_non_paired':
            if not self.guy_to_right_bet_size:
                return 'betting_river_opp_check_called_flop_and_turn_I_am_going_all_the_way', 'bet_river'

        # high_paired_card_low_non_paired_card
        if flopped == 'bpof_opp_checked_to_me_twice_on_flop_and_turn_I_am_betting_high_pair_low_non_pair':
            # run randomiser here, not sure
            if not self.guy_to_right_bet_size:
                return 'BET', 'bpof_opp_checked_to_me_twice_on_flop_and_turn_I_am_betting_high_pair_low_non_pair', 'bet_river'

        if flopped == 'bpof_SPR_less_than_2_on_turn_planning_to_pot_river_if_checked_to_me_then':
            if not self.guy_to_right_bet_size:
                return 'BET', 'sense_weakness_from_opp_so_bet', 'bet_river'

        if flopped == 'opp_story_does_not_make_sense_checking_flop_to_bet_turn_I_am_calling_to_bet_on_river_if_he_checks':
            if not self.guy_to_right_bet_size:
                return 'BET', 'sense_weakness_from_opp_so_bet', 'bet_river'

        if flopped == 'bpof_betting_turn_my_flop_bet_was_called_and_then_checked_to_me_on_turn_high_pair_low_non_pair':
            # check if we are OOP to position 6
            if not self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    return 'sense_weakness_from_opp_so_bet', 'bet_river'

        # high_paired_card_high_non_paired_card
        if flopped == 'bpof_bet_flop_was_called_betting_turn_high_pair_high_non_pair' or \
                flopped == 'bpof_SPR_is_low_checking_turn_to_bet_river_potentially_high_pair_high_non_pair':
            if not self.positions_of_players_to_act_ahead_of_me:
                if not self.guy_to_right_bet_size:
                    return 'sense_weakness_from_opp_so_bet', 'bet_river'

        # low_paired_card_low_non_paired_card
        # When I think about it on the river there are not many scenarios, here are all of them:
        # 1) unlikely opp has nothing
        # 2) opp has second house or just trips
        # 3) opp is sand bagging quads or over house
        # I THINK ON THE RIVER I SHOULD ERR ON THE SIDE OF GIVING UP. BECAUSE THEY LIKELY HAVE IT; AND IF THEY DON'T AND ARE
        # WILLING TO CALL THE TURN YOU ARE JUST TRYING TO GET THEM OFF THEIR HAND - AND IN THESE CASES I THINK THERE ARE
        # DEFINITELY BETTER SPOTS TO GET THE MONEY IN.

        # play the above and see but leave this note here, as I think it's true, and I'll need to adjust river to be more passive.

        # adding a catch all where if I am in position, checked to me and SPR is high enough I will just bet and see what happens
        if not self.positions_of_players_to_act_ahead_of_me:
            if not self.guy_to_right_bet_size:
                if lowest_spr >= 2:
                    return 'BET', 'bpof_default_hit_where_its_checked_t', 'bet_river'

        # I don't have much, check/fold
        if not self.guy_to_right_bet_size:
            return 'CALL', 'I_have_nothing_checking', 'I_have_nothing_I_check'
        else:
            return 'FOLD', 'I_have_nothing_folding', 'I_have_nothing_I_fold'

    def dry_board_on_flop_river_play(self, flopped, card_helper):
        """
        EXPLOIT

        Need to add straight completing on river play - once added can remove this note and
        if we are still here that means nothing completed on river
        """
        if not self.guy_to_right_bet_size:
            return 'BET', 'I bet on flop and turn and it was called, go all the way regardless of SPR', 'bet flop turn and river'

    def flush_completed_on_turn_play_river_exploit(self, flopped, card_helper):
        """EXPLOIT"""
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            # add randomiser, but I think lean towards folding as most would call river if they call turn with flush unless
            # they are pulling for house, so in any case, only worth betting 3/4
            if lowest_spr >= 2:
                return 'BET', 'betting river after flush completed on turn', 'bet river'

    def flush_completed_on_flop_river_play(self, flopped, card_helper):
        """EXPLOIT"""
        lowest_spr = 10000
        for stack in self.stack_tracker:
            if stack:
                stack = float(stack)
                pot_size = float(self.pot_size)
                current_spr = stack/pot_size
                lowest_spr = min(current_spr, lowest_spr)

        if not self.guy_to_right_bet_size:
            if not self.positions_of_players_to_act_ahead_of_me:
                if lowest_spr >= 1:
                    return 'BET', 'My bets were called on flop and turn and it was chcked to me on river, betting', 'bet flop turn betting river'
            else:
                # not so sure here, someone could be camping with nuts
                # add randomiser, but I'll give up for now
                # may be worth betting small to get sets to fold.
                return 'FOLD', 'folding river to someone to act ahead of me, they called my flop and turn bet',

    def straight_completed_on_turn_river_play(self, flopped, card_helper):
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
                return 'BET', 'betting river when straight completed on turn it was checked to me and I bet and opp called', 'bet turn and river'

        # Can add a distinction here if obvious straight got there on turn and no real other draw available
        # worth giving up on the river. But if draws available then worth betting again on river, small perhaps
        # because you are targeting people who had a draw on turn

        # Whereas if general/weird straight got there on turn
        # then worth betting river if checked to you on turn and river.

    def straight_completed_on_river_river_play(self, flopped, card_helper):
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
                return 'BET', 'straight got there on river and checked to me', 'bet river'

    def analyse_my_hand_against_river(self, action_on_turn, extra_information=None):
        """
        (R)!!!!!
        At the start of every main hand you MUST check
        1) did the board pair
        2) did a flush complete
        3) did a straight complete, and do I have the nut straight
        if 1) or 2) is True then coded a separate function to guide the play strategy.
        For 3), just check if straight got there and if so, to bet if I have the nut straight. Otherwise, other
        straight scenarios will be covered in the main hand.

        Doing the above check at the start will make your life 100% easier as you code out the possibilities of each hand.

        To make my life easier, it's also worth checking if I have the nut straight draw on the river and the board isn't paired and no flush
        because then I can comfortably get it all in. I might miss this in the main hand sometimes, because of all the complicated scenario -
        having this check makes it that much easier to play.

        N.B. if I do the above, I do not need to code as many scenarios over and over again,
        e.g. if I am drawing to the nut flush; then I won't need to repeatedly code the scenario if the flush got there on the
        river as it is taken care of at the start of the function.
        -------------------------------------------------------------

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
        """

        if self.guy_to_right_bet_size <= 3:
            return 'call'
        if self.guy_to_right_bet_size == 0:
            return 'check'
        return 'fold'
