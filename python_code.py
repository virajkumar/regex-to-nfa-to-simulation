"""This solution is still under construction"""
from typing import Dict, List, Set
from string import ascii_lowercase
from pprint import pprint

class State:
    num_states = 0
    every_state = []
    def __init__(self):
        State.num_states += 1
        State.every_state.append(self)
        self.state_id = State.num_states
        self.epsilon_transitions = []
        self.symbol_transitions = {}

    def add_transition(self, symbol, state):
        if symbol == '':
            self.epsilon_transitions.append(state)
        else:
            if symbol not in self.symbol_transitions:
                self.symbol_transitions[symbol] = []
            self.symbol_transitions[symbol].append(state)

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

    @staticmethod
    def from_symbol(symbol):
        start_state = State()
        accept_state = State()
        start_state.add_transition(symbol, accept_state)
        return NFA(start_state, accept_state)

    @staticmethod
    def concatenate(nfa1, nfa2):
        nfa1.accept.add_transition('', nfa2.start)
        return NFA(nfa1.start, nfa2.accept)

    @staticmethod
    def union(nfa1, nfa2):
        start_state = State()
        accept_state = State()
        start_state.add_transition('', nfa1.start)
        start_state.add_transition('', nfa2.start)
        nfa1.accept.add_transition('', accept_state)
        nfa2.accept.add_transition('', accept_state)
        return NFA(start_state, accept_state)

    @staticmethod
    def kleene_star(nfa):
        start_state = State()
        accept_state = State()
        start_state.add_transition('', nfa.start)
        start_state.add_transition('', accept_state)
        nfa.accept.add_transition('', nfa.start)
        nfa.accept.add_transition('', accept_state)
        return NFA(start_state, accept_state)

    @staticmethod
    def build_from_regex(regex):
        stack = []
        operators = {'*', '|', '.'}
        
        for char in regex:
            if char not in operators:
                stack.append(NFA.from_symbol(char))
            elif char == '.':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(NFA.concatenate(nfa1, nfa2))
            elif char == '|':
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(NFA.union(nfa1, nfa2))
            elif char == '*':
                nfa = stack.pop()
                stack.append(NFA.kleene_star(nfa))

        return stack.pop()

def prune_stars(p):
    i = 0
    old_p = p
    mid_p = [0 for i in p]
    new_p = []
    flag1 = False
    for c in old_p:
        if flag1:
            if c == '*':
                mid_p[i] = 1
            else:
                flag1 = False
        if c == '*':
            flag1 = True
        i += 1

    for i in range(0, len(old_p)):
        if mid_p[i] == 0:
            new_p.append(old_p[i])

    return "".join(new_p)

def match_expr(s, nfa):
    if s == '':
        if len(nfa.start.epsilon_transitions) >= 2 and nfa.start.epsilon_transitions[1] is nfa.accept:
            return True
        else:
            return False
    else:
        i = 0
        c = s[i]
        ep_states = {}
        curr_states = [nfa.start]
        flag_is_accept_state = {'val': False}

        def check_ep_transitions(start_states):
            for state in start_states:
                keys = state.symbol_transitions.keys()
                if len(keys) > 0:
                    for k in state.symbol_transitions:
                        val = state.symbol_transitions[k]
                        if k in ep_states.keys():
                            ep_states[k] = ep_states[k] + val
                        else:
                            ep_states.update({k: val})
                check_ep_transitions(state.epsilon_transitions)

        def check_ep_accept(accept_state, curr_states):
            for curr_state in curr_states:
                if accept_state is curr_state:
                    flag_is_accept_state['val'] = True
                else:
                    check_ep_accept(accept_state, curr_state.epsilon_transitions)

        while True:
            check_ep_transitions(curr_states)

            all_states = ep_states

            for state in curr_states:
                all_states.update(state.symbol_transitions)

            ep_states = {}

            if c in all_states.keys() and i < len(s):
                flag_is_accept_state['val'] = False
                curr_states = all_states[c]
                check_ep_accept(nfa.accept, curr_states)
                if flag_is_accept_state['val'] and i == len(s) - 1:
                    return True
                elif i == len(s) - 1:
                    return False
                elif i < len(s) - 1:
                    i += 1
                    c = s[i]
            else:
                return False

def build_NFA_star():
    NFA_0 = NFA.from_symbol('a')
    NFA_star = NFA_0

    for c in ascii_lowercase[1:len(ascii_lowercase)]:
        NFA_star = NFA.union(NFA_star, NFA.from_symbol(c))  
    
    NFA_star = NFA.kleene_star(NFA_star)

    return NFA_star

def build_NFA_question():
    NFA_0 = NFA.from_symbol('a')
    NFA_question = NFA_0

    for c in ascii_lowercase[1:len(ascii_lowercase)]:
        NFA_question = NFA.union(NFA_question, NFA.from_symbol(c))

    return NFA_question

