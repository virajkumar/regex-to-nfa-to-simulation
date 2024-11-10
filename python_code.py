"""This solution is still under construction"""
from typing import Dict, List, Set
from string import ascii_lowercase
from pprint import pprint

# class State:
#     num_states = 0
#     every_state = []
#     def __init__(self):
#         State.num_states += 1
#         State.every_state.append(self)
#         self.state_id = State.num_states
#         self.epsilon_transitions = []
#         self.symbol_transitions = {}

#     def add_transition(self, symbol, state):
#         if symbol == '':
#             self.epsilon_transitions.append(state)
#         else:
#             if symbol not in self.symbol_transitions:
#                 self.symbol_transitions[symbol] = []
#             self.symbol_transitions[symbol].append(state)

# class NFA:
#     def __init__(self, start, accept):
#         self.start = start
#         self.accept = accept

#     @staticmethod
#     def from_symbol(symbol):
#         start_state = State()
#         accept_state = State()
#         start_state.add_transition(symbol, accept_state)
#         return NFA(start_state, accept_state)

#     @staticmethod
#     def concatenate(nfa1, nfa2):
#         nfa1.accept.add_transition('', nfa2.start)
#         return NFA(nfa1.start, nfa2.accept)

#     @staticmethod
#     def union(nfa1, nfa2):
#         start_state = State()
#         accept_state = State()
#         start_state.add_transition('', nfa1.start)
#         start_state.add_transition('', nfa2.start)
#         nfa1.accept.add_transition('', accept_state)
#         nfa2.accept.add_transition('', accept_state)
#         return NFA(start_state, accept_state)

#     @staticmethod
#     def kleene_star(nfa):
#         start_state = State()
#         accept_state = State()
#         start_state.add_transition('', nfa.start)
#         start_state.add_transition('', accept_state)
#         nfa.accept.add_transition('', nfa.start)
#         nfa.accept.add_transition('', accept_state)
#         return NFA(start_state, accept_state)

#     @staticmethod
#     def build_from_regex(regex):
#         stack = []
#         operators = {'*', '|', '.'}
        
#         for char in regex:
#             if char not in operators:
#                 stack.append(NFA.from_symbol(char))
#             elif char == '.':
#                 nfa2 = stack.pop()
#                 nfa1 = stack.pop()
#                 stack.append(NFA.concatenate(nfa1, nfa2))
#             elif char == '|':
#                 nfa2 = stack.pop()
#                 nfa1 = stack.pop()
#                 stack.append(NFA.union(nfa1, nfa2))
#             elif char == '*':
#                 nfa = stack.pop()
#                 stack.append(NFA.kleene_star(nfa))

#         return stack.pop()

# def prune_stars(p):
#     i = 0
#     old_p = p
#     mid_p = [0 for i in p]
#     new_p = []
#     flag1 = False
#     for c in old_p:
#         if flag1:
#             if c == '*':
#                 mid_p[i] = 1
#             else:
#                 flag1 = False
#         if c == '*':
#             flag1 = True
#         i += 1

#     for i in range(0, len(old_p)):
#         if mid_p[i] == 0:
#             new_p.append(old_p[i])

#     return "".join(new_p)

# def match_expr(s, nfa):
#     if s == '':
#         if len(nfa.start.epsilon_transitions) >= 2 and nfa.start.epsilon_transitions[1] is nfa.accept:
#             return True
#         else:
#             return False
#     else:
#         i = 0
#         c = s[i]
#         ep_states = {}
#         curr_states = [nfa.start]
#         flag_is_accept_state = {'val': False}

#         def check_ep_transitions(start_states):
#             for state in start_states:
#                 keys = state.symbol_transitions.keys()
#                 if len(keys) > 0:
#                     for k in state.symbol_transitions:
#                         val = state.symbol_transitions[k]
#                         if k in ep_states.keys():
#                             ep_states[k] = ep_states[k] + val
#                         else:
#                             ep_states.update({k: val})
#                 check_ep_transitions(state.epsilon_transitions)

