from itertools import product
from HornKnowledgeBase import HornKnowledgeBase

def generate_all_models(symbols):
    """Generate all possible models based on a list of propositional symbols."""
    return list(product([True, False], repeat=len(symbols)))

def evaluate_fact(fact, model={}):
    """Check the truth value of a fact in a model."""
    return model.get(fact, False)

def evaluate_horn_clause(clause, model={}):
    """Check the truth value of a Horn Clause in a model."""
    premise_true = all(model.get(premise, False) for premise in clause.premises)
    conclusion_true = model.get(clause.conclusion, False)
    return (not premise_true) or conclusion_true

def evaluate_horn_knowledge_base(kb, model={}):
    """Check if the Horn Knowledge Base (KB) is true in a model."""
    for fact in kb.facts:
        if not evaluate_fact(fact, model):
            return False
    for clause in kb.clauses:
        if not evaluate_horn_clause(clause, model):
            return False
    return True

def truth_table_check_hornkb(kb, query):
    """Main evaluation function for Horn KB."""
    count = 0
    symbols = kb.get_all_symbols()

    if query not in symbols:
        return ("NO", count)

    entailed = True
    models = generate_all_models(symbols)
    for model in models:
        symbol_model = dict(zip(symbols, model))
        if evaluate_horn_knowledge_base(kb, symbol_model):
            count += 1
            if not evaluate_fact(query, symbol_model):
                entailed = False

    return ("YES", count) if entailed else ("NO", count)
