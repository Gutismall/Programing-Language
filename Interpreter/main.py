from lexer import Lexer
from parser import Parser
from Interpreter import Interpreter
import sys


def read_code_from_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code


def run_code_from_file(file_path):
    code = read_code_from_file(file_path)

    lexer = Lexer(code)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()


def run_repl():
    while True:
        try:
            text = input('New_line> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        if result is None:
            print("Command executed")
        else:
            print(result)


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        # Check if the file ends with .lambda
        if not file_path.endswith('.lambda'):
            print("Error: The file must have a .lambda extension.")
            sys.exit(1)
        run_code_from_file(file_path)
    else:
        run_repl()


if __name__ == '__main__':
    run_code_from_file('/Users/ariguterman/Documents/School/Second year/Second semester/Programming Languages/Interpreter project/Interpreter/program_test.lambda')
    #main()