#         def check_ep_accept(accept_state, curr_states):
#             for curr_state in curr_states:
#                 if accept_state is curr_state:
#                     flag_is_accept_state['val'] = True
#                 else:
#                     check_ep_accept(accept_state, curr_state.epsilon_transitions)

#         while True:
#             check_ep_transitions(curr_states)

#             all_states = ep_states

#             for state in curr_states:
#                 all_states.update(state.symbol_transitions)

#             ep_states = {}

#             if c in all_states.keys() and i < len(s):
#                 flag_is_accept_state['val'] = False
#                 curr_states = all_states[c]
#                 check_ep_accept(nfa.accept, curr_states)
#                 if flag_is_accept_state['val'] and i == len(s) - 1:
#                     return True
#                 elif i == len(s) - 1:
#                     return False
#                 elif i < len(s) - 1:
#                     i += 1
#                     c = s[i]
#             else:
#                 return False

# def build_NFA_star():
#     NFA_0 = NFA.from_symbol('a')
#     NFA_star = NFA_0

#     for c in ascii_lowercase[1:len(ascii_lowercase)]:
#         NFA_star = NFA.union(NFA_star, NFA.from_symbol(c))  
    
#     NFA_star = NFA.kleene_star(NFA_star)

#     return NFA_star

# def build_NFA_question():
#     NFA_0 = NFA.from_symbol('a')
#     NFA_question = NFA_0

#     for c in ascii_lowercase[1:len(ascii_lowercase)]:
#         NFA_question = NFA.union(NFA_question, NFA.from_symbol(c))

#     return NFA_question

# def build_NFA(regex):
#     flag1 = True
#     nfa = {}
#     for c in regex:
#         if flag1:
#             if c == '*':
#                 nfa = build_NFA_star()
#             elif c == '?':
#                 nfa = build_NFA_question()
#             else:
#                 nfa = NFA.from_symbol(c)
#             flag1 = False
#             continue
#         if c == '*':
#             nfa = NFA.concatenate(nfa, build_NFA_star())
#         elif c == '?':
#             nfa = NFA.concatenate(nfa, build_NFA_question())
#         else:
#             nfa = NFA.concatenate(nfa, NFA.from_symbol(c))
#     return nfa

# # my_nfa = build_NFA(prune_stars("abc"))

# # ep_states = []

# # oldStates = []
# # newStates = []

# # alreadyOn = {}

# # move = {}

# def E_closure_s(state):
#     # if state not in ep_states:
#     #     ep_states.append()
#     for ep_state in state.epsilon_transitions:
#         ep_states.append(ep_state)
#         for ep_state_2 in ep_state.epsilon_transitions:
#             E_closure_s(ep_state_2)

# def iterate_states():
#     for state in State.every_state:
#         move.update({(state, "epsilon"): [state]})
#         alreadyOn.update({state: False})

#     for state in State.every_state:
#         move[(state, "epsilon")] += state.epsilon_transitions
#         sy_trans = state.symbol_transitions
#         for sy_key in sy_trans.keys():
#             move.update({(state, sy_key): sy_trans[sy_key]})
    
#     # for ep_state in start_state.epsilon_transitions:
#     #     alreadyOn.update({ep_state: False})
#     #     if (start_state, "epsilon") in move.keys() and ep_state not in move[(start_state, "epsilon")]:
#     #         move[(start_state, "epsilon")] += [ep_state]
#     #     elif (start_state, "epsilon") not in move.keys():
#     #         move.update({(start_state, "epsilon"): [ep_state]})
#     #     iterate_states(ep_state)

#     # sy_trans = start_state.symbol_transitions
#     # for sy_key in sy_trans:
#     #     for sy_state in sy_trans[sy_key]:
#     #         if (start_state, sy_key) in move.keys() and sy_state not in move[(start_state, sy_key)]:
#     #             move[(sy_state, sy_key)] += [sy_state]
#     #         elif (start_state, sy_key) not in move.keys():
#     #             move.update({(start_state, sy_key): [sy_state]})
#     #         if sy_state in alreadyOn.keys():
#     #             return
#     #         else:
#     #             alreadyOn.update({sy_state: False})
#     #     iterate_states(sy_state)

