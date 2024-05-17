import sys
import itertools
import re

# Function to parse the knowledge base and query from the input file
def parse_kb_and_query(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]  # Strip and ignore empty lines

    tell_section = ""
    ask_section = ""

    reading_tell = False
    reading_ask = False

    for line in lines:
        if line == "TELL":
            reading_tell = True
            reading_ask = False
        elif line == "ASK":
            reading_ask = True
            reading_tell = False
        elif reading_tell:
            tell_section = line
            reading_tell = False  # Stop reading after capturing the next line
        elif reading_ask:
            ask_section = line
            reading_ask = False  # Stop reading after capturing the next line
    
    if not tell_section:
        raise ValueError("Missing or invalid 'TELL' section in the input file.")
    if not ask_section:
        raise ValueError("Missing or invalid 'ASK' section in the input file.")

    kb = [clause.strip() for clause in tell_section.split(";") if clause.strip()]
    query = ask_section.strip()

    return kb, query

# Function to parse a propositional expression and extract the variables and clauses
def parse_expression(expression):
    clauses = re.split(r'\s*;\s*', expression)  # Split clauses using semicolons
    variables = sorted(set(re.findall(r'\w+', expression)))
    return variables, clauses

# Function to evaluate a propositional expression with a given truth assignment
def evaluate_expression(expression, truth_assignment):
    expression = expression.replace("=>", " or not ")  # Implication
    expression = expression.replace("<=>", " == ")  # Biconditional
    expression = expression.replace("&", " and ")  # Conjunction
    expression = expression.replace("||", " or ")  # Disjunction
    expression = expression.replace("~", " not ")  # Negation
    
    for var, val in truth_assignment.items():
        expression = re.sub(r'\b' + var + r'\b', str(val), expression)
    
    return eval(expression)

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

    print("Inferred:", inferred)  # Debug print

    query_components = [q.strip() for q in query.split("||")]
    query_holds = any(all(component in inferred for component in conjunct.split("&")) for conjunct in query_components)

    prefix = "YES:" if query_holds else "NO:"
    inferred_list_str = ", ".join(sorted(inferred))
    result = f"{prefix} {inferred_list_str}"
    
    return result

def backward_chaining_entailment(kb, query):
    horn_clauses = []
    for clause in kb:
        if "=>" in clause:
            premises, conclusion = clause.split("=>")
            horn_clauses.append((premises.strip(), conclusion.strip()))
        else:
            horn_clauses.append(("", clause.strip()))

    def bc_recursive(current_query, inferred):
        if current_query in inferred:
            return True

        relevant_clauses = [clause for clause in horn_clauses if clause[1] == current_query]

        if not relevant_clauses:
            return False

        for premises, _ in relevant_clauses:
            premises_set = {p.strip() for p in premises.split("&") if p.strip()}
            if all(bc_recursive(premise, inferred) for premise in premises_set):
                inferred.add(current_query)
                return True

        return False

    inferred = set()
    query_components = query.split("&")
    success = all(bc_recursive(component.strip(), inferred) for component in query_components)

    return success, list(inferred)

def truth_table_entailment(kb, query):
    variables, _ = parse_expression(" & ".join(kb))
    
    query_variables = set(re.findall(r'\w+', query))
    if not query_variables.issubset(set(variables)):
        return "NO"
    
    num_vars = len(variables)
    all_truth_assignments = list(itertools.product([False, True], repeat=num_vars))
    variable_index = {var: i for i, var in enumerate(variables)}
    
    valid_assignments = 0
    kb_holds_assignments = 0

    for assignment in all_truth_assignments:
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

        if kb_holds:
            kb_holds_assignments += 1
            if evaluate_expression(query, truth_assignment):
                valid_assignments += 1

    result = f"YES: {valid_assignments}" if valid_assignments > 0 and valid_assignments == kb_holds_assignments else "NO"
    return result

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
                inferred_str = ", ".join(sorted(inferred))
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
