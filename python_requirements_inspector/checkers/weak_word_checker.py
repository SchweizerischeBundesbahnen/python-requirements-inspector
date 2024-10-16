"""
Implementation of weak word checker
"""

from spacy.matcher import PhraseMatcher

from python_requirements_inspector import constants
from python_requirements_inspector.text_processor import TextProcessor
from python_requirements_inspector.type_definitions import MatcherId

# initialize list of weak words
weak_word_list_de = [
    "ähnlich wie",
    "anders als",
    "ausreichend",
    "ausreichende",
    "automatisch",
    "breit",
    "derzeitig",
    "eigentlich",
    "entsprechend",
    "entsprechende",
    "falls",
    "gemäss",
    "gemäß",
    "gleich wie",
    "gross",
    "grosse",
    "grosser",
    "grosses",
    "grossen",
    "groß",
    "große",
    "heutige",
    "heutigen",
    "hoch",
    "häufig",
    "in erster Linie",
    "kaum",
    "klein",
    "kleine",
    "kontinuierlich",
    "kontinuierliche",
    "korrekt",
    "kurz",
    "lang",
    "laufend",
    "meistens",
    "niedrig",
    "oft",
    "regelmässig",
    "sehr",
    "schnell",
    "tatsächlich",
    "tief",
    "überwiegend",
    "überwiegende",
    "verbessert",
    "vergleichbar",
    "vor allem",
    "wenig",
]
weak_word_list_en = [
    "according to",
    "accordingly",
    "as much",
    "automatically",
    "concerned",
    "enough",
    "mainly",
    "maintain",
    "necessary",
    "triggers",
    "user friendly",
    "user-friendly",
]


class WeakWordChecker:
    """
    A class for analyzing the presence of weak words in sentences.
    """

    def __init__(self, text_processor: TextProcessor):
        """
        Initializes a WeakWordChecker object.

        Parameters:
            text_processor (TextProcessor): An instance of the TextProcessor class for text processing.

        """

        self.__text_processor = text_processor

        # Language-specific initialization
        lang = text_processor.get_language()
        if lang == constants.ENGLISH:
            weak_word_list = weak_word_list_en
        elif lang == constants.GERMAN:
            weak_word_list = weak_word_list_de
        else:
            raise ValueError(f"Unsupported language: {lang}")

        self.__weak_word_matcher = PhraseMatcher(text_processor.get_vocab(), attr="LEMMA")
        patterns = [text_processor.tokenize(name) for name in text_processor.lemmatize_list(weak_word_list)]
        self.__weak_word_matcher.add(MatcherId.WEAKWORD_MATCHER_ID.value, patterns)

    def check_sentence(self, sent: str) -> tuple[int, str]:
        """
        Analyzes a sentence for weak words.

        Parameters:
            sent (str): The sentence to be analyzed.

        Returns:
            tuple: A tuples with detected findings in the sentence. The tuple contains:
                - Finding count (int)
                - Finding description (str)

        """

        # make the sentence lowercase to ensure detection is case-insensitive
        text = sent.lower()
        doc = self.__text_processor.tokenize(text)

        matches = self.__weak_word_matcher(doc)

        finding_desc = ""
        finding_count = len(matches)

        for _, start, end in matches:
            matched_word = doc[start:end].text
            finding_desc += f"{matched_word} [{start}] "

        return finding_count, finding_desc
