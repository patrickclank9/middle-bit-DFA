########################################################################################################################
# Project 2: DFA Middle Bit Success Rate Evaluator
# Group Members:
#   - Patrick Hernandez
#   -
#   -
#   -
# To Run Program:
#   Insert Input DFA in main, area is labeled
#   Run program and enter the length of the string to test
########################################################################################################################
import copy


# Alphabet is {0, 1}
class Dfa:
    def __init__(self, transitions=None, accepting=None, start='0'):
        if transitions is None:
            transitions = {}
        if accepting is None:
            accepting = []
        self.transitions = transitions
        self.accepting = accepting
        self.start = start

    def __copy__(self):
        transitions = copy.deepcopy(self.transitions)
        accepting = self.accepting.copy()
        start = copy.copy(self.start)
        return Dfa(transitions, accepting, start)

    # prints the DFA
    def print(self, end='\n'):
        print("{:9}{:_^11}|{:_^11}".format("Trans:", "'0'", "'1'"))
        for stateName in self.transitions:
            print('{:>9}'.format("['{}']:".format(stateName)), end="")
            for transition in self.transitions[stateName]:
                print("{:^11}".format("'{}'".format(transition)), end=" ")
            print("")
        print("Accepting: {}".format(self.accepting))
        print("Start: '{}'".format(self.start), end=end)

    # negates the accepting states
    def flip_accepting_states(self):
        inverted_accepting = []
        for stateName in self.transitions:
            if stateName not in self.accepting:
                inverted_accepting.append(stateName)
        self.accepting = inverted_accepting
        return self

    # returns true if input_str is accepted by the DFA, else false
    def accepts_str(self, input_str):
        current_state = self.start
        for char in input_str:
            bit = int(char)
            current_state = self.transitions[current_state][bit]
        return current_state in self.accepting