# # def add_self_ep_trans():
# #     for state in State.every_state:
# #         if (state, "epsilon") in move.keys() and state not in move[(state, "epsilon")]:
# #             move[(state, "epsilon")] += [state]
# #         elif (state, "epsilon") not in move.keys():
# #             move.update({(state, "epsilon"): [state]})

# def addState(state):
#     newStates.append(state)
#     alreadyOn[state] = True
#     for state_t in move[(state, "epsilon")]:
#         if (not alreadyOn[state_t]):
#             addState(state_t)

# #print(move)

# #build_move()

# #print(move)

# #print(alreadyOn)

# def simulate_NFA(s, nfa):
#     iterate_states()
#     E_closure_s(nfa.start)
#     #add_self_ep_trans()

#     ep_states.append(nfa.start)
#     alreadyOn.update({nfa.start: False})

#     for state in ep_states:
#         oldStates.append(state)
#         alreadyOn[state] = True

#     for c in s:
#         oldStates.reverse()
#         for state in oldStates:
#             if (state, c) in move.keys():
#                 for state_t in move[(state, c)]:
#                     if not alreadyOn[state_t]:
#                         addState(state_t)
#                 oldStates.reverse()
#                 oldStates.pop()
#                 oldStates.reverse()
#         oldStates.reverse()

#         newStates.reverse()
#         for state in newStates:
#             state = newStates.pop()
#             oldStates.append(state)
#             alreadyOn[state] = False
#         newStates.reverse()

#     if nfa.accept in oldStates:
#         return True
#     else:
#         return False

#print(State.every_state)

#print(simulate_NFA("abc", my_nfa))

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

# class State:
#     def __init__(self, is_accept=False):
#         self.is_accept = is_accept
#         self.transitions = {}

#     def add_transition(self, symbol, state):
#         if symbol in self.transitions:
#             self.transitions[symbol].append(state)
#         else:
#             self.transitions[symbol] = [state]

# class NFA:
#     def __init__(self, start, accept):
#         self.start = start
#         self.accept = accept
#         self.states = set()
#         self.add_state(start)
#         self.add_state(accept)

#     def add_state(self, state):
#         self.states.add(state)

#     def epsilon_closure(self, states):
#         stack = list(states)
#         closure = set(states)
#         while stack:
#             state = stack.pop()
#             if '' in state.transitions:
#                 for next_state in state.transitions['']:
#                     if next_state not in closure:
#                         closure.add(next_state)
#                         stack.append(next_state)
#         return closure

#     def move(self, states, symbol):
#         next_states = set()
#         for state in states:
#             if symbol in state.transitions:
#                 next_states.update(state.transitions[symbol])
#         return self.epsilon_closure(next_states)

#     def simulate(self, string):
#         current_states = self.epsilon_closure({self.start})
#         for symbol in string:
#             current_states = self.move(current_states, symbol)
#         return any(state.is_accept for state in current_states)

# def regex_to_nfa(regex):
#     stack = []

#     def create_basic_nfa(symbol):
#         start = State()
#         accept = State(is_accept=True)
#         start.add_transition(symbol, accept)
#         return NFA(start, accept)

#     operators = {'*', '|', '.'}
#     output = []
#     for i, char in enumerate(regex):
#         if char not in operators and (i == 0 or regex[i - 1] in operators or regex[i - 1] == '('):
#             output.append(char)
#         elif char not in operators and regex[i - 1] not in operators and regex[i - 1] != '(':
#             output.append('.')
#             output.append(char)
#         else:
#             output.append(char)

