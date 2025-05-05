# Parser and AST for Arithmetic & Trigonometric Expressions

### Course: Formal Languages & Finite Automata  
### Author: Madalina Chirpicinic, FAF-233

----

## Theory  
Syntactic analysis—or parsing—is the phase in which a token stream is organized into a hierarchical structure called an **Abstract Syntax Tree (AST)**. The AST abstracts away irrelevant details (whitespace, exact punctuation) and retains the essential constructs and nesting of the source text. Once built, an AST can be traversed for semantic checks, optimizations or code generation in a compiler, interpreter, or any tool that needs to understand code structure.

## Objectives

* To implement a **regex-based lexer** that categorizes input into tokens: integers, floats, complex literals, operators, parentheses, commas, function names (`sin`, `cos`, `tan`) and identifiers.  
* To define a **TokenType** enum and a `Token` data structure for clear token classification.  
* To design **AST node classes** representing numbers, complex numbers, unary and binary operations, function calls and identifiers.  
* To build a **recursive-descent parser** that constructs the AST from the token stream, handling operator precedence and nested function calls.  
* To provide a **pretty-printer** that outputs the AST with indentation for easy reading.

## Implementation Description

The solution consists of:

1. **TokenType enum & Token**  
   The `TokenType` enum lists all token categories. Each `Token` carries a `type` and a `value`.

   ```python
   class TokenType(enum.Enum):
       INTEGER    = "INTEGER"
       FLOAT      = "FLOAT"
       COMPLEX    = "COMPLEX"
       PLUS       = "PLUS"
       MINUS      = "MINUS"
       MULTIPLY   = "MULTIPLY"
       DIVIDE     = "DIVIDE"
       LPAREN     = "LPAREN"
       RPAREN     = "RPAREN"
       COMMA      = "COMMA"
       IDENTIFIER = "IDENTIFIER"
       SIN        = "SIN"
       COS        = "COS"
       TAN        = "TAN"
       EOF        = "EOF"
   ```

We import enum to define TokenType and create a clear mapping of token categories. Each enum member is self-documenting, which improves code readability and maintainability. The Token class encapsulates both the token type and its raw or converted value, providing a unified object for parser consumption. Additionally, implementing __repr__ aids in debugging by giving a concise, human-readable representation of tokens.

2. **Lexer with Regular Expressions**  
   We compile a single master pattern that matches every token type (using named capture groups) and advance over whitespace automatically:

   ```python
   class Lexer:
       _specs = [
           (TokenType.COMPLEX,    r'(?P<complex>\d+(?:\.\d+)?[jJ])'),
           (TokenType.FLOAT,      r'(?P<float>\d+\.\d+)'),
           (TokenType.INTEGER,    r'(?P<integer>\d+)'),
           (TokenType.SIN,        r'(?P<sin>sin)'),
           …  
           (TokenType.LPAREN,     r'(?P<lparen>\()'),
           (TokenType.RPAREN,     r'(?P<rparen>\))'),
           (TokenType.COMMA,      r'(?P<comma>,)'),
           (None,                 r'(?P<ws>\s+)'),  # skip whitespace
       ]
       _master_pat = re.compile('|'.join(p for _, p in _specs))
       …
   ```
We build a single, optimized regex by OR-ing patterns, which improves lexing performance by minimizing backtracking. Named capture groups allow us to differentiate token types directly from the match object without additional string comparisons. Converting numeric strings to Python number types early simplifies downstream AST construction and evaluation. Skipping whitespace transparently keeps the lexer focused on meaningful tokens and reduces parser complexity.


3. **AST Node Classes**  
   Each node type captures one language element:

   ```python
   class Number(AST):
       def __init__(self, value): self.value = value

   class ComplexNumber(AST):
       def __init__(self, value): self.value = value

   class Identifier(AST):
       def __init__(self, name): self.name = name

   class BinOp(AST):
       def __init__(self, left, op, right):
           self.left, self.op, self.right = left, op, right

   class UnaryOp(AST):
       def __init__(self, op, expr):
           self.op, self.expr = op, expr

   class FunctionCall(AST):
       def __init__(self, func_name, args):
           self.func_name, self.args = func_name, args
   ```

Defining a base AST class allows uniform handling of different node types in traversal algorithms like visitors or evaluators. Each subclass encapsulates the minimal data necessary to represent language constructs, promoting single-responsibility design. By directly storing tokens in operator nodes, we preserve contextual information (like operator type) for later stages, such as type checking or code generation. This structure is easily extended to add new node types, supporting future language features or optimizations.

4. **Recursive-Descent Parser**  
   The parser implements the usual grammar:

   ```
   expr   : term ((PLUS | MINUS) term)*
   term   : factor ((MUL | DIV) factor)*
   factor : (PLUS|MINUS) factor
          | INTEGER | FLOAT | COMPLEX
          | (SIN|COS|TAN|IDENTIFIER) [ LPAREN expr (COMMA expr)* RPAREN ]
          | LPAREN expr RPAREN
   ```

   ```python
   class Parser:
       def expr(self):
           node = self.term()
           while self.lexer.next_token.type in (TokenType.PLUS, TokenType.MINUS):
               op = self.lexer.next_token; self.lexer.eat(op.type)
               node = BinOp(node, op, self.term())
           return node
       …
   ```

The parser implements the grammar rules using one function per nonterminal. It enforces operator precedence by the order of calls (expr → term → factor):

5. **AST Pretty-Printer**  
   A helper walks the AST and prints each node with indentation:

   ```
   python
   def ast_to_string(node, indent=0):
       prefix = '  ' * indent
       if isinstance(node, Number):
           return f"{prefix}Number({node.value})"
       if isinstance(node, BinOp):
           s  = f"{prefix}BinOp({node.op.type.name})
           s += ast_to_string(node.left, indent+1) + "
           s += ast_to_string(node.right, indent+1)
           return s
       …```

## Example Run

```
$ python main.py
Enter expression ▶ sin(30) + cos(45) - (3 + 4j) * 2
AST ▶
BinOp(MINUS)
  BinOp(PLUS)
    Call(sin)
      Number(30)
    Call(cos)
      Number(45)
  BinOp(MULTIPLY)
    BinOp(PLUS)
      Number(3)
      Complex((0+4j))
    Number(2)
```


## Conclusions / Results

In conclusion, in this laboratory work I have successfully managed to accomplish the task given: the lexer correctly distinguishes integers, floats, complex literals, operators, parentheses and reserved trig functions. The parser respects operator precedence and grouping, producing a clear AST. The pretty-printer outputs a human-readable, indented tree that reflects the expression’s hierarchical structure. This AST foundation can be extended for full evaluation, semantic checks, or code generation in future labs.

## References

1. [Lexical analysis – Wikipedia](https://en.wikipedia.org/wiki/Lexical_analysis)  