# returns  a dfa that accepts strings of length 'size' + 1 (size is number of states) with the middle bit being
# 'middle_bit'
def construct_middle_bit_dfa(input_dfa, size, middle_bit):
    output_dfa = Dfa()
    output_dfa.start = '0-{}'.format(input_dfa.start)
    final_layer = 0
    for layer in range(size):
        for stateName in input_dfa.transitions:
            current_key = '{}-{}'.format(layer, stateName)
            output_dfa.transitions[current_key] = ['', '']
            for transitionIdx in range(len(input_dfa.transitions[stateName])):
                next_state = '{}-{}'.format(layer + 1, input_dfa.transitions[stateName][transitionIdx])
                if layer == (size // 2) - 1:
                    if transitionIdx != middle_bit:
                        output_dfa.transitions[current_key][transitionIdx] = 'fail'
                    else:
                        output_dfa.transitions[current_key][transitionIdx] = next_state
                elif layer == size - 1:
                    output_dfa.transitions[current_key][transitionIdx] = 'fail'
                else:
                    output_dfa.transitions[current_key][transitionIdx] = next_state

        final_layer = layer
    for stateName in input_dfa.accepting:
        output_dfa.accepting.append('{}-{}'.format(final_layer, stateName))
    output_dfa.transitions['fail'] = ['fail', 'fail']
    return output_dfa


# returns the number of strings accepted by the dfa of length n
def count_num_of_strings(input_dfa, n):
    prev_col = {}
    for name in input_dfa.transitions:
        if name in input_dfa.accepting:
            prev_col[name] = 1
        else:
            prev_col[name] = 0
    next_col = {}

    # dynamic_table = [prev_col]

    def generate_next_col():
        current_state_str_count = 0
        for stateName in input_dfa.transitions:
            current_state_str_count = 0
            for transitionIdx in range(len(input_dfa.transitions[stateName])):
                next_transition = input_dfa.transitions[stateName][transitionIdx]
                current_state_str_count += prev_col[next_transition]
            next_col[stateName] = current_state_str_count
        return current_state_str_count

    for i in range(1, n + 1):
        generate_next_col()
        prev_col = next_col.copy()
        # dynamic_table.append(prev_col)
        next_col = {}
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(dynamic_table)
    return int(prev_col[input_dfa.start])


def count_dfa_successes_with_str_len(input_dfa, str_len):
    middle_bit_1_success_dfa = construct_middle_bit_dfa(input_dfa, str_len + 1, 1)
    middle_bit_0_fail_dfa = construct_middle_bit_dfa(copy.copy(input_dfa).flip_accepting_states(), str_len + 1, 0)
    middle_bit_1_success_dfa_count = count_num_of_strings(middle_bit_1_success_dfa, str_len)
    middle_bit_0_fail_dfa_count = count_num_of_strings(middle_bit_0_fail_dfa, str_len)
    # print("middle_bit_1_success_dfa_count: {}".format(middle_bit_1_success_dfa_count))
    # print("middle_bit_0_fail_dfa_count: {}".format(middle_bit_0_fail_dfa_count))
    return int(middle_bit_1_success_dfa_count + middle_bit_0_fail_dfa_count)


def count_dfa_successes_up_to_str_len(input_dfa, str_len):
    total = 0
    for length in range(1, str_len + 1):
        total += count_dfa_successes_with_str_len(input_dfa, length)
    return int(total)


# Only used for testing, ignore this
def brute_force_calc_successes(input_dfa, str_len):
    all_strings = []
    for i in range((2 ** str_len)):
        all_strings.append(("{0:0>" + "{}".format(str_len) + "b}").format(i))

    def has_middle_bit_1(input_str):
        return input_str[len(input_str) // 2] == '1'

    correctly_accepted = []
    correctly_rejected = []
    incorrectly_accepted = []
    incorrectly_rejected = []
    num_accepted_strings = 0
    for i in all_strings:
        if input_dfa.accepts_str(i):
            if has_middle_bit_1(i):
                num_accepted_strings += 1
                correctly_accepted.append(i)
            else:
                incorrectly_accepted.append(i)
        else:
            if not has_middle_bit_1(i):
                num_accepted_strings += 1
                correctly_rejected.append(i)
            else:
                incorrectly_rejected.append(i)

    # print("Successes = {}".format(successes))
    # print("correctly_accepted[{}] = {}".format(len(correctly_accepted), correctly_accepted))
    # print("correctly_rejected[{}] = {}".format(len(correctly_rejected), correctly_rejected))
    # print("incorrectly_accepted[{}] = {}".format(len(incorrectly_accepted), incorrectly_accepted))
    # print("incorrectly_rejected[{}] = {}".format(len(incorrectly_rejected), incorrectly_rejected))
    return int(num_accepted_strings)


def main():
    ##############################################################################################################
    # DFA INPUT HERE                                                                                                 #
    ##############################################################################################################

    # START STATE (ex. '0' ):
    start_state = '0'

    # ACCEPTING STATES (ex. ['0'] ):
    accepting_states = ['0']

    # TRANSITIONS (ex. { '0': ['0', '1'], '1': ['1', '0'] } ):
    transitions = {
        '0': ['0', '1'],
        '1': ['1', '0']
    }

    ##############################################################################################################
    # DFA INPUT END                                                                                                  #
    ##############################################################################################################
    M = Dfa(transitions, accepting_states, start_state)

    dfa_examples = [
        Dfa({
            '0': ['1', '0'],
            '1': ['0', '2'],
            '2': ['2', '2']
        }, ['0', '2'], '0'),
        Dfa({
            '0': ['0', '0']
        }, ['0'], '0'),
        Dfa({
            '0': ['0', '1'],
            '1': ['1', '0']
        }, ['0'], '0')
    ]
    print("Dfa M:")
    M.print('\n\n')
    print("Success rate of DFA M with strings of EXACTLY length n is\n -> (Number of successes)/(2^n)")
    print("Success rate of DFA M with strings UP TO length n is")
    print(" -> (Total number of successes)/(2^n + 2^(n-1) + ... + 2^1)")
    prompt = "##################################################################\nEnter length for n (0 to stop): "
    n = int(input(prompt))
    # n = 300 takes about 24 seconds to compute
    while n > 0:
        strings = 2 ** n
        total_strings = 0
        for i in range(1, n + 1):
            total_strings += 2 ** i
        successes_of_len = count_dfa_successes_with_str_len(M, n)
        successes_up_to_len = count_dfa_successes_up_to_str_len(M, n)
        print("Success rate of EXACTLY length n:\n{}\n/{}".format(successes_of_len, strings))
        print("≈ {}".format(successes_of_len / strings))
        print("Success rate UP TO length n:\n{}\n/{}".format(successes_up_to_len, total_strings))
        print("≈ {}".format(successes_up_to_len / total_strings))
        n = int(input(prompt))


main()
