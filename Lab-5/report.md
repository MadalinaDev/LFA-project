# Converting a Context-Free Grammar to Chomsky Normal Form

### Course: Formal Languages & Finite Automata  
### Author: Madalina Chirpicinic, FAF-233

----

## Theory
Chomsky Normal Form (CNF) is a restricted grammar form in which every production rule is either A → BC (two nonterminals) or A → a (single terminal), with an optional S → ε if the start symbol can derive the empty string. Converting an arbitrary context-free grammar into CNF is useful for algorithms like CYK parsing and theoretical proofs. The standard conversion process involves eliminating ε-productions, unit productions, and useless symbols, then restructuring productions to meet CNF constraints.

## Objectives:

* To understand the theory behind Chomsky Normal Form.
* To implement a conversion method that normalizes any given grammar into CNF.
* To encapsulate the functionality in a reusable `Grammar` class.
* To demonstrate correctness by executing and testing the conversion on Variant 6 grammar.
* **Bonus:** accept any grammar specification, not just a single hardcoded variant.

## Implementation description

The implementation centers around the `Grammar` class, which stores nonterminals, terminals, productions, and the start symbol. Productions are held as a dictionary mapping each nonterminal to a set of right-hand-side tuples. The method `to_cnf()` orchestrates the following steps:

### 1. Grammar Class

```python
class Grammar:
    def __init__(self, non_terminals=None, terminals=None, productions=None, start_symbol=None):
        self.non_terminals = non_terminals if non_terminals else set()
        self.terminals     = terminals if terminals else set()
        self.productions   = productions if productions else {}
        self.start_symbol  = start_symbol

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
        for nt in sorted(self.productions):
            prods = self.productions[nt]
            result += f"  {nt} -> {' | '.join(prods)}\n"
        return result
```

### 2. CNFConverter Initialization & Fresh Nonterminal Generation

```python
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
```

### 3. Eliminating ε-Productions

```python
def eliminate_epsilon_productions(self):
    nullable = set()
    for nt, prods in self.grammar.productions.items():
        if "" in prods:
            nullable.add(nt)
    changed = True
    while changed:
        changed = False
        for nt, prods in self.grammar.productions.items():
            if nt not in nullable:
                for prod in prods:
                    if all(sym in nullable for sym in prod):
                        nullable.add(nt)
                        changed = True
                        break

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
            nullable_positions = [i for i, sym in enumerate(prod) if sym in nullable]
            for mask in range(1, 1 << len(nullable_positions)):
                rm = [nullable_positions[i] for i in range(len(nullable_positions)) if mask & (1 << i)]
                new_prod = "".join(prod[i] for i in range(len(prod)) if i not in rm)
                if new_prod or nt == self.grammar.start_symbol:
                    new_grammar.add_production(nt, new_prod)
    self.grammar = new_grammar
    return new_grammar
```

### 4. Eliminating Unit Productions

```python
def eliminate_unit_productions(self):
    unit_pairs = {nt: {nt} for nt in self.grammar.non_terminals}
    changed = True
    while changed:
        changed = False
        for nt in self.grammar.non_terminals:
            for prod in self.grammar.productions.get(nt, []):
                if len(prod) == 1 and prod in self.grammar.non_terminals:
                    for b in unit_pairs[prod]:
                        if b not in unit_pairs[nt]:
                            unit_pairs[nt].add(b)
                            changed = True

    new_grammar = Grammar(
        non_terminals=self.grammar.non_terminals.copy(),
        terminals=self.grammar.terminals.copy(),
        start_symbol=self.grammar.start_symbol
    )
    for A, bs in unit_pairs.items():
        for B in bs:
            for prod in self.grammar.productions.get(B, []):
                if not (len(prod) == 1 and prod in self.grammar.non_terminals):
                    new_grammar.add_production(A, prod)

    self.grammar = new_grammar
    return new_grammar
```

### 5. Removing Non-Productive & Inaccessible Symbols

```python
def eliminate_non_productive_symbols(self):
    productive = set(self.grammar.terminals)
    changed = True
    while changed:
        changed = False
        for nt, prods in self.grammar.productions.items():
            if nt not in productive:
                for prod in prods:
                    if all(sym in productive for sym in prod):
                        productive.add(nt)
                        changed = True
                        break
    new_grammar = Grammar(
        non_terminals=self.grammar.non_terminals.intersection(productive),
        terminals=self.grammar.terminals.copy(),
        start_symbol=self.grammar.start_symbol if self.grammar.start_symbol in productive else None
    )
    for nt in new_grammar.non_terminals:
        for prod in self.grammar.productions[nt]:
            if all(sym in productive for sym in prod):
                new_grammar.add_production(nt, prod)
    self.grammar = new_grammar
    return new_grammar

def eliminate_inaccessible_symbols(self):
    accessible = {self.grammar.start_symbol}
    changed = True
    while changed:
        changed = False
        for nt in list(accessible):
            for prod in self.grammar.productions.get(nt, []):
                for sym in prod:
                    if sym not in accessible:
                        accessible.add(sym)
                        changed = True
    new_grammar = Grammar(
        non_terminals=self.grammar.non_terminals.intersection(accessible),
        terminals=self.grammar.terminals.intersection(accessible),
        start_symbol=self.grammar.start_symbol
    )
    for nt in new_grammar.non_terminals:
        for prod in self.grammar.productions.get(nt, []):
            if all(sym in accessible for sym in prod):
                new_grammar.add_production(nt, prod)
    self.grammar = new_grammar
    return new_grammar
```

### 6. Final CNF Conversion (`convert_to_cnf`)

```python
def convert_to_cnf(self):
    self.eliminate_epsilon_productions()
    self.eliminate_unit_productions()
    self.eliminate_non_productive_symbols()
    self.eliminate_inaccessible_symbols()

    new_grammar = Grammar(
        non_terminals=self.grammar.non_terminals.copy(),
        terminals=self.grammar.terminals.copy(),
        start_symbol=self.grammar.start_symbol
    )
    terminal_to_nt = {}
    for t in self.grammar.terminals:
        X = self.generate_new_non_terminal()
        new_grammar.non_terminals.add(X)
        new_grammar.add_production(X, t)
        terminal_to_nt[t] = X

    for A, prods in self.grammar.productions.items():
        for prod in prods:
            if prod == "" and A == self.grammar.start_symbol:
                new_grammar.add_production(A, "")
            elif len(prod) == 1 and prod in self.grammar.terminals:
                new_grammar.add_production(A, prod)
            else:
                symbols = [terminal_to_nt[s] if s in self.grammar.terminals else s for s in prod]
                while len(symbols) > 2:
                    X = self.generate_new_non_terminal()
                    new_grammar.non_terminals.add(X)
                    first, second, *rest = symbols
                    new_grammar.add_production(A, first + X)
                    symbols = [second] + rest
                new_grammar.add_production(A, "".join(symbols))
    self.grammar = new_grammar
    return new_grammar
```

----
## Conclusions

After calling `to_cnf()`, the Variant 6 grammar has only productions of the form `A → B C` or `A → a`. All ε-productions, unit productions, and useless symbols are removed, and any longer rules are binarized. This fully satisfies CNF requirements and enables algorithms like CYK. The Grammar class successfully transforms any context-free grammar into CNF. Each step is modular, testable, and documented—enabling future extensions (e.g., keeping track of positions for error reporting). This implementation can be integrated into a larger parser or used as a standalone preprocessing tool for CYK parsing.

----
## References

1. [Chomsky Normal Form – Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form)
