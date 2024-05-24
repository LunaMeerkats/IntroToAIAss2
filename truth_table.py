from itertools import product
import re

def generate_all_models(symbols):
    """Generate all possible models based on a list of propositional symbols."""
    return list(product([True, False], repeat=len(symbols)))

def evaluate_expression(expression, model):
    """Evaluate a logical expression in a given model."""
    expression = expression.replace("~", " not ").replace("&", " and ").replace("||", " or ")
    # Replace propositional symbols with their truth values from the model
    for symbol in model:
        expression = re.sub(rf'\b{symbol}\b', str(model[symbol]), expression)
    return eval(expression)

def evaluate_clause(clause, model):
    """Check the truth value of a general clause in a model."""
    if "<=>" in clause:
        lhs, rhs = clause.split("<=>")
        return evaluate_expression(lhs.strip(), model) == evaluate_expression(rhs.strip(), model)
    elif "=>" in clause:
        lhs, rhs = clause.split("=>")
        return not evaluate_expression(lhs.strip(), model) or evaluate_expression(rhs.strip(), model)
    else:
        return evaluate_expression(clause, model)

def evaluate_knowledge_base(kb, model):
    """Check if the Knowledge Base (KB) is true in a model."""
    for fact in kb.facts:
        if not evaluate_expression(fact, model):
            return False
    for clause in kb.clauses:
        if not evaluate_clause(clause.clause, model):
            return False
    return True

def truth_table_check_hornkb(kb, query):
    """Main evaluation function for the Knowledge Base."""
    count = 0
    symbols = kb.get_all_symbols()
    true_models = []

    if query not in symbols:
        return ("NO", count)

    entailed = True
    models = generate_all_models(symbols)
    
    for model in models:
        symbol_model = dict(zip(symbols, model))
        if evaluate_knowledge_base(kb, symbol_model):
            count += 1
            true_models.append(symbol_model)
            if not evaluate_expression(query, symbol_model):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)
