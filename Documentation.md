
---

# Custom Functional Language Interpreter Project Report

## Introduction

This report details the development of a custom interpreter for a functional programming language, as required by the project specifications. The interpreter supports fundamental features such as integer and boolean data types, arithmetic and boolean operations, comparison operations, function definitions, lambda expressions, recursion, and immutability. The language is designed to emphasize functional programming principles, particularly the use of functions and lambdas without variable assignments or mutable states.

## Design Decisions

### Language Features

1. **Data Types**:
  - **INTEGER**: Supports whole numbers, both positive and negative (e.g., `-3`, `0`, `42`).
  - **BOOLEAN**: Supports `True` and `False` values for logical operations.

2. **Operations**:
  - **Arithmetic Operations**: Includes addition (`+`), subtraction (`-`), multiplication (`*`), division (`/`), and modulo (`%`), specifically for integers.
  - **Boolean Operations**: Implements logical AND (`&&`), OR (`||`), and NOT (`!`) for boolean values.
  - **Comparison Operations**: Supports `==`, `!=`, `>`, `<`, `>=`, and `<=` to facilitate conditional logic.

3. **Functions**:
  - **Named Functions**: Allows users to define functions with specific names for reuse.
  - **Lambda Expressions**: Supports anonymous functions for concise function definitions.
  - **Recursion**: Functions can call themselves, enabling the simulation of loops through recursive calls.

4. **Immutability**:
  - All values are immutable, reinforcing the functional programming paradigm. The language does not allow variable assignments or state changes, ensuring purity in function execution.

### Abstract Syntax Tree (AST)

The interpreter constructs an Abstract Syntax Tree (AST) from the parsed input. This tree represents the hierarchical structure of the program, where different nodes correspond to data types, operations, functions, and expressions. The AST serves as the core structure for the interpreter to traverse and evaluate the program.

### Environment and Call Stack

The environment is responsible for managing the scope of variables and functions during execution. A call stack is implemented to handle function calls and recursion, ensuring correct scope resolution and tracking active function calls.

## Challenges Faced

### 1. Lexer and Parser Development

**Challenge**:
- Developing a lexer that accurately tokenizes input and a parser that correctly constructs an AST according to the language's BNF (Backus–Naur form) was complex, especially for handling nested expressions and ensuring correct precedence of operations.

**Solution**:
- A robust lexer was implemented to handle whitespace, comments, and all language constructs. The parser was designed to follow the BNF grammar, ensuring accurate representation of the program's structure in the AST.

### 2. Function and Lambda Handling

**Challenge**:
- Implementing functions and lambda expressions required careful handling of scope and closures, particularly when functions are defined within other functions.

**Solution**:
- Nested environments were used to capture the scope in which a function or lambda was defined. This approach ensured that the function or lambda could access variables from its defining scope, even when executed in a different context.

### 3. Recursion and Immutability

**Challenge**:
- Supporting recursion without mutable states required the interpreter to handle function calls efficiently, especially when simulating loops through recursive calls.

**Solution**:
- The call stack was designed to manage function calls and recursion effectively. Each function call was pushed onto the stack with its own environment, and immutability was maintained by avoiding any state changes within these environments.

## Solutions Implemented

### Lexer and Parser

- The lexer tokenizes the input code into symbols, while the parser builds the AST from these tokens. The parser adheres to the language's BNF grammar, ensuring that the structure of the input code is correctly represented in the AST.

### Interpreter

- The interpreter traverses the AST, evaluating each node according to its type. It handles arithmetic and boolean operations, function applications, and recursion, while maintaining immutability throughout the execution.

### Error Handling

- Comprehensive error handling was implemented, including syntax errors, type mismatches, and runtime errors. The interpreter provides meaningful error messages to help users identify and resolve issues in their code.

### REPL (Read-Eval-Print Loop)

- A REPL was developed for interactive use, allowing users to execute commands line by line and see the results immediately. This mode is particularly useful for testing and debugging individual expressions or functions.

### Testing and Validation

- A comprehensive test suite was developed to ensure the correctness of the interpreter. Test cases covered all language features, including edge cases and error conditions. A 30-line program was written to demonstrate the language's capabilities, particularly focusing on recursion and higher-order functions.
 ```plaintext
    # Define functions
    defun subtract(a, b) { a - b }
    defun divide(a, b) { a / b }
    defun fibonacci(n) {
        if (n <= 1) {
            return n
        } else {
            return fibonacci(n - 1) + fibonacci(n - 2)
        }
    }
    
    # Define a function to calculate the square of a number
    defun square(x) { x * x }
    
    # Define a function to add two numbers
    defun add(a, b) { a + b }
    
    # Define a function that applies a lambda to a number
    defun apply_lambda_to_num(f, x) { f(x) }
    
    # Function calls
    subtract(15, 5)        # Expected output: 10
    divide(40, 8)          # Expected output: 5
    fibonacci(7)           # Expected output: 13 (0, 1, 1, 2, 3, 5, 8, 13)
    
    # Lambda function calls
    lambda x: x + 10(20)          # Expected output: 30
    lambda f: f(4)(lambda x: x * 3) # Expected output: 12
    
    # Nested function calls
    lambda f: f(5)(lambda x: x - 3) # Expected output: 2
    
    # Boolean and comparison operations
    true && false  # Expected output: false
    true || false  # Expected output: true
    !false         # Expected output: true
    
    !(3 == 3) && (3 != 4)  # Expected output: false
    (3 < 4) || (4 > 3)   # Expected output: true
    (3 <= 3) != true  # Expected output: false
    
    # If-Else expressions
    if (true){ return 1 }else{ return 0 }  # Expected output: 1
    if (false){ return 1 }else{ return 0}  # Expected output: 0


 ```

## Conclusion

The custom functional language interpreter project successfully implemented a functional programming language with a focus on immutability and recursion. The development process involved significant challenges, particularly in handling functions and lambdas within a strict functional paradigm. However, through careful design and robust implementation, these challenges were overcome. The final interpreter supports both interactive and program execution modes, providing a reliable platform for exploring functional programming concepts.

---