import random
import sympy as sp

def generate_one_variable_problem(difficulty):
    variable = 'x'
    try:
        dd = (difficulty or '').lower()
        # normalize and check difficulty robustly
        if 'add' in dd or 'sub' in dd or dd in ('ad', 'as', 'a/s'):
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            sign = random.choice(['+', '-'])
            order = [a, b, variable]
            random.shuffle(order)
            problem = f"{order[1]} {sign} {order[2]} = {order[0]}"
        elif 'mult' in dd or 'div' in dd or dd in ('md', 'm/d'):
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
                problem = f"{variable} {sign} {order2[0]} = {order3[0]}"
        
        elif 'exponent' in dd or 'root' in dd or dd in ('er', 'e/r'):
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

        elif 'mixed' in dd:
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
        dd = (difficulty or '').lower()
        if 'add' in dd or 'sub' in dd or dd in ('as', 'a/s', 'ad'):
            a = random.choice([-1, 1]) * random.randint(1, 10)
            sign = random.choice(['+', '-'])
            order = [a, variable1, variable2]
            random.shuffle(order)
            problem = f"{order[1]} {sign} {order[2]} = {order[0]}"
        elif 'mult' in dd or 'div' in dd or dd in ('md', 'm/d'):
            a = random.choice([-1, 1]) * random.randint(1, 10)
            b = random.choice([-1, 1]) * random.randint(1, 10)
            c = random.choice([-1, 1]) * random.randint(1, 10)
            sign = random.choice(['+', '-'])
            MD = ['*', '/']
            order = [a,b,c, variable1, variable2]
            random.shuffle(order)
            problem = f"{order[1]}{random.choice(MD)}{order[2]} {sign} {order[3]}{random.choice(MD)}{order[4]} = {order[0]}"
        elif 'exponent' in dd or 'root' in dd or dd in ('er', 'e/r'):
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

        elif 'mixed' in dd:
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

def generate_Calc_problem(CalcType):
    x = sp.symbols('x')
    try:
        def random_polynomial(max_deg=3):
            deg = random.randint(1, max_deg)
            coeffs = [random.randint(-5, 5) for _ in range(deg + 1)]
            return sum(coeffs[i] * x**i for i in range(deg + 1))

        def random_trig() -> sp.Expr:
            a = sp.Integer(random.randint(1, 5))
            b = sp.Integer(random.randint(1, 3))
            c = sp.Integer(random.randint(1, 5))
            d = sp.Integer(random.randint(1, 3))
            result: sp.Expr = a * sp.sin(b * x) + c * sp.cos(d * x)  # type: ignore[operator]
            return result

        def random_exp_log() -> sp.Expr:
            a = sp.Integer(random.randint(1, 4))
            b = sp.Integer(random.randint(1, 3))
            expr: sp.Expr = a * sp.exp(b * x)  # type: ignore[operator]
            if random.choice([True, False]):
                c = sp.Integer(random.randint(1, 3))
                expr = expr + c * sp.log(x)  # type: ignore[operator]
            return expr

        generators = [random_polynomial, random_trig, random_exp_log]
        f = random.choice(generators)()

        if CalcType == 'D':
            problem = f"Differentiate: {f}"
            solution = sp.diff(f, x)
        elif CalcType == 'I':
            problem = f"Integrate: {f}"
            solution = sp.integrate(f, x)
        else:
            print("CalcType must be 'D' or 'I'")
            return None

        return problem, solution
    except Exception as e:
        print("Incorrect Input:", e)
        return None
    
def main():
    while True:
        ProblemType = input("Would you like to solve a Calculus or Algerbra Problem? Press C for Calculus and A for Algerbra: ")
        if ProblemType == 'A':
            variableAmount = input("Choose variable amount (one/two) or or press 'q' to go back: ")
            if variableAmount == 'one':
                difficulty = input("Choose difficulty (addition/subtraction(AS), multiplication/division(MD), exponents/roots(ER), mixed): ")
                problem = generate_one_variable_problem(difficulty)
                print(f"Generated problem: {problem}")
            elif variableAmount == 'two':
                difficulty = input("Choose difficulty (addition/subtraction(AS), multiplication/division(MD), exponents/roots(ER), mixed): ")
                problem = generate_two_variable_problem(difficulty)
                print(f"Generated problem: {problem}")
            elif variableAmount == 'q':
                print("Goodbye!")
                break
            else:
                    print("Invalid variable amount!")
        elif ProblemType == 'C':
            CalcType = input("Derivative(D) or Integral(I) problem: ")
            res = generate_Calc_problem(CalcType)
            if res:
                prob, sol = res
                print(f"Generated problem: {prob}")
                print(f"Solution (SymPy): {sol}")
                try:
                    print(f"Solution (LaTeX): {sp.latex(sol)}")
                except Exception:
                    pass
            else:
                print("Could not generate calculus problem.")
            

if __name__ == "__main__":
    main()
