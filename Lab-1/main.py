import random

class Grammar:
    # defining in the constructor my terminals, non-terminals, production rules, and initial state S
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

    # using recursion to derive randomly words based on the grammar rules
    def generate_string(self):
        def expand(symbol):
            if symbol in self.VT:
                return symbol
            else:
                production = random.choice(self.P[symbol])
                expanded_results = []
                for sym in production:
                    expanded_results.append(expand(sym))
                return ''.join(expanded_results)
        return expand(self.S)

    # transforming my grammar into a finite automaton
    def to_finite_automaton(self):
        return FiniteAutomaton(self)



class FiniteAutomaton:
    # defining  in the constructor my finite automaton components
    def __init__(self, grammar):
        self.states = grammar.VN.union({'F'})
        self.alphabet = grammar.VT
        
        self.transitions = self.build_transitions(grammar)
        
        self.start_state = grammar.S
        self.final_states = {'F'}


    # to build transitions, implementing a dictionary of states and transitions
    def build_transitions(self, grammar):
        transitions = {}
        for state in grammar.VN:
            transitions[state] = {}
        
            for production in grammar.P[state]:
                # it has in a single terminal symbol
                if len(production) == 1 and production[0] in grammar.VT:
                    transitions[state][production[0]] = 'F'
                
                # it has a terminal symbol + a non-terminal symbol
                elif len(production) == 2:
                    # for sure that it's a right-linear grammar 
                    transitions[state][production[0]] = production[1]
        return transitions

    # method to checking if my word is in the language 
    def string_in_language(self, input_string):
        current_state = self.start_state
        for symbol in input_string:
            if current_state == 'F':
                return True
            if symbol in self.transitions[current_state]:
                current_state = self.transitions[current_state][symbol]
            else:
                return False
        return current_state in self.final_states


def main():
    grammar = Grammar()
    print("Generated strings:")
    for aux in range(5):
        print(grammar.generate_string())
    fa = grammar.to_finite_automaton()

    test_strings = ['cbncm', 'cfbncm', 'ce', 'cbncbncm', 'cfefbncm']
    print("\nChecking if strings belong to the language:")
    for s in test_strings:
        is_true = fa.string_in_language(s)
        print(f"'{s}' belongs to the language: {is_true}")



if __name__ == "__main__":
    main()