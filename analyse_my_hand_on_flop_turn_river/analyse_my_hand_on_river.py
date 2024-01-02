"""
Information I need to make best river decision possible:
1. Do I have the nuts on either/both board (absolute coconuts vs. nuts)?
Two people can have nut straight but two people cannot have nut flush; the latter is absolute coconuts.
2. Was I last aggressor on turn?
3. Did nuts change on either board with the river card?
4. Any draws (especially flush draws) on the turn that missed?/ got there
5. What is the SPR of those still in pot?
6. Anyone ahead of me to act / are we heads up?

Coding steps to gather above information:
- organise river cards into the turn
1. Check if I have absolute coconuts on either board or nut nut on either board; if so easy bet
To do this, just like on turn I'll need to code out, board pair, flush completed, straight completed. No need to check for draws.
2. My action on turn should be passed on in action_on_turn
3. Create function to check if nuts changes on either boards; particularly if flushes got there
This is important because if opp bet on turn and river changed and he check and we are heads up, I'll bet regardless.
This is a huge exploit that is easy to code.
4. Another function to check if many draws on turn and if they missed or got there
5/6 information we already have available, just think how to use it in decision making.
"""
from collections import defaultdict

from .analyse_my_hand_on_turn import AnalyseMyHandOnTurn
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

        self.river1, self.river2 = self.organise_river()
        self.positions_of_players_to_act_ahead_of_me_f = positions_of_players_to_act_ahead_of_me

        # Check what is available to hit on the turn - copied the below straight from the turn
        # Did board pair
        self.did_board_pair_on_turn_generator = AnalyseMyHandOnTurn.did_board_pair_on_turn(self.turn1)
        self.did_board_pair_on_turn1 = self.did_board_pair_on_turn_generator[0]
        self.board_pair_top_card_turn1 = self.did_board_pair_on_turn_generator[1]
        self.did_board_pair_on_turn_generator = AnalyseMyHandOnTurn.did_board_pair_on_turn(self.turn2)
        self.did_board_pair_on_turn2 = self.did_board_pair_on_turn_generator[0]
        self.board_pair_top_card_turn2 = self.did_board_pair_on_turn_generator[1]
        # Did flush complete
        self.flush_complete_on_turn = AnalyseMyHandOnTurn.flush_completed_on_turn(self.turn1)
        self.did_flush_completed_on_turn1 = self.flush_complete_on_turn[0]
        self.nut_flush_nums_turn1 = self.flush_complete_on_turn[1]
        self.nut_flush_suit_turn1 = self.flush_complete_on_turn[2]
        self.flush_complete_on_turn = AnalyseMyHandOnTurn.flush_completed_on_turn(self.turn2)
        self.did_flush_completed_on_turn2 = self.flush_complete_on_turn[0]
        self.nut_flush_nums_turn2 = self.flush_complete_on_turn[1]
        self.nut_flush_suit_turn2 = self.flush_complete_on_turn[2]
        # Did straight complete
        self.any_straight_completed_on_turn_generator = AnalyseMyHandOnTurn.any_straight_completed_on_turn(self.turn1)
        self.did_straight_complete_on_turn1 = self.any_straight_completed_on_turn_generator[0]
        self.two_card_combi_completing_straight_on_turn1 = self.any_straight_completed_on_turn_generator[1]
        self.any_straight_completed_on_turn_generator = AnalyseMyHandOnTurn.any_straight_completed_on_turn(self.turn2)
        self.did_straight_complete_on_turn2 = self.any_straight_completed_on_turn_generator[0]
        self.two_card_combi_completing_straight_on_turn2 = self.any_straight_completed_on_turn_generator[1]

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
        pass

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

    def organise_river(self):
        """
        river will look like: [[13, 'S'], [10, 'C'], [9, 'S'], [8, 'C'], [2, 'C] ; after we sort it.
        """
        river1_card, river2_card = TR.detect_river_nums_and_suit()

        # TO DO: add a breakpoint here when running integration test and check if self.flop and self.turn is correct,
        # previously self.flop was incorrect in this position; delete this funciton once checked.
        river1 = self.turn1 + [river1_card]
        river2 = self.turn2 + [river2_card]

        # Sort the turn cards with flop so everything is in descending order
        river1 = sorted(river1, key=lambda x: x[0], reverse=True)  # Sorting from largest to smallest, hence reverse=True
        river2 = sorted(river2, key=lambda x: x[0], reverse=True)  # Sorting from largest to smallest, hence reverse=True

        return river1, river2

    # copied below function straight from turn
    def analyse_my_hand_against_river(self, action_on_flop=None, extra_information=None):
        """
        action_on_flop will be 'BET' or 'CALL' - tells us what we did on the flop; who aggressor was on last street.

        It's quite important to know on the turn in general the SPR of the person who bet and anyone who called.
        Because if it is small, then a fold should be a call many times.

        Another thing to consider is that if board is paired, there's no need to run through
        straight or flush or draws functions, as they will be void.
        With this in mind it makes sense to pass it in a certain order and if something like a paired
        board is detected, stop passing and can return there.
        Order to check things on turn:
        1) did board pair -                  self.hand_ratings_turn1['board_paired']
        2) did flush complete -              self.hand_ratings_turn1['made_flush']
        3) did straight complete-            self.hand_ratings_turn1['made_straight']
        4) Combo draws -                     self.hand_ratings_turn1['combo_draw']
        5) two pair no st8/flush/board pair- self.hand_ratings_turn1['dry_two_pair']

        Ratings and what they mean:
        7 : the absolute coconuts - e.g. quads
        6.5: coconuts but only blast if I have something good on other hand, as coconuts can change (e.g. top set)
        6:  very close to the coconuts - e.g. house with overhouse available, or middle set.
        5.5: strongish - e.g. top two pair on board with no flush or straight made; or bottom set
        4:  something non nutted- e.g. lower house or lower straight

        Strategy of play with ratings:
        - 7 bet regardless of other hand
        - 6.5 + 6 bet
        - 6.5 + lower ; call a bet or bet if not bet
        - 6 and 6 bet if not bet otherwise call
        - Check fold anything less

        The 6.5 created for a made straight, but on it's own not good enough cos other might have it too.
        So need to consider other board to determine if I should bet/raise or not.
        It will also be used on board where I have top set and no flush or straight completed.
        On a draw heavy board multiway, this is not ideal to blast unless I have something else on other board.
        """

        # Fill out my hand ratings based on what is on board and what I have
        self.is_board_paired_on_turn()
        self.two_pair_no_flush_or_straight_completed()
        self.is_flush_completed_on_turn()
        self.is_straight_completed_on_turn()
        self.combo_draw()

        # Add logic here to check both my hand ratings and then return 'BET', 'CALL' or 'FOLD'.
        hand_rating_on_turn1 = max(self.hand_ratings_turn1.values())
        hand_rating_on_turn2 = max(self.hand_ratings_turn2.values())

        # STRATEGY FOR MY PLAY:
        # For now I'll ignore SPR for check raising. When I record my plays; much easier to identify where I can go for check raises;
        action_behind_me = self.check_bet_three_bet()  # 'check', 'bet', 'three_bet'
        if hand_rating_on_turn1 == 7 or hand_rating_on_turn2 == 7:
            return 'BET'
        if (hand_rating_on_turn1 == 6.75 and hand_rating_on_turn2 >= 5.5) or (hand_rating_on_turn2 == 6.75 and hand_rating_on_turn1 >= 5.5):
            return 'BET'
        if (hand_rating_on_turn1 == 6.5 and hand_rating_on_turn2 == 6) or (hand_rating_on_turn2 == 6.5 and hand_rating_on_turn1 == 6):
            return 'BET'
        if (hand_rating_on_turn1 == 6.5 and hand_rating_on_turn2 < 6) or (hand_rating_on_turn2 == 6.5 and hand_rating_on_turn1 < 6):
            if not self.guy_to_right_bet_size:
                return 'BET'
            else:
                # Consider SPR here? What if guy is going call in, still call? I think so.
                return 'CALL'
        # Think about adding more cases to call, when I am in position and no one to act ahead of me - especilly heads up.
        # or even non-heads up but I am in position (exploit) - like the chinese guy does all the time, blasts when:
        # he has position + nuts changed on river + checked to him.
        # (I believe I noticed he doesn't do it on baords where straight completed but more closed like flush completing or board pairing).

        if action_behind_me == 'check':
            return 'CALL'
        else:
            return 'FOLD'

        # For testing the flow of code vs. real app, comment out all of the above, and comment in all of below:
        # if self.guy_to_right_bet_size <= 3:
        #     return 'CALL'
        # if self.guy_to_right_bet_size == 0:
        #     return 'CALL'
        # return 'FOLD'
