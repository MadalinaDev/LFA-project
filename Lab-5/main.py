from collections import defaultdict

class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):

        self.non_terminals = set(non_terminals)
        self.terminals = set(terminals)
        self.start = start_symbol

        self.productions = defaultdict(set)
        for A, rhss in productions.items():
            for rhs in rhss:
                self.productions[A].add(tuple(rhs))

        self._fresh_id = 1

    def to_cnf(self):
        self._remove_epsilon()
        self._remove_unit()
        self._remove_useless()
        self._terminals_to_nonterminals()
        self._binarize()
        return self

    def _remove_epsilon(self):
        nullable = set()
        changed = True
        while changed:
            changed = False
            for A, rhss in self.productions.items():
                if A not in nullable:
                    for rhs in rhss:
                        if all((sym in nullable) or sym == "" for sym in rhs) or rhs == ():
                            nullable.add(A)
                            changed = True
                            break

        new_prods = defaultdict(set)
        for A, rhss in self.productions.items():
            for rhs in rhss:
                if rhs == ():  
                    continue
                from itertools import product
                choices = []
                for sym in rhs:
                    if sym in nullable:
                        choices.append([sym, None])
                    else:
                        choices.append([sym])
                for combo in product(*choices):
                    new_rhs = tuple(s for s in combo if s is not None)
                    if new_rhs:
                        new_prods[A].add(new_rhs)
                    else:
                        new_prods[A].add(())
        self.productions = new_prods

    def _remove_unit(self):
        unit_pairs = {(A,A) for A in self.non_terminals}
        for A in self.non_terminals:
            for rhs in self.productions[A]:
                if len(rhs)==1 and rhs[0] in self.non_terminals:
                    unit_pairs.add((A, rhs[0]))

        changed = True
        while changed:
            changed = False
            for (A,B) in list(unit_pairs):
                for (C,D) in list(unit_pairs):
                    if B == C and (A,D) not in unit_pairs:
                        unit_pairs.add((A,D))
                        changed = True

        new_prods = defaultdict(set)
        for (A,B) in unit_pairs:
            for rhs in self.productions[B]:
                if not (len(rhs)==1 and rhs[0] in self.non_terminals):
                    new_prods[A].add(rhs)
        self.productions = new_prods

    def _remove_useless(self):
        generating = set()
        changed = True
        while changed:
            changed = False
            for A, rhss in self.productions.items():
                for rhs in rhss:
                    if all(sym in self.terminals or sym in generating for sym in rhs):
                        if A not in generating:
                            generating.add(A)
                            changed = True
        self.non_terminals &= generating
        self.productions = {
            A: {rhs for rhs in rhss if all(sym in self.terminals or sym in self.non_terminals for sym in rhs)}
            for A, rhss in self.productions.items()
            if A in self.non_terminals
        }

        reachable = {self.start}
        changed = True
        while changed:
            changed = False
            for A in list(reachable):
                for rhs in self.productions.get(A, []):
                    for sym in rhs:
                        if sym in self.non_terminals and sym not in reachable:
                            reachable.add(sym)
                            changed = True
        self.non_terminals &= reachable
        self.productions = {A:rhss for A,rhss in self.productions.items() if A in reachable}

    def _terminals_to_nonterminals(self):
        mapping = {}  
        new_prods = defaultdict(set)

        for A, rhss in self.productions.items():
            for rhs in rhss:
                if len(rhs) > 1:
                    new_rhs = []
                    for sym in rhs:
                        if sym in self.terminals:
                            if sym not in mapping:
                                X = self._fresh_nonterminal()
                                mapping[sym] = X
                                self.non_terminals.add(X)
                                new_prods[X].add((sym,))
                            new_rhs.append(mapping[sym])
                        else:
                            new_rhs.append(sym)
                    new_prods[A].add(tuple(new_rhs))
                else:
                    new_prods[A].add(rhs)

        self.productions = new_prods

    def _binarize(self):
        new_prods = defaultdict(set)
        for A, rhss in self.productions.items():
            for rhs in rhss:
                if len(rhs) <= 2:
                    new_prods[A].add(rhs)
                else:
                    symbols = list(rhs)
                    prev = A
                    while len(symbols) > 2:
                        X1, X2, *rest = symbols
                        X = self._fresh_nonterminal()
                        self.non_terminals.add(X)
                        new_prods[prev].add((X1, X))
                        prev = X
                        symbols = [X2] + rest
                    new_prods[prev].add(tuple(symbols))

        self.productions = new_prods

    def _fresh_nonterminal(self):
        while True:
            X = f"X{self._fresh_id}"
            self._fresh_id += 1
            if X not in self.non_terminals and X not in self.terminals:
                return X

    def __str__(self):
        out = []
        for A in sorted(self.productions):
            for rhs in sorted(self.productions[A]):
                out.append(f"{A} → {' '.join(rhs) if rhs else 'ε'}")
        return "\n".join(out)


if __name__ == "__main__":
    NT = ['S','A','B','C','E']
    T  = ['a','b']
    P  = {
      'S': [['a','B'], ['A','C']],
      'A': [['a'], ['A','S','C'], ['B','C']],
      'B': [['b'], ['b','S']],
      'C': [[], ['B','A']], 
      'E': [['b','B']],
    }
    G = Grammar(NT, T, P, start_symbol='S')

    print("=== original ===")
    print(G)
    G.to_cnf()
    print("\n=== in CNF ===")
    print(G)
