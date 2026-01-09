"""Contains functions relating to parsing an expression."""

import re
import math
from app.models import operations

CONSTANTS = {"pi": math.pi,
            "e": math.e,
            "tau": math.tau}

class Parser():
    """Handles converting a string of numbers and operations into a float"""
    def __init__(self):
        self.last_result: float = 0

    def parse_and_eval(self, expression: str) -> float:
        """Evaluates math expression. Supports +, -, *, and /.
        
        Args:
            expression: the initial expression string
        
        Returns:
            The result of the evaluated expression
        
        Raises:
            ValueError: If expression is invalid
            ZeroDivisionError: Division by zero"""
        tokens = _to_tokens(expression)
        tokens = _resolve_constants(tokens, self.last_result)
        tokens = _process_ops(tokens, ["*", "/"])
        tokens = _process_ops(tokens, ["+", "-"])

        if len(tokens) != 1:
            raise ValueError("Invalid expression")

        self.last_result = float(tokens[0])
        return self.last_result

def _to_tokens(expression: str) -> list:
    """Removes all spaces from the expression and splits into tokens.

    Returns a list of numbers and operators as strings.
    Example: "2 + 3 * 4" -> ["2", "+", "3", "*", "4"]
    """
    expr_no_spaces = expression.replace(" ", "")
    pattern = r"([\+\-\*/]|pi|tau|e|r)"
    return [t for t in re.split(pattern, expr_no_spaces) if t]

def _resolve_constants(tokens: list, last_result: float) -> list:
    """Finds constants in their string form and swaps them with floats

    Example: ["2", "*", "pi"] -> ["2", "*", "3.141592653589793"]
    """
    for i, token in enumerate(tokens):
        if token in CONSTANTS:
            tokens[i] = CONSTANTS[token]
        elif token == "r":
            tokens[i] = last_result
    return tokens

def _process_ops(tokens: list, operators: list) -> list:
    """Process specific operators left-to-right"""
    i = 0
    while i < len(tokens):
        if tokens[i] in operators:
            op = operations.OperationFactory.create_operation(tokens[i])
            left = float(tokens[i - 1])
            right = float(tokens[i + 1])
            result = op.execute(left, right)
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i = 0
        else:
            i += 1
    return tokens

