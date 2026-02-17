try:
    import sympy as sp
except ImportError:
    print("SymPy is not installed. Install with:\n  py -m pip install sympy\nor\n  python -m pip install sympy")
    raise SystemExit(1)

import random

x = sp.symbols('x')

def gen_expr(depth=0):
    if depth >= 2 or random.random() < 0.5:
        base = random.choice(['const','poly','sin','cos','exp','log'])
        if base == 'const':
            return sp.Integer(random.randint(1, 9))
        if base == 'poly':
            a = random.randint(1, 5)
            p = random.randint(0, 4)
            return a * x**p
        if base == 'sin':
            return sp.sin(gen_expr(depth+1))
        if base == 'cos':
            return sp.cos(gen_expr(depth+1))
        if base == 'exp':
            return sp.exp(gen_expr(depth+1))
        if base == 'log':
            inner = gen_expr(depth+1)
            return sp.log(sp.Abs(inner)) if inner.has(x) else sp.log(inner + 1)

    op = random.choice(['add','mul','pow'])
    if op == 'add':
        return gen_expr(depth+1) + gen_expr(depth+1)
    if op == 'mul':
        return gen_expr(depth+1) * gen_expr(depth+1)
    if op == 'pow':
        base = gen_expr(depth+1)
        exp = random.randint(1, 3)
        return base**exp


def make_problem():
    expr = sp.simplify(gen_expr())
    deriv = sp.diff(expr, x)
    return expr, sp.simplify(deriv)


def main():
    expr, deriv = make_problem()
    print("Differentiate the following with respect to x:\n")
    print(sp.pretty(expr))
    print("\nAnswer:\n")
    print(sp.pretty(deriv))
    print("\nLaTeX (problem):")
    print(sp.latex(expr))
    print("\nLaTeX (answer):")
    print(sp.latex(deriv))

if __name__ == '__main__':
    main()
