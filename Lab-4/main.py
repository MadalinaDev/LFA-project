import itertools

def split_expression(expr):
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
                raise ValueError("Unmatched parenthesis in expression")
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
        try:
            n = int(suffix[1:])
        except ValueError:
            raise ValueError("Invalid repetition specifier in segment: " + segment)
        return [s * n for s in base_symbols]
    else:
        raise ValueError(f"Unrecognized segment suffix: {suffix}")

def expand_expression(expr):
    segments = split_expression(expr)
    expansions_per_segment = [parse_segment(seg) for seg in segments]
    return [''.join(combo) for combo in itertools.product(*expansions_per_segment)]

def process_sequence(expr):
    segments = split_expression(expr)
    print("Processing expression:", expr)
    for idx, seg in enumerate(segments, start=1):
        possible_outputs = parse_segment(seg)
        preview = possible_outputs[:5]
        preview_str = f"{preview}{' ...' if len(possible_outputs) > 5 else ''}"
        print(f"  Step {idx}: segment '{seg}' -> {preview_str}")

if __name__ == '__main__':
    regex_variants = [
        "M?N^2(O|P)^3Q*R+",
        "(X|Y|Z)^3 8+(9|0)^2",
        "(H|I)(J|K)L*N?"
    ]
    for variant_index in range(0, 3):
        chosen_regex = regex_variants[variant_index]
        print(f"\nprocessing regex variant: {chosen_regex}")
        process_sequence(chosen_regex)
        combinations = expand_expression(chosen_regex)
        print("total number of valid combinations:", len(combinations))
        print("sample results:")
        for result in combinations[:5]:
            print(result)
