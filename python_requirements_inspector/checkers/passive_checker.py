"""
Implementation of passive checker
"""

from spacy.matcher import Matcher

from python_requirements_inspector import constants
from python_requirements_inspector.text_processor import TextProcessor
from python_requirements_inspector.type_definitions import MatcherId

# rules pattern for passive in english
passive_rule_en = [
    [
        {"DEP": "nsubjpass"},
        {"DEP": "aux", "OP": "*"},
        {"DEP": "auxpass"},
        {"TAG": "VBN"},
    ]
]

# rules pattern for passive in german
# Pattern: finite verb + perfect participle | finite verb, full
# Example VVPP: Damit es möglich ist, wird eine Bewegungserlaubnis benötigt.
# Example VVFIN: weil gewisse SR40-Systemteile nicht nur in der Schweiz angewendet werden sollen
# 2nd Pattern Example: .. zu erstellen sein
passive_rule_de = [
    [{"TAG": "VAFIN"}, {"OP": "*"}, {"TAG": {"IN": ["VVPP", "VVFIN"]}}],
    [{"TAG": "PTKZU"}, {"TAG": "VVINF"}, {"TAG": "VAFIN"}],
]


class PassiveChecker:
    """
    A class for analyzing passive voice constructions in sentences.
    """

    def __init__(self, text_processor: TextProcessor):
        """
        Initializes a PassiveChecker object.

        Parameters:
            text_processor (TextProcessor): An instance of the TextProcessor class for text processing.

        """

        self.__text_processor = text_processor

        # Language-specific initialization
        lang = text_processor.get_language()
        if lang == constants.ENGLISH:
            passive_rule = passive_rule_en
        elif lang == constants.GERMAN:
            passive_rule = passive_rule_de  # type: ignore
        else:
            raise ValueError(f"Unsupported language: {lang}")

        self.__passive_matcher = Matcher(text_processor.get_vocab())
        self.__passive_matcher.add(MatcherId.PASSIVE_MATCHER_ID.value, passive_rule)

    def check_sentence(self, sent: str) -> tuple[int, str]:
        """
        Analyzes a sentence for passive voice constructions.

        Parameters:
            sent (str): The sentence to be analyzed.

        Returns:
            tuple: A tuples with detected findings in the sentence. The tuple contains:
                - Finding count (int)
                - Finding description (str)

        """

        doc = self.__text_processor.tokenize(sent)

        matches = self.__passive_matcher(doc)

        finding_desc = ""
        finding_count = len(matches)

        for _, start, end in matches:
            # Add the matched range to the error description
            finding_desc += f" [{start}:{end}]"

        return finding_count, finding_desc
