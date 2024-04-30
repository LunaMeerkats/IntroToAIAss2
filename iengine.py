import sys
import itertools
import collections
import re

# Function to parse the knowledge base and query from the input file
def parse_kb_and_query(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]  # Strip and ignore empty lines

    # Initialize KB and query
    tell_section = ""
    ask_section = ""

    # Loop through the lines to identify TELL and ASK sections
    reading_tell = False
    reading_ask = False

    for i, line in enumerate(lines):
        if line == "TELL":
            reading_tell = True
            reading_ask = False
        elif line == "ASK":
            reading_ask = True
            reading_tell = False
        elif reading_tell:
            # If we're reading TELL, append this line to tell_section
            tell_section = line
            reading_tell = False  # Stop reading after capturing the next line
        elif reading_ask:
            # If we're reading ASK, set this line as ask_section
            ask_section = line
            reading_ask = False  # Stop reading after capturing the next line
    
    # Ensure TELL and ASK sections are valid
    if not tell_section:
        raise ValueError("Missing or invalid 'TELL' section in the input file.")
    if not ask_section:
        raise ValueError("Missing or invalid 'ASK' section in the input file.")

    # Parse the knowledge base into Horn clauses
    kb = [clause.strip() for clause in tell_section.split(";") if clause.strip()]
    query = ask_section.strip()

    return kb, query

# Main function to run the inference engine from the command line
def main():
    if len(sys.argv) < 3:
        print("Usage: python iengine.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2]

    try:
        kb, query = parse_kb_and_query(filename)

        print(kb)
        print(query)
        
        if method == "TT":
            result = truth_table_entailment(kb, query)
        elif method == "FC":
            result = forward_chaining_entailment(kb, query)
        elif method == "BC":
            success, inferred = backward_chaining_entailment(kb, query)
            if success:
                inferred_str = ", ".join(sorted(inferred))  # Sort for consistent output
                result = f"YES: {inferred_str}"
            else:
                result = "NO"
        else:
            print("Invalid method. Use TT, FC, or BC.")
            sys.exit(1)

        print(result)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
