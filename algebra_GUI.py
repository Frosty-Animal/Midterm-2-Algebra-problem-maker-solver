# Run python ./algebra_GUI.py with main.py & solver.py in same folder for program to work

import tkinter as tk
from tkinter import scrolledtext
from main import generate_one_variable_problem, generate_two_variable_problem, generate_Calc_problem
from solver import (
    solve_algebra,
    check_algebra_answer,
    check_calc_answer,
    algebra_steps,
    calc_steps,
)

# ==========================================================
# App state
# ==========================================================
num_variables = None          # 1 or 2
operation_type = None         # a/s, m/d, e/r, mixed
current_problem = None        # problem string shown to user
current_solution = None       # for calc problems
calc_kind = None              # derivative or integral 
solve_for_var = None          # x or y for 2-variable problems


# Map GUI button labels
DIFFICULTY_MAP = {
    "A/S": "addition/subtraction",
    "M/D": "multiplication/division",
    "E/S": "exponents/roots",
    "Mixed": "mixed",
}


# ---------- Navigation helper ----------
def show_frame(frame):
    """Hide all frames and show the selected one."""
    for f in FRAMES:
        f.pack_forget()
    frame.pack(expand=True)


# ---------- Selection functions ----------
def choose_variables(n: int):
    """User chooses 1 or 2 variables."""
    global num_variables, operation_type, current_problem
    num_variables = n
    operation_type = None
    current_problem = None

    entry_box.delete(0, tk.END)
    result_label.config(text="", fg="black")
    problem_value_label.config(text="(pick an operation to generate a problem)")
    show_frame(op_frame)


def choose_operation(op: str):
    """User chooses an operation type; generate + display a problem."""
    global operation_type, current_problem

    operation_type = op
    difficulty = DIFFICULTY_MAP.get(op)

    if num_variables == 1:
        current_problem = generate_one_variable_problem(difficulty)
    elif num_variables == 2:
        current_problem = generate_two_variable_problem(difficulty)
    else:
        current_problem = None

    if current_problem:
        problem_value_label.config(text=current_problem)
    else:
        problem_value_label.config(text="(couldn't generate a problem — try again)")

    entry_box.delete(0, tk.END)
    result_label.config(text="", fg="black")

    # Show / hide the "Solve for x / y" selector
    if num_variables == 2:
        solve_for_selector.pack(pady=(0, 6))
        solve_for_strvar.set("x")       # default to x
    else:
        solve_for_selector.pack_forget()

    show_frame(input_frame)


def choose_type(kind: str):
    # user chooses algebra or calc
    global operation_type
    operation_type = kind
    entry_box.delete(0, tk.END)
    result_label.config(text="", fg="black")
    problem_value_label.config(text="(pick an operation to generate a problem)")
    if kind == "Algebra":
        show_frame(var_frame)
    else:
        show_frame(calc_frame)


def choose_calc(kind: str):
    # user chooses derivative or integral
    global current_problem, current_solution, calc_kind, operation_type
    calc_kind = kind
    operation_type = "Calculus"
    arg = 'D' if kind == 'Derivative' else 'I'
    res = generate_Calc_problem(arg)
    if res:
        prob, sol = res
        current_problem = prob
        current_solution = sol
        problem_value_label.config(text=current_problem)
    else:
        problem_value_label.config(text="(couldn't generate a problem — try again)")
    entry_box.delete(0, tk.END)
    result_label.config(text="", fg="black")
    solve_for_selector.pack_forget()      # not needed for calculus
    show_frame(input_frame)


# ---------- Check answer ----------
def get_entry_value():
    # check answer & get feedback
    user_input = entry_box.get().strip()
    if not user_input:
        result_label.config(text="Please enter an answer.", fg="#b8860b")
        return

    if operation_type == "Calculus":
        if current_solution is None:
            result_label.config(text="No solution to check against.", fg="red")
            return
        is_correct, msg = check_calc_answer(user_input, current_solution)
    else:
        if current_problem is None:
            result_label.config(text="No problem loaded.", fg="red")
            return
        # for 2-variable problems, pass the chosen target variable
        target = solve_for_strvar.get() if (num_variables or 0) == 2 else None
        is_correct, msg = check_algebra_answer(
            current_problem, user_input, num_variables or 1, solve_for=target
        )

    if is_correct is True:
        result_label.config(text=msg, fg="green")
    elif is_correct is False:
        result_label.config(text=msg, fg="red")
    else:
        result_label.config(text=msg, fg="#b8860b")