def build_NFA(regex):
    flag1 = True
    nfa = {}
    for c in regex:
        if flag1:
            if c == '*':
                nfa = build_NFA_star()
            elif c == '?':
                nfa = build_NFA_question()
            else:
                nfa = NFA.from_symbol(c)
            flag1 = False
            continue
        if c == '*':
            nfa = NFA.concatenate(nfa, build_NFA_star())
        elif c == '?':
            nfa = NFA.concatenate(nfa, build_NFA_question())
        else:
            nfa = NFA.concatenate(nfa, NFA.from_symbol(c))
    return nfa

my_nfa = build_NFA(prune_stars("abc"))

ep_states = []

oldStates = []
newStates = []

alreadyOn = {}

move = {}

def E_closure_s(state):
    # if state not in ep_states:
    #     ep_states.append()
    for ep_state in state.epsilon_transitions:
        ep_states.append(ep_state)
        for ep_state_2 in ep_state.epsilon_transitions:
            E_closure_s(ep_state_2)

def iterate_states():
    for state in State.every_state:
        move.update({(state, "epsilon"): [state]})
        alreadyOn.update({state: False})

    for state in State.every_state:
        move[(state, "epsilon")] += state.epsilon_transitions
        sy_trans = state.symbol_transitions
        for sy_key in sy_trans.keys():
            move.update({(state, sy_key): sy_trans[sy_key]})
    
    # for ep_state in start_state.epsilon_transitions:
    #     alreadyOn.update({ep_state: False})
    #     if (start_state, "epsilon") in move.keys() and ep_state not in move[(start_state, "epsilon")]:
    #         move[(start_state, "epsilon")] += [ep_state]
    #     elif (start_state, "epsilon") not in move.keys():
    #         move.update({(start_state, "epsilon"): [ep_state]})
    #     iterate_states(ep_state)

    # sy_trans = start_state.symbol_transitions
    # for sy_key in sy_trans:
    #     for sy_state in sy_trans[sy_key]:
    #         if (start_state, sy_key) in move.keys() and sy_state not in move[(start_state, sy_key)]:
    #             move[(sy_state, sy_key)] += [sy_state]
    #         elif (start_state, sy_key) not in move.keys():
    #             move.update({(start_state, sy_key): [sy_state]})
    #         if sy_state in alreadyOn.keys():
    #             return
    #         else:
    #             alreadyOn.update({sy_state: False})
    #     iterate_states(sy_state)

# def add_self_ep_trans():
#     for state in State.every_state:
#         if (state, "epsilon") in move.keys() and state not in move[(state, "epsilon")]:
#             move[(state, "epsilon")] += [state]
#         elif (state, "epsilon") not in move.keys():
#             move.update({(state, "epsilon"): [state]})

def addState(state):
    newStates.append(state)
    alreadyOn[state] = True
    for state_t in move[(state, "epsilon")]:
        if (not alreadyOn[state_t]):
            addState(state_t)

#print(move)

#build_move()

#print(move)

#print(alreadyOn)

def simulate_NFA(s, nfa):
    iterate_states()
    E_closure_s(nfa.start)
    #add_self_ep_trans()

    ep_states.append(nfa.start)
    alreadyOn.update({nfa.start: False})

    for state in ep_states:
        oldStates.append(state)
        alreadyOn[state] = True

    for c in s:
        oldStates.reverse()
        for state in oldStates:
            if (state, c) in move.keys():
                for state_t in move[(state, c)]:
                    if not alreadyOn[state_t]:
                        addState(state_t)
                oldStates.reverse()
                oldStates.pop()
                oldStates.reverse()
        oldStates.reverse()

        newStates.reverse()
        for state in newStates:
            state = newStates.pop()
            oldStates.append(state)
            alreadyOn[state] = False
        newStates.reverse()

    if nfa.accept in oldStates:
        return True
    else:
        return False

#print(State.every_state)

print(simulate_NFA("abc", my_nfa))

#print(ep_states)

#print(match_expr("aabbba", my_nfa))

#print(match_expr("aaabababaaabaababbbaaaabbbbbbabbbbabbbabbaabbababab", my_nfa))

# for key, value in NFA_star.start.epsilon_transitions[1].symbol_transitions:
#     print(NFA_star.start.epsilon_transitions[1].symbol_transitions.keys())

# print(type(NFA_star.start.epsilon_transitions[1].symbol_transitions))
#print(NFA_star.start.symbol_transitions['a'])

#NFA_star = NFA.union(NFA_star, NFA.from_symbol('b'))

#NFA_star = NFA.union(NFA_star, NFA.from_symbol(''))

#NFA_star = NFA.concatenate(NFA_star, NFA.from_symbol('d'))

# x = []
# x.append(NFA_star.start.epsilon_transitions[0].epsilon_transitions[1].symbol_transitions['z'][0])
# pprint(x[0])

#pprint(vars(NFA_star.start.epsilon_transitions[1].symbol_transitions['b'][0]))