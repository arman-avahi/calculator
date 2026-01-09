import pytest
import math
from app.parser import Parser


@pytest.fixture
def parser():
    """Fixture that provides a fresh Parser instance for each test."""
    return Parser()


class TestParser:
    """Tests for Parser class."""

    def test_simple_addition(self, parser):
        assert parser.parse_and_eval("2 + 3") == 5

    def test_simple_subtraction(self, parser):
        assert parser.parse_and_eval("10 - 4") == 6

    def test_simple_multiplication(self, parser):
        assert parser.parse_and_eval("4 * 5") == 20

    def test_simple_division(self, parser):
        assert parser.parse_and_eval("10 / 2") == 5

    def test_order_of_operations_multiply_first(self, parser):
        assert parser.parse_and_eval("2 + 3 * 4") == 14

    def test_order_of_operations_divide_first(self, parser):
        assert parser.parse_and_eval("10 - 8 / 2") == 6

    def test_multiple_operations(self, parser):
        assert parser.parse_and_eval("2 + 3 * 4 - 1") == 13

    def test_negative_number_at_start(self, parser):
        assert parser.parse_and_eval("-5 + 3") == -2

    def test_negative_number_after_operator(self, parser):
        assert parser.parse_and_eval("2 * -3") == -6

    def test_multiple_negative_numbers(self, parser):
        assert parser.parse_and_eval("-4 * -2") == 8

    def test_division_by_zero(self, parser):
        with pytest.raises(ZeroDivisionError):
            parser.parse_and_eval("5 / 0")

    def test_invalid_expression_double_operator(self, parser):
        with pytest.raises((ValueError, IndexError)):
            parser.parse_and_eval("2 + + 3")

    def test_invalid_expression_ends_with_operator(self, parser):
        with pytest.raises((ValueError, IndexError)):
            parser.parse_and_eval("2 + ")

    def test_last_result_stored(self, parser):
        parser.parse_and_eval("5 + 3")
        assert parser.parse_and_eval("r") == 8

    def test_last_result_updates(self, parser):
        parser.parse_and_eval("5 + 3")
        parser.parse_and_eval("10 - 2")
        assert parser.parse_and_eval("r") == 8

    def test_constant_pi(self, parser):
        assert parser.parse_and_eval("2 * pi") == pytest.approx(2 * math.pi, rel=1e-9)

    def test_constant_e(self, parser):
        assert parser.parse_and_eval("1 + e") == pytest.approx(1 + math.e, rel=1e-9)

    def test_constant_tau(self, parser):
        assert parser.parse_and_eval("tau / 2") == pytest.approx(math.tau / 2, rel=1e-9)

    def test_previous_result_r(self, parser):
        parser.parse_and_eval("5 + 3")
        assert parser.parse_and_eval("r * 2") == 16

    def test_previous_result_r_initial_zero(self, parser):
        assert parser.parse_and_eval("r + 5") == 5

    def test_expression_with_spaces(self, parser):
        assert parser.parse_and_eval("  2   +   3  ") == 5

    def test_expression_without_spaces(self, parser):
        assert parser.parse_and_eval("2+3") == 5

    def test_float_numbers(self, parser):
        assert parser.parse_and_eval("2.5 + 3.5") == 6.0

    def test_complex_expression(self, parser):
        assert parser.parse_and_eval("10 + 2 * 5 - 8 / 4") == 18

    def test_power_simple(self, parser):
        assert parser.parse_and_eval("2^3") == 8

    def test_power_square(self, parser):
        assert parser.parse_and_eval("5^2") == 25

    def test_power_precedence_over_addition(self, parser):
        assert parser.parse_and_eval("2 + 3^2") == 11

    def test_power_precedence_over_multiplication(self, parser):
        assert parser.parse_and_eval("2 * 3^2") == 18

    def test_power_with_division(self, parser):
        assert parser.parse_and_eval("100 / 10^2") == 1

    def test_power_negative_exponent(self, parser):
        assert parser.parse_and_eval("2^-1") == 0.5

    def test_power_fractional_exponent(self, parser):
        assert parser.parse_and_eval("4^0.5") == 2.0

    def test_brackets_simple(self, parser):
        assert parser.parse_and_eval("(2 + 3)") == 5

    def test_brackets_with_multiplication(self, parser):
        assert parser.parse_and_eval("2 * (3 + 4)") == 14

    def test_brackets_implicit_multiplication(self, parser):
        assert parser.parse_and_eval("4(2 + 3)") == 20

    def test_brackets_nested(self, parser):
        assert parser.parse_and_eval("2 * (3 + (4 * 5))") == 46

    def test_brackets_multiple(self, parser):
        assert parser.parse_and_eval("(2 + 3) * (4 + 5)") == 45

    def test_brackets_with_power(self, parser):
        assert parser.parse_and_eval("(2 + 3)^2") == 25

    def test_brackets_override_precedence(self, parser):
        assert parser.parse_and_eval("(2 + 3) * 4") == 20

    def test_brackets_complex_nested(self, parser):
        assert parser.parse_and_eval("((2 + 3) * (4 + 1))") == 25

    def test_brackets_with_division(self, parser):
        assert parser.parse_and_eval("(10 + 5) / 3") == 5

    def test_brackets_implicit_with_constant(self, parser):
        assert parser.parse_and_eval("2(pi)") == pytest.approx(2 * math.pi, rel=1e-9)

    def test_power_in_brackets(self, parser):
        assert parser.parse_and_eval("(2^3) + 1") == 9

    def test_complex_with_power_and_brackets(self, parser):
        assert parser.parse_and_eval("2 * (3 + 1)^2 - 5") == 27

    def test_brackets_mismatched_opening(self, parser):
        with pytest.raises(ValueError):
            parser.parse_and_eval("(2 + 3")

    def test_brackets_mismatched_closing(self, parser):
        with pytest.raises(ValueError):
            parser.parse_and_eval("2 + 3)")

    def test_brackets_empty(self, parser):
        with pytest.raises((ValueError, IndexError)):
            parser.parse_and_eval("()")
