# solver.py  –  parse, solve, check, and explain algebra / calculus problems
# Requires: sympy          pip install sympy

import re
import sympy as sp

__all__ = [
    "find_variables",
    "solve_algebra",
    "check_algebra_answer",
    "check_calc_answer",
    "algebra_steps",
    "calc_steps",
]


# ── helpers ──────────────────────────────────────────────────────────────

def find_variables(equation_str: str) -> list[str]:
    """Return every unique single-letter variable found in *equation_str*."""
    seen: list[str] = []
    for ch in equation_str:
        if ch.isalpha() and ch not in seen:
            seen.append(ch)
    return seen


def _preprocess(eq_str: str) -> str:
    """Convert the custom notation produced by main.py into a string that
    ``sympy.sympify`` can parse.

    Transformations
    ---------------
    √N        →  sqrt(N)
    ^          →  **
    3x  / 5y  →  3*x / 5*y      (implicit multiplication)
    )x  / )3  →  )*x / )*3
    """
    s = eq_str.strip()

    # 1.  √<digits>  →  sqrt(<digits>)
    s = re.sub(r"√(\d+)", r"sqrt(\1)", s)

    # 2.  ^  →  **
    s = s.replace("^", "**")

    # 3.  Implicit multiplication: digit immediately before a letter
    s = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", s)

    # 4.  Closing paren immediately before letter or digit  →  insert *
    s = re.sub(r"\)([a-zA-Z0-9])", r")*\1", s)

    # 5.  Fix any accidentally broken 'sqrt' from step 3
    #     (shouldn't happen because sqrt starts with a letter, but safety net)
    for bad in ("s*q*r*t", "s*qrt", "sq*rt", "sqr*t"):
        s = s.replace(bad, "sqrt")

    return s


def _parse_equation(problem_str: str):
    """Parse an equation string into a SymPy Eq and a list of Symbol objects.

    Returns ``(equation, symbol_list)`` or ``(None, [])`` on failure.
    """
    if "=" not in problem_str:
        return None, []

    lhs_raw, rhs_raw = problem_str.split("=", 1)
    lhs_s = _preprocess(lhs_raw)
    rhs_s = _preprocess(rhs_raw)

    var_names = find_variables(problem_str)
    symbols = {v: sp.Symbol(v) for v in var_names}
    local_dict = {**symbols, "sqrt": sp.sqrt}

    try:
        lhs = sp.sympify(lhs_s, locals=local_dict)
        rhs = sp.sympify(rhs_s, locals=local_dict)
    except Exception:
        return None, []

    return sp.Eq(lhs, rhs), [symbols[v] for v in var_names]


# ── algebra solving ──────────────────────────────────────────────────────

def solve_algebra(problem_str: str, solve_for: str | None = None):
    """Solve an algebra equation.

    Parameters
    ----------
    problem_str : str               – the equation string
    solve_for   : str | None        – e.g. "x" or "y"; when given the solver
                                      isolates that specific variable.

    Returns a list of solution dicts, e.g. ``[{x: 3}]`` or
    ``[{x: 5 - y}]``.  Returns ``[]`` on failure.
    """
    eq, syms = _parse_equation(problem_str)
    if eq is None:
        return []
    try:
        if solve_for:
            target = sp.Symbol(solve_for)
            sols = sp.solve(eq, target, dict=True)
        else:
            sols = sp.solve(eq, syms, dict=True)
        return sols if sols else []
    except Exception:
        return []


# ── answer checking ──────────────────────────────────────────────────────

