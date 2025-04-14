# token types
INTEGER, FLOAT, COMPLEX, PLUS, MINUS, MULTIPLY, DIVIDE, LPAREN, RPAREN, COMMA, SIN, COS, TAN, IDENTIFIER, EOF = (
    'INTEGER', 'FLOAT', 'COMPLEX', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'LPAREN', 'RPAREN', 'COMMA',
    'SIN', 'COS', 'TAN', 'IDENTIFIER', 'EOF'
)

# reserved keywords for trig functions
RESERVED_KEYWORDS = {
    'sin': SIN,
    'cos': COS,
    'tan': TAN,
}

class Token:
    def __init__(self, type_, value):
        self.type = type_  # token type (like integer, float, etc.)
        self.value = value  # actual value (for example, 3, 3.14, or 'sin')
        
    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"
    
    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text      # the input string
        self.pos = 0          # current position in the input
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception("invalid character encountered during lexing.")

    def advance(self):
        # move the position pointer and update the current character
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None  # no more input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        # look at the next character without moving the pointer
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        # skip over spaces and other whitespace
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """
        get a token for a number.
        it can be an integer, a float, or a complex number if it ends with a 'j'.
        """
        result = ''
        dot_count = 0
        
        # read digits and at most one dot
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break  # already got a dot, so break out
                dot_count += 1
            result += self.current_char
            self.advance()
        
        # if the next char is 'j', then it is a complex number literal
        if self.current_char is not None and self.current_char.lower() == 'j':
            self.advance()
            # now, treat the number as the imaginary part, with a real part of 0
            if dot_count == 0:
                return Token(COMPLEX, complex(0, int(result)))
            else:
                return Token(COMPLEX, complex(0, float(result)))
        
        # return integer or float token based on the dot count
        if dot_count == 0:
            return Token(INTEGER, int(result))
        else:
            return Token(FLOAT, float(result))
    
    def identifier(self):
        """
        collect letters to form an identifier.
        check if it is a reserved trig keyword (sin, cos, tan) and return the corresponding token.
        """
        result = ''
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        
        token_type = RESERVED_KEYWORDS.get(result.lower(), IDENTIFIER)
        return Token(token_type, result)
    
    def get_next_token(self):
        # this function goes through the input and returns one token at a time.
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                return self.number()
            
            if self.current_char.isalpha():
                return self.identifier()
            
            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')
            if self.current_char == '*':
                self.advance()
                return Token(MULTIPLY, '*')
            if self.current_char == '/':
                self.advance()
                return Token(DIVIDE, '/')
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            
            # if we reach here, the character is not recognized
            self.error()
        
        # once there is no input left, return an end-of-file token
        return Token(EOF, None)

if __name__ == '__main__':
    input_text = "sin(30) + cos(45.0) - tan(1.57) + 3 + 4j - 2.5j"
    lexer = Lexer(input_text)
    
    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()
    print(token)  # print the eof token