#     for char in output:
#         if char.isalnum():  # Handle literal characters
#             stack.append(create_basic_nfa(char))
#         elif char == '*':
#             nfa = stack.pop()
#             start = State()
#             accept = State(is_accept=True)
#             start.add_transition('', nfa.start)
#             nfa.accept.add_transition('', accept)
#             nfa.accept.add_transition('', nfa.start)
#             stack.append(NFA(start, accept))
#         elif char == '|':
#             nfa2 = stack.pop()
#             nfa1 = stack.pop()
#             start = State()
#             accept = State(is_accept=True)
#             start.add_transition('', nfa1.start)
#             start.add_transition('', nfa2.start)
#             nfa1.accept.add_transition('', accept)
#             nfa2.accept.add_transition('', accept)
#             stack.append(NFA(start, accept))
#         elif char == '.':
#             nfa2 = stack.pop()
#             nfa1 = stack.pop()
#             nfa1.accept.add_transition('', nfa2.start)
#             stack.append(NFA(nfa1.start, nfa2.accept))

#     if len(stack) != 1:
#         raise ValueError("Invalid regular expression")

#     return stack.pop()

# # Example usage:
# if __name__ == "__main__":
#     regex = "a.b|c*"  # Example regular expression
#     nfa = regex_to_nfa(regex)
#     test_string = "ab"  # Example string to simulate
#     result = nfa.simulate(test_string)
#     print("Accepted" if result else "Rejected")

class State:
    num_states = 0
    all_states = []
    
    def __init__(self):
        self.state_id = State.num_states
        State.num_states += 1
        State.all_states.append(self)
        self.epsilon_transitions = []
        self.symbol_transitions = {}
        self.epsilon_transitions.append(self)

    def __del__(self):
        if self in State.all_states:
            State.all_states.remove(self)
            State.num_states -= 1
        for i in range(State.num_states):
            State.all_states[i].state_id = i
    
    def add_transition(self, symbol, state):
        if symbol == '':
            self.epsilon_transitions.append(state)
        else:
            if symbol not in self.symbol_transitions:
                self.symbol_transitions[symbol] = []
            self.symbol_transitions[symbol].append(state)

class NFA:
    def __init__(self, start_state, accept_state):
        self.s0 = start_state
        self.accept_state = accept_state

    @staticmethod
    def from_symbol(symbol):
        start_state = State()
        accept_state = State()
        start_state.add_transition(symbol, accept_state)
        return NFA(start_state, accept_state)

    @staticmethod
    def concatenate(nfa1, nfa2):
        for state in State.all_states:
            if nfa1.accept_state in state.epsilon_transitions:
                state.epsilon_transitions.remove(nfa1.accept_state)
                nfa1.accept_state.__del__()
                state.epsilon_transitions.append(nfa2.s0)
            for symbol in state.symbol_transitions:
                if nfa1.accept_state in state.symbol_transitions[symbol]:
                    state.symbol_transitions[symbol].remove(nfa1.accept_state)
                    nfa1.accept_state.__del__()
                    state.symbol_transitions[symbol].append(nfa2.s0)

        #nfa1.accept.add_transition('', nfa2.start)
        return NFA(nfa1.s0, nfa2.accept_state)

    @staticmethod
    def union(nfa1, nfa2):
        for state in nfa2.s0.epsilon_transitions:
            nfa1.s0.add_transition('', state)
        for symbol in nfa2.s0.symbol_transitions:
            for state in nfa2.s0.symbol_transitions[symbol]:
                nfa1.s0.add_transition(symbol, state)

        for state in State.all_states:
            if nfa2.accept_state in state.epsilon_transitions:
                state.epsilon_transitions.remove(nfa2.accept_state)
                nfa2.accept_state.__del__()
                state.epsilon_transitions.append(nfa1.accept_state)
            for symbol in state.symbol_transitions:
                if nfa2.accept_state in state.symbol_transitions[symbol]:
                    state.symbol_transitions[symbol].remove(nfa2.accept_state)
                    nfa2.accept_state.__del__()
                    state.symbol_transitions[symbol].append(nfa1.accept_state)

        return nfa1

    @staticmethod
    def kleene_star(nfa):
        start_state = State()
        accept_state = State()
        start_state.add_transition('', nfa.s0)
        start_state.add_transition('', accept_state)
        nfa.accept_state.add_transition('', nfa.s0)
        nfa.accept_state.add_transition('', accept_state)

        return NFA(start_state, accept_state)
    
    @staticmethod
    def e_closure(s0):
        return s0.epsilon_transitions

    @staticmethod
    def move(state, c, move_table):
        if state in move_table:
            if c in move_table[state]:  
                return move_table[state][c]
        return []

