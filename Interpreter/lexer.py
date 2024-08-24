# lexer.py

# Token types
tokens = (
    'INTEGER',
    'BOOLEAN',
    'VARIABLE',
    'DEFUN',
    'RETURN',
    'PLUS',
    'MINUS',
    'MUL',
    'DIV',
    'MODULO',
    'EQUAL',
    'NEQUAL',  # !=
    'EQEQ',  # ==
    'COMMA',
    'GT',  # >
    'LT',  # <
    'GTE',  # >=
    'LTE',  # <=
    'AND',  # &&
    'OR',  # ||
    'NOT',  # !
    'LPAREN',  # (
    'RPAREN',  # )
    'LBRACE',  # {
    'RBRACE',  # }
    'NEWLINE',
    'EOF',
    'COMMENT',
)

t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_EQEQ = r'=='
t_NEQUAL = r'!='
t_GT = r'>'
t_LT = r'<'
t_GTE = r'>='
t_LTE = r'<='
t_COLLON = r':'


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, message="Invalid character"):
        raise Exception(f"Lexer error: {message} at position {self.pos}")

    def advance(self):
        """Advance the token by one character."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_comment(self):
        """Comment handling"""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()  # Move to the next character
        self.advance()  # Skip the newline character

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def identifier(self):
        """Handle identifiers and keywords like WHILE, DEFUN, etc."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        if result == 'true' or result == 'false':
            return Token('BOOLEAN', result)
        elif result == 'defun':
            return Token('DEFUN', result)
        elif result == 'return':
            return Token('RETURN', result)
        elif result == 'if':
            return Token('IF', result)
        elif result == 'else':
            return Token('ELSE', result)
        elif result == 'lambda':
            return Token('LAMBDA', result)
        else:
            return Token('VARIABLE', result)

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token('INTEGER', int(result))

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '+':
                self.advance()
                if self.current_char == '+':
                    self.advance()
                    return Token('PLUSONE', '++')
                return Token('PLUS', '+')

            if self.current_char == '-':
                self.advance()
                if self.current_char == '-':
                    self.advance()
                    return Token('MINUSONE', '--')
                return Token('MINUS', '-')

            if self.current_char == '*':
                self.advance()
                return Token('MUL', '*')

            if self.current_char == '/':
                self.advance()
                return Token('DIV', '/')

            if self.current_char == '%':
                self.advance()
                return Token('MODULO', '%')

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('EQEQ', '==')
                return Token('EQUAL', '=')

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('NEQUAL', '!=')
                else:
                    return Token('NOT', '!')
                self.error()

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('GTE', '>=')
                return Token('GT', '>')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('LTE', '<=')
                return Token('LT', '<')

            if self.current_char == ',':
                self.advance()
                return Token('COMMA', ',')

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN', '(')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN', ')')

            if self.current_char == '{':
                self.advance()
                return Token('LBRACE', '{')

            if self.current_char == '}':
                self.advance()
                return Token('RBRACE', '}')

            if self.current_char == '\n':
                self.advance()
                return Token('NEWLINE', '\n')
            if self.current_char == ':':
                self.advance()
                return Token('COLON', ':')
            if self.current_char == '&':
                self.advance()
                if self.current_char == '&':
                    self.advance()
                    return Token('AND', '&&')
                self.error("Expected '&' after '&' for '&&'")

            if self.current_char == '|':
                self.advance()
                if self.current_char == '|':
                    self.advance()
                    return Token('OR', '||')
                self.error("Expected '|' after '|' for '||'")

            self.error(f"Unexpected character '{self.current_char}'")

        return Token('EOF', None)

    def peek_next_token(self):
        # Save the current state
        current_pos = self.pos
        current_char = self.current_char

        # Get the next token
        next_token = self.get_next_token()

        # Restore the state
        self.pos = current_pos
        self.current_char = current_char

        return next_token
