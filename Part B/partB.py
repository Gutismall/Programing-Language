from functools import reduce
from typing import List

#Q1
fibonacci = lambda n: reduce(lambda x, _: x + [x[-1] + x[-2]], range(n-2), [0, 1][:n])
print(fibonacci(10))
#Q2
do_space = lambda lst: reduce(lambda x, y: x + ' ' + y, lst)
print(do_space(['This', 'is', 'Question', 'number', '2']))
#Q3
sum_even = lambda lst: list(map(
    lambda sublist: reduce(
        lambda acc, num: acc + (lambda x: x**2)(num),
        filter(
            lambda x: (lambda y: y % 2 == 0)(x),
            sublist
        ),
        0
    ),
    lst
))
print(sum_even([[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]))
# Q4
def cumulative_operation(op):
    return lambda seq: reduce(lambda x, y: op(x, y), seq)

# Factorial using the higher-order function
factorial = lambda n: cumulative_operation(lambda x, y: x * y)(range(1, n + 1))

# Exponentiation using the higher-order function
exponentiation = lambda base, exp: cumulative_operation(lambda x, y: x * y)([base] * exp)

# Example usage:
print(factorial(5))          # Output: 120
print(exponentiation(2, 3))  # Output: 8
# Q5
print(reduce(lambda acc, x: acc + x, map(lambda y: y**2, filter(lambda z: z % 2 == 0, [3, 4, 5, 6, 7, 8])), 0))
#Q6
count_palindromes = lambda lst: list(map(lambda sublist: reduce(lambda acc, s: acc + 1, filter(lambda x: x == x[::-1], sublist), 0), lst))

# Example usage:
print(count_palindromes([["level", "world", "radar"], ["hello", "madam", "noon"], ["python", "java"]]))

#Q7
print("Text based question, answer is written as a comment in the code.")
'''Lazy evaluation is a programming technique where expressions are not evaluated when they are assigned, 
but only when their values are actually needed. In the provided program, during eager evaluation, all values from 
`generate_values()` are generated and stored in memory before any further operations, leading to immediate 
computation and storage of results. Conversely, in lazy evaluation, `generate_values()` yields values one at a time 
as needed by the `square` function, delaying computation until each value is specifically required. This approach can 
improve efficiency by saving memory and avoiding unnecessary computations, especially when dealing with large 
datasets or complex operations.'''
#Q8
primes_desc = lambda lst: sorted([x for x in lst if all(x % i != 0 for i in range(2, int(x**0.5) + 1)) and x > 1], reverse=True)
print(primes_desc([10, 3, 5, 7, 11, 14, 17, 19, 23, 24, 29]))