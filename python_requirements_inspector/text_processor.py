"""
Implementation of text processor
"""

import spacy
from spacy.lang.de import German
from spacy.lang.en import English
from spacy.tokens.doc import Doc
from spacy.vocab import Vocab

from python_requirements_inspector import constants


class TextProcessor:
    """
    A class for processing text using language-specific Spacy models.
    """

    __small_nlp: English | German

    def __init__(self, lang: str):
        """
        Initializes a TextProcessor object.

        Parameters:
            lang (str): The language of the text being processed.

        """

        # Language-specific initialization
        if lang == constants.ENGLISH:
            self.__nlp = spacy.load("en_core_web_md")
            self.__small_nlp = English()
        elif lang == constants.GERMAN:
            self.__nlp = spacy.load("de_core_news_md")
            self.__small_nlp = German()
        else:
            raise ValueError(f"Unsupported language: {lang}")

        self.__small_nlp.add_pipe("sentencizer")

    def sentenize(self, text: str) -> Doc:
        """
        Tokenizes a text into sentences using the language-specific Spacy language model.

        Parameters:
            text (str): The text to be tokenized.

        Returns:
            spacy.tokens.doc.Doc: The Spacy Doc object representing the tokenized sentences.

        """
        return self.__small_nlp(text)

    def tokenize(self, text: str) -> Doc:
        """
        Tokenizes a text using the language-specific Spacy language model.

        Parameters:
            text (str): The text to be tokenized.

        Returns:
            spacy.tokens.doc.Doc: The Spacy Doc object representing the tokenized text.

        """
        return self.__nlp(text)

    def lemmatize_list(self, word_list: list[str]) -> list[str]:
        """
        Lemmatizes a list of words using the language-specific Spacy language model.

        Parameters:
            word_list (list): The list of words to be lemmatized.

        Returns:
            list: The lemmatized list of words.

        """
        lemma_list: list[str] = []

        for word in word_list:
            doc = self.tokenize(word.lower())
            lemma = " ".join(f"{token}" for token in doc).strip()  # Append each token's lemma to the string
            lemma_list.append(lemma.strip())  # Append the processed lemma to the lemma list

        return lemma_list

    def get_language(self) -> str | None:
        """
        Get the language from this instance of the text processor.

        Returns:
            str: The language code.
        """
        return self.__nlp.lang

    def get_vocab(self) -> Vocab:
        """
        Get the vocabulary from this instance of the text processor.

        Returns:
            spacy.vocab.Vocab: The vocabulary of the language model.
        """
        return self.__nlp.vocab