# ---------- Show answer / steps ----------
def show_answer():
    """Display the step-by-step solution in the solution frame."""
    if current_problem is None:
        return

    if operation_type == "Calculus":
        if current_solution is None:
            return
        text = calc_steps(current_problem, current_solution, calc_kind or "Derivative")
    else:
        target = solve_for_strvar.get() if (num_variables or 0) == 2 else None
        text = algebra_steps(current_problem, num_variables or 1, solve_for=target)

    # also show the problem at the top of the solution frame
    solution_problem_label.config(text=current_problem)

    solution_text.config(state=tk.NORMAL)
    solution_text.delete("1.0", tk.END)
    solution_text.insert(tk.END, text)
    solution_text.config(state=tk.DISABLED)

    show_frame(solution_frame)


# ---------- New problem (same settings) ----------
def new_problem():
    """Generate another problem with the same settings."""
    if operation_type is None:
        return
    if operation_type == "Calculus":
        if calc_kind:
            choose_calc(calc_kind)
    else:
        choose_operation(operation_type)


# ---------- Reset ----------
def reset_app():
    global num_variables, operation_type, current_problem, current_solution, calc_kind
    num_variables = None
    operation_type = None
    current_problem = None
    current_solution = None
    calc_kind = None

    entry_box.delete(0, tk.END)
    result_label.config(text="", fg="black")
    problem_value_label.config(text="")
    solve_for_selector.pack_forget()
    solve_for_strvar.set("x")
    show_frame(type_frame)


# ==========================================================
# Main window
# ==========================================================
root = tk.Tk()
root.title("Math Problem Generator")
root.geometry("640x520")
root.resizable(False, False)


# ==========================================================
# Frame — Choose Algebra or Calculus
# ==========================================================
type_frame = tk.Frame(root)

tk.Label(type_frame, text="Choose problem type", font=("Arial", 14)).pack(pady=20)
tk.Button(type_frame, text="Algebra", width=20, command=lambda: choose_type("Algebra")).pack(pady=5)
tk.Button(type_frame, text="Calculus", width=20, command=lambda: choose_type("Calculus")).pack(pady=5)
tk.Button(type_frame, text="Quit", width=20, command=root.destroy).pack(pady=15)


# ==========================================================
# Frame — Choose number of variables
# ==========================================================
var_frame = tk.Frame(root)

tk.Label(var_frame, text="Choose number of variables", font=("Arial", 14)).pack(pady=20)
tk.Button(var_frame, text="1 Variable", width=20, command=lambda: choose_variables(1)).pack(pady=5)
tk.Button(var_frame, text="2 Variables", width=20, command=lambda: choose_variables(2)).pack(pady=5)
tk.Button(var_frame, text="Back", width=20, command=lambda: show_frame(type_frame)).pack(pady=15)


# ==========================================================
# Frame — Choose operation type
# ==========================================================
op_frame = tk.Frame(root)

tk.Label(op_frame, text="Choose operation type", font=("Arial", 14)).pack(pady=20)
tk.Button(op_frame, text="Addition / Subtraction", width=24, command=lambda: choose_operation("A/S")).pack(pady=5)
tk.Button(op_frame, text="Multiplication / Division", width=24, command=lambda: choose_operation("M/D")).pack(pady=5)
tk.Button(op_frame, text="Exponents / Square Root", width=24, command=lambda: choose_operation("E/S")).pack(pady=5)
tk.Button(op_frame, text="Mixed", width=24, command=lambda: choose_operation("Mixed")).pack(pady=5)
tk.Button(op_frame, text="Back", width=24, command=lambda: show_frame(var_frame)).pack(pady=15)


# ==========================================================
# Frame — Derivative or Integral
# ==========================================================
calc_frame = tk.Frame(root)

