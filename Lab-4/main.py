import itertools

def parse_segment(segment):
    MAX_REPEAT = 5

    def repeat_symbol(symbols, min_times, max_times):
        results = []
        for times in range(min_times, max_times + 1):
            for combo in itertools.product(symbols, repeat=times):
                results.append(''.join(combo))
        return results

    if segment.startswith('('):
        close_idx = segment.find(')')
        base_symbols = segment[1:close_idx].split('|')
        suffix = segment[close_idx+1:]
    else:
        base_symbols = [segment[0]]
        suffix = segment[1:]

    if suffix == '':
        return base_symbols
    elif suffix == '?':
        return [''] + base_symbols
    elif suffix == '*':
        return repeat_symbol(base_symbols, 0, MAX_REPEAT)
    elif suffix == '+':
        return repeat_symbol(base_symbols, 1, MAX_REPEAT)
    elif suffix.startswith('^'):
        n = int(suffix[1:])
        return repeat_symbol(base_symbols, n, n)
    else:
        raise ValueError(f"Unrecognized segment suffix: {suffix}")

def expand_expression(expr):
    segments = expr.split()
    all_expansions = [parse_segment(seg) for seg in segments]
    return [''.join(combo) for combo in itertools.product(*all_expansions)]

if __name__ == '__main__':
    expr1 = "M? N^2 (O|P)^3 Q* R+"
    expr2 = "(X|Y|Z)^3 8+ (9|0)"
    expr3 = "(H|I) (J|K) L* N?"

    results1 = expand_expression(expr1)
    results2 = expand_expression(expr2)
    results3 = expand_expression(expr3)

    print("=== Expression 1:", expr1, "===")
    print("Number of combinations:", len(results1))
    print("Sample 5 results:", results1[:5], "\n")

    print("=== Expression 2:", expr2, "===")
    print("Number of combinations:", len(results2))
    print("Sample 5 results:", results2[:5], "\n")

    print("=== Expression 3:", expr3, "===")
    print("Number of combinations:", len(results3))
    print("Sample 5 results:", results3[:5], "\n")
