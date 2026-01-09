"""Tests for parser module."""
import pytest
import math
from app.parser import Parser


class TestParser:
    """Tests for Parser class."""

    def test_simple_addition(self):
        parser = Parser()
        result = parser.parse_and_eval("2 + 3")
        assert result == 5

    def test_simple_subtraction(self):
        parser = Parser()
        result = parser.parse_and_eval("10 - 4")
        assert result == 6

    def test_simple_multiplication(self):
        parser = Parser()
        result = parser.parse_and_eval("4 * 5")
        assert result == 20

    def test_simple_division(self):
        parser = Parser()
        result = parser.parse_and_eval("10 / 2")
        assert result == 5

    def test_order_of_operations_multiply_first(self):
        parser = Parser()
        result = parser.parse_and_eval("2 + 3 * 4")
        assert result == 14

    def test_order_of_operations_divide_first(self):
        parser = Parser()
        result = parser.parse_and_eval("10 - 8 / 2")
        assert result == 6

    def test_multiple_operations(self):
        parser = Parser()
        result = parser.parse_and_eval("2 + 3 * 4 - 1")
        assert result == 13

    def test_negative_number_at_start(self):
        parser = Parser()
        result = parser.parse_and_eval("-5 + 3")
        assert result == -2

    def test_negative_number_after_operator(self):
        parser = Parser()
        result = parser.parse_and_eval("2 * -3")
        assert result == -6

    def test_multiple_negative_numbers(self):
        parser = Parser()
        result = parser.parse_and_eval("-4 * -2")
        assert result == 8

    def test_division_by_zero(self):
        parser = Parser()
        with pytest.raises(ZeroDivisionError):
            parser.parse_and_eval("5 / 0")

    def test_invalid_expression_double_operator(self):
        parser = Parser()
        with pytest.raises((ValueError, IndexError)):
            parser.parse_and_eval("2 + + 3")

    def test_invalid_expression_ends_with_operator(self):
        parser = Parser()
        with pytest.raises((ValueError, IndexError)):
            parser.parse_and_eval("2 + ")

    def test_last_result_stored(self):
        parser = Parser()
        parser.parse_and_eval("5 + 3")
        assert parser.last_result == 8

    def test_last_result_updates(self):
        parser = Parser()
        parser.parse_and_eval("5 + 3")
        parser.parse_and_eval("10 - 2")
        assert parser.last_result == 8

    def test_constant_pi(self):
        parser = Parser()
        result = parser.parse_and_eval("2 * pi")
        assert result == pytest.approx(2 * math.pi, rel=1e-9)

    def test_constant_e(self):
        parser = Parser()
        result = parser.parse_and_eval("1 + e")
        assert result == pytest.approx(1 + math.e, rel=1e-9)

    def test_constant_tau(self):
        parser = Parser()
        result = parser.parse_and_eval("tau / 2")
        assert result == pytest.approx(math.tau / 2, rel=1e-9)

    def test_previous_result_r(self):
        parser = Parser()
        parser.parse_and_eval("5 + 3")
        result = parser.parse_and_eval("r * 2")
        assert result == 16

    def test_previous_result_r_initial_zero(self):
        parser = Parser()
        result = parser.parse_and_eval("r + 5")
        assert result == 5

    def test_expression_with_spaces(self):
        parser = Parser()
        result = parser.parse_and_eval("  2   +   3  ")
        assert result == 5

    def test_expression_without_spaces(self):
        parser = Parser()
        result = parser.parse_and_eval("2+3")
        assert result == 5

    def test_float_numbers(self):
        parser = Parser()
        result = parser.parse_and_eval("2.5 + 3.5")
        assert result == 6.0

    def test_complex_expression(self):
        parser = Parser()
        result = parser.parse_and_eval("10 + 2 * 5 - 8 / 4")
        assert result == 18
