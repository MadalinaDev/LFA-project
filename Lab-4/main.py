import itertools

def split_expression(expr):
    # split the expression into segments (supports expressions without spaces)
    segments = []
    i, n = 0, len(expr)
    while i < n:
        if expr[i].isspace():
            i += 1
            continue
        if expr[i] == '(':
            start = i
            i += 1
            while i < n and expr[i] != ')':
                i += 1
            if i >= n:
                raise ValueError("unmatched parenthesis")
            group = expr[start:i+1]
            i += 1
            suffix = ''
            if i < n and expr[i] in '?*+':
                suffix = expr[i]
                i += 1
            elif i < n and expr[i] == '^':
                suffix = '^'
                i += 1
                digits = ''
                while i < n and expr[i].isdigit():
                    digits += expr[i]
                    i += 1
                suffix += digits
            segments.append(group + suffix)
        else:
            seg = expr[i]
            i += 1
            suffix = ''
            if i < n and expr[i] in '?*+':
                suffix = expr[i]
                i += 1
            elif i < n and expr[i] == '^':
                suffix = '^'
                i += 1
                digits = ''
                while i < n and expr[i].isdigit():
                    digits += expr[i]
                    i += 1
                suffix += digits
            segments.append(seg + suffix)
    return segments

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
        raise ValueError(f"unrecognized segment suffix: {suffix}")

def expand_expression(expr):
    segments = split_expression(expr)
    expansions = [parse_segment(seg) for seg in segments]
    return [''.join(combo) for combo in itertools.product(*expansions)]

def process_sequence(expr):
    # show the step-by-step processing of the regex-like expression
    segments = split_expression(expr)
    print("processing sequence:")
    for i, seg in enumerate(segments, 1):
        print(f" step {i}: segment '{seg}' -> {parse_segment(seg)[:5]}{' ...' if len(parse_segment(seg)) > 5 else ''}")

# demo
if __name__ == '__main__':
    expr = "M?N^2(O|P)^3Q*R+"
    print("expression:", expr)
    process_sequence(expr)
    results = expand_expression(expr)
    print("\nnumber of combinations:", len(results))
    print("sample 5 results:", results[:5])
