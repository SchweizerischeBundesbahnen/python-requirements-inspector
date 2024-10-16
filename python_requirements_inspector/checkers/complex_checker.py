"""
Implementation of complex checker
"""

from spacy.matcher import Matcher

from python_requirements_inspector import constants
from python_requirements_inspector.text_processor import TextProcessor
from python_requirements_inspector.type_definitions import MatcherId

# matcher rules
relevant_words_rule = [[{"IS_PUNCT": False, "IS_STOP": False, "IS_SPACE": False}]]
all_words_rule = [[{"IS_PUNCT": False, "IS_SPACE": False}]]


class ComplexChecker:
    """
    A class for analyzing sentence complexity.
    """

    def __init__(self, text_processor: TextProcessor):
        """
        Initializes a ComplexChecker object.

        Parameters:
            text_processor (TextProcessor): An instance of the TextProcessor class for text processing.

        """

        self.__text_processor = text_processor

        self.__relevant_words_matcher = Matcher(text_processor.get_vocab())
        self.__relevant_words_matcher.add(MatcherId.RELEVANT_WORDS_MATCHER_ID.value, relevant_words_rule)

        self.__all_words_matcher = Matcher(text_processor.get_vocab())
        self.__all_words_matcher.add(MatcherId.ALL_WORDS_MATCHER_ID.value, all_words_rule)

    def check_sentence(self, sent: str) -> tuple[int, str]:
        """
        Analyzes a sentence for complexity based on word count.

        Parameters:
            sent (str): The sentence to be analyzed.

        Returns:
            tuple: A tuples with detected findings in the sentence. The tuple contains:
                - Finding count (int)
                - Finding description (str)

        """

        doc = self.__text_processor.tokenize(sent)

        # Remove stopwords, punctuations and spaces for tooMuch check
        relevant_words = self.__relevant_words_matcher(doc, as_spans=True)

        # Remove punctuations and spaces for tooLong check
        all_words = self.__all_words_matcher(doc, as_spans=True)

        word_count = len(all_words)
        relevant_word_count = len(relevant_words)

        finding_desc = ""
        finding_count = 0

        # Check rules
        if relevant_word_count > constants.TOO_MUCH or word_count > constants.TOO_LONG:
            finding_count = 1  # Since complexity affects the whole sentence, the finding count is maximum 1.
            finding_desc = f"The sentence is too complex. Contains {word_count} words and {relevant_word_count} relevant words."

        return finding_count, finding_desc
