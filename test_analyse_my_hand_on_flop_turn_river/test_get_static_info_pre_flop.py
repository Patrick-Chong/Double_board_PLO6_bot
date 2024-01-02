"""
The main thing this test package will test is the timing of running all the static information;
this part of the bot takes the most time to process due to the number of ss that need to be taken.

The only other thing to test is that the type() that each function spits out is what we expect.

N.B. To test this I need to have a real version of the app running, because it needs to take ss.
Need to run this pre_flop, but the nice thing is that IT DOES NOT need to be my turn to run it.
"""
import time

from get_static_info_pre_flop import RunFirstOneTime


class TestRunFirstOneTime:
    # Below takes 4 seconds to run, with table blinds slightly hacked.
    def test_how_long_it_takes_to_run_static_information(self):
        """
        To run this TEST, need to have the real pokerbros open, and in the right position!

        Can run this on single board table - just the blinds that won't be detected correctly.
        """
        start_time = time.time()
        rfot = RunFirstOneTime()
        my_position = rfot.take_SS_and_determine_position()
        num_suit_list_generator = rfot.run_num_list_suit_list()
        num_list = num_suit_list_generator[0]  # [14, 14, 10, 6, 5, 2]
        suit_list = num_suit_list_generator[1]  # ['C', 'D', 'S', 'H', 'H', 'S']
        empty_seat_tracker_f = RunFirstOneTime.get_empty_seat_tracker(my_position)
        big_blind = RunFirstOneTime.determine_table_blinds()
        print(f'type of my_position is: {type(my_position)} and the value is: {my_position}')
        print(f'type of num_list is: {type(num_list)} and the value is: {num_list}')
        print(f'type of suit_list is: {type(suit_list)} and the value is: {suit_list}')
        print(f'type of empty_seat_tracker_f is: {type(empty_seat_tracker_f)} and the value is: {empty_seat_tracker_f}')
        print(f'type of big_blind is: {type(big_blind)} and the value is: {big_blind}')
        end_time = time.time()
        print(f'The total time it takes to run static information is {round(end_time-start_time)} seconds')

