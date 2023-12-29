"""
In this test package I will write unit tests to make sure that all the functions input and output what I'd expect.

Also, I will test how long it takes to run each of the classes- as timing is crucial when running the bot in real time.
"""
import pytest
import mock
from analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop import FlopHelper, AnalyseMyHandOnFlop


x = FlopHelper()


class TestFlopHelper:
    @pytest.mark.parametrize('flop,expected_output', [
        ([[14, 'S'], [6, 'S'], [6, 'C']], [True, 'low']),
        ([[14, 'S'], [14, 'S'], [5, 'C']], [True, 'high']),
        ([[14, 'S'], [13, 'S'], [5, 'C']], [False, None])

    ])
    def test_board_paired_on_flop(self, flop, expected_output):
        actual_output = x.is_any_board_paired_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]

    @pytest.mark.parametrize('flop,expected_output', [
        ([[14, 'S'], [6, 'S'], [5, 'S']], [True, 13, 'S']),
        ([[13, 'S'], [6, 'S'], [5, 'S']], [True, 14, 'S']),
        ([[14, 'S'], [13, 'S'], [5, 'S']], [True, 12, 'S']),
        ([[14, 'S'], [13, 'S'], [12, 'S']], [True, 11, 'S'])
    ])
    def test_made_flush_on_flop(self, flop, expected_output):
        actual_output = x.made_flush_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]
        assert actual_output[2] == expected_output[2]

    @pytest.mark.parametrize('flop,expected_output', [
        ([[9, 'S'], [7, 'S'], [5, 'S']], [True, [[8,6]], 'C']),
        ([[9, 'S'], [8, 'S'], [7, 'S']], [True, [[11,10],[10,6],[6,5]], 'C']),
        ([[9, 'S'], [6, 'S'], [5, 'S']], [True, [[8,7]], 'C']),
        ([[9, 'S'], [8, 'S'], [5, 'S']], [True, [[7,6]], 'O']),
        ([[9, 'S'], [8, 'S'], [6, 'S']], [True, [[10,7],[7,5]], 'C']),
        ([[9, 'S'], [7, 'S'], [6, 'S']], [True, [[10,8],[8,5]], 'C']),
        ([[14, 'S'], [13, 'S'], [12, 'S']], [True, [[11,10]], 'C']),
        ([[13, 'S'], [12, 'S'], [10, 'S']], [True, [[14,11],[11,9]], 'C']),
        ([[14, 'S'], [12, 'S'], [11, 'S']], [True, [[13,10]], 'C']),
        ([[13, 'S'], [11, 'S'], [10, 'S']], [True, [[14,12],[12,9]], 'C'])
    ])
    @mock.patch('analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop.FlopHelper')
    def test_made_straight_on_flop(self, mock_organise_flop, flop, expected_output):
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
    def test_flush_draw_on_flop(self, flop, expected_output):
        actual_output = x.flush_draw_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]
        assert actual_output[2] == expected_output[2]

    @pytest.mark.parametrize('flop,expected_output', [
        ([[14, 'S'], [13, 'S'], [8, 'C']], [False, None, []]),
        ([[14, 'S'], [13, 'S'], [9, 'C']], [True, True, [[12,11,10]]]),
        ([[14, 'S'], [9, 'S'], [5, 'C']], [True, True, [[12,11,10],[8,7,6]]]),
        ([[10, 'S'], [7, 'S'], [6, 'C']], [True, True, [[11,9,8],[9,8,5]]]),
        ([[14, 'S'], [11, 'S'], [10, 'C']], [True, True, [[13,12,9]]]),
        ([[10, 'S'], [9, 'S'], [6, 'C']], [True, False, [[13,12,11],[12,11,8],[11,8,7],[8,7,5]]]),
    ])
    def test_wrap_draw_on_flop(self, flop, expected_output):
        actual_output = x.wrap_draw_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]

    @pytest.mark.parametrize('flop,expected_output', [
        # first two cards, straight draw
        ([[14, 'S'], [10, 'S'], [6, 'C']], [False, []]),
        ([[10, 'S'], [7, 'S'], [2, 'C']], [True, [[9,8]]]),
        ([[10, 'S'], [8, 'S'], [2, 'C']], [True, [[11,9],[9,7]]]),
        ([[10, 'S'], [9, 'S'], [2, 'C']], [True, [[12,11],[11,8],[8,7]]]),
        ([[14, 'S'], [12, 'S'], [2, 'C']], [True, [[13,11]]]),
        ([[13, 'S'], [12, 'S'], [2, 'C']], [True, [[14,11],[11,10]]]),
        ([[14, 'S'], [13, 'S'], [2, 'C']], [True, [[12,11]]]),
        # second two cards, straight draw
        # ([[14, 'S'], [10, 'S'], [6, 'C']], [False, []]),
        # ([[14, 'S'], [7, 'S'], [4, 'C']], [True, [[6,5]]]),
        # ([[14, 'S'], [8, 'S'], [6, 'C']], [True, [[9,7],[7,5]]]),
        # ([[13, 'S'], [9, 'S'], [8, 'C']], [True, [[11,10],[10,7],[7,6]]]),
        # ([[14, 'S'], [14, 'S'], [13, 'C']], [True, [[12,11]]]),
        # ([[14, 'S'], [13, 'S'], [12, 'C']], [True, [[11,10]]]),
    ])
    def test_straight_draw_on_flop(self, flop, expected_output):
        actual_output = x.wrap_draw_on_flop(flop)
        assert actual_output[0] == expected_output[0]
        assert actual_output[1] == expected_output[1]




def test_helper_flopped_nut_flush_draw():
    stack_tracker = {1:356, 2:356, 3:377.10, 4:0, 5:331.40, 6:0}
    SPR_tracker = {1:20, 2:25, 3:25, 4:0, 5:23, 6:0}
    guy_to_right_bet_size = 0
    positions_of_players_to_act_ahead_of_me = []
    pot_size = 20.0
    my_position = 4
    num_list = [13, 13, 6]
    suit_list = ['S', 'C', 'S']
    big_blind = 0.4
    x = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
                            positions_of_players_to_act_ahead_of_me,
                            pot_size, my_position, num_list, suit_list, big_blind)
    x.is_flush_completed_on_flop1 = True
    x.nut_flush_nums_flop1 = 13
    x.nut_flush_suit_flop1 = 'C'

    x.nut_flush_check()
