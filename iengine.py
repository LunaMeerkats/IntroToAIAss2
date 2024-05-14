import sys
import itertools
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

# Function to parse a propositional expression and extract the variables and clauses
def parse_expression(expression):
    clauses = re.split(r'\s*;\s*', expression)  # Split clauses using semicolons
    # Find unique propositional variables
    variables = sorted(set(re.findall(r'\w+', expression)))
    return variables, clauses

# Function to evaluate a propositional expression with a given truth assignment
def evaluate_expression(expression, truth_assignment):
    # Replace logical operators with Python operators
    expression = expression.replace("=>", " or not ")  # Implication
    expression = expression.replace("<=>", " == ")  # Biconditional
    expression = expression.replace("&", " and ")  # Conjunction
    expression = expression.replace("||", " or ")  # Disjunction
    expression = expression.replace("~", " not ")  # Negation

    # Replace variables with truth values
    for var, val in truth_assignment.items():
        expression = re.sub(r'\b' + var + r'\b', str(val), expression)

    # Evaluate the expression
    return eval(expression)

# Function to perform forward chaining
def forward_chaining_entailment(kb, query):
    inferred = set()
    horn_clauses = []

    for clause in kb:
        if "=>" in clause:
            premises, conclusion = clause.split("=>")
            horn_clauses.append((premises.strip(), conclusion.strip()))
        else:
            inferred.add(clause.strip())

    new_inferences = True
    while new_inferences:
        new_inferences = False

        for premises, conclusion in horn_clauses:
            premises_set = {p.strip() for p in premises.split("&")}

            if premises_set.issubset(inferred) and conclusion not in inferred:
                inferred.add(conclusion)
                new_inferences = True

    prefix = "YES:" if query in inferred else "NO:"
    inferred_list_str = ", ".join(sorted(inferred))  # Sort inferred propositions alphabetically
    result = f"{prefix} {inferred_list_str}"
    
    return result

# Function to perform backward chaining
def backward_chaining_entailment(kb, query):
    # Convert KB into a list of Horn clauses
    horn_clauses = []
    for clause in kb:
        if "=>" in clause:
            premises, conclusion = clause.split("=>")
            horn_clauses.append((premises.strip(), conclusion.strip()))
        else:
            # If there's no implication, treat it as a direct fact
            horn_clauses.append(("", clause.strip()))

    # Helper function to perform recursive backward chaining
    def bc_recursive(current_query, inferred):
        # If the current query is already inferred, return True
        if current_query in inferred:
            return True

        # Find clauses where the current query is the conclusion
        relevant_clauses = [clause for clause in horn_clauses if clause[1] == current_query]

        # If no such clauses, return False
        if not relevant_clauses:
            return False

        # Attempt to infer the current query
        for premises, _ in relevant_clauses:
            # Recursively check all premises
            premises_set = {p.strip() for p in premises.split("&") if p.strip()}
            if all(bc_recursive(premise, inferred) for premise in premises_set):
                inferred.add(current_query)
                return True

        return False

    inferred = set()  # Set to track inferred propositions
    success = bc_recursive(query, inferred)

    return success, list(inferred)

def truth_table_entailment(kb, query):
    # Parse the expression to get the list of variables
    variables, _ = parse_expression(" & ".join(kb) + " & " + query)
    num_vars = len(variables)
    all_truth_assignments = list(itertools.product([False, True], repeat=num_vars))
    variable_index = {var: i for i, var in enumerate(variables)}
    valid_assignments = 0
    
    # Identify the single variables in the KB that represent constant truths
    constant_truths = set()
    for clause in kb:
        if "=>" not in clause and "&" not in clause:
            constant_truths.add(clause.strip())
    
    # Filter truth assignments based on the presence of constant truths
    filtered_truth_assignments = [
        assignment for assignment in all_truth_assignments
        if all(assignment[variable_index[var]] for var in constant_truths)
    ]
    
    for assignment in filtered_truth_assignments:
        truth_assignment = {var: assignment[variable_index[var]] for var in variables}
        kb_holds = True
        for clause in kb:
            if "=>" in clause:
                premises, conclusion = clause.split("=>")
                if not evaluate_expression(premises.strip(), truth_assignment) or evaluate_expression(conclusion.strip(), truth_assignment):
                    continue
                else:
                    kb_holds = False
                    break
            else:
                if not evaluate_expression(clause, truth_assignment):
                    kb_holds = False
                    break

        if kb_holds and evaluate_expression(query, truth_assignment):
            valid_assignments += 1

    result = f"YES: {valid_assignments}" if valid_assignments > 0 else "NO"
    return result


# Main function to run the inference engine from the command line
def main():
    if len(sys.argv) < 3:
        print("Usage: python iengine.py <filename> <method>")
        sys.exit(1)

    filename = sys.argv[1]
    method = sys.argv[2]

    try:
        kb, query = parse_kb_and_query(filename)
        
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
