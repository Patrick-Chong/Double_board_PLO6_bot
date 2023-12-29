from all_the_steps_with_coordinates.step_2_my_hand.is_my_hand_folded import check_if_my_cards_are_live
from all_the_steps_with_coordinates.step_2_my_hand.app import run_num_list_suit_list
from all_the_steps_with_coordinates.step_3_stack_sizes.my_stack import get_stack_sizes
from all_the_steps_with_coordinates.step_6_number_of_players_in_pot.num_of_players_in_pot import PlayersLeftInPot
from all_the_steps_with_coordinates.step_4_flop_turn_river.flop_turn_river import FlopTurnRiver
from all_the_steps_with_coordinates.step_5_how_muchbet_and_in_pot.pot_size_and_action_behind import PotSizeAndActionBehindMe
from all_the_steps_with_coordinates.step_7_detect_whos_turn_to_act.whos_turn_to_act import IsItMyTurnToAct
from get_static_info_pre_flop import RunFirstOneTime
from pre_flop_play.app_pre_flop import RunPreFlop
from analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_flop import AnalyseMyHandOnFlop
from CLICKING import click_fold_call_bet
from analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_turn import AnalyseMyHandOnTurn
from analyse_my_hand_on_flop_turn_river.analyse_my_hand_on_river import AnalyseMyHandOnRiver

ftr = FlopTurnRiver()
plip = PlayersLeftInPot()
rfot = RunFirstOneTime()


def go_to_the_right_street(action, street_we_are_on, extra_information, street_count):
	"""
	"""
	if street_we_are_on == 'pre_flop_play':
		print('running_pre_flop_analysis')
		action, extra_information = run_this_on_pre_flop_app_dot_py()
		print('finished_pre_flop_analysis')
	elif street_we_are_on == 'on_flop':
		print('running_on_flop_analysis')
		action, extra_information = run_this_on_the_flop_app_dot_py(action, extra_information)
	elif street_we_are_on == 'on_turn':
		print('running_on_turn_analysis')
		action, extra_information = run_this_on_the_turn_app_dot_py(action, extra_information)
	elif street_we_are_on == 'on_river':
		print('running_on_river_analysis')
		action, extra_information = run_this_on_the_river_app_dot_py(action, extra_information)

	return action, extra_information, street_count + 1


def run_this_on_pre_flop_app_dot_py():
	plip = PlayersLeftInPot()
	fold_tracker = plip.detect_if_cards_in_hand(my_position, empty_seat_tracker)
	stack_tracker = get_stack_sizes(my_position, fold_tracker)  # Set stack to 0 if someone folded; make this the universal way to check
	RPF = RunPreFlop(my_position, num_list, suit_list, big_blind, stack_tracker, empty_seat_tracker)
	action_pre_flop, extra_information = RPF.pre_flop_action()
	# all of the above takes a total of 6 seconds to run!
	click_fold_call_bet(action_pre_flop)
	return action_pre_flop, extra_information


def run_this_on_the_flop_app_dot_py(action, extra_information):
	fold_tracker = plip.detect_if_cards_in_hand(my_position, empty_seat_tracker)
	stack_tracker = get_stack_sizes(my_position, fold_tracker)  # Set stack to 0 if someone folded; make this the universal way to check

	PSABM = PotSizeAndActionBehindMe(my_position, fold_tracker, stack_tracker)
	pot_size = PSABM.pot_size()
	guy_to_right_bet_size = PSABM.scan_call_button_to_see_bet_amount()
	how_much_can_i_bet_or_raise_to = PSABM.how_much_can_i_raise_to(guy_to_right_bet_size)
	SPR_tracker = PSABM.calculate_SPR(how_much_can_i_bet_or_raise_to)
	positions_of_players_to_act_ahead_of_me = PSABM.are_there_players_to_act_ahead_of_me(how_much_can_i_bet_or_raise_to)
	# print('generating needed info on flop took 10s to run')

	AMHOF = AnalyseMyHandOnFlop(stack_tracker, SPR_tracker, guy_to_right_bet_size,
								positions_of_players_to_act_ahead_of_me, pot_size,
								my_position, num_list, suit_list, big_blind)

	action_on_flop, extra_information = AMHOF.analyse_my_hand_against_flop(action, extra_information)
	click_fold_call_bet(action_on_flop)
	return action_on_flop, extra_information


