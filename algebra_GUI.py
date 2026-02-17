import tkinter as tk
from main import generate_one_variable_problem, generate_two_variable_problem

# ==========================================================
# App state
# ==========================================================
num_variables = None          # 1 or 2
operation_type = None         # "A/S", "M/D", "E/S", "Mixed"
current_problem = None        # problem string shown to user


# Map GUI button labels -> difficulty strings expected by main.py
DIFFICULTY_MAP = {
    "A/S": "addition/subtraction",
    "M/D": "multiplication/division",
    "E/S": "exponents/roots",
    "Mixed": "mixed",
}


# ---------- Navigation helper ----------
def show_frame(frame):
    """Hide all frames and show the selected one."""
    for f in (var_frame, op_frame, input_frame):
        f.pack_forget()
    frame.pack(expand=True)


# ---------- Selection functions ----------
def choose_variables(n: int):
    """User chooses 1 or 2 variables."""
    global num_variables, operation_type, current_problem
    num_variables = n
    operation_type = None
    current_problem = None

    # Clear any prior answer/problem display
    entry_box.delete(0, tk.END)
    problem_value_label.config(text="(pick an operation to generate a problem)")
    show_frame(op_frame)


def choose_operation(op: str):
    """User chooses an operation type; generate + display a problem."""
    global operation_type, current_problem

    operation_type = op
    difficulty = DIFFICULTY_MAP.get(op)

    # Generate the problem using the correct function from main.py
    if num_variables == 1:
        current_problem = generate_one_variable_problem(difficulty)
    elif num_variables == 2:
        current_problem = generate_two_variable_problem(difficulty)
    else:
        current_problem = None

    # Display it (fallback message if generation failed)
    if current_problem:
        problem_value_label.config(text=current_problem)
    else:
        problem_value_label.config(text="(couldn't generate a problem — try again)")

    # Clear answer box each time we generate a new problem
    entry_box.delete(0, tk.END)
    show_frame(input_frame)


def get_entry_value():
    user_input = entry_box.get().strip()
    print("Problem:", current_problem)
    print("User entered:", user_input)
    print("Variables:", num_variables)
    print("Operation:", operation_type)


def new_problem():
    """Generate another problem with the same settings."""
    if operation_type is None:
        return
    choose_operation(operation_type)


# ---------- Reset function ----------
def reset_app():
    global num_variables, operation_type, current_problem
    num_variables = None
    operation_type = None
    current_problem = None

    entry_box.delete(0, tk.END)
    problem_value_label.config(text="")
    show_frame(var_frame)


# ==========================================================
# Main window
# ==========================================================
root = tk.Tk()
root.title("Algebra Generator")
root.geometry("600x450")


# ==========================================================
# Frame 1 — Choose number of variables
# ==========================================================
var_frame = tk.Frame(root)

tk.Label(var_frame, text="Choose number of variables", font=("Arial", 14)).pack(pady=20)

tk.Button(var_frame, text="1 Variable", command=lambda: choose_variables(1)).pack(pady=5)
tk.Button(var_frame, text="2 Variables", command=lambda: choose_variables(2)).pack(pady=5)


# ==========================================================
# Frame 2 — Choose operation type
# ==========================================================
op_frame = tk.Frame(root)

tk.Label(op_frame, text="Choose operation type", font=("Arial", 14)).pack(pady=20)

tk.Button(op_frame, text="Addition/Subtraction", command=lambda: choose_operation("A/S")).pack(pady=5)
tk.Button(op_frame, text="Multiplication/Division", command=lambda: choose_operation("M/D")).pack(pady=5)
tk.Button(op_frame, text="Exponents/Square Root", command=lambda: choose_operation("E/S")).pack(pady=5)
tk.Button(op_frame, text="Mixed", command=lambda: choose_operation("Mixed")).pack(pady=5)

tk.Button(op_frame, text="Back", command=lambda: show_frame(var_frame)).pack(pady=15)


# ==========================================================
# Frame 3 — Show problem + input answer
# ==========================================================
input_frame = tk.Frame(root)

tk.Label(input_frame, text="Solve this problem:", font=("Arial", 14)).pack(pady=(20, 8))

problem_value_label = tk.Label(
    input_frame,
    text="(pick an operation to generate a problem)",
    font=("Arial", 16),
    wraplength=560,
    justify="center",
)
problem_value_label.pack(pady=(0, 20))

tk.Label(input_frame, text="Enter your answer:", font=("Arial", 12)).pack()

entry_box = tk.Entry(input_frame, width=35, font=("Arial", 12))
entry_box.pack(pady=10)

button_row = tk.Frame(input_frame)
button_row.pack(pady=10)

tk.Button(button_row, text="Submit", command=get_entry_value, width=10).pack(side="left", padx=6)
tk.Button(button_row, text="New Problem", command=new_problem, width=12).pack(side="left", padx=6)
tk.Button(button_row, text="Change Type", command=lambda: show_frame(op_frame), width=12).pack(side="left", padx=6)

tk.Button(input_frame, text="Reset", command=reset_app).pack(pady=(10, 0))


# ---------- Start on first screen ----------
show_frame(var_frame)
root.mainloop()
