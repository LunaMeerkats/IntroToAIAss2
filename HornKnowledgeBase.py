from HornClause import HornClause
import re

class HornKnowledgeBase:
    def __init__(self):
        """Initialize an empty Horn Knowledge Base."""
        self.clauses = []
        self.facts = []
        self.query = None

    def parse_input(self, sentences, query):
        """Parse input sentences and query to populate the Horn Knowledge Base.

        Args:
            sentences (list): List of strings representing sentences in the knowledge base.
            query (str): The query to be answered by the knowledge base.
        """
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                if "=>" in sentence:
                    self.clauses.append(HornClause(sentence))
                else:
                    self.facts.append(sentence)

        self.query = query

    def get_all_symbols(self):
        """Get all propositional symbols present in the knowledge base.

        Returns:
            list: List of unique propositional symbols.
        """
        all_symbols = set(self.facts)

        for clause in self.clauses:
            all_symbols.update(clause.get_symbols())

        return list(all_symbols)
