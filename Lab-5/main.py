class Grammar:
    def __init__(self, non_terminals=None, terminals=None, productions=None, start_symbol=None):
        self.non_terminals = non_terminals if non_terminals else set()
        self.terminals = terminals if terminals else set()
        self.productions = productions if productions else {}
        self.start_symbol = start_symbol
    def add_production(self, non_terminal, production):
        if non_terminal not in self.productions:
            self.productions[non_terminal] = []
        if production not in self.productions[non_terminal]:
            self.productions[non_terminal].append(production)
    def __str__(self):
        result = "Grammar:\n"
        result += f"Non-terminals: {', '.join(sorted(self.non_terminals))}\n"
        result += f"Terminals: {', '.join(sorted(self.terminals))}\n"
        result += f"Start symbol: {self.start_symbol}\n"
        result += "Productions:\n"
        for nt in sorted(self.productions.keys()):
            prods = self.productions[nt]
            result += f"  {nt} -> {' | '.join(prods)}\n"
        return result

class CNFConverter:
    def __init__(self, grammar):
        self.grammar = grammar
        self.new_non_terminal_index = 0
    def generate_new_non_terminal(self):
        while True:
            new_nt = f"X{self.new_non_terminal_index}"
            self.new_non_terminal_index += 1
            if new_nt not in self.grammar.non_terminals:
                return new_nt
    def eliminate_epsilon_productions(self):
        nullable = set()
        changed = True
        for nt, prods in self.grammar.productions.items():
            if "" in prods:
                nullable.add(nt)
        while changed:
            changed = False
            for nt, prods in self.grammar.productions.items():
                if nt in nullable:
                    continue
                for prod in prods:
                    if all(symbol in nullable for symbol in prod):
                        nullable.add(nt)
                        changed = True
                        break
        print(f"Nullable non-terminals: {nullable}")
        new_grammar = Grammar(
            non_terminals=self.grammar.non_terminals.copy(),
            terminals=self.grammar.terminals.copy(),
            start_symbol=self.grammar.start_symbol
        )
        for nt, prods in self.grammar.productions.items():
            for prod in prods:
                if prod == "":
                    if nt == self.grammar.start_symbol:
                        new_grammar.add_production(nt, "")
                    continue
                new_grammar.add_production(nt, prod)
                nullable_positions = [i for i, symbol in enumerate(prod) if symbol in nullable]
                for mask in range(1, 1 << len(nullable_positions)):
                    positions_to_remove = [nullable_positions[i] for i in range(len(nullable_positions)) if (mask & (1 << i))]
                    new_prod = "".join(prod[i] for i in range(len(prod)) if i not in positions_to_remove)
                    if new_prod:
                        new_grammar.add_production(nt, new_prod)
                    elif nt == self.grammar.start_symbol:
                        new_grammar.add_production(nt, "")
        self.grammar = new_grammar
        return new_grammar
    def eliminate_unit_productions(self):
        unit_pairs = {}
        for nt in self.grammar.non_terminals:
            unit_pairs[nt] = {nt}
        changed = True
        while changed:
            changed = False
            for nt in self.grammar.non_terminals:
                for prod in self.grammar.productions.get(nt, []):
                    if len(prod) == 1 and prod in self.grammar.non_terminals:
                        for b in unit_pairs.get(prod, set()):
                            if b not in unit_pairs[nt]:
                                unit_pairs[nt].add(b)
                                changed = True
        print(f"Unit pairs: {unit_pairs}")
        new_grammar = Grammar(
            non_terminals=self.grammar.non_terminals.copy(),
            terminals=self.grammar.terminals.copy(),
            start_symbol=self.grammar.start_symbol
        )
        for a in self.grammar.non_terminals:
            for b in unit_pairs.get(a, set()):
                for prod in self.grammar.productions.get(b, []):
                    if not (len(prod) == 1 and prod in self.grammar.non_terminals):
                        new_grammar.add_production(a, prod)
        self.grammar = new_grammar
        return new_grammar
    def eliminate_non_productive_symbols(self):
        productive = set()
        productive.update(self.grammar.terminals)
        changed = True
        while changed:
            changed = False
            for nt, prods in self.grammar.productions.items():
                if nt in productive:
                    continue
                for prod in prods:
                    if all(symbol in productive for symbol in prod):
                        productive.add(nt)
                        changed = True
                        break
        print(f"Productive symbols: {productive}")
        new_grammar = Grammar(
            non_terminals=self.grammar.non_terminals.intersection(productive),
            terminals=self.grammar.terminals.copy(),
            start_symbol=self.grammar.start_symbol if self.grammar.start_symbol in productive else None
        )
        for nt, prods in self.grammar.productions.items():
            if nt in productive:
                for prod in prods:
                    if all(symbol in productive for symbol in prod):
                        new_grammar.add_production(nt, prod)
        self.grammar = new_grammar
        return new_grammar
    def eliminate_inaccessible_symbols(self):
        accessible = {self.grammar.start_symbol}
        changed = True
        while changed:
            changed = False
            new_accessible = accessible.copy()
            for nt in accessible:
                if nt in self.grammar.productions:
                    for prod in self.grammar.productions[nt]:
                        for symbol in prod:
                            if symbol not in new_accessible:
                                new_accessible.add(symbol)
                                changed = True
            accessible = new_accessible
        print(f"Accessible symbols: {accessible}")
        new_grammar = Grammar(
            non_terminals=self.grammar.non_terminals.intersection(accessible),
            terminals=self.grammar.terminals.intersection(accessible),
            start_symbol=self.grammar.start_symbol
        )
        for nt, prods in self.grammar.productions.items():
            if nt in accessible:
                for prod in prods:
                    if all(symbol in accessible for symbol in prod):
                        new_grammar.add_production(nt, prod)
        self.grammar = new_grammar
        return new_grammar
    def convert_to_cnf(self):
        self.eliminate_epsilon_productions()
        print("\nAfter eliminating ε-productions:")
        print(self.grammar)
        self.eliminate_unit_productions()
        print("\nAfter eliminating unit productions:")
        print(self.grammar)
        self.eliminate_non_productive_symbols()
        print("\nAfter eliminating non-productive symbols:")
        print(self.grammar)
        self.eliminate_inaccessible_symbols()
        print("\nAfter eliminating inaccessible symbols:")
        print(self.grammar)
        new_grammar = Grammar(
            non_terminals=self.grammar.non_terminals.copy(),
            terminals=self.grammar.terminals.copy(),
            start_symbol=self.grammar.start_symbol
        )
        terminal_to_nt = {}
        for terminal in self.grammar.terminals:
            new_nt = self.generate_new_non_terminal()
            new_grammar.non_terminals.add(new_nt)
            new_grammar.add_production(new_nt, terminal)
            terminal_to_nt[terminal] = new_nt
        for nt, prods in self.grammar.productions.items():
            for prod in prods:
                if prod == "":
                    if nt == self.grammar.start_symbol:
                        new_grammar.add_production(nt, prod)
                elif len(prod) == 1 and prod in self.grammar.terminals:
                    new_grammar.add_production(nt, prod)
                else:
                    symbols = []
                    for symbol in prod:
                        if symbol in self.grammar.terminals:
                            symbols.append(terminal_to_nt[symbol])
                        else:
                            symbols.append(symbol)
                    while len(symbols) > 2:
                        new_nt = self.generate_new_non_terminal()
                        new_grammar.non_terminals.add(new_nt)
                        new_grammar.add_production(new_nt, symbols[-2] + symbols[-1])
                        symbols = symbols[:-2] + [new_nt]
                    new_grammar.add_production(nt, "".join(symbols))
        self.grammar = new_grammar
        return new_grammar

def main():
    grammar = Grammar(
        non_terminals={'S','A','B','C','E'},
        terminals={'a', 'b'},
        productions={
           'S': ['aB',  'AC'],
            'A': ['a',   'ASC',  'BC'],
            'B': ['b',   'bS'],
            'C': ['',    'BA'], 
            'E': ['bB'],
        },
        start_symbol='S'
    )
    print("Original Grammar:")
    print(grammar)
    converter = CNFConverter(grammar)
    cnf_grammar = converter.convert_to_cnf()
    print("\nFinal Grammar in CNF:")
    print(cnf_grammar)

if __name__ == "__main__":
    main()
