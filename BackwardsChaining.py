from collections import defaultdict

def backwards_entails(knowledge_base, query, inferred=None):
    """
    Perform backward chaining to determine if the query can be inferred from the knowledge base.

    Args:
        knowledge_base (HornKnowledgeBase): The Horn Knowledge Base object.
        query (str): The query to be evaluated.
        inferred (defaultdict(bool), optional): Dictionary to store inferred symbols. Defaults to None.

    Returns:
        tuple: A tuple containing a boolean value indicating if the query is entailed,
               and a list of all entailed symbols.
    """
    # Initialize inferred dictionary if not provided
    if inferred is None:
        inferred = defaultdict(bool)

    # Check if the query is already a known fact
    if query in knowledge_base.facts:
        inferred[query] = True
        return True, list(inferred.keys())

    # Explore each clause in the KB to see if it can conclude the query
    for clause in knowledge_base.clauses:
        if clause.conclusion == query:
            # All premises of the clause must be proven true
            all_premises_proven = all(inferred[premise] for premise in clause.premises)

            if all_premises_proven:
                inferred[query] = True
                return True, list(inferred.keys())

            # Try to prove each premise recursively
            for premise in clause.premises:
                if not inferred[premise]:
                    _, _ = backwards_entails(knowledge_base, premise, inferred)

            # Recheck if all premises are proven after recursive calls
            all_premises_proven = all(inferred[premise] for premise in clause.premises)

            if all_premises_proven:
                inferred[query] = True
                return True, list(inferred.keys())

    # If the query cannot be inferred, return False along with all inferred symbols
    return False, list(inferred.keys())
