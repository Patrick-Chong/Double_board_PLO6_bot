"""
In this test package I will write unit tests to make sure that all the functions input and output what I'd expect.

Also, I will test how long it takes to run each of the classes- as timing is crucial when running the bot in real time.
"""
import pytest
import mock
from analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop import FlopHelper, AnalyseMyHandOnFlop


class TestFlopHelper:

    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.wrap_draw_on_flop')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.flush_draw_on_flop')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.made_straight_on_flop')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.made_flush_on_flop')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.is_any_board_paired_on_flop')
    # note that the line directly below this comment is to mock out the screenshot taking of the flop; so it will appear quite often.
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_organise_flop(self, mock_detect_turn_nums_and_suit, mock_is_any_board_paired_on_flop, mock_made_flush_on_flop, mock_made_straight_on_flop,
                           mock_flush_draw_on_flop, mock_wrap_draw_on_flop):
        x = FlopHelper()
        actual_flops = x.organise_flop()
        expected_flops = [[14, 'D'], [10, 'H'], [8, 'C']], [[12, 'D'], [10, 'H'], [8, 'C']]
        assert actual_flops == expected_flops

    @pytest.mark.parametrize('flop,expected_output', [
        ([[14, 'S'], [6, 'S'], [6, 'C']], [True, 'low']),
        ([[14, 'S'], [14, 'S'], [5, 'C']], [True, 'high']),
        ([[14, 'S'], [13, 'S'], [5, 'C']], [False, None])
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_is_any_board_paired_on_flop(self, mock_detect_turn_nums_and_suit, flop, expected_output):
        x = FlopHelper()
        actual_output = x.is_any_board_paired_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]

    @pytest.mark.parametrize('flop,expected_output', [
        ([[14, 'S'], [6, 'S'], [5, 'S']], [True, 13, 'S']),
        ([[13, 'S'], [6, 'S'], [5, 'S']], [True, 14, 'S']),
        ([[14, 'S'], [13, 'S'], [5, 'S']], [True, 12, 'S']),
        ([[14, 'S'], [13, 'S'], [12, 'S']], [True, 11, 'S'])
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_made_flush_on_flop(self, mock_detect_turn_nums_and_suit, flop, expected_output):
        x = FlopHelper()
        actual_output = x.made_flush_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]
        assert actual_output[2] == expected_output[2]

    @pytest.mark.parametrize('flop,expected_output', [
        ([[9, 'S'], [7, 'S'], [5, 'S']], [True, [[8, 6]], 'C']),
        ([[9, 'S'], [8, 'S'], [7, 'S']], [True, [[11, 10], [10, 6], [6, 5]], 'C']),
        ([[9, 'S'], [6, 'S'], [5, 'S']], [True, [[8, 7]], 'C']),
        ([[9, 'S'], [8, 'S'], [5, 'S']], [True, [[7, 6]], 'O']),
        ([[9, 'S'], [8, 'S'], [6, 'S']], [True, [[10, 7], [7, 5]], 'C']),
        ([[9, 'S'], [7, 'S'], [6, 'S']], [True, [[10, 8], [8, 5]], 'C']),
        ([[14, 'S'], [13, 'S'], [12, 'S']], [True, [[11, 10]], 'C']),
        ([[13, 'S'], [12, 'S'], [10, 'S']], [True, [[14, 11], [11, 9]], 'C']),
        ([[14, 'S'], [12, 'S'], [11, 'S']], [True, [[13, 10]], 'C']),
        ([[13, 'S'], [11, 'S'], [10, 'S']], [True, [[14, 12], [12, 9]], 'C'])
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper')
    def test_made_straight_on_flop(self, mock_organise_flop, mock_detect_turn_nums_and_suit, flop, expected_output):
        x = FlopHelper()
        actual_output = x.made_straight_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]
        assert actual_output[2] == expected_output[2]

    @pytest.mark.parametrize('flop,expected_output', [
        ([[9, 'S'], [7, 'S'], [5, 'C']], [True, 14, 'S']),
        ([[9, 'S'], [8, 'C'], [7, 'D']], [False, None, None]),
        ([[14, 'S'], [6, 'S'], [5, 'C']], [True, 13, 'S']),
        ([[14, 'S'], [13, 'S'], [5, 'C']], [True, 12, 'S']),
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_flush_draw_on_flop(self, mock_detect_turn_nums_and_suit, flop, expected_output):
        x = FlopHelper()
        actual_output = x.flush_draw_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]
        assert actual_output[2] == expected_output[2]

    @pytest.mark.parametrize('flop1,flop2,expected_output', [
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], [False, None, []]),
        ([[14, 'S'], [13, 'S'], [9, 'C']], [[14, 'S'], [13, 'S'], [9, 'C']], [True, True, [[12, 11, 10]]]),
        ([[14, 'S'], [9, 'S'], [5, 'C']], [[14, 'S'], [9, 'S'], [5, 'C']], [True, True, [[8, 7, 6]]]),
        ([[10, 'S'], [7, 'S'], [5, 'C']], [[10, 'S'], [7, 'S'], [5, 'C']], [True, True, [[11, 9, 8], [9, 8, 6], [8, 6, 4], [6, 4, 3]]]),
        ([[14, 'S'], [11, 'S'], [2, 'C']], [[14, 'S'], [11, 'S'], [2, 'C']], [True, True, [[13, 12, 10]]]),
        ([[10, 'S'], [9, 'S'], [2, 'C']], [[10, 'S'], [9, 'S'], [2, 'C']], [True, False, [[12, 11, 8], [13, 12, 11], [11, 8, 7], [8, 7, 6]]]),
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.flush_draw_on_flop')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.made_straight_on_flop')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.made_flush_on_flop')
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper.is_any_board_paired_on_flop')
    def test_wrap_draw_on_flop(self, mock_is_any_board_paired_on_flop, mock_made_flush_on_flop, mock_made_straight_on_flop,
                               mock_flush_draw_on_flop, flop1, flop2, expected_output):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            x = FlopHelper()
            actual_output = x.wrap_draw_on_flop(flop1)
            assert actual_output[0] == expected_output[0]
            assert all(card in actual_output[2] for card in expected_output[2])



stack_tracker = {1:356, 2:356, 3:377.10, 4:0, 5:331.40, 6:0}
SPR_tracker = {1:20, 2:25, 3:25, 4:0, 5:23, 6:0}
guy_to_right_bet_size = 0
positions_of_players_to_act_ahead_of_me = []
pot_size = 20.0
my_position = 4
num_list = [13, 13, 6]
suit_list = ['S', 'C', 'S']
big_blind = 0.4


class TestAnalyseMyHandOnFlop:

    @pytest.mark.parametrize('flop1,flop2,hand_rating_flop1, hand_rating_flop2,guy_to_right_bet_size,extra_information,expected_action', [
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], 7, None, 0, {}, ('BET', {})),  # I have 7 rated hand on flop, bet regardless of anything
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], 6.75, 5.5, 0, {}, ('BET', {})),  # I have 6.75 5.5 rated hands on flop
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], 7, None, 10, {'three_bet_pre_flop': True}, ('BET', {'three_bet_pre_flop': True})),  # I have 7 rated hand and it is three bet pre_flop and 14 on flop
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], 6.75, None, 10, {'three_bet_pre_flop': True}, ('FOLD', {'three_bet_pre_flop': True})),  # I have 6.75 None rated hand and it is three bet pre_flop and 14 on flop
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], 5.5, 5.5, 10, {}, ('CALL', {})),  # I have 5.5 rated for both and last to act and bet into me
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], 6.75, None, 10, {}, ('FOLD', {})),  # I have not strong enough to continue hand and it's bet into me
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], 6.75, None, 0, {}, ('CALL', {})),  # I have not strong enough to continue hand and it's NOT bet into me
    ])
    def test_analyse_my_hand_against_flop(self, flop1, flop2, hand_rating_flop1, hand_rating_flop2, guy_to_right_bet_size, extra_information, expected_action):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)
            amhof.my_hand_rating_on_flop1[hand_rating_flop1] = 'something'
            amhof.my_hand_rating_on_flop2[hand_rating_flop2] = 'something'
            amhof.guy_to_right_bet_size = guy_to_right_bet_size
            amhof.check_bet_three_bet_behind_me = 'bet'
            amhof.SPR_tracker = {1: 10, 2: 5, 5: 10}
            actual_action = amhof.analyse_my_hand_against_flop(extra_information=extra_information)

            assert actual_action == expected_action

    @pytest.mark.parametrize('set_True_or_False1,set_True_or_False2,set_True_or_False3,hand_rating_True', [
        (True, False, False, 7),
        (False, True, False, 6.75),
        (False, False, True, 5.5),
        (True, True, True, 7),
        ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_my_hand_ratings_on_both_flops(self, mock_detect_flop_nums_and_suit, set_True_or_False1, set_True_or_False2, set_True_or_False3, hand_rating_True):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.overhouse_on_flop1 = set_True_or_False1
        amhof.flopped_top_set_no_made_flush_straight_flop1 = set_True_or_False2
        amhof.top_set_on_made_flush_straight_board_flop1 = set_True_or_False3
        amhof.overhouse_on_flop2 = set_True_or_False1
        amhof.flopped_top_set_no_made_flush_straight_flop2 = set_True_or_False2
        amhof.top_set_on_made_flush_straight_board_flop2 = set_True_or_False3

        actual_hand_rating_flop1, actual_hand_rating_flop2 = amhof.my_hand_ratings_on_both_flops()
        assert actual_hand_rating_flop1[hand_rating_True]

    @pytest.mark.parametrize('is_flush_draw_on_flop,nut_flush_draw_nums_on_flop,nut_flush_draw_suit_on_flop,num_list,suit_list,expected_flopped_nut_flush_draw_flop1', [
        (True, 14, 'S', [14, 14, 13, 13, 12, 12], ['S', 'C', 'S', 'C', 'S', 'C'], (True, True)),  # I have nut flush draw
        (True, 14, 'S', [13, 14, 13, 13, 12, 12], ['S', 'C', 'S', 'C', 'S', 'C'], (False, False)),  # I do not have nut flush draw
        (True, 14, 'S', [13, 14, 13, 13, 12, 12], ['S', 'C', 'S', 'C', 'S', 'C'], (False, False))  # there is no flush draw on board
                             ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_helper_flopped_nut_flush_draw(self, mock_detect_flop_nums_and_suit, is_flush_draw_on_flop, nut_flush_draw_nums_on_flop,
                                           nut_flush_draw_suit_on_flop, num_list,suit_list, expected_flopped_nut_flush_draw_flop1):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                            positions_of_players_to_act_ahead_of_me,
                            pot_size, my_position, num_list, suit_list, big_blind)
        amhof.is_flush_draw_on_flop1 = is_flush_draw_on_flop
        amhof.is_flush_draw_on_flop2 = is_flush_draw_on_flop
        amhof.nut_flush_draw_nums_on_flop1 = nut_flush_draw_nums_on_flop
        amhof.nut_flush_draw_suit_on_flop1 = nut_flush_draw_suit_on_flop
        amhof.nut_flush_draw_nums_on_flop2 = nut_flush_draw_nums_on_flop
        amhof.nut_flush_draw_suit_on_flop2 = nut_flush_draw_suit_on_flop
        amhof.num_list = num_list
        amhof.suit_list = suit_list
        actual_flopped_nut_flush_draw_flop1 = amhof.helper_flopped_nut_flush_draw()
        assert actual_flopped_nut_flush_draw_flop1 == expected_flopped_nut_flush_draw_flop1

    @pytest.mark.parametrize('flop1,flop2,num_list,expected_res', [
    ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], [14, 14, 13, 13, 12, 12], ('top', 'top')),  # I have top set
        ([[14, 'S'], [9, 'S'], [2, 'C']], [[14, 'S'], [9, 'S'], [2, 'C']], [9, 9, 8, 8, 7, 7], ('middle', 'middle')),  # I have middle set
        ([[14, 'S'], [10, 'S'], [2, 'C']], [[14, 'S'], [10, 'S'], [2, 'C']], [9, 9, 8, 8, 2, 2], ('bottom', 'bottom')),  # I have bottom set
        ([[14, 'S'], [10, 'S'], [2, 'C']], [[14, 'S'], [10, 'S'], [2, 'C']], [9, 9, 8, 8, 3, 3], (None, None)),  # I have no set
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_helper_set_checker(self, mock_detect_flop_nums_and_suit, flop1, flop2, num_list, expected_res):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)

            actual_res = amhof.helper_set_checker()
            assert actual_res == expected_res

    @pytest.mark.parametrize('flop1,flop2,num_list,high_or_low_paired_board_flop,expected_res', [
        ([[14, 'S'], [9, 'S'], [9, 'C']], [[14, 'S'], [9, 'S'], [9, 'C']], [14, 14, 13, 13, 12, 12], 'low', (True, True)),  # I have over house
        ([[10, 'S'], [9, 'S'], [9, 'C']], [[10, 'S'], [9, 'S'], [9, 'C']], [14, 14, 13, 13, 12, 12], 'low', (False, False)),  # I do not have over house
        ([[10, 'S'], [9, 'S'], [9, 'C']], [[10, 'S'], [9, 'S'], [9, 'C']], [14, 14, 13, 13, 12, 12], 'low', (False, False)),  # I do not have over house
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [14, 14, 13, 13, 12, 12], 'high', (False, False)),  # over house not possible

    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_over_house_check(self, mock_detect_flop_nums_and_suit, flop1, flop2, num_list, high_or_low_paired_board_flop, expected_res):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)

            actual_res = amhof.over_house_check()
            assert actual_res == expected_res

    @pytest.mark.parametrize('flop1,flop2,num_list,high_or_low_paired_board_flop,expected_res', [
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [14, 13, 13, 12, 12, 9], 'high', (True, True)),  # I have nut house
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [14, 13, 13, 12, 12, 8], 'high', (False, False)),  # I have trips
        ([[14, 'S'], [13, 'S'], [9, 'C']], [[14, 'S'], [13, 'S'], [9, 'C']], [14, 13, 13, 12, 12, 8], None, (False, False)),  # board is not paired
                             ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.AnalyseMyHandOnFlop.helper_flopped_nut_flush_draw')
    def test_check_nut_house_on_flop(self, mock_detect_flop_nums_and_suit, mock_helper_flopped_nut_flush_draw, flop1, flop2, num_list, high_or_low_paired_board_flop, expected_res):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                positions_of_players_to_act_ahead_of_me,
                                pot_size, my_position, num_list, suit_list, big_blind)
            amhof.high_or_low_paired_board_flop1 = high_or_low_paired_board_flop
            amhof.high_or_low_paired_board_flop2 = high_or_low_paired_board_flop
            actual_res = amhof.check_nut_house_on_flop()
            assert actual_res == expected_res

    @pytest.mark.parametrize('flop1,flop2,num_list,high_or_low_paired_board_flop,expected_res', [
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [13, 13, 12, 12, 9, 9], 'high', (True, True)),  # I have underhouse
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [14, 13, 12, 12, 9, 8], 'high', (False, False)),  # I do not have
                             ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.AnalyseMyHandOnFlop.helper_flopped_nut_flush_draw')
    def test_flopped_under_house(self, mock_detect_flop_nums_and_suit, mock_helper_flopped_nut_flush_draw, flop1, flop2, num_list, high_or_low_paired_board_flop, expected_res):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                positions_of_players_to_act_ahead_of_me,
                                pot_size, my_position, num_list, suit_list, big_blind)
            amhof.high_or_low_paired_board_flop1 = high_or_low_paired_board_flop
            amhof.high_or_low_paired_board_flop2 = high_or_low_paired_board_flop
            actual_res = amhof.flopped_under_house()
            assert actual_res == expected_res

    @pytest.mark.parametrize('flop1,flop2,num_list,high_or_low_paired_board_flop,expected_res', [
        ([[14, 'S'], [9, 'S'], [9, 'C']], [[14, 'S'], [9, 'S'], [9, 'C']], [14, 13, 12, 12, 9, 8], 'high', (True, True)),  # I have nut house with overhouse avail
        ([[14, 'S'], [9, 'S'], [9, 'C']], [[14, 'S'], [9, 'S'], [9, 'C']], [14, 13, 12, 12, 8, 8], 'high', (False, False)),  # I do not have nut house
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [14, 13, 12, 12, 9, 8], 'low', (False, False)),  # board is not high paired
                             ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.AnalyseMyHandOnFlop.helper_flopped_nut_flush_draw')
    def test_flopped_house_with_overhouse_avail(self, mock_detect_flop_nums_and_suit, mock_helper_flopped_nut_flush_draw, flop1, flop2, num_list, high_or_low_paired_board_flop, expected_res):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                positions_of_players_to_act_ahead_of_me,
                                pot_size, my_position, num_list, suit_list, big_blind)
            amhof.high_or_low_paired_board_flop1 = high_or_low_paired_board_flop
            amhof.high_or_low_paired_board_flop2 = high_or_low_paired_board_flop
            actual_res = amhof.flopped_house_with_overhouse_avail()
            assert actual_res == expected_res

    @pytest.mark.parametrize('flop1,flop2,num_list,high_or_low_paired_board_flop,expected_res', [
        ([[14, 'S'], [9, 'S'], [9, 'C']], [[14, 'S'], [9, 'S'], [9, 'C']], [14, 14, 13, 13, 9, 9], 'low', (True, True)),  # I have quads
        ([[14, 'S'], [9, 'S'], [9, 'C']], [[14, 'S'], [9, 'S'], [9, 'C']], [14, 14, 13, 13, 10, 9], 'low', (False, False)),  # I do not have quads
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [14, 14, 13, 13, 10, 9], 'high', (True, True)),  # I have quads
        ([[14, 'S'], [14, 'S'], [9, 'C']], [[14, 'S'], [14, 'S'], [9, 'C']], [13, 13, 12, 12, 10, 9], 'high', (False, False)),  # I do not have quads
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_quads_checker(self, mock_detect_flop_nums_and_suit, flop1, flop2, num_list, high_or_low_paired_board_flop, expected_res):
        with mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=(flop1, flop2)):
            amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                        positions_of_players_to_act_ahead_of_me,
                                        pot_size, my_position, num_list, suit_list, big_blind)

            actual_res = amhof.quads_checker()
            assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,is_flush_completed_on_flop,nut_flush_nums_flop,nut_flush_suit_flop,expected_res', [
        ([14, 14, 13, 13, 12, 12], ['S', 'C', 'H', 'C', 'S', 'C'], True, 14, 'S', (True, True)),  # I have nut flush
        ([14, 14, 13, 13, 12, 12], ['S', 'C', 'H', 'C', 'S', 'C'], True, 12, 'S', (True, True)),  # I have nut flush
        ([14, 14, 13, 13, 12, 12], ['S', 'C', 'H', 'C', 'S', 'C'], True, 13, 'S', (False, False)),  # I do not have nut flush
        ([14, 14, 13, 13, 12, 12], ['S', 'C', 'H', 'C', 'S', 'C'], False, 14, 'S', (False, False)),  # No made flush on board
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_nut_flush_check(self, mock_detect_flop_nums_and_suit, num_list, suit_list, is_flush_completed_on_flop, nut_flush_nums_flop,
                             nut_flush_suit_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.is_flush_completed_on_flop1 = is_flush_completed_on_flop
        amhof.is_flush_completed_on_flop2 = is_flush_completed_on_flop
        amhof.nut_flush_nums_flop1 = nut_flush_nums_flop
        amhof.nut_flush_nums_flop2 = nut_flush_nums_flop
        amhof.nut_flush_suit_flop1 = nut_flush_suit_flop
        amhof.nut_flush_suit_flop2 = nut_flush_suit_flop
        amhof.num_list = num_list
        amhof.suit_list = suit_list

        actual_res = amhof.nut_flush_check()
        assert actual_res == expected_res

    @pytest.mark.parametrize('flopped_which_set_on_flop,made_flush_on_flop,made_straight_on_flop,expected_res', [
        ('top', False, False, (True, True)),  # I flopped top set no made flush straight on flop
        ('middle', False, False, (False, False)),  # I flopped middle set no made flush straight on flop
        ('top', True, False, (False, False)),  # I flopped top set but made flush
        ('top', False, True, (False, False)),  # I flopped top set but made straight
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_top_set_no_made_flush_straight_checker(self, mock_detect_flop_nums_and_suit, flopped_which_set_on_flop, made_flush_on_flop,
                                                    made_straight_on_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.flopped_set_flop1 = flopped_which_set_on_flop
        amhof.flopped_set_flop2 = flopped_which_set_on_flop
        amhof.is_flush_completed_on_flop1 = made_flush_on_flop
        amhof.is_flush_completed_on_flop2 = made_flush_on_flop
        amhof.is_straight_completed_on_flop1 = made_straight_on_flop
        amhof.is_straight_completed_on_flop2 = made_straight_on_flop

        actual_res = amhof.top_set_no_made_flush_straight_checker()
        assert actual_res == expected_res

    @pytest.mark.parametrize('flopped_which_set_on_flop,made_flush_on_flop,made_straight_on_flop,expected_res', [
        ('top', False, False, (True, True)),  # I flopped top set no made flush straight on flop
        ('middle', False, False, (True, True)),  # I flopped middle set no made flush straight on flop
        ('bottom', False, False, (True, True)),  # I flopped bottom set no made flush straight on flop
        ('top', True, False, (False, False)),  # I flopped top set but made flush
        ('top', False, True, (False, False)),  # I flopped top set but made straight
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_any_set_no_made_flush_straight_checker(self, mock_detect_flop_nums_and_suit, flopped_which_set_on_flop, made_flush_on_flop,
                                                    made_straight_on_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.flopped_set_flop1 = flopped_which_set_on_flop
        amhof.flopped_set_flop2 = flopped_which_set_on_flop
        amhof.is_flush_completed_on_flop1 = made_flush_on_flop
        amhof.is_flush_completed_on_flop2 = made_flush_on_flop
        amhof.is_straight_completed_on_flop1 = made_straight_on_flop
        amhof.is_straight_completed_on_flop2 = made_straight_on_flop

        actual_res = amhof.any_set_no_made_flush_straight_checker()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,three_card_wrap_combis_on_flop,flopped_nut_flush_draw_flop,expected_res', [
        ([14, 14, 13, 9, 8, 7], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, (True, True)),  # I have nut flush draw and nut wrap draw
        ([14, 14, 13, 8, 7, 4], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, (False, False)),  # I have nut flush draw but not nut wrap
        ([14, 14, 13, 8, 7, 4], [], True, (False, False)),  # No wrap draw on flop
        ([14, 14, 13, 9, 8, 7], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], False, (False, False)),  # No flush draw on flop

    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_nut_flush_draw_nut_wrap(self, mock_detect_flop_nums_and_suit, num_list, three_card_wrap_combis_on_flop,
                                     flopped_nut_flush_draw_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.three_card_wrap_combis_on_flop1 = three_card_wrap_combis_on_flop
        amhof.three_card_wrap_combis_on_flop2 = three_card_wrap_combis_on_flop
        amhof.flopped_nut_flush_draw_flop1 = flopped_nut_flush_draw_flop
        amhof.flopped_nut_flush_draw_flop2 = flopped_nut_flush_draw_flop

        actual_res = amhof.nut_flush_draw_nut_wrap()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,is_flush_draw_on_flop,nut_flush_draw_suit_on_flop,two_card_combis_that_complete_the_straight_on_flop,'
                             'flopped_set_flop,expected_res', [
        ([14, 14, 13, 9, 8, 7], ['S', 'C', 'H', 'C', 'S', 'C'], True, 'S',  [[9, 8], [8, 4], [4, 3]], None, (True, True)),  # nut straight + flush draw
        ([14, 14, 13, 9, 8, 7], ['S', 'C', 'H', 'C', 'S', 'C'], False, None,  [[9, 8], [8, 4], [4, 3]], 'middle', (True, True)),  # nut straight + set
        ([14, 14, 13, 9, 8, 7], ['S', 'C', 'H', 'C', 'S', 'C'], False, None,  [[9, 8], [8, 4], [4, 3]], None, (False, False)),  # nut straight + no set no flush draw
        ([14, 14, 13, 9, 7, 4], ['S', 'C', 'H', 'C', 'S', 'C'], True, 'S',  [[9, 8], [8, 4], [4, 3]], 'middle', (False, False)),  # got the non nut straight
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[5, 'H'], [6, 'C'], [7, 'D']], [[7, 'H'], [6, 'C'], [5, 'D']]))
    def test_flopped_nut_straight_with_house_or_flush_redraw(self, mock_detect_flop_nums_and_suit, num_list, suit_list, is_flush_draw_on_flop,
                                                             nut_flush_draw_suit_on_flop, two_card_combis_that_complete_the_straight_on_flop,
                                                             flopped_set_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.num_list = num_list
        amhof.suit_list = suit_list
        amhof.nut_flush_draw_suit_on_flop1 = nut_flush_draw_suit_on_flop
        amhof.nut_flush_draw_suit_on_flop2 = nut_flush_draw_suit_on_flop
        amhof.two_card_combis_that_complete_the_straight_on_flop1 = two_card_combis_that_complete_the_straight_on_flop
        amhof.two_card_combis_that_complete_the_straight_on_flop2 = two_card_combis_that_complete_the_straight_on_flop
        amhof.is_flush_draw_on_flop1 = is_flush_draw_on_flop
        amhof.is_flush_draw_on_flop2 = is_flush_draw_on_flop
        amhof.flopped_set_flop1 = flopped_set_flop
        amhof.flopped_set_flop2 = flopped_set_flop

        actual_res = amhof.flopped_nut_straight_with_house_or_flush_redraw()
        assert actual_res == expected_res

    @pytest.mark.parametrize('flopped_set_flop,is_straight_completed_on_flop,is_flush_completed_on_flop,expected_res', [
        ('top', True, False, (True, True)),  # I flopped top set on made straight board
        ('middle', True, False, (True, True)),  # I flopped middle set on made straight board
        ('bottom', True, False, (True, True)),  # I flopped bottom set on made straight board
        ('middle', False, False, (False, False)),  # I flopped top set but no made straight or flush
        (None, True, True, (False, False)),  # I did not flop any set
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[10, 'H'], [8, 'C'], [14, 'D']], [[10, 'H'], [8, 'C'], [12, 'D']]))
    def test_any_set_on_made_flush_straight_board(self, mock_detect_flop_nums_and_suit, flopped_set_flop,
                                                  is_straight_completed_on_flop, is_flush_completed_on_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.flopped_set_flop1 = flopped_set_flop
        amhof.flopped_set_flop2 = flopped_set_flop
        amhof.is_straight_completed_on_flop1 = is_straight_completed_on_flop
        amhof.is_straight_completed_on_flop2 = is_straight_completed_on_flop
        amhof.is_flush_completed_on_flop1 = is_flush_completed_on_flop
        amhof.is_flush_completed_on_flop2 = is_flush_completed_on_flop

        actual_res = amhof.any_set_on_made_flush_straight_board()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,three_card_wrap_combis_on_flop,is_flush_draw_on_flop,nut_flush_draw_suit_on_flop,expected_res', [
        ([14, 14, 13, 9, 8, 7], ['S', 'C', 'H', 'C', 'S', 'C'], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, 'S', (True, True)),  # nut wrap + non nut flush draw
        ([14, 14, 13, 8, 7, 4], ['S', 'C', 'H', 'C', 'S', 'C'], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, 'S', (False, False)),  # non nut wrap + non nut flush draw
        ([14, 14, 13, 9, 8, 7], ['S', 'C', 'H', 'C', 'S', 'C'], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], False, None, (False, False)),  # nu wrap but no flush draw on flop
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[5, 'H'], [6, 'C'], [7, 'D']], [[7, 'H'], [6, 'C'], [5, 'D']]))
    def test_nut_wrap_non_nut_flush_draw(self, mock_detect_flop_nums_and_suit, num_list, suit_list, three_card_wrap_combis_on_flop,
                                         is_flush_draw_on_flop, nut_flush_draw_suit_on_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.num_list = num_list
        amhof.suit_list = suit_list
        amhof.three_card_wrap_combis_on_flop1 = three_card_wrap_combis_on_flop
        amhof.three_card_wrap_combis_on_flop2 = three_card_wrap_combis_on_flop
        amhof.is_flush_draw_on_flop1 = is_flush_draw_on_flop
        amhof.is_flush_draw_on_flop2 = is_flush_draw_on_flop
        amhof.nut_flush_draw_suit_on_flop1 = nut_flush_draw_suit_on_flop
        amhof.nut_flush_draw_suit_on_flop2 = nut_flush_draw_suit_on_flop

        actual_res = amhof.nut_wrap_non_nut_flush_draw()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,suit_list,three_card_wrap_combis_on_flop,flopped_nut_flush_draw_flop1,expected_res', [
        ([14, 14, 13, 8, 7, 4], ['S', 'C', 'H', 'C', 'S', 'C'], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, (True, True)),  # nut flush draw + non nut wrap
        ([14, 14, 13, 7, 4, 3], ['S', 'C', 'H', 'C', 'S', 'C'], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, (True, True)),  # nut flush draw + non nut wrap
        ([14, 14, 13, 7, 4, 3], ['S', 'C', 'H', 'C', 'S', 'C'], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], False, (False, False)),  # no nut flush draw + wrap
        ([14, 14, 13, 7, 3, 3], ['S', 'C', 'H', 'C', 'S', 'C'], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, (False, False)),  # nut flush draw + no wrap
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[5, 'H'], [6, 'C'], [7, 'D']], [[7, 'H'], [6, 'C'], [5, 'D']]))
    def test_non_nut_wrap_nut_flush_draw(self, mock_detect_flop_nums_and_suit, num_list, suit_list, three_card_wrap_combis_on_flop,
                                         flopped_nut_flush_draw_flop1, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.num_list = num_list
        amhof.suit_list = suit_list
        amhof.three_card_wrap_combis_on_flop1 = three_card_wrap_combis_on_flop
        amhof.three_card_wrap_combis_on_flop2 = three_card_wrap_combis_on_flop
        amhof.flopped_nut_flush_draw_flop1 = flopped_nut_flush_draw_flop1
        amhof.flopped_nut_flush_draw_flop2 = flopped_nut_flush_draw_flop1

        actual_res = amhof.non_nut_wrap_nut_flush_draw()
        assert actual_res == expected_res

    @pytest.mark.parametrize('num_list,three_card_wrap_combis_on_flop,is_flush_draw_on_flop,is_flush_completed_on_flop,expected_res', [
        ([14, 14, 13, 8, 7, 4], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], False, False, (True, True)),  # any wrap on rainbow board
        ([14, 14, 13, 8, 7, 4], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], False, True, (False, False)),  # any wrap on non rainbow board
        ([14, 14, 13, 8, 7, 4], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], True, False, (False, False)),  # any wrap on non rainbow board
        ([14, 14, 13, 8, 7, 7], [[9, 8, 7], [8, 7, 4], [7, 4, 3], [4, 3, 2]], False, False, (False, False)),  # no wrap on rainbow board
    ])
    @mock.patch('flop_turn_river_cards.TheFlop.detect_flop_nums_and_suit', return_value=([[5, 'H'], [6, 'C'], [7, 'D']], [[7, 'H'], [6, 'C'], [5, 'D']]))
    def test_non_nut_wrap_nut_flush_draw(self, mock_detect_flop_nums_and_suit, num_list, three_card_wrap_combis_on_flop,
                                         is_flush_draw_on_flop, is_flush_completed_on_flop, expected_res):
        amhof = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                                    positions_of_players_to_act_ahead_of_me,
                                    pot_size, my_position, num_list, suit_list, big_blind)
        amhof.num_list = num_list
        amhof.suit_list = suit_list
        amhof.three_card_wrap_combis_on_flop1 = three_card_wrap_combis_on_flop
        amhof.three_card_wrap_combis_on_flop2 = three_card_wrap_combis_on_flop
        amhof.is_flush_draw_on_flop1 = is_flush_draw_on_flop
        amhof.is_flush_draw_on_flop2 = is_flush_draw_on_flop
        amhof.is_flush_completed_on_flop1 = is_flush_completed_on_flop
        amhof.is_flush_completed_on_flop2 = is_flush_completed_on_flop

        actual_res = amhof.any_wrap_on_rainbow_board()
        assert actual_res == expected_res


