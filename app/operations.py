"""Basic calculator operations using simple functions."""

from collections.abc import Callable

def add(a: float, b: float) -> float:
    """Return sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return quotient of a divided by b."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}


def get_operation(operator: str) -> Callable[[float, float], float]:
    """Get operation function for operator symbol.

    Args:
        operator: The operator symbol ('+', '-', '*', '/').

    Returns:
        The corresponding operation function.

    Raises:
        ValueError: If operator is not recognized.
    """
    if operator not in OPERATIONS:
        raise ValueError(f"Unknown operator: {operator}")
    return OPERATIONS[operator]
