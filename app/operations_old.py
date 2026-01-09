"""Basic calculator operations"""

import abc

class Operation(abc.ABC):
    """Abstract base class for calculator operations."""

    @abc.abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Execute the operation on two operands.
        
        Args:
            a: First operand
            b: Second operand
        
        Returns:
            Result of the operation
        """

class Add(Operation):
    """Addition operation."""

    def execute(self, a: float, b: float) -> float:
        return a + b

class Subtract(Operation):
    """Subtraction operation."""

    def execute(self, a: float, b: float) -> float:
        return a - b

class Multiply(Operation):
    """Multiplication operation."""

    def execute(self, a: float, b: float) -> float:
        return a * b

class Divide(Operation):
    """Division operation."""

    def execute(self, a: float, b: float) -> float:
        return a / b

class OperationFactory:
    """Creates exectuable operations"""

    OPERATIONS = {
        "+": Add,
        "-": Subtract,
        "*": Multiply,
        "/": Divide
    }

    @staticmethod
    def create_operation(operator: str) -> Operation:
        """Create an operation instance based on operator symbol.
    
        Args:
            operator: The operator symbol ('+', '-', '*', '/')
            
        Returns:
            An instance of the appropriate Operation subclass
            
        Raises:
            ValueError: If operator is not recognized
        """

        operation_class = OperationFactory.OPERATIONS.get(operator)
        if not operation_class:
            raise ValueError(f"Unknown operator: {operator}")
        return operation_class()