def check_algebra_answer(problem_str: str, user_input: str, num_variables: int,
                         solve_for: str | None = None):
    """Check the user's answer for an algebra problem.

    Parameters
    ----------
    problem_str   : str        – the equation shown to the user
    user_input    : str        – what the user typed
    num_variables : int        – 1 or 2
    solve_for     : str | None – target variable for 2-variable problems ("x" or "y")

    Returns
    -------
    (is_correct: bool | None, message: str)
        *is_correct* is ``True`` / ``False``, or ``None`` if we can't decide.
    """
    if not user_input.strip():
        return None, "Please enter an answer."

    solutions = solve_algebra(problem_str, solve_for=solve_for)
    if not solutions:
        return None, "Sorry – the solver couldn't find a solution for this problem."

    # Build a readable solution string for feedback
    sol_strs = []
    for sol_dict in solutions:
        parts = [f"{v} = {expr}" for v, expr in sol_dict.items()]
        sol_strs.append(", ".join(parts))
    correct_display = "  or  ".join(sol_strs)

    # ── one-variable problems ────────────────────────────────────────
    if num_variables == 1:
        # Expect a numeric value (or simple expression).
        # Collect all numeric solution values across solution dicts.
        correct_values: list[sp.Expr] = []
        for sol_dict in solutions:
            for expr in sol_dict.values():
                correct_values.append(sp.nsimplify(expr))

        # Parse user input – they might give comma-separated answers
        user_parts = re.split(r"[,;]", user_input)
        user_values: list[sp.Expr] = []
        for part in user_parts:
            part = part.strip()
            # strip optional "x =" prefix
            part = re.sub(r"^[a-zA-Z]\s*=\s*", "", part)
            part = _preprocess(part)
            try:
                user_values.append(sp.nsimplify(sp.sympify(part)))
            except Exception:
                return False, f"Couldn't parse your answer \"{part}\".\nCorrect answer: {correct_display}"

        # Check: does the set of user values match the set of correct values?
        matched_all = True
        for uv in user_values:
            if not any(sp.simplify(uv - cv) == 0 for cv in correct_values):
                matched_all = False
                break

        if matched_all and len(user_values) == len(correct_values):
            return True, "Correct! ✓"
        elif matched_all and len(user_values) < len(correct_values):
            return False, (
                f"Partially correct – you found {len(user_values)} of "
                f"{len(correct_values)} solutions.\n"
                f"Full answer: {correct_display}"
            )
        else:
            return False, f"Not quite.\nCorrect answer: {correct_display}"

    # ── two-variable problems ────────────────────────────────────────
    else:
        # The solution is one variable in terms of the other.
        eq, syms = _parse_equation(problem_str)
        if eq is None:
            return None, "Couldn't parse the problem."

        target = sp.Symbol(solve_for) if solve_for else None

        user_clean = user_input.strip()
        # Check if user wrote e.g. "x = 3 - y"
        m = re.match(r"([a-zA-Z])\s*=\s*(.+)", user_clean)
        if m:
            var_name, expr_str = m.group(1), m.group(2)
            var_sym = sp.Symbol(var_name)
        elif target:
            # User typed just the expression — assume they're solving for the target
            var_sym = target
            expr_str = user_clean
        else:
            return None, (
                f"Tip: enter your answer as  x = <expression>  or  y = <expression>.\n"
                f"Correct answer: {correct_display}"
            )

        expr_str = _preprocess(expr_str)
        local_dict = {str(s): s for s in syms}
        local_dict["sqrt"] = sp.sqrt
        try:
            user_expr = sp.sympify(expr_str, locals=local_dict)
        except Exception:
            return False, f"Couldn't parse your expression.\nCorrect answer: {correct_display}"

        # Check against each solution
        for sol_dict in solutions:
            if var_sym in sol_dict:
                if sp.simplify(user_expr - sol_dict[var_sym]) == 0:
                    return True, "Correct! ✓"
        return False, f"Not quite.\nCorrect answer: {correct_display}"


