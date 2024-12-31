from itertools import permutations, product

GOAL = 24
MAX = 13

def evaluate_polish(expression):
    tokens = expression.split()
    stack = []

    operators = {'+', '-', '*', '/'}

    for token in reversed(tokens):
        if token in operators:
            operand1 = stack.pop()
            operand2 = stack.pop()
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 / operand2
            stack.append(result)
        else:
            stack.append(float(token))

    return stack.pop()

def polish_to_infix(expression):
    stack = []
    operators = set(['+', '-', '*', '/', '^'])

    for token in reversed(expression.split()):
        if token in operators:
            operand1 = stack.pop()
            operand2 = stack.pop()
            stack.append(f"({operand1} {token} {operand2})")
        else:
            stack.append(token)

    return stack[0]

def generate_expressions(numbers, pattern):
    expressions = []
    for num_perm in permutations(numbers):  
        for ops in product(["+", "-", "*", "/"], repeat=pattern.count("A")):
            exp = []
            num_idx = 0
            op_idx = 0

            for char in pattern:
                if char == "D":
                    exp.append(str(num_perm[num_idx]))
                    num_idx += 1
                elif char == "A":
                    exp.append(ops[op_idx])
                    op_idx += 1

            expressions.append(" ".join(exp))
    return expressions

def twentyfour(numbers):
    patterns = ["AAADDDD", "AADADDD", "AADDADD", "ADAADDD", "ADADADD"]
    working = []

    for pattern in patterns:
        expressions = generate_expressions(numbers, pattern)
        for expression in expressions:
            try:
                if abs(evaluate_polish(expression) - GOAL) < 1e-5 and evaluate_polish(expression) - GOAL >= -1e-5: 
                    if expression not in working:
                        working.append(expression)
            except (IndexError, ZeroDivisionError):
                continue

    return working

def get_valid_number(prompt, max_value):
    while True:
        try:
            num = int(input(prompt))
            if 0 <= num <= max_value:
                return num
            else:
                print(f"Please enter a number between 0 and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


numbers = []

MAX = int(input("Maximum value of the numbers to be assembled (e.g. 13): "))
GOAL = int(input("Number to make (e.g. 24): "))

numbers.append(get_valid_number(f"First number (0-{MAX}): ", MAX))
numbers.append(get_valid_number(f"Second number (0-{MAX}): ", MAX))
numbers.append(get_valid_number(f"Third number (0-{MAX}): ", MAX))
numbers.append(get_valid_number(f"Fourth number (0-{MAX}): ", MAX))

solutions = twentyfour(numbers)

if solutions:
    print(f"Solutions that evaluate to {GOAL}:")
    for solution in solutions:
        print(polish_to_infix(solution)[1:len(polish_to_infix(solution)) - 1] + f" = {GOAL}")
else:
    print("No solutions found.")
