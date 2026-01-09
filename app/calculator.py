"""Calculator loop for user input."""

from app.models import parser

def print_help():
    print("\nCalculator by Arman Bains\n")
    print("Constants: ")
    for c in parser.CONSTANTS:
        print(f"  {c}")
    print("\nPrevious expression's result will be stored in variable 'r'\n"
          "Enter q to quit\n"
          "      h for help\n")

def run_calculator():
    calc = parser.Parser()
    print_help()
    while True:
        user_input = input("> ").lower()

        match(user_input):
            case "q":
                print("Goodbye!")
                break
            case "h":
                print_help()
                continue

        print(calc.parse_and_eval(user_input))
