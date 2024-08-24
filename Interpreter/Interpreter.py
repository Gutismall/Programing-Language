from parser import  Var, ReturnNode, IfNode, FunctionCallNode, LambdaNode

"""Global variables / functions"""
functions = {}
variables = {}


class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.call_stack = []

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_IfNode(self, node):
        condition = self.visit(node.condition)
        if condition:
            return self.visit(node.block)
        elif node.else_block is not None:
            return self.visit(node.else_block)

    def visit_LambdaNode(self, node):
        if node.arg is not None:
            local_scope = {}
            # Map parameters to argument values in the local scope
            for param, arg in zip(node.params, node.arg):
                local_scope[param] = arg

            # Push the local scope onto the call stack
            self.call_stack.append(local_scope)

            if isinstance(node.expr, FunctionCallNode):
                new_args = []
                func = local_scope[node.expr.name]
                for arg in node.expr.args:
                    new_args.append(arg)
                func.arg = new_args
                result = self.visit(func)
            else:
                result = self.visit(node.expr)

            # Pop the local scope off the call stack
            self.call_stack.pop()

            return result

    def visit_BlockNode(self, node):
        result = None
        for statement in node.statements:
            result = self.visit(statement)
            if isinstance(statement, ReturnNode):
                return result  # Return immediately if a return statement is encountered
        return result  # Return the result of the last statement in the block

    def visit_Var(self, node):
        var_name = node.name

        # Check the top of the call stack (local scope)
        if self.call_stack and var_name in self.call_stack[-1]:
            return self.call_stack[-1][var_name]

        # If not found in the local scope, check the global scope
        if var_name in variables:
            return variables[var_name]

        raise Exception(f"Variable '{var_name}' not found.")

    def visit_Assign(self, node):
        var_name = node.variable.name
        var_value = self.visit(node.expr)

        # Assign to the local scope if a function is active
        if self.call_stack:
            self.call_stack[-1][var_name] = var_value
        else:
            variables[var_name] = var_value

    def visit_int(self, node):
        return node

    def visit_Boolean(self, node):
        return node.value

    def visit_FunctionDecNode(self, node):
        functions[node.name] = node

    def visit_FunctionCallNode(self, node):
        if isinstance(node, LambdaNode):
            lambda_result = self.visit_LambdaNode(node.name)
            return lambda_result
        func_def = functions.get(node.name)
        if not func_def:
            raise Exception(f"Function '{node.name}' is not defined.")

        local_vars = {}
        for parameter, argument in zip(func_def.params, node.args):
            local_vars[parameter.name] = self.visit(argument)  # Evaluate the argument

        # Push the new local scope onto the call stack
        self.call_stack.append(local_vars)

        # Execute the function body
        result = self.visit(func_def.block)

        self.call_stack.pop()
        return result

    def visit_ReturnNode(self, node):
        return self.visit(node.expr)

    def visit_UnaryOp(self, node):
        op_type = node.op.type
        operand = self.visit(node.expr)

        if op_type == 'NOT':
            return not operand
        elif op_type == 'PLUS':
            return +operand
        elif op_type == 'MINUS':
            return -operand
        else:
            raise Exception(f"Unsupported unary operator {op_type}")

    def visit_BinOp(self, node):
        left_value = self.visit(node.left)
        right_value = self.visit(node.right)

        if node.op.type == 'PLUS':
            return left_value + right_value
        elif node.op.type == 'MINUS':
            return left_value - right_value
        elif node.op.type == 'MUL':
            return left_value * right_value
        elif node.op.type == 'DIV':
            if right_value == 0:
                raise Exception("Division by zero error")
            return left_value // right_value
        elif node.op.type == 'EQEQ':
            return left_value == right_value
        elif node.op.type == 'NEQUAL':
            return left_value != right_value
        elif node.op.type == 'GT':
            return left_value > right_value
        elif node.op.type == 'LT':
            return left_value < right_value
        elif node.op.type == 'GTE':
            return left_value >= right_value
        elif node.op.type == 'LTE':
            return left_value <= right_value
        elif node.op.type == 'AND':
            return left_value and right_value
        elif node.op.type == 'OR':
            return left_value or right_value
        else:
            raise Exception(f"Unsupported binary operator {node.op.type}")

    def interpret(self):
        tree = self.parser.parse()
        for node in tree.statements:
            result = self.visit(node)
            if result is not None:
                print(result)
        return
