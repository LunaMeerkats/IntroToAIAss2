from collections import defaultdict
from HornKnowledgeBase import HornClause

def forwards_entails(knowledge_base, query):
    """
    Perform forward chaining to determine if the query can be inferred from the knowledge base.

    Args:
        knowledge_base (HornKnowledgeBase): The Horn Knowledge Base object.
        query (str): The query to be evaluated.

    Returns:
        tuple: A tuple containing a boolean value indicating if the query is entailed,
               and a list of all entailed symbols.
    """
    # Initialize a dictionary to keep track of the number of premises for each clause
    premise_count = {clause: len(clause.premises) for clause in knowledge_base.clauses}
    
    # Initialize the agenda with the facts in the knowledge base
    agenda = knowledge_base.facts[:]
    
    # Initialize a dictionary to keep track of whether a symbol has been inferred
    inferred = defaultdict(bool)
    
    # Set to store all entailed symbols
    entailed_symbols = set(knowledge_base.facts)
    
    # Loop until agenda is empty
    while agenda:
        p = agenda.pop(0)  # Pop the first symbol from the agenda
        
        # If the symbol matches the query, return True along with all inferred symbols
        if p == query:
            entailed_symbols.add(p)
            return True, list(entailed_symbols)
        
        # If the symbol has not been inferred before
        if not inferred[p]:
            inferred[p] = True  # Mark the symbol as inferred
            entailed_symbols.add(p)
            
            # Update the premise count for each clause that contains the symbol
            for clause in knowledge_base.clauses:
                if p in clause.premises:
                    premise_count[clause] -= 1
                    # If all premises are satisfied, add the conclusion to the agenda
                    if premise_count[clause] == 0:
                        agenda.append(clause.conclusion)
    
    # If the loop completes without finding the query, return False along with all inferred symbols
    return False, list(entailed_symbols)