def check_calc_answer(user_input: str, correct_solution: sp.Expr):
    """Check the user's answer for a calculus problem.

    Returns ``(is_correct: bool | None, message: str)``.
    """
    if not user_input.strip():
        return None, "Please enter an answer."

    x = sp.Symbol("x")
    user_clean = _preprocess(user_input.strip())
    local_dict = {"x": x, "sqrt": sp.sqrt,
                  "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
                  "exp": sp.exp, "log": sp.log, "ln": sp.log,
                  "e": sp.E, "pi": sp.pi}
    try:
        user_expr = sp.sympify(user_clean, locals=local_dict)
    except Exception:
        return None, f"Couldn't parse your answer."

    diff = sp.simplify(sp.expand(user_expr) - sp.expand(correct_solution))
    if diff == 0:
        return True, "Correct! ✓"

    # For integrals the answers can differ by a constant – check derivative
    if sp.simplify(sp.diff(user_expr - correct_solution, x)) == 0:
        return True, "Correct (equivalent up to a constant)! ✓"

    pretty_sol = sp.pretty(correct_solution, use_unicode=True)
    return False, f"Not quite.\nCorrect answer: {pretty_sol}"


# ── step-by-step explanations ────────────────────────────────────────────

def algebra_steps(problem_str: str, num_variables: int,
                  solve_for: str | None = None) -> str:
    """Return a human-readable, step-by-step solution for an algebra problem.

    Parameters
    ----------
    solve_for : str | None – for 2-variable problems, which variable to isolate
    """
    eq, syms = _parse_equation(problem_str)
    if eq is None:
        return "Could not parse the equation."

    solutions = solve_algebra(problem_str, solve_for=solve_for)
    if not solutions:
        return "The solver could not find a solution."

    # Determine the target symbol for labeling
    target = sp.Symbol(solve_for) if solve_for else None

    lines: list[str] = []
    lines.append("─" * 48)
    lines.append("STEP-BY-STEP SOLUTION")
    lines.append("─" * 48)

    # Step 1 – restate
    lines.append("")
    lines.append(f"Step 1 ▸ Original equation")
    lines.append(f"   {problem_str}")
    if target:
        lines.append(f"   (Solving for {solve_for})")

    # Step 2 – rewrite: move everything to LHS = 0
    lhs_minus_rhs = sp.expand(eq.lhs - eq.rhs)
    lines.append("")
    lines.append(f"Step 2 ▸ Move everything to one side")
    lines.append(f"   {lhs_minus_rhs} = 0")

    # Step 3 – factor / collect if helpful
    factored = sp.factor(lhs_minus_rhs)
    if factored != lhs_minus_rhs:
        lines.append("")
        lines.append(f"Step 3 ▸ Factor / simplify")
        lines.append(f"   {factored} = 0")
        step_num = 4
    else:
        collected = lhs_minus_rhs
        for s in syms:
            collected = sp.collect(collected, s)
        if collected != lhs_minus_rhs:
            lines.append("")
            lines.append(f"Step 3 ▸ Collect like terms")
            lines.append(f"   {collected} = 0")
            step_num = 4
        else:
            step_num = 3

    # Step N – solve for each variable
    for sol_dict in solutions:
        for var, expr in sol_dict.items():
            lines.append("")
            lines.append(f"Step {step_num} ▸ Solve for {var}")

            # Show isolation reasoning based on equation structure
            # Get coefficients if linear in this variable
            try:
                coeff = lhs_minus_rhs.coeff(var, 1)
                const = lhs_minus_rhs.subs(var, 0)
                if coeff != 0 and sp.degree(lhs_minus_rhs, var) == 1:
                    lines.append(f"   Isolate {var}:")
                    lines.append(f"     {coeff}·{var} = {sp.simplify(-const)}")
                    if coeff != 1:
                        lines.append(f"     {var} = {sp.simplify(-const)} / {coeff}")
            except Exception:
                pass

            simplified = sp.nsimplify(expr)
            lines.append(f"   ➜  {var} = {simplified}")
            step_num += 1

    # If multiple solution sets, list them
    if len(solutions) > 1:
        lines.append("")
        lines.append(f"Note: there are {len(solutions)} solution(s).")

    lines.append("")
    lines.append("─" * 48)
    return "\n".join(lines)


