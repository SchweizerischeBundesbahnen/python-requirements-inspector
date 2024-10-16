"""
Implementation of language detector
"""

import spacy
from spacy.language import Language
from spacy_language_detection import LanguageDetector  # type: ignore

from python_requirements_inspector import constants


class LangDetector:
    """
    Language Detector class for detecting the language of text using Spacy and langdetect.
    """

    def __init__(self) -> None:
        """
        Initializes the LangDetector class.

        """

        # For language detection a model must be loaded. Could be possibly work with any model.
        self.__nlp = spacy.load("en_core_web_md")

        # Define a factory function for the language detector
        Language.factory("language_detector", func=self.__get_lang_detector)

        # Add the language detector to the pipeline
        self.__nlp.add_pipe("language_detector", last=True)

    @staticmethod
    def __get_lang_detector(nlp: Language, name: str) -> LanguageDetector:
        """
        Factory function for the language detector.

        Returns:
            spacy_langdetect.LanguageDetector: The language detector instance.

        """
        return LanguageDetector(seed=42)

    def detect_language(self, text: str | None) -> str:
        """
        Detects the language of the given text.

        Parameters:
            text (str): The text to detect the language of.

        Returns:
            str: The detected language ('de' or 'en').

        """
        if not text:
            return ""

        # Process the text with the Spacy language model
        doc = self.__nlp(text)

        # Extract the language information from the document
        language_object = doc._.language
        language = language_object["language"]

        return language if language in constants.SUPPORTED_LANGUAGES else ""