def construct_nfa(regex):
    nfa = {}
    flag1 = True
    flag_union = False
    operators = {'*', '|', '(', ')'}    
    i = 0

    for char in regex:
        if flag_union:
            flag_union = False
            continue
        if char not in operators:
            if flag1:
                nfa = NFA.from_symbol(char)
                flag1 = False
            else:
                nfa = NFA.concatenate(nfa, (NFA.from_symbol(char)))
        if char == '(':
            j = 0
            while regex[i + j] != ')':
                j += 1
            nfa = NFA.concatenate(nfa, construct_nfa(regex[i + 1, j + 1]))
        elif char == '|':                                                    #'|' union operator can only occur between alphabets, not between brackets. The whole union expression must be closed in brackets. eg: (a|b|c) is ok, but (ka|b|c) is not ok.
            nfa = NFA.union(nfa, NFA.from_symbol(regex[i + 1]))
            flag_union = True
        elif char == '*':
            nfa = NFA.kleene_star(nfa)
        i += 1

    return nfa

def construct_already_on(nfa):
    already_on = []
    for i in range(State.num_states):
        already_on.append(False)
    return already_on

def construct_move(nfa, unique_chars, move_table):
    for ep_state in nfa.s0.epsilon_transitions:
        if nfa.s0.state_id not in move_table:
            move_table[nfa.s0.state_id] = {}
            move_table[nfa.s0.state_id]['('] = []
        if ep_state not in move_table[nfa.s0.state_id]['(']:
            move_table[nfa.s0.state_id]['('].append(ep_state)
            construct_move(NFA(ep_state, nfa.accept_state), unique_chars, move_table)
    for symbol in nfa.s0.symbol_transitions:
        for state in nfa.s0.symbol_transitions[symbol]:
            if nfa.s0.state_id not in move_table:
                move_table[nfa.s0.state_id] = {}
            if symbol not in move_table[nfa.s0.state_id]:
                move_table[nfa.s0.state_id][symbol] = []
            if state not in move_table[nfa.s0.state_id][symbol]:        
                move_table[nfa.s0.state_id][symbol].append(state)
                construct_move(NFA(state, nfa.accept_state), unique_chars, move_table)

def find_unique_chars(input_str):
    unique_chars = []
    unique_chars.append('(')
    for c in input_str:
        if c not in unique_chars:
            unique_chars.append(c)
    return unique_chars

regex = "abcd"
nfa = construct_nfa(regex)
already_on = construct_already_on(nfa)
old_states = NFA.e_closure(nfa.s0)
new_states = []

for state in old_states:
    already_on[state.state_id] = True

def simulate_nfa(input_str, nfa):
    input_str = list(input_str)
    input_str.reverse()
    unique_chars = find_unique_chars(input_str)
    move = {}
    construct_move(nfa, unique_chars, move)

    def add_state(s):
        new_states.append(s)
        already_on[s.state_id] = True
        if '(' in move[s.state_id]:
            for t in move[s.state_id]['(']:
                if not already_on[t.state_id]:
                    add_state(t)

    while input_str != []:
        c = input_str.pop()
        for state in old_states:
            if c in move[state.state_id]:
                for t in move[state.state_id][c]:
                    if not already_on[t.state_id]:
                        add_state(t)
            old_states.remove(state)    

        for state in new_states:
            curr_state = new_states.pop(new_states.index(state))
            old_states.append(curr_state)
            already_on[state.state_id] = False

        #new_states = nfa.e_closure(nfa.move(old_states, c))
        #old_states = new_states
    
    if nfa.accept_state in old_states:
        return True
    else:
        return False

print(simulate_nfa("abcd", nfa))