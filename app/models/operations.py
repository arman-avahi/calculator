"""Basic calculator operations"""

import abc

class Operation(abc.ABC):
    @abc.abstractmethod
    def execute(self, a: float, b: float) -> float:
        pass

class Add(Operation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class Subtract(Operation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class Multiply(Operation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class Divide(Operation):
    def execute(self, a: float, b: float) -> float:
        return a / b

class OperationFactory:
    """This is the factory - it creates operations for you"""

    @staticmethod
    def create_operation(operator: str) -> Operation:
        operations = {
            "+": Add,
            "-": Subtract,
            "*": Multiply,
            "/": Divide
        }

        operation_class = operations.get(operator)
        if not operation_class:
            raise ValueError(f"Unknown operator: {operator}")
        return operation_class()

