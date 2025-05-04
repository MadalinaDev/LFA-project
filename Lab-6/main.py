import re
import enum
from typing import NamedTuple, List, Optional, Union

class TokenType(enum.Enum):
    INTEGER      = "INTEGER"
    FLOAT        = "FLOAT"
    COMPLEX      = "COMPLEX"
    PLUS         = "PLUS"
    MINUS        = "MINUS"
    MULTIPLY     = "MULTIPLY"
    DIVIDE       = "DIVIDE"
    LPAREN       = "LPAREN"
    RPAREN       = "RPAREN"
    COMMA        = "COMMA"
    IDENTIFIER   = "IDENTIFIER"
    SIN          = "SIN"
    COS          = "COS"
    TAN          = "TAN"
    EOF          = "EOF"

class Token(NamedTuple):
    type: TokenType
    value: Optional[Union[int, float, complex, str]]

class Lexer:
    _specs = [
        (TokenType.COMPLEX,    r'(?P<complex>\d+(?:\.\d+)?[jJ])'),
        (TokenType.FLOAT,      r'(?P<float>\d+\.\d+)'),
        (TokenType.INTEGER,    r'(?P<integer>\d+)'),
        (TokenType.SIN,        r'(?P<sin>\bsin\b)'),
        (TokenType.COS,        r'(?P<cos>\bcos\b)'),
        (TokenType.TAN,        r'(?P<tan>\btan\b)'),
        (TokenType.IDENTIFIER, r'(?P<identifier>[A-Za-z_]\w*)'),
        (TokenType.PLUS,       r'(?P<plus>\+)'),
        (TokenType.MINUS,      r'(?P<minus>-)'),
        (TokenType.MULTIPLY,   r'(?P<multiply>\*)'),
        (TokenType.DIVIDE,     r'(?P<divide>/)'),
        (TokenType.LPAREN,     r'(?P<lparen>\()'),
        (TokenType.RPAREN,     r'(?P<rparen>\))'),
        (TokenType.COMMA,      r'(?P<comma>,)'),
        (None,                 r'(?P<ws>\s+)'),
    ]
    _master_pat = re.compile('|'.join(p for _, p in _specs))

    def __init__(self, text: str):
        self._scanner = Lexer._master_pat.scanner(text)
        self.next_token: Token = self._advance()

    def _advance(self) -> Token:
        m = self._scanner.match()
        if not m:
            return Token(TokenType.EOF, None)
        typ = None
        for tok_type, _ in self._specs:
            name = tok_type.name.lower() if tok_type else 'ws'
            if m.lastgroup == name:
                typ = tok_type
                break
        if typ is None:
            return self._advance()
        txt = m.group(m.lastgroup)
        if typ is TokenType.INTEGER:
            val = int(txt)
        elif typ is TokenType.FLOAT:
            val = float(txt)
        elif typ is TokenType.COMPLEX:
            val = complex(txt)
        else:
            val = txt
        return Token(typ, val)

    def eat(self, typ: TokenType) -> Token:
        cur = self.next_token
        if cur.type is typ:
            self.next_token = self._advance()
            return cur
        raise SyntaxError(f"Expected {typ}, got {cur.type}")

class AST: pass

class Number(AST):
    def __init__(self, value: Union[int, float]):
        self.value = value
    def __repr__(self):
        return f"Number({self.value})"

class ComplexNumber(AST):
    def __init__(self, value: complex):
        self.value = value
    def __repr__(self):
        return f"Complex({self.value})"

class Identifier(AST):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f"Ident({self.name})"

class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left, self.op, self.right = left, op, right
    def __repr__(self):
        return f"BinOp({self.left}, {self.op.type.name}, {self.right})"

class UnaryOp(AST):
    def __init__(self, op: Token, expr: AST):
        self.op, self.expr = op, expr
    def __repr__(self):
        return f"UnaryOp({self.op.type.name}, {self.expr})"

