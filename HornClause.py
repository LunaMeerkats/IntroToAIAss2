class HornClause:
    def __init__(self, clause):
        """Initialize a Horn clause with premises and conclusion."""
        self.premises = []
        self.conclusion = None
        self.parse_clause(clause)

    def parse_clause(self, clause):
        """Parse the clause string into premises and conclusion."""
        parts = clause.split('=>')
        if len(parts) != 2:
            raise ValueError("Invalid clause format: Missing '=>'")
        self.conclusion = parts[1].strip()
        self.premises = [p.strip() for p in parts[0].split('&')]

    def get_symbols(self):
        """Get all propositional symbols in the clause."""
        symbols = set(self.premises)
        symbols.add(self.conclusion.strip())
        return symbols

    def display(self):
        """Display the clause for debugging purposes."""
        print(', '.join(self.premises), "=>", self.conclusion)
