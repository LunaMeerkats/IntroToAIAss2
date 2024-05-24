from GeneralClause import GeneralClause
class GeneralKnowledgeBase:
    def __init__(self):
        """Initialize an empty Knowledge Base."""
        self.clauses = []
        self.facts = []
        self.query = None

    def parse_input(self, sentences, query):
        """Parse input sentences and query to populate the Knowledge Base.

        Args:
            sentences (list): List of strings representing sentences in the knowledge base.
            query (str): The query to be answered by the knowledge base.
        """
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                self.clauses.append(GeneralClause(sentence))
        self.query = query

    def get_all_symbols(self):
        """Get all propositional symbols present in the knowledge base.

        Returns:
            list: List of unique propositional symbols.
        """
        all_symbols = set()

        for clause in self.clauses:
            all_symbols.update(clause.get_symbols())

        return list(all_symbols)
