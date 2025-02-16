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
                return ''.join(expand(s) for s in production)
        return expand(self.S)