def run_this_on_the_turn_app_dot_py(action_on_flop, extra_information):
	fold_tracker = plip.detect_if_cards_in_hand(my_position, empty_seat_tracker)
	stack_tracker = get_stack_sizes(my_position, fold_tracker)  # Set stack to 0 if someone folded; make this the universal way to check

	PSABM = PotSizeAndActionBehindMe(my_position, fold_tracker, stack_tracker)
	pot_size = PSABM.pot_size()
	guy_to_right_bet_size = PSABM.scan_call_button_to_see_bet_amount()
	how_much_can_i_bet_or_raise_to = PSABM.how_much_can_i_raise_to(guy_to_right_bet_size)
	SPR_tracker = PSABM.calculate_SPR(how_much_can_i_bet_or_raise_to)
	positions_of_players_to_act_ahead_of_me = PSABM.are_there_players_to_act_ahead_of_me(how_much_can_i_bet_or_raise_to)

	AMHOT = AnalyseMyHandOnTurn(stack_tracker, SPR_tracker, guy_to_right_bet_size,
								positions_of_players_to_act_ahead_of_me, pot_size,
								my_position, num_list, suit_list, big_blind)

	action_on_turn = None
	if ftr.determine_street() == 'on_turn':
		action_on_turn, flopped, card_helper = AMHOT.analyse_my_hand_against_turn(action_on_flop, extra_information)
	click_fold_call_bet(action_on_turn)
	return action_on_turn, extra_information


def run_this_on_the_river_app_dot_py(action_on_turn, extra_information):

	fold_tracker = plip.detect_if_cards_in_hand(my_position, empty_seat_tracker)
	stack_tracker = get_stack_sizes(my_position, fold_tracker)  # Set stack to 0 if someone folded; make this the universal way to check
	# hu = run_throughout.are_we_heads_up()  - add this heads up function somewhere else.

	PSABM = PotSizeAndActionBehindMe(my_position, fold_tracker, stack_tracker)
	pot_size = PSABM.pot_size()
	guy_to_right_bet_size = PSABM.scan_call_button_to_see_bet_amount()
	how_much_can_i_bet_or_raise_to = PSABM.how_much_can_i_raise_to(guy_to_right_bet_size)
	SPR_tracker = PSABM.calculate_SPR(how_much_can_i_bet_or_raise_to)
	positions_of_players_to_act_ahead_of_me = PSABM.are_there_players_to_act_ahead_of_me(how_much_can_i_bet_or_raise_to)

	AMHOR = AnalyseMyHandOnRiver(stack_tracker, SPR_tracker, guy_to_right_bet_size,
								 positions_of_players_to_act_ahead_of_me,
								 pot_size, my_position, num_list, suit_list, big_blind)

	action_on_river = None
	if ftr.determine_street() == 'on_river':
		action_on_river, flopped, card_helper = AMHOR.analyse_my_hand_against_river(action_on_turn, extra_information)
	click_fold_call_bet(action_on_river)
	return action_on_river, extra_information


def run_new_hand():
	action = None
	extra_information = None
	street_count = 0  # to help determine when we are in a new hand

	# For each hand, we are inside the following while loop and DO NOT break out of it until end of hand
	while True:
		is_it_my_turn_to_act = IsItMyTurnToAct()
		while not is_it_my_turn_to_act.is_it_my_turn_to_act():
			street_we_are_on = ftr.determine_street()
			print(f'waiting for my turn to act, we are on street {street_we_are_on}')
		street_we_are_on = ftr.determine_street()
		action, extra_information, current_street = go_to_the_right_street(action, street_we_are_on, extra_information,
																		   street_count)
		# Check if we are in a new hand
		if action == 'fold':
			break
		if current_street > 0 and street_we_are_on == 'pre_flop':
			if num_list != run_num_list_suit_list()[0]:
				break

	print('end of hand detected, moving to new hand')


while True:
	print('waiting for a new hand to begin')
	# Small note worth mentioning - I think this runs constantly in the background - so if you cover your cards at the wrong time when it
	# scans this, then it has issues - only will happen when running against video because against real thing nothing will cover your cards
	# but in video when you hover over the screen something pops up.

	while check_if_my_cards_are_live():  # checked if I have folded - if so no need to run anything
		print('we are in a live hand')
		# generate static information
		my_position = rfot.take_SS_and_determine_position()
		num_list = rfot.num_list
		suit_list = rfot.suit_list
		empty_seat_tracker = rfot.empty_seat_tracker_f
		big_blind = rfot.big_blind
		print(f'my_position:{my_position}')
		print(f'num_list:{num_list}')
		print(f'suit_list:{suit_list}')
		print(f'empty_seat_tracker:{empty_seat_tracker}')
		print(f'big_blind:{big_blind}')
		if ftr.determine_street() == 'pre_flop_play' or ftr.determine_street() == 'on_flop':
			print('run new hand analysis')
			run_new_hand()


# BELOW IS TO HELP TRACK TIMING OF FUNCTIONS
# start_time = time.time()
# end_time = time.time()
# print(f'RPF above and pre_flop_action takes {round(end_time-start_time)}, "seconds")')
