import re

class GeneralClause:
    def __init__(self, clause):
        #Initialize a clause with logical expressions.
        self.clause = clause.strip()

    def get_symbols(self):
        #Get all propositional symbols in the clause
        symbols = set(re.findall(r'\b\w+\b', self.clause))
        return symbols

    def display(self):
        #Display the clause for debugging purposes
        print(self.clause)
