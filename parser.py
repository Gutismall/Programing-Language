class AST(object):
    pass


class LambdaNode(AST):
    def __init__(self, params, expr, arg):
        self.params = params
        self.expr = expr
        self.arg = arg


class FunctionCallNode(AST):
    def __init__(self, name, args):
        if isinstance(name, Var):
            self.name = name.name
        else:
            self.name = name
        self.args = args


class FunctionDecNode(AST):
    def __init__(self, name, params, block):
        self.name = name
        self.params = params
        self.block = block


class ReturnNode(AST):
    def __init__(self, expr):
        self.expr = expr


class Assign:
    def __init__(self, variable, expr):
        self.variable = variable
        self.expr = expr


class Var:
    def __init__(self, name):
        self.name = name


class Boolean(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value == 'true'



class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class BlockNode:
    def __init__(self, statements):
        self.statements = statements


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class IfNode(AST):
    def __init__(self, condition, block, else_block):
        self.condition = condition
        self.block = block
        self.else_block = else_block


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, message="Invalid syntax"):
        raise Exception(message)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expected token {token_type}, but got {self.current_token.type} instead.")

    def factor(self):
        """
        factor : (PLUS | MINUS | NOT) factor
               | INTEGER
               | LPAREN expr RPAREN
               | VARIABLE
               | FUNCTION_CALL
               | BOOLEAN
               | IF_STATEMENT
               | LAMBDA_FUNCTION
        """
        token = self.current_token
        if token.type == 'PLUS':
            self.eat('PLUS')
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == 'MINUS':
            self.eat('MINUS')
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == 'NOT':
            self.eat('NOT')
            node = UnaryOp(token, self.factor())
            return node
        elif token.type == 'INTEGER':
            self.eat('INTEGER')
            return token.value
        elif token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        elif token.type == 'BOOLEAN':
            node = Boolean(token)
            self.eat('BOOLEAN')
            return node
        elif token.type == 'VARIABLE':
            var_name = token.value
            self.eat('VARIABLE')
            if self.current_token.type == 'LPAREN':
                return self.function_call(var_name)
            else:
                return Var(var_name)
        elif token.type == 'IF':
            node = self.ifStatement()
            return node
        elif token.type == 'LAMBDA':
            return self.lambda_function()
        else:
            self.error(f"Unexpected token {token.type} in factor.")

    def term(self):
        """
        term : factor ((MUL | DIV | MODULO | AND | OR) factor)*
        """
        node = self.factor()

        while self.current_token.type in ('MUL', 'DIV', 'MODULO', 'AND', 'OR'):
            token = self.current_token
            if token.type == 'MUL':
                self.eat('MUL')
            elif token.type == 'DIV':
                self.eat('DIV')
            elif token.type == 'MODULO':
                self.eat('MODULO')
            elif token.type == 'AND':
                self.eat('AND')
            elif token.type == 'OR':
                self.eat('OR')

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def assignment_statement(self):
        """assignment_statement : VARIABLE EQUAL expr"""
        var_name = self.current_token.value
        self.eat('VARIABLE')
        self.eat('EQUAL')
        expr = self.expr()
        return Assign(Var(var_name), expr)

    def expr(self):
        """expr : term ((PLUS | MINUS | EQEQ | NEQUAL | GT | LT | GTE | LTE | AND | OR) term)*"""
        node = self.term()

        while self.current_token.type in ('PLUS', 'MINUS', 'EQEQ', 'NEQUAL', 'GT', 'LT', 'GTE', 'LTE', 'AND', 'OR'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())

        return node

    def statement(self):
        """
        statement : IF_STATEMENT
                  | FUNCTION_DECLARATION
                  | VARIABLE (function_call | assignment_statement)
                  | RETURN expr
                  | LAMBDA_FUNCTION
                  | expr
        """
        token = self.current_token
        if token.type == 'IF':
            return self.ifStatement()

        elif token.type == 'DEFUN':
            return self.function_declaration()

        elif token.type == 'VARIABLE':
            next_token = self.lexer.peek_next_token()
            if next_token.type == 'LPAREN':
                self.eat('VARIABLE')
                return self.function_call(token.value)
            elif next_token.type == 'EQUAL':
                return self.assignment_statement()
            else:
                return self.expr()
        elif token.type == 'RETURN':
            self.eat('RETURN')
            expr = self.expr() if self.current_token.type != 'RBRACE' else None
            return ReturnNode(expr)
        elif token.type == 'LAMBDA':
            return self.lambda_function()

        else:
            return self.expr()

    def ifStatement(self):
        """
        ifStatement : IF LPAREN expr RPAREN LBRACE block RBRACE (ELSE LBRACE block RBRACE)?
        """
        self.eat('IF')
        self.eat('LPAREN')
        condition = self.expr()
        self.eat('RPAREN')
        self.eat('LBRACE')
        block = self.block()
        self.eat('RBRACE')
        if self.current_token.type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            else_block = self.block()
            self.eat('RBRACE')
            return IfNode(condition=condition, block=block, else_block=else_block)

        return IfNode(condition=condition, block=block, else_block=None)

    def block(self):
        """block : (statement NEWLINE)*"""
        statements = []
        while self.current_token.type != 'RBRACE' and self.current_token.type != 'EOF':
            statement = self.statement()
            statements.append(statement)
            if self.current_token.type == 'NEWLINE':
                self.eat('NEWLINE')
        return BlockNode(statements)

    def arguments(self):
        """
        arguments : expr (COMMA expr)*
        """
        arg = []
        while self.current_token.type != 'RPAREN':
            arg.append(self.expr())
            if self.current_token.type == 'COMMA':
                self.eat('COMMA')
        return arg

    def parameters(self):
        """
        parameters : VARIABLE (COMMA VARIABLE)*
        """
        parameters = []
        while self.current_token.type != 'RPAREN':
            parameters.append(self.factor())
            if self.current_token.type == 'COMMA':
                self.eat('COMMA')
        return parameters

    def function_declaration(self):
        """
        function_declaration : DEFUN VARIABLE LPAREN parameters RPAREN LBRACE block RBRACE
        """
        self.eat('DEFUN')
        name = self.current_token.value
        self.eat('VARIABLE')
        self.eat('LPAREN')
        params = self.parameters()
        self.eat('RPAREN')
        self.eat('LBRACE')
        block = self.block()
        self.eat('RBRACE')

        return FunctionDecNode(name=name, params=params, block=block)

    def function_call(self, func_name):
        """
        function_call : VARIABLE LPAREN arguments RPAREN
        """
        self.eat('LPAREN')
        args = self.arguments()
        self.eat('RPAREN')
        return FunctionCallNode(name=func_name, args=args)

    def lambda_function(self):
        """
        lambda_function : LAMBDA (VARIABLE | LPAREN (VARIABLE (COMMA VARIABLE)*)? RPAREN) COLON expr (LPAREN arguments RPAREN)?
        """
        self.eat('LAMBDA')
        params = []
        if self.current_token.type == 'VARIABLE':
            params.append(self.current_token.value)
            self.eat('VARIABLE')
        elif self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            while self.current_token.type == 'VARIABLE':
                params.append(self.current_token.value)
                self.eat('VARIABLE')
                if self.current_token.type == 'COMMA':
                    self.eat('COMMA')
                elif self.current_token.type == 'RPAREN':
                    break
            self.eat('RPAREN')
        self.eat('COLON')
        expr = self.expr()
        if self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            arg = self.arguments()
            self.eat('RPAREN')
            return LambdaNode(params=params, expr=expr,arg=arg)
        return LambdaNode(params=params, expr=expr,arg=None)

    def parse(self):
        statements = []
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'NEWLINE':
                self.eat('NEWLINE')
                continue
            statement = self.statement()
            statements.append(statement)
        return BlockNode(statements)
