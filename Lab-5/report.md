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

1. **Eliminate ε-productions**: computes nullable nonterminals and regenerates productions without ε.  
2. **Eliminate unit productions**: removes rules of the form A → B by closure over unit pairs.  
3. **Remove useless symbols**: discards non-generating and unreachable symbols.  
4. **Terminal lifting**: replaces terminals in long productions with fresh nonterminals.  
5. **Binarization**: splits productions with more than two symbols into binary rules using fresh nonterminals.

Below, the most crucial snippets of code are listed and explained.

1. Class & Constructor

```python
from collections import defaultdict

class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = set(non_terminals)
        self.terminals     = set(terminals)
        self.start         = start_symbol
        # map each nonterminal → set of RHS-tuples
        self.productions   = defaultdict(set)
        for A, rhss in productions.items():
            for rhs in rhss:
                self.productions[A].add(tuple(rhs))
        self._fresh_id = 1  # for generating X1, X2, ...
```

*Explanation:* Initializes grammar components and normalizes RHSs into tuples for easy deduplication.

2. Eliminating ε-Productions

```python
def _remove_epsilon(self):
    # 1. Find nullable nonterminals
    nullable = set()
    changed = True
    while changed:
        changed = False
        for A, rhss in self.productions.items():
            for rhs in rhss:
                if not rhs or all(sym in nullable for sym in rhs):
                    nullable.add(A)
                    changed = True

    # 2. Rebuild productions without ε
    new_prods = defaultdict(set)
    from itertools import product
    for A, rhss in self.productions.items():
        for rhs in rhss:
            if not rhs:
                continue
            choices = [
                [sym, None] if sym in nullable else [sym]
                for sym in rhs
            ]
            for combo in product(*choices):
                new_rhs = tuple(s for s in combo if s)
                new_prods[A].add(new_rhs or ())
    self.productions = new_prods
```

*Explanation:* Computes all nullable symbols, then for each production builds every variant omitting nullable occurrences to remove ε-rules.

3. Lifting Terminals to Single Nonterminals

```python
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
```

*Explanation:* Ensures that in any RHS of length >1, terminals are replaced by fresh nonterminals producing that terminal.

4. Binarization of Long Rules

```python
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
                    first, *rest = symbols
                    X = self._fresh_nonterminal()
                    self.non_terminals.add(X)
                    new_prods[prev].add((first, X))
                    symbols = rest
                    prev = X
                new_prods[prev].add(tuple(symbols))
    self.productions = new_prods
```

*Explanation:* Splits any RHS longer than two symbols into a chain of binary productions using new nonterminals.

---

## Conclusions / Screenshots / Results

After calling `to_cnf()`, the Variant 6 grammar has only productions of the form `A → B C` or `A → a`. All ε-productions, unit productions, and useless symbols are removed, and any longer rules are binarized. This fully satisfies CNF requirements and enables algorithms like CYK. The Grammar class successfully transforms any context-free grammar into CNF. Each step is modular, testable, and documented—enabling future extensions (e.g., keeping track of positions for error reporting). This implementation can be integrated into a larger parser or used as a standalone preprocessing tool for CYK parsing.

---

## References

1. “Chomsky normal form,” *Wikipedia*:  
   https://en.wikipedia.org/wiki/Chomsky_normal_form  