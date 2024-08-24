Based on the project requirements provided in the PDF, here is a sample `README.md` file that includes all the necessary documentation for your project.

---

# Functional Programming Language Interpreter

## Overview

This project is a simple interpreter for a functional programming language that emphasizes function definitions, lambda expressions, and immutability. The language supports basic arithmetic operations, boolean logic, recursion, and higher-order functions. It is designed to provide an environment where functional programming concepts can be explored and utilized.

## Features

- **Data Types**: Supports integers and booleans.
- **Operations**: 
  - Arithmetic: `+`, `-`, `*`, `/`, `%`
  - Boolean: `&&`, `||`, `!`
  - Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Functions**: 
  - Named function definitions using `defun`.
  - Anonymous functions (lambda expressions).
  - Function applications.
- **Recursion**: Supports recursive function calls, enabling the creation of functions like factorial.
- **Immutability**: All values are immutable, and no variable assignments or state changes are allowed.
- **REPL (Read-Eval-Print Loop)**: Interactive mode for executing commands line by line.
- **Error Handling**: Comprehensive error handling for syntax, type, and runtime errors.

## Documentation

### 1. BNF Grammar

The following is the Backus–Naur form (BNF) grammar for the language:

```
<program> ::= <statement> NEWLINE <program> | EOF

<statement> ::= "if" "(" <expr> ")" "{" <block> "}" ["else" "{" <block> "}"] 
              | "defun" <variable> "(" <parameters> ")" "{" <block> "}" 
              | <variable> "=" <expr> 
              | <variable> <function_call> 
              | "return" <expr> 
              | <expr>

<block> ::= <statement> NEWLINE <block> | ""

<expr> ::= <term> ((PLUS | MINUS | EQEQ | NEQUAL | GT | LT | GTE | LTE | AND | OR) <term>)*
<term> ::= <factor> ((MUL | DIV | MODULO | AND | OR) <factor>)*
<factor> ::= (PLUS | MINUS | NOT) <factor> 
           | INTEGER 
           | BOOLEAN 
           | "(" <expr> ")" 
           | <variable> 
           | <function_call> 
           | "if" "(" <expr> ")" "{" <block> "}" ["else" "{" <block> "}"] 
           | "lambda" "(" <parameters> ")" ":" <expr> 
<parameters> ::= <variable> ("," <variable>)*
<arguments> ::= <expr> ("," <expr>)*
<function_call> ::= "(" <arguments> ")"
```

### 2. Language Syntax

- **Function Definition**: `defun factorial(n) { if (n == 0) { return 1 } else { return n * factorial(n - 1) } }`
- **Lambda Expression**: `lambda x: x + 1(arg)`
- **Function Application**: `factorial(5)`
- **Boolean Operations**: `(x > 0) && (y < 10)`
- **Arithmetic Operations**: `(3 + 4) * (2 - 1)`
- **Comments**: Lines beginning with `#` are comments and are ignored.

### 3. Design Considerations and Assumptions

- **Immutability**: The language enforces immutability, ensuring that once a value is bound to a variable, it cannot be changed. This encourages functional programming principles.
- **Recursion as Control Flow**: Since the language does not have loops, recursion is used as the primary mechanism for iteration.
- **Error Handling**: The interpreter provides meaningful error messages to help users debug their code. This includes syntax errors, type errors, and runtime errors such as division by zero.
- **Lambda Expressions**: The language supports anonymous functions via lambda expressions, which can be passed as arguments to higher-order functions.
- **Call Stack**: A call stack is implemented to manage function calls, especially for handling recursion.

### 4. Code Structure

- **`lexer.py`**: Responsible for tokenizing the input source code.
- **`parser.py`**: Builds an Abstract Syntax Tree (AST) from the tokens provided by the lexer.
- **`interpreter.py`**: Executes the AST, evaluating expressions and handling function calls.
- **`main.py`**: Entry point of the application. It includes the REPL and file execution modes.

### 5. How to Run

#### Running a `.lambda` File

To execute a `.lambda` file:

```bash
python3 main.py your_file_name.lambda
```

#### Interactive Mode (REPL)

To enter the REPL mode:

```bash
python3 main.py
```

You can then type commands line by line, and the interpreter will execute them and print the results.

### 6. Testing

A comprehensive test suite is provided in the `test.lambda` file. This file contains various examples demonstrating the language's features, including:

- Function definitions and recursion.
- Lambda expressions and higher-order functions.
- Boolean and arithmetic operations.
- Error handling cases.

### 7. Challenges and Solutions

- **Challenge**: Implementing recursion without loops.
  - **Solution**: Using the call stack to manage recursive function calls effectively.
- **Challenge**: Enforcing immutability while allowing functional programming constructs.
  - **Solution**: The language design inherently avoids mutable state, ensuring that all variables are immutable.
- **Challenge**: Error handling.
  - **Solution**: Comprehensive checks at every stage (lexer, parser, interpreter) with clear error messages.

### 8. Theoretical Questions

Answers to theoretical questions can be found in the `finalProject2024B.pdf` document, covering topics such as lazy evaluation, functional programming concepts, and more.

## Conclusion

This project demonstrates the key concepts of functional programming through a custom-designed interpreter. By focusing on immutability, recursion, and higher-order functions, it provides a platform for exploring the power of functional programming in a controlled environment.

---

This `README.md` provides a complete overview of your project, fulfilling the documentation requirements specified in your project guidelines.