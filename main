import random

def generate_one_variable_problem(difficulty):
    variable = 'x'
    try:
        if difficulty == 'addition/subtraction':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            sign = random.choice(['+', '-'])
            order = [a, b, variable]
            random.shuffle(order)
            problem = f"{order[1]} {sign} {order[2]} = {order[0]}"

        elif difficulty == 'multiplication/division':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            c = random.choice([-1, 1]) * random.randint(1, 10)
            sign = random.choice(['+', '-'])
            MD = (['/','*'])
            variableExist = ([variable, random.randint(1,5)])
            order1 = [a, random.choice(variableExist)]
            order2 = [b, random.choice(variableExist)]
            order3 = [c, random.choice(variableExist)]
            random.shuffle(order1)
            random.shuffle(order2)
            random.shuffle(order3)
            problem = f"{order1[0]}{random.choice(MD)}{order1[1]} {sign} {order2[0]}{random.choice(MD)}{order2[1]} = {order3[0]}{random.choice(MD)}{order3[1]}"
            if variable not in problem:
                # fallback: explicitly include the variable so result always contains it
                problem = f"{variable} {sign} {order2[0]} = {order3[0]}"
        
        elif difficulty == 'exponents/roots':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            c = random.choice([-1, 1]) * random.randint(1, 10)
            exponent = random.randint(2, 3)
            sign = random.choice(['^', '√'])
            AS = random.choice(['+', '-'])
            order = [a, b, c]
            variableExist = ([variable, ''])
            random.shuffle(order)
            if sign == '^':
                problem = f"{order[1]}{random.choice(variableExist)} {AS} {order[2]}{random.choice(variableExist)}^{exponent} = {order[0]}{random.choice(variableExist)}"
                if variable not in problem:
                    problem = f"{order[1]} {AS} {order[2]} = {variable}^{exponent}"
            else:
                problem = f"{order[1]}{random.choice(variableExist)} {AS} √{order[2]*order[2]}{random.choice(variableExist)} = {order[0]}{random.choice(variableExist)}"
                if variable not in problem:
                    problem = f"{order[1]} {AS} √{order[2]*order[2]} = {variable}"

        elif difficulty == 'mixed':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            c = random.choice([-1, 1]) * random.randint(1, 10)
            AS = random.choice(['+', '-'])
            MD = random.choice(['*', '/'])
            ER = random.choice(['^', '√'])
            variableExist = ([variable, random.randint(1,5)])
            order1 = [a, random.choice(variableExist)]
            order2 = [b, random.choice(variableExist)]
            order3 = [c, random.choice(variableExist)]
            random.shuffle(order1)
            random.shuffle(order2)
            random.shuffle(order3)
            signs = [MD, ER]
            random.shuffle(signs)
            problem = f"{order1[0]}{signs[0]}{order1[1]} {AS} {order2[0]}{signs[1]}{order2[1]} = {order3[0]}{signs[0]}{order3[1]}"
            if variable not in problem:
                problem = f"{order1[0]}{signs[0]}{order1[1]} {AS} {order2[0]}{signs[1]}{order2[1]} = {variable}{signs[0]}{order3[1]}"
        return problem
    
    except (UnboundLocalError, EOFError):
      print("Incorrect Input!")
      return None
    
def generate_two_variable_problem(difficulty):
    variable1 = 'x'
    variable2 = 'y'
    try:
        if difficulty == 'addition/subtraction':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            sign = random.choice(['+', '-'])
            order = [a, variable1, variable2]
            random.shuffle(order)
            problem = f"{order[1]} {sign} {order[2]} = {order[0]}"

        elif difficulty == 'multiplication/division':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            c = random.choice([-1, 1]) * random.randint(1, 10)
            sign = random.choice(['+', '-'])
            MD = ['*', '/']
            order = [a,b,c, variable1, variable2]
            random.shuffle(order)
            problem = f"{order[1]}{random.choice(MD)}{order[2]} {sign} {order[3]}{random.choice(MD)}{order[4]} = {order[0]}"

        elif difficulty == 'exponents/roots':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            c = random.choice([-1, 1]) * random.randint(1, 10)
            exponent = random.randint(2, 3)
            sign = random.choice(['^', '√'])
            AS = random.choice(['+', '-'])
            order = [a, b, c]
            random.shuffle(order)
            if sign == '^':
                problem = f"{order[1]}{random.choice([variable1, variable2])} {AS} {order[2]}{random.choice([variable1, variable2])}^{exponent} = {order[0]}{random.choice([variable1, variable2])}"
                if variable1 not in problem or variable2 not in problem:
                    problem = f"{order[1]} {AS} {order[2]} = {variable1}^{exponent}*{variable2}"
            else:
                problem = f"{order[0]}{random.choice([variable1, variable2])} {AS} √{order[1]*order[1]}{random.choice([variable1, variable2])} = {order[2]}{random.choice([variable1, variable2])}"
                if variable1 not in problem or variable2 not in problem:
                    problem = f"{order[0]} {AS} √{order[1]*order[1]} = {variable1}*{variable2}"

        elif difficulty == 'mixed':
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            c = random.choice([-1, 1]) * random.randint(1, 10)
            AS = random.choice(['+', '-'])
            MD = random.choice(['*', '/'])
            ER = random.choice(['^', '√'])
            order = [a,b,c, variable1, variable2]
            random.shuffle(order)
            signs = [MD, ER]
            random.shuffle(signs)
            problem = f"{order[0]}{signs[0]}{order[3]} {AS} {order[1]}{signs[1]}{order[4]} = {order[2]}{signs[0]}{order[3]}"
        return problem


    except (UnboundLocalError, EOFError):
        print("Incorrect Input!")
        return None

def main():
    while True:
        variableAmount = input("Choose variable amount (one/two) or press 'q' to quit: ")
        if variableAmount == 'one':
            difficulty = input("Choose difficulty (addition/subtraction, multiplication/division, exponents/roots, mixed): ")
            problem = generate_one_variable_problem(difficulty)
            print(f"Generated problem: {problem}")
        elif variableAmount == 'two':
            difficulty = input("Choose difficulty (addition/subtraction, multiplication/division, exponents/roots, mixed): ")
            problem = generate_two_variable_problem(difficulty)
            print(f"Generated problem: {problem}")
        elif variableAmount == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid variable amount!")

if __name__ == "__main__":
    main()
