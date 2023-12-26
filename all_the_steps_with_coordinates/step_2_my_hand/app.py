from generate_num_and_suit_list import generate_num_list_from_my_hand


def run_num_list_suit_list():
    num_list, suit_list = generate_num_list_from_my_hand()

    # num list is an integer at this point, and suit list is made up of strings
    return num_list, suit_list


run_num_list_suit_list()
