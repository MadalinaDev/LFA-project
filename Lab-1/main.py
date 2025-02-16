class Grammar:
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



class FiniteAutomaton:
    def __init__(self, grammar):
        self.states = grammar.VN.union({'F'})
        self.alphabet = grammar.VT
        
        self.transitions = self.build_transitions(grammar)
        
        self.start_state = grammar.S
        self.final_states = {'F'}


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
                # we are for sure that it's a right-linear grammar 
                transitions[state][production[0]] = production[1]
    return transitions