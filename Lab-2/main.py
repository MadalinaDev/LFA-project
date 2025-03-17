class Grammar:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    # check if the grammar is regular (type 3)
    def __check_type3(self):
        for A, prods in self.productions.items():
            # we assume A is a nonterminal (even if not a single letter)
            if A not in self.non_terminals:
                return False
            for prod in prods:
                if len(prod) == 1:
                    if prod not in self.terminals:
                        return False
                else:
                    # first symbol must be terminal, remainder must be one of the nonterminals
                    if prod[0] not in self.terminals or prod[1:] not in self.non_terminals:
                        return False
        return True

    # return regular grammar if type 3
    def return_grammar_type(self):
        if self.__check_type3():
            return "regular grammar"
        return "grammar type"


class FiniteAutomaton:
    def __init__(self, states, alphabet, initial_state, final_states, transitions):
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.final_states = final_states
        self.transitions = transitions  # list of dicts: {state: , symbol: , to: }

    # check determinism: one transition for each state + symbol combination
    def is_deterministic(self):
        seen = set()
        for t in self.transitions:
            key = (t["state"], t["symbol"])
            if key in seen:
                return False
            seen.add(key)
        return True

    # generate productions for fa -> regular grammar conversion
    def __get_productions(self):
        productions = {state: [] for state in self.states}
        for t in self.transitions:
            if t["to"] in self.final_states:
                productions[t["state"]].append(t["symbol"])
            else:
                productions[t["state"]].append(t["symbol"] + t["to"])
        return productions

    # convert fa to regular grammar
    def convert_to_grammar(self):
        prods = self.__get_productions()
        return Grammar(self.states, self.alphabet, prods, self.initial_state)

    # convert ndfa to dfa using subset construction
    def convert_to_dfa(self):
        if self.is_deterministic():
            return self

        def move(states, symbol):
            result = set()
            for t in self.transitions:
                if t["state"] in states and t["symbol"] == symbol:
                    result.add(t["to"])
            return result

        start = frozenset([self.initial_state])
        unprocessed = [start]
        state_mapping = {start: "q0"}
        dfa_transitions = []
        dfa_states = [start]

        while unprocessed:
            current = unprocessed.pop(0)
            for symbol in self.alphabet:
                nxt = frozenset(move(current, symbol))
                if nxt:
                    if nxt not in state_mapping:
                        state_mapping[nxt] = f"q{len(state_mapping)}"
                        unprocessed.append(nxt)
                        dfa_states.append(nxt)
                    dfa_transitions.append({
                        "state": state_mapping[current],
                        "symbol": symbol,
                        "to": state_mapping[nxt]
                    })

        dfa_state_names = set(state_mapping.values())
        dfa_final_states = {state_mapping[s] for s in dfa_states if any(st in self.final_states for st in s)}
        return FiniteAutomaton(dfa_state_names, self.alphabet, "q0", dfa_final_states, dfa_transitions)


def variant6_fa():
    states = {"q0", "q1", "q2", "q3", "q4"}
    alphabet = {"a", "b"}
    initial_state = "q0"
    final_states = {"q4"}
    transitions = [
        {"state": "q0", "symbol": "a", "to": "q1"},
        {"state": "q1", "symbol": "b", "to": "q1"},
        {"state": "q1", "symbol": "b", "to": "q2"},
        {"state": "q2", "symbol": "b", "to": "q3"},
        {"state": "q3", "symbol": "a", "to": "q1"},
        {"state": "q2", "symbol": "a", "to": "q4"},
    ]
    return FiniteAutomaton(states, alphabet, initial_state, final_states, transitions)


def main():
    fa = variant6_fa()

    # derive and show regular grammar from variant 6 fa
    rg = fa.convert_to_grammar()
    print("grammar derived from variant 6 fa:")
    print("non-terminals:", rg.non_terminals)
    print("terminals:", rg.terminals)
    print("productions:")
    for nt in rg.productions:
        print(f"  {nt} -> {rg.productions[nt]}")

    # display original nfa transitions
    print("\nnfa transitions:")
    for t in sorted(fa.transitions, key=lambda x: (x["state"], x["symbol"])):
        print(t)

    # check if the fa is deterministic
    print("\nfa determinism check:")
    print("is the variant 6 fa deterministic?")
    print(fa.is_deterministic())

    # convert ndfa to dfa and show transitions
    dfa = fa.convert_to_dfa()
    print("\ndfa transitions:")
    for t in sorted(dfa.transitions, key=lambda x: (x["state"], x["symbol"])):
        print(t)

    # grammar classification based on our regular grammar check
    print("\ngrammar classification:")
    print(rg.return_grammar_type())


if __name__ == "__main__":
    main()