class FunctionCall(AST):
    def __init__(self, func_name: str, args: List[AST]):
        self.func_name, self.args = func_name, args
    def __repr__(self):
        return f"Call({self.func_name}, {self.args})"

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

    def parse(self) -> AST:
        node = self.expr()
        if self.lexer.next_token.type is not TokenType.EOF:
            raise SyntaxError("Unexpected token after expression")
        return node

    def expr(self) -> AST:
        node = self.term()
        while self.lexer.next_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.lexer.next_token
            self.lexer.eat(op.type)
            node = BinOp(node, op, self.term())
        return node

    def term(self) -> AST:
        node = self.factor()
        while self.lexer.next_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op = self.lexer.next_token
            self.lexer.eat(op.type)
            node = BinOp(node, op, self.factor())
        return node

    def factor(self) -> AST:
        tok = self.lexer.next_token
        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            self.lexer.eat(tok.type)
            return UnaryOp(tok, self.factor())

        if tok.type is TokenType.INTEGER:
            self.lexer.eat(TokenType.INTEGER)
            return Number(tok.value)
        if tok.type is TokenType.FLOAT:
            self.lexer.eat(TokenType.FLOAT)
            return Number(tok.value)
        if tok.type is TokenType.COMPLEX:
            self.lexer.eat(TokenType.COMPLEX)
            return ComplexNumber(tok.value)

        if tok.type in (TokenType.SIN, TokenType.COS, TokenType.TAN, TokenType.IDENTIFIER):
            name = tok.value
            self.lexer.eat(tok.type)
            if self.lexer.next_token.type is TokenType.LPAREN:
                self.lexer.eat(TokenType.LPAREN)
                args = []
                if self.lexer.next_token.type is not TokenType.RPAREN:
                    args.append(self.expr())
                    while self.lexer.next_token.type is TokenType.COMMA:
                        self.lexer.eat(TokenType.COMMA)
                        args.append(self.expr())
                self.lexer.eat(TokenType.RPAREN)
                return FunctionCall(name, args)
            else:
                return Identifier(name)

        if tok.type is TokenType.LPAREN:
            self.lexer.eat(TokenType.LPAREN)
            node = self.expr()
            self.lexer.eat(TokenType.RPAREN)
            return node

        raise SyntaxError(f"Unexpected token {tok}")

def ast_to_string(node: AST, indent: int = 0) -> str:
    prefix = '  ' * indent
    if isinstance(node, Number):
        return f"{prefix}Number({node.value})"
    if isinstance(node, ComplexNumber):
        return f"{prefix}Complex({node.value})"
    if isinstance(node, Identifier):
        return f"{prefix}Ident({node.name})"
    if isinstance(node, UnaryOp):
        s = f"{prefix}UnaryOp({node.op.type.name})\n"
        s += ast_to_string(node.expr, indent + 1)
        return s
    if isinstance(node, BinOp):
        s = f"{prefix}BinOp({node.op.type.name})\n"
        s += ast_to_string(node.left, indent + 1) + "\n"
        s += ast_to_string(node.right, indent + 1)
        return s
    if isinstance(node, FunctionCall):
        s = f"{prefix}Call({node.func_name})\n"
        for i, arg in enumerate(node.args):
            s += ast_to_string(arg, indent + 1)
            if i != len(node.args) - 1:
                s += "\n"
        return s
    return f"{prefix}{node}"

if __name__ == '__main__':
    text = input("Enter expression ▶ ")
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()
    print("AST ▶")
    print(ast_to_string(ast))


# sample inputs
# sin(30) + cos(45.0) - tan(1.57) + 3 + 4j - 2.5j
# sin(cos(45) + tan(30)) * (3 + 4) - 5j / (2 - 1.5)
# cos(sin(60) * tan(30)) + (7.2 - 3j) * (4 + 5.5)
# (1 + 4j) * (2 - 3j) + sin(0.25) * cos(1.5) - tan(0.75)