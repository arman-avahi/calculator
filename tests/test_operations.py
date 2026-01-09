"""Tests for calculator operations."""
import pytest
from app.operations import add, subtract, multiply, divide, get_operation


class TestAdd:
    """Tests for add function."""

    def test_add_positive_numbers(self):
        assert add(5, 3) == 8

    def test_add_negative_numbers(self):
        assert add(-5, -3) == -8

    def test_add_mixed_signs(self):
        assert add(5, -3) == 2

    def test_add_with_zero(self):
        assert add(5, 0) == 5

    def test_add_floats(self):
        assert add(2.5, 3.5) == 6.0


class TestSubtract:
    """Tests for subtract function."""

    def test_subtract_positive_numbers(self):
        assert subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        assert subtract(3, 5) == -2

    def test_subtract_negative_numbers(self):
        assert subtract(-5, -3) == -2

    def test_subtract_with_zero(self):
        assert subtract(5, 0) == 5

    def test_subtract_floats(self):
        assert subtract(5.5, 2.5) == 3.0


class TestMultiply:
    """Tests for multiply function."""

    def test_multiply_positive_numbers(self):
        assert multiply(5, 3) == 15

    def test_multiply_by_zero(self):
        assert multiply(5, 0) == 0

    def test_multiply_negative_numbers(self):
        assert multiply(-5, -3) == 15

    def test_multiply_mixed_signs(self):
        assert multiply(5, -3) == -15

    def test_multiply_floats(self):
        assert multiply(2.5, 4) == 10.0


class TestDivide:
    """Tests for divide function."""

    def test_divide_positive_numbers(self):
        assert divide(10, 2) == 5

    def test_divide_negative_numbers(self):
        assert divide(-10, -2) == 5

    def test_divide_mixed_signs(self):
        assert divide(10, -2) == -5

    def test_divide_floats(self):
        assert divide(7.5, 2.5) == 3.0

    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ZeroDivisionError):
            divide(5, 0)


class TestGetOperation:
    """Tests for get_operation function."""

    def test_get_add_operation(self):
        op = get_operation("+")
        assert op(2, 3) == 5

    def test_get_subtract_operation(self):
        op = get_operation("-")
        assert op(5, 3) == 2

    def test_get_multiply_operation(self):
        op = get_operation("*")
        assert op(4, 5) == 20

    def test_get_divide_operation(self):
        op = get_operation("/")
        assert op(10, 2) == 5

    def test_unknown_operator_raises_error(self):
        with pytest.raises(ValueError, match="Unknown operator"):
            get_operation("^")

    def test_invalid_operator_raises_error(self):
        with pytest.raises(ValueError):
            get_operation("abc")

    def test_operation_returns_callable(self):
        op = get_operation("+")
        assert callable(op)
