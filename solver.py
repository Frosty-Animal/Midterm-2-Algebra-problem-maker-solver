# Requires: sympy
# Install (if needed): pip install sympy

# Import SymPy so we can do symbolic algebra
import sympy as sp

# This tells Python that the main program should only import "solve"
__all__ = ["solve"]

#   Look through the equation string and collect all letters.
def find_variables(equation_str):

    # Create an empty list to store variables
    variables = []

    # Loop through every character in the string
    for char in equation_str:

        # isalpha() checks if the character is a letter
        if char.isalpha():

            # Only add it if we have not already seen it
            if char not in variables:
                variables.append(char)

    # Return the list of variables
    return variables