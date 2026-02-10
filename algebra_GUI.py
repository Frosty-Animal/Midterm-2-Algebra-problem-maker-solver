import tkinter as tk

# ---------- Navigation helper ----------
def show_frame(frame):
    """Hide all frames and show the selected one."""
    for f in (var_frame, op_frame, input_frame):
        f.pack_forget()
    frame.pack(expand=True)


# ---------- Stored selections ----------
num_variables = None
operation_type = None


# ---------- Selection functions ----------
def choose_variables(n):
    global num_variables
    num_variables = n
    print(f"Variables chosen: {n}")

    show_frame(op_frame)


def choose_operation(op):
    global operation_type
    operation_type = op
    print(f"Operation chosen: {op}")

    show_frame(input_frame)


def get_entry_value():
    user_input = entry_box.get()
    print("User entered:", user_input)
    print("Variables:", num_variables)
    print("Operation:", operation_type)


# ---------- Reset function ----------
def reset_app():
    global num_variables, operation_type

    # Clear stored selections
    num_variables = None
    operation_type = None

    # Clear textbox
    entry_box.delete(0, tk.END)

    # Return to first screen
    show_frame(var_frame)


# ---------- Main window ----------
root = tk.Tk()
root.title("Algebra Generator")
root.geometry("500x400")


# ==========================================================
# Frame 1 — Choose number of variables
# ==========================================================
var_frame = tk.Frame(root)

tk.Label(var_frame, text="Choose number of variables",
         font=("Arial", 14)).pack(pady=20)

tk.Button(var_frame, text="1 Variable",
          command=lambda: choose_variables(1)).pack(pady=5)

tk.Button(var_frame, text="2 Variables",
          command=lambda: choose_variables(2)).pack(pady=5)


# ==========================================================
# Frame 2 — Choose operation type
# ==========================================================
op_frame = tk.Frame(root)

tk.Label(op_frame, text="Choose operation type",
         font=("Arial", 14)).pack(pady=20)

tk.Button(op_frame, text="Addition/Subtraction",
          command=lambda: choose_operation("A/S")).pack(pady=5)

tk.Button(op_frame, text="Multiplication/Division",
          command=lambda: choose_operation("M/D")).pack(pady=5)

tk.Button(op_frame, text="Exponents/Square Root",
          command=lambda: choose_operation("E/S")).pack(pady=5)

tk.Button(op_frame, text="Mixed",
          command=lambda: choose_operation("Mixed")).pack(pady=5)

# ==========================================================
# Frame 3 — Input answer
# ==========================================================
input_frame = tk.Frame(root)

tk.Label(input_frame, text="Enter your answer:",
         font=("Arial", 14)).pack(pady=20)

entry_box = tk.Entry(input_frame, width=30)
entry_box.pack(pady=10)

tk.Button(input_frame, text="Submit",
          command=get_entry_value).pack(pady=5)

tk.Button(input_frame, text="Reset",
          command=reset_app).pack(pady=10)


# ---------- Start on first screen ----------
show_frame(var_frame)

root.mainloop()
