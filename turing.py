# a turing machine
# written by Graham Knight (@nikukatansa)
# and Jesse Sibley (@chickencoder)

import sys

def load_rules(filename, bits):
    max_state = 0
    rule_lines = []
    move_tracker = []
    move_states = 0

    # Work out max state and track moves that are greater than 1 cell
    f = open(filename, 'r')

    # Line syntax [v,s] => [V,S,M]
    for ln in f.readlines():
        ln = ln.replace("\n", "")
        ln = ln.replace("n", bits)
        lxs = ln.split(" => ")
        state_part = eval(lxs[0])
        rule_part = eval(lxs[1])

        if state_part[1] > max_state:
            max_state = state_part[1]

        if abs(rule_part[2]) > 1:
            # move_tracker entries = [state after move, move distance, beginning state for move (calculated later)]
            # don't add any duplicate tuples
            if ([rule_part[1], rule_part[2], 0]) not in move_tracker:
                move_tracker.append([rule_part[1], rule_part[2], 0])
                move_states += abs(rule_part[2])

        rule_lines.append(ln)

    # add an extra 2 * move_states to rules
    # when we encounter a rule with abs(M)>1, replace with M states each moving head by +/- 1. Advance to next state apart from on final state which uses move_states[n][0] to return to original state.  Need a v=0 and v=1 rule for each, with V=0 and V=1 respectively

    rules = [[0, -2, 0]] * (2 * (max_state + move_states +1))

    move_state_index = max_state + 1
    move_state_pos = 2 * (max_state + 1)

    for moves in move_tracker:
        if moves[1] > 0:
            move_dir = 1
        else:
            move_dir = -1
        
        moves[2] = move_state_index

        for move_state_part in range (0, abs(moves[1]) - 1):
            rules[move_state_pos] = [0, move_state_index + 1, move_dir]
            move_state_pos += 1
            rules[move_state_pos] = [1, move_state_index + 1, move_dir]
            move_state_pos += 1
            move_state_index += 1

        rules[move_state_pos] = [0, moves[0], move_dir]
        move_state_pos += 1
        rules[move_state_pos] = [1, moves[0], move_dir]
        move_state_pos += 1
        move_state_index += 1

    f_prime = open("adjusted_" + filename, 'w')
    for rule in rule_lines:
        r = rule.split(" => ")
        v = eval(r[0])[0]
        s = eval(r[0])[1]

        if abs(eval(r[1])[2]) > 1:
            subs = [tup for tup in move_tracker if tup[0] == eval(r[1])[1] and tup[1] == eval(r[1])[2]]
            rules[(2 * s) + v] = [eval(r[1])[0], subs[0][2], 0]
            f_prime.write("[" + str(v) + ", " + str(s) + "] => [" + str(eval(r[1])[0]) + ", " + str(subs[0][2]) + ", 0]\n") 
        else:
            rules[(2 * s) + v] = eval(r[1])
            f_prime.write("[" + str(v) + ", " + str(s) + "] => " + str(eval(r[1])) + "\n")

    for new_rule_idx in range (2 * (max_state + 1), len(rules)):
        v = new_rule_idx % 2
        s = new_rule_idx // 2
        f_prime.write(str([v,s]) + " => " + str(rules[new_rule_idx])+ "\n")

    return rules

def run(rule_file, tape_data, bits):
    tape = eval(tape_data)
    rules = load_rules(rule_file, bits)
    min_index = 0
    max_index = len(tape)
    head = 0
    state = 0

    while state > -1:
        val = tape[head]
        current_rule = rules[(2 * state) + val]
        tape_str = str(tape[0:head]) + "_" + str(val) + "_" + str(tape[head+1:])
        tape_str = tape_str.replace('[','').replace(']','').replace(', ','')
        print("State " + str(state) + ", rule " + str(current_rule))
        print("Tape " + tape_str + '\n')

        tape[head] = current_rule[0]
        state = current_rule[1]
        head += current_rule[2]

        if head > max_index:
            tape += [0] * 3
            max_index += 3

        if head < min_index:
            tape = [0] * 3 + tape
            max_index += 3
            head += 3

    print("Result = " + str(tape).replace('[','').replace(']','').replace(', ',''))

if __name__ == "__main__":
    if(len(sys.argv) == 4):
        run(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        run(sys.argv[1], sys.argv[2], 0)
