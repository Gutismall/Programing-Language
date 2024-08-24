# Custom Language Interpreter

## Introduction

This guide explains how to run your custom language interpreter, execute programs, and run tests using both interactive mode and full program execution mode. The interpreter is designed to handle files with the `.lambda` extension.

## Prerequisites

- Ensure you have Python installed on your system.
- Save your language programs with the `.lambda` extension.

## Running the Interpreter

### Interactive Mode

1. Open a terminal or command prompt.
2. Navigate to the directory containing all the file from the Interpreter folder.
3. Run the following command:

    ```sh
    python3 main.py
    ```

4. You will see the prompt `New_line>`. You can now enter commands line by line. After typing each command, press Enter to execute it and see the result.

   Example:

    ```plaintext
    New_line> 2 + 3
    5
    New_line> def multiply(a, b): a * b
    Command executed
    New_line> multiply(4, 5)
    20
    New_line> lambda x: x + 1(7)
    8
    ```

   To exit the interactive mode, press `Ctrl+C` and press Enter.

### Full Program Execution Mode

1. Open a terminal or command prompt.
2. Navigate to the directory containing `main.py` and your `.lambda` program file.
3. Run the following command:

    ```sh
    python3 main.py your_program.lambda
    ```

   Replace `your_program` with the name of your file.

   Example:

   Assuming you have a file named `test.lambda` with the following content:

    ```plaintext
    # Define functions
    defun subtract(a, b){ a - b }
    defun divide(a, b){ a / b }
    defun fibonacci(n){ if (n <= 1){ return n } else{ return fibonacci(n - 1) + fibonacci(n - 2) }}

    # Function calls
    subtract(10, 4)      # Expected output: 6
    divide(20, 5)        # Expected output: 4
    fibonacci(6)         # Expected output: 8 (0, 1, 1, 2, 3, 5, 8)

    # Lambda function calls
    lambda x: x * 2(15)          # Expected output: 30
    lambda f: f(3)(lambda x: x * x) # Expected output: 9

    # Nested function call
    lambda f: f(3)(lambda x: x * 2) # Expected output: 6
    ```

   Run the following command:

    ```sh
    python interpreter.py test.lambda
    ```

   The interpreter will execute each line and print the results:

   ```plaintext
    6
    4
    8
    30
    9
    6
    ```

## Conclusion

This guide covers how to run your custom language interpreter in both interactive mode and full program execution mode. By following these steps, you can easily execute and test your `.lambda` programs. If you encounter any issues, ensure that your Python installation is correctly set up and that your program files are properly formatted.

---