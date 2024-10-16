"""
Implementation of text analyzer
"""

from typing import Protocol

from python_requirements_inspector.checkers.comparative_checker import ComparativeChecker
from python_requirements_inspector.checkers.complex_checker import ComplexChecker
from python_requirements_inspector.checkers.passive_checker import PassiveChecker
from python_requirements_inspector.checkers.process_word_checker import (
    ProcessWordChecker,
)
from python_requirements_inspector.checkers.weak_word_checker import WeakWordChecker
from python_requirements_inspector.text_processor import TextProcessor
from python_requirements_inspector.type_definitions import Finding, FindingType, PartialFinding


# Define a protocol that all checkers must follow
class CheckerProtocol(Protocol):
    def check_sentence(self, sentence: str) -> tuple[int, str]:
        """
        Analyzes a sentence.

        Parameters:
            sent (str): The sentence to be analyzed.

        Returns:
            tuple: A tuples with detected findings in the sentence. The tuple contains:
                - Finding count (int)
                - Finding description (str)

        """
        pass


class TextAnalyzer:
    """
    A class for analyzing text for various types of linguistic issues.
    """

    def __init__(self, lang: str):
        """
        Initialize the TextAnalyzer.

        Parameters:
            lang (str): The language for text analysis.
        """

        self.__text_processor = TextProcessor(lang)
        self.__available_checks: dict[FindingType, CheckerProtocol] = {
            FindingType.COMPLEX: ComplexChecker(self.__text_processor),
            FindingType.PASSIVE: PassiveChecker(self.__text_processor),
            FindingType.COMPARATIVE: ComparativeChecker(self.__text_processor),
            FindingType.WEAKWORD: WeakWordChecker(self.__text_processor),
            FindingType.PROCESS: ProcessWordChecker(self.__text_processor),
        }

    def process_sentence(self, sent: str, list_of_checks: list[FindingType]) -> list[PartialFinding]:
        """
        Process a sentence for specified types of linguistic issues.

        Parameters:
            sent (str): The sentence to be processed.
            list_of_checks (list): A list of linguistic issues to check for.

        Returns:
            list: A list of tuples representing detected findings in the sentence. Each tuple contains:
                - Finding type (str)
                - Finding count (int)
                - Finding description (str)
        """

        findings: list[PartialFinding] = []

        for check in list_of_checks:
            checker = self.__available_checks.get(check)
            result = checker.check_sentence(sent) if checker is not None else (0, "")

            if result[0] <= 0:
                continue

            findings.append(
                PartialFinding(
                    finding_type=check,
                    finding_count=result[0],
                    finding_desc=result[1],
                )
            )

        return findings

    def analyze_text(self, text: str, list_of_checks: list[FindingType]) -> list[Finding]:
        """
        Analyze the entire text, sentence by sentence, for specified types of linguistic issues.

        Parameters:
            text (str): The text to be analyzed.
            list_of_checks (list): A list of linguistic issues to check for.

        Returns:
            list: A list of Finding representing detected findings in the text. Each Finding contains:
                - Sentence number (int)
                - First three words of the sentence (str)
                - Finding type (str)
                - Finding count (int)
                - Finding description (str)
        """

        findings: list[Finding] = []  # stores the detected problems
        # Split text into sentences
        doc = self.__text_processor.sentenize(text)
        for sent_num, sent in enumerate(doc.sents):
            results = self.process_sentence(sent.text, list_of_checks)

            findings.extend(
                [
                    Finding(
                        sent_num=sent_num + 1,
                        sent_start=sent[0:3].text,
                        finding_count=result.finding_count,
                        finding_desc=result.finding_desc,
                        finding_type=result.finding_type,
                    )
                    for result in results
                ]
            )

        return findings