tk.Label(calc_frame, text="Choose calculus type", font=("Arial", 14)).pack(pady=20)
tk.Button(calc_frame, text="Derivative", width=20, command=lambda: choose_calc("Derivative")).pack(pady=5)
tk.Button(calc_frame, text="Integral", width=20, command=lambda: choose_calc("Integral")).pack(pady=5)
tk.Button(calc_frame, text="Back", width=20, command=lambda: show_frame(type_frame)).pack(pady=15)


# ==========================================================
# Frame — Show problem + input answer
# ==========================================================
input_frame = tk.Frame(root)

tk.Label(input_frame, text="Solve this problem:", font=("Arial", 14)).pack(pady=(20, 8))

problem_value_label = tk.Label(
    input_frame,
    text="(pick an operation to generate a problem)",
    font=("Arial", 16),
    wraplength=600,
    justify="center",
)
problem_value_label.pack(pady=(0, 15))

# "Solve for x / y" selector for 2 var problems
solve_for_strvar = tk.StringVar(value="x")
solve_for_selector = tk.Frame(input_frame)
tk.Label(solve_for_selector, text="Solve for:", font=("Arial", 11)).pack(side="left", padx=(0, 8))
tk.Radiobutton(solve_for_selector, text="x", variable=solve_for_strvar,
               value="x", font=("Arial", 11)).pack(side="left", padx=4)
tk.Radiobutton(solve_for_selector, text="y", variable=solve_for_strvar,
               value="y", font=("Arial", 11)).pack(side="left", padx=4)
# starts hidden, choose_operation packs it when num_variables == 2

tk.Label(input_frame, text="Enter your answer:", font=("Arial", 12)).pack()
entry_box = tk.Entry(input_frame, width=35, font=("Arial", 12))
entry_box.pack(pady=8)

# feedback label (correct / incorrect)
result_label = tk.Label(input_frame, text="", font=("Arial", 12), wraplength=560, justify="center")
result_label.pack(pady=(0, 8))

# --- button row 1: Submit / Show Answer ---
btn_row1 = tk.Frame(input_frame)
btn_row1.pack(pady=4)

tk.Button(btn_row1, text="Submit", command=get_entry_value, width=12).pack(side="left", padx=6)
tk.Button(btn_row1, text="Show Answer", command=show_answer, width=12).pack(side="left", padx=6)

# --- button row 2: New Problem / Change Type / Reset ---
btn_row2 = tk.Frame(input_frame)
btn_row2.pack(pady=4)

tk.Button(btn_row2, text="New Problem", command=new_problem, width=12).pack(side="left", padx=6)
tk.Button(
    btn_row2,
    text="Change Type",
    command=lambda: show_frame(calc_frame) if operation_type == "Calculus" else show_frame(op_frame),
    width=12,
).pack(side="left", padx=6)
tk.Button(btn_row2, text="Reset", command=reset_app, width=12).pack(side="left", padx=6)


# ==========================================================
# Frame — Step-by-step solution display
# ==========================================================
solution_frame = tk.Frame(root)

tk.Label(solution_frame, text="Step-by-Step Solution", font=("Arial", 14, "bold")).pack(pady=(15, 5))

solution_problem_label = tk.Label(
    solution_frame, text="", font=("Arial", 13), wraplength=600, justify="center",
)
solution_problem_label.pack(pady=(0, 8))

solution_text = scrolledtext.ScrolledText(
    solution_frame, width=62, height=14, font=("Courier", 11),
    wrap=tk.WORD, state=tk.DISABLED, bg="#f9f9f9",
)
solution_text.pack(padx=15, pady=(0, 10))

# --- post-solution buttons ---
sol_btn_row = tk.Frame(solution_frame)
sol_btn_row.pack(pady=8)

tk.Button(sol_btn_row, text="New Problem", command=new_problem, width=14).pack(side="left", padx=8)
tk.Button(sol_btn_row, text="Reset", command=reset_app, width=14).pack(side="left", padx=8)


# ---------- Start on the type selection screen ----------
FRAMES = [type_frame, var_frame, op_frame, calc_frame, input_frame, solution_frame]
show_frame(type_frame)
root.mainloop()
