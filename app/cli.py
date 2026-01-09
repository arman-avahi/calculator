"""Calculator loop for user input."""

from app import parser

def print_help():
    """Display help info including any constants and commands."""
    print("\nCalculator by Arman Bains\n")
    print("Constants: ")
    for c in parser.CONSTANTS:
        print(f"  {c}")
    print("\nPrevious expression's result will be stored in variable 'r'\n"
          "Enter q to quit\n"
          "      h for help\n")

def run_calculator():
    """Run the interactive calculator loop.

    Continuously prompts user for user input and special commands.
    """
    calc = parser.Parser()
    print_help()
    while True:
        try:
            user_input = input("> ").lower()

            match user_input:
                case "q":
                    print("Goodbye!")
                    break
                case "h":
                    print_help()
                    continue

            result = calc.parse_and_eval(user_input)
            print(result)
        except ValueError:
            print("Invalid expression! Check operators, brackets, and numbers.")
        except IndexError:
            print("Incomplete expression! Missing operands.")
        except ZeroDivisionError:
            print("Cannot divide by zero!")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
