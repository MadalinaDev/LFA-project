import random
from collections import deque

class Grammar:
    # Defining in the constructor my terminals, non-terminals, production rules, and initial state S
    def __init__(self):
        self.VN = {'S', 'I', 'J', 'K'}
        self.VT = {'a', 'b', 'c', 'e', 'n', 'f', 'm'}
        self.P = {
            'S': ['cI'],
            'I': ['bJ', 'fI', 'eK', 'e'],
            'J': ['nJ', 'cS'],
            'K': ['nK', 'm']
        }
        self.S = 'S'

    # Using recursion to derive randomly words based on the grammar rules
    def generate_string(self):
        def expand(symbol):
            if symbol in self.VT:
                return symbol
            else:
                production = random.choice(self.P[symbol])
                return ''.join(expand(sym) for sym in production)
        return expand(self.S)

    # Transforming my grammar into a finite automaton
    def to_finite_automaton(self):
        return FiniteAutomaton(self)


class FiniteAutomaton:
    # Defining in the constructor my finite automaton components
    def __init__(self, grammar):
        self.states = grammar.VN.union({'F'})
        self.alphabet = grammar.VT
        self.transitions = {state: {} for state in self.states}
        self.start_state = grammar.S
        self.final_states = {'F'}
        self.__form_transitions(grammar)

    # To build transitions, implementing a map of states and transitions
    def __form_transitions(self, grammar):
        for state in grammar.VN:
            for production in grammar.P[state]:
                if len(production) == 1 and production[0] in grammar.VT:
                    # transitioning to final state 'F' for single terminal
                    self.transitions[state].setdefault(production[0], []).append('F')
                elif len(production) == 2:
                    # transitioning to another state for terminal + non-terminal
                    self.transitions[state].setdefault(production[0], []).append(production[1])

    # Method to check if my word is in the language
    def string_in_language(self, input_string):
        queue = deque([(self.start_state, 0)])

        while queue:
            current_state, index = queue.popleft()

            if index == len(input_string):
                if current_state in self.final_states:
                    return True
                continue

            symbol = input_string[index]

            if symbol in self.transitions.get(current_state, {}):
                for next_state in self.transitions[current_state][symbol]:
                    queue.append((next_state, index + 1))

        return False


def main():
    grammar = Grammar()
    print("Generated strings:")
    for _ in range(5):
        print(grammar.generate_string())

    fa = grammar.to_finite_automaton()

    test_strings = ['cfe', 'cffffem', 'cfemff', 'cemem', 'ce', 'gg']
    print("\nChecking if strings belong to the language:")
    for s in test_strings:
        is_true = fa.string_in_language(s)
        print(f"'{s}' belongs to the language: {is_true}")


if __name__ == "__main__":
    main()
