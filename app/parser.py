"""Contains functions relating to parsing an expression."""
import re
import math
from app import operations


CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


class Parser:
    """Handles converting a string of numbers and operations into a float."""

    def __init__(self):
        self._last_result: float = 0

    def parse_and_eval(self, expression: str) -> float:
        """Evaluates math expression. Supports +, -, *, /, and ^.

        Args:
            expression: The initial expression string.

        Returns:
            The result of the evaluated expression.

        Raises:
            ValueError: If expression is invalid.
            ZeroDivisionError: If division by zero occurs.
        """
        tokens = _to_tokens(expression)
        tokens = _resolve_constants(tokens, self._last_result)
        tokens = _process_tokens(tokens)

        if len(tokens) != 1:
            raise ValueError("Invalid expression")
        self._last_result = float(tokens[0])
        return self._last_result


def _process_tokens(tokens: list[str]) -> list[str]:
    """Process tokens by handling brackets first, then operations.

    Args:
        tokens: List of tokens to process.

    Returns:
        Processed list of tokens.
    """
    tokens = _process_brackets(tokens)
    tokens = _process_ops(tokens, ["^"])
    tokens = _process_ops(tokens, ["*", "/"])
    tokens = _process_ops(tokens, ["+", "-"])
    return tokens


def _to_tokens(expression: str) -> list[str]:
    """Removes all spaces from the expression and splits into tokens.

    Returns a list of numbers and operators as strings.
    Example: "2 + -3 * 4" -> ["2", "+", "-3", "*", "4"]

    Args:
        expression: The initial expression string.

    Returns:
        A list of tokens as strings.

    Raises:
        IndexError: If a '-' is found alone at the beginning.
    """
    pattern = r"([\+\-\*/\^\(\)]|pi|tau|e|r)"
    tokens: list[str] = re.split(pattern, expression.replace(" ", ""))
    filt_tokens = []
    for token in tokens:
        if token:
            filt_tokens.append(token)

    # handle negative numbers by merging '-' with number on its right
    i = 0
    while i < len(filt_tokens) - 1:
        # If current token is an operator and next is "-"
        if (filt_tokens[i] in operations.OPERATIONS and
            filt_tokens[i + 1] == "-" and
            i + 2 < len(filt_tokens)):
            # Merge "-" with the number after it
            filt_tokens = (filt_tokens[:i + 1] +
                          [filt_tokens[i + 1] + filt_tokens[i + 2]] +
                          filt_tokens[i + 3:])
        i += 1

    if filt_tokens[0] == "-":
        filt_tokens = [filt_tokens[0] + filt_tokens[1]] + filt_tokens[2:]
    return filt_tokens


def _resolve_constants(tokens: list[str], last_result: float) -> list[str]:
    """Finds constants in their string form and swaps them with floats.

    Example: ["2", "*", "pi"] -> ["2", "*", "3.141592653589793"]

    Args:
        tokens: List of tokens to resolve constants for.
        last_result: The value used to replace all 'r' constants.

    Returns:
        A mutated version of tokens with no alphabet constants.
    """
    for i, token in enumerate(tokens):
        if token in CONSTANTS:
            tokens[i] = str(CONSTANTS[token])
        elif token == "r":
            tokens[i] = str(last_result)
    return tokens


def _process_ops(tokens: list[str], operators: list[str]) -> list[str]:
    """Process specific operators left-to-right.

    Example: list: ["2", "*", "3"], operators: ["*"] -> ["6"]

    Args:
        tokens: List of tokens that will shrink after evaluating operators.
        operators: List of operators as strings to be processed.

    Returns:
        Modified token list with specified operations evaluated.

    Raises:
        ValueError: If operands cannot be converted to float.
        ZeroDivisionError: If division by zero occurs.
    """
    i = 0
    while i < len(tokens):
        if tokens[i] in operators:
            op = operations.get_operation(tokens[i])
            left = float(tokens[i - 1])
            right = float(tokens[i + 1])
            result = op(left, right)
            tokens = tokens[:i - 1] + [str(result)] + tokens[i + 2:]
            i = 0
        else:
            i += 1
    return tokens


def _process_brackets(tokens: list[str]) -> list[str]:
    """Process brackets recursively with implicit multiplication.

    Example: ["4", "(", "2", "+", "3", ")"] -> ["4", "*", "5"]
             ["(", "2", "+", "3", ")"] -> ["5"]

    Args:
        tokens: List of tokens that may contain brackets.

    Returns:
        Modified token list with brackets evaluated.

    Raises:
        ValueError: If brackets are mismatched.
    """
    i = 0
    open_i = close_i = -1
    while i < len(tokens):
        # seek open bracket
        if tokens[i] == "(":
            open_i = i
            break
        i += 1

    if open_i == -1:
        # No opening bracket found, check for stray closing bracket
        for token in tokens:
            if token == ")":
                raise ValueError("Mismatched brackets")
        return tokens

    # Find matching closing bracket by going forward from open_i
    depth = 1
    i = open_i + 1
    while i < len(tokens):
        if tokens[i] == "(":
            depth += 1
        elif tokens[i] == ")":
            depth -= 1
            if depth == 0:
                close_i = i
                break
        i += 1

    if close_i == -1 or close_i < open_i:
        raise ValueError("Mismatched brackets")

    sub_tokens: list[str] = tokens[open_i + 1: close_i]
    sub_tokens = _process_tokens(sub_tokens)

    # Handle implicit multiplication: 4(...) becomes 4 * (...)
    if open_i > 0 and tokens[open_i - 1] not in operations.OPERATIONS:
        tokens = tokens[:open_i] + ["*"] + sub_tokens + tokens[close_i + 1:]
    else:
        # "(" is at start OR there's already an operator before it
        tokens = tokens[:open_i] + sub_tokens + tokens[close_i + 1:]

    # Recursively process remaining brackets
    return _process_brackets(tokens)
