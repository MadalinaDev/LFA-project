# Lexer for trigonometric complex expressions

### Course: Formal Languages & Finite Automata
### Author: Madalina Chirpicinic, FAF-233

----

## Theory
Lexical analysis is the first step in the compilation or interpretation process. it involves scanning an input string and breaking it down into meaningful tokens. in this project, the lexer is designed to recognize numbers (integers, floats, and complex numbers), arithmetic operators, parentheses, commas, and reserved keywords for trigonometric functions (sin, cos, tan). this provides a foundational tool for further processing, such as parsing expressions or building a simple interpreter.


## Objectives:

* to understand and apply the principles of lexical analysis
* to implement a lexer that tokenizes complex expressions including arithmetic and trigonometric functions
* to handle various numeric types (integers, floats, and complex numbers)
* to create a modular and well-documented codebase that can be expanded in future projects


## Implementation description

The implementation is structured around two main classes: the Token class and the Lexer class. The token class defines the structure for tokens, storing both a type (e.g., integer, float, complex) and its corresponding value. The lexer class processes the input string character by character. it uses helper methods like number() to distinguish between integers, floats, and complex numbers (by detecting a trailing 'j') and identifier() to collect letters that form reserved trigonometric function names. The get_next_token() method iterates over the input, returning one token at a time until the entire string has been processed.

Below, the most crucial snippets of code of the implementation are listed and explained.

1. Token Class

This class defines the structure for tokens, each having a type and a value. This snippet creates token objects, which are the basic units produced by the lexer. Each token carries a type (like INTEGER, FLOAT, etc.) and its associated value.

```
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"
```

2. Number Parsing

This method reads numeric input, handling integers, floats, and complex numbers (with an ending 'j'). This snippet processes a sequence of digits (and at most one dot) to build numbers. If a 'j' is encountered, it creates a complex token with a 0 real part and the parsed number as the imaginary part.

``` 
def number(self):
    result, dot_count = '', 0
    while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
        if self.current_char == '.' and dot_count:
            break
        if self.current_char == '.':
            dot_count += 1
        result += self.current_char
        self.advance()
    if self.current_char and self.current_char.lower() == 'j':
        self.advance()
        return Token(COMPLEX, complex(0, float(result) if dot_count else int(result)))
    return Token(FLOAT, float(result)) if dot_count else Token(INTEGER, int(result))
```

3. Tokenization Loop

This method scans the input and returns one token at a time based on the current character. This loop is the heart of the lexer. It skips whitespace, checks whether the current character starts a number, identifier, or operator, and then returns the corresponding token. If no recognized character is found, it raises an error; when input is exhausted, it returns an EOF token.

```
def get_next_token(self):
    while self.current_char:
        if self.current_char.isspace():
            self.skip_whitespace()
            continue
        if self.current_char.isdigit():
            return self.number()
        if self.current_char.isalpha():
            return self.identifier()
        if self.current_char in '+-*/(),':
            char = self.current_char
            self.advance()
            token_map = {'+': PLUS, '-': MINUS, '*': MULTIPLY, '/': DIVIDE, 
                         '(': LPAREN, ')': RPAREN, ',': COMMA}
            return Token(token_map[char], char)
        self.error()
    return Token(EOF, None)
```

For example of input:
``` sin(30) + cos(45.0) - tan(1.57) + 3 + 4j - 2.5j ```
the screenshot below ilustrates its respective output:
<br>
![alt text](verification.png)


## Conclusions / Screenshots / Results
the lexer successfully tokenizes complex expressions that involve trigonometric function calls, arithmetic operations, and different numeric types. for instance, when processing the input string:
sin(30) + cos(45.0) - tan(1.57) + 3 + 4j - 2.5j
the lexer produces a clear sequence of tokens corresponding to each element in the expression. this outcome confirms that the lexer is robust and serves as a solid foundation for further parsing or interpreter development.
(a screenshot of the terminal output or debugging session can be added here if desired)

## References

1. [A sample of a lexer implementation](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)
2. [Lexical analysis](https://en.wikipedia.org/wiki/Lexical_analysis)