"""Tests."""

from python_requirements_inspector import constants, lang_detector


def test_lang_detector_detect_en():
    """
    Test case for the LangDetector class detecting English in a sentence.
    """
    test_sentence = "I am a text for detecting english as language."

    expected_language = constants.ENGLISH

    test_lang_detector = lang_detector.LangDetector()
    result = test_lang_detector.detect_language(test_sentence)

    assert result == expected_language


def test_lang_detector_detect_de():
    """
    Test case for the LangDetector class detecting German in a sentence.
    """
    test_sentence = "Ich bin ein Text zur Erkennung von Deutsch als Sprache."

    expected_language = constants.GERMAN

    test_lang_detector = lang_detector.LangDetector()
    result = test_lang_detector.detect_language(test_sentence)

    assert result == expected_language


def test_lang_detector_detect_unsupported_language():
    """
    Test case for the LangDetector class detecting no supported language in a sentence.
    """
    test_sentence = "Nihongo wo gengo toshite kenshutsu suru tame no tekisuto desu."

    expected_language = ""

    test_lang_detector = lang_detector.LangDetector()
    result = test_lang_detector.detect_language(test_sentence)

    assert result == expected_language


def test_lang_detector_text_empty():
    """ """
    test_sentence_empty = ""
    expected_language = ""

    result = lang_detector.LangDetector().detect_language(test_sentence_empty)
    assert result == expected_language


def test_lang_detector_text_none():
    """ """
    test_sentence_empty = None
    expected_language = ""

    result = lang_detector.LangDetector().detect_language(test_sentence_empty)
    assert result == expected_language