def calc_steps(problem_str: str, solution: sp.Expr, calc_kind: str) -> str:
    """Return a step-by-step explanation for a calculus problem.

    Parameters
    ----------
    problem_str : str        – e.g. "Differentiate: 3*x**2 + sin(x)"
    solution    : sp.Expr    – the correct SymPy result
    calc_kind   : str        – "Derivative" or "Integral"
    """
    x = sp.Symbol("x")

    # Extract the expression from the problem string
    for prefix in ("Differentiate:", "Integrate:"):
        if problem_str.startswith(prefix):
            expr_str = problem_str[len(prefix):].strip()
            break
    else:
        expr_str = problem_str

    local_dict = {"x": x, "sqrt": sp.sqrt,
                  "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
                  "exp": sp.exp, "log": sp.log, "e": sp.E, "pi": sp.pi}
    try:
        expr = sp.sympify(expr_str, locals=local_dict)
    except Exception:
        expr = None

    lines: list[str] = []
    lines.append("─" * 48)
    lines.append("STEP-BY-STEP SOLUTION")
    lines.append("─" * 48)

    # Step 1 – restate
    op_word = "differentiate" if calc_kind == "Derivative" else "integrate"
    lines.append("")
    lines.append(f"Step 1 ▸ We need to {op_word}:")
    lines.append(f"   f(x) = {expr_str}")

    if expr is None:
        lines.append("")
        lines.append(f"Final answer: {sp.pretty(solution, use_unicode=True)}")
        lines.append("─" * 48)
        return "\n".join(lines)

    # Step 2 – break into terms
    terms = sp.Add.make_args(sp.expand(expr))
    if len(terms) > 1:
        lines.append("")
        lines.append(f"Step 2 ▸ Apply {op_word[:-1]}ion term by term")
        lines.append(f"   The expression has {len(terms)} term(s):")
        for i, t in enumerate(terms, 1):
            lines.append(f"     Term {i}: {t}")

    # Step 3 – show rule applied to each term
    step_num = 3
    results = []
    for t in terms:
        if calc_kind == "Derivative":
            result = sp.diff(t, x)
        else:
            result = sp.integrate(t, x)

        rule = _identify_rule(t, x, calc_kind)
        lines.append("")
        lines.append(f"Step {step_num} ▸ {rule}")
        lines.append(f"   {t}  →  {result}")
        results.append(result)
        step_num += 1

    # Step N – combine
    lines.append("")
    lines.append(f"Step {step_num} ▸ Combine results")
    combined = sum(results)
    simplified = sp.simplify(combined)
    lines.append(f"   = {simplified}")

    if calc_kind == "Integral":
        lines.append(f"   = {simplified} + C")

    lines.append("")
    lines.append("─" * 48)
    return "\n".join(lines)


def _identify_rule(term: sp.Expr, x: sp.Symbol, calc_kind: str) -> str:
    """Return a short description of which rule applies to *term*."""
    action = "Differentiate" if calc_kind == "Derivative" else "Integrate"

    # Constant (no x)
    if x not in term.free_symbols:
        if calc_kind == "Derivative":
            return f"{action} constant → 0"
        return f"{action} constant → multiply by x"

    # Pure power of x:  a * x**n
    if term.is_Mul or term.is_Pow or term == x:
        base_terms = sp.Mul.make_args(term)
        powers = [b for b in base_terms if x in b.free_symbols]
        if len(powers) == 1 and powers[0].is_Pow and powers[0].base == x:
            n = powers[0].exp
            return f"Power rule on x**{n}"
        if len(powers) == 1 and powers[0] == x:
            return f"Power rule on x  (n = 1)"

    # Trig
    if term.has(sp.sin):
        return f"{action} sin term"
    if term.has(sp.cos):
        return f"{action} cos term"
    if term.has(sp.tan):
        return f"{action} tan term"

    # Exponential
    if term.has(sp.exp):
        return f"{action} exponential term  (d/dx e^(kx) = k·e^(kx))"

    # Logarithm
    if term.has(sp.log):
        return f"{action} logarithm term  (d/dx ln(x) = 1/x)"

    return f"{action} this term"
