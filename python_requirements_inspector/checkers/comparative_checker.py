"""
Implementation of comparative checker
"""

from spacy.matcher import Matcher

from python_requirements_inspector import constants
from python_requirements_inspector.text_processor import TextProcessor
from python_requirements_inspector.type_definitions import MatcherId

# matcher rules
comparative_rule_en = [[{"TAG": {"IN": ["JJR", "RBR"]}}]]

comparative_rule_de = [[{"MORPH": {"IS_SUPERSET": ["Degree=Cmp"]}}]]

superlative_rule_en = [[{"TAG": {"IN": ["JJS", "RBS"]}}]]

superlative_rule_de = [[{"MORPH": {"IS_SUPERSET": ["Degree=Sup"]}}]]


class ComparativeChecker:
    """
    A class for checking comparative and superlative constructions in a given text.
    """

    def __init__(self, text_processor: TextProcessor):
        """
        Initializes a ComparativeChecker object.

        Parameters:
            text_processor (TextProcessor): A TextProcessor instance for processing text.

        """
        self.__text_processor = text_processor

        # Language-specific initialization
        lang = text_processor.get_language()
        if lang == constants.ENGLISH:
            comparative_rule = comparative_rule_en
            superlative_rule = superlative_rule_en
        elif lang == constants.GERMAN:
            comparative_rule = comparative_rule_de
            superlative_rule = superlative_rule_de
        else:
            raise ValueError(f"Unsupported language: {lang}")

        self.__comparative_matcher = Matcher(text_processor.get_vocab())
        self.__comparative_matcher.add(MatcherId.COMPARATIVE_MATCHER_ID.value, comparative_rule)
        self.__superlative_matcher = Matcher(text_processor.get_vocab())
        self.__superlative_matcher.add(MatcherId.SUPERLATIVE_MATCHER_ID.value, superlative_rule)

    def check_sentence(self, sent: str) -> tuple[int, str]:
        """
        Analyzes a sentence for comparative and superlative constructions.

        Parameters:
            sent (str): The sentence to be analyzed.

        Returns:
            tuple: A tuples with detected findings in the sentence. The tuple contains:
                - Finding count (int)
                - Finding description (str)

        """

        doc = self.__text_processor.tokenize(sent)
        comp_matches = self.__comparative_matcher(doc, as_spans=True)
        sup_matches = self.__superlative_matcher(doc, as_spans=True)
        comparatives = [match.text for match in comp_matches]
        superlatives = [match.text for match in sup_matches]

        finding_desc = ""
        finding_count = 0

        comparative_count = len(comparatives)
        superlative_count = len(superlatives)

        # Update the count and error description based on the matched constructions
        if comparative_count > 0:
            finding_count += comparative_count
            finding_desc += f" {MatcherId.COMPARATIVE_MATCHER_ID.value} " + ", ".join(comparatives)
        if superlative_count > 0:
            finding_count += superlative_count
            finding_desc += f" {MatcherId.SUPERLATIVE_MATCHER_ID.value} " + ", ".join(superlatives)

        return finding_count, finding_desc
