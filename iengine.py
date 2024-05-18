import sys
from HornKnowledgeBase import HornKnowledgeBase
from ForwardsChaining import forwards_entails
from BackwardsChaining import backwards_entails
from truth_table import truth_table_check_hornkb

def parse_input(input_str):
    """
    Parse the input string to create a Horn Knowledge Base (KB) object.

    Args:
        input_str (str): The input string containing TELL and ASK sections.

    Returns:
        HornKnowledgeBase: The Horn Knowledge Base object.
    """
    # Split the input into TELL and ASK sections
    content = input_str.split("ASK")

    # Check if both TELL and ASK sections are present
    if len(content) != 2:
        raise ValueError("Invalid input file format: Missing TELL or ASK section")

    # Extract TELL and ASK sections
    sentences = content[0].strip().replace("TELL", "").strip().split(';')
    query = content[1].strip()

    # Create a new HornKnowledgeBase object
    kb = HornKnowledgeBase()

    # Parse the input and return the Knowledge Base object
    kb.parse_input(sentences, query)
    return kb

def main():
    """
    Main function to execute the program.
    """
    try:
        # Check if command line arguments are provided
        if len(sys.argv) < 2:
            print("Usage: python iengine.py <filename> <method>")
            sys.exit(1)

        if len(sys.argv) < 3:
            print("Usage: python iengine.py <filename> <method>\n\tMethods include:\n\tTT: Truth Table Check\n\tFC: Forward Chaining Check\n\tBC: Backwards Chaining Check")
            sys.exit(1)

        # Extract filename and method from command line arguments
        filename = sys.argv[1]
        method = sys.argv[2]

        # Read the input file
        with open(filename, 'r') as file:
            input_str = file.read()

        # Parse the input file and create the knowledge base
        kb = parse_input(input_str)

        # Execute the specified method
        if method == "FC":
            result, prop_list = forwards_entails(kb, kb.query)
        elif method == "BC":
            result, prop_list = backwards_entails(kb, kb.query)
        elif method == "TT":
            result, models_count = truth_table_check_hornkb(kb, kb.query)
        else:
            print("Invalid method!")
            sys.exit(1)

        # Print the result
        if method in ["FC", "BC"]:
            if result:
                print("YES:", ", ".join(sorted(prop_list)))
            else:
                print("Result: NO")
        elif method == "TT":
            if result == "NO":
                print("Result: NO")
            else:
                print("YES:", models_count)

    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    except ValueError as e:
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
