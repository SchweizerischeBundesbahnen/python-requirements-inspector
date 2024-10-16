"""Tests."""

from python_requirements_inspector import constants, text_analyzer
from python_requirements_inspector.type_definitions import FindingType, MatcherId

######################################################
# TESTS FOR ENGLISH
######################################################


def test_text_analyzer_find_nothing_en():
    """
    Test case for the TextAnalyzer class when no issues are detected in an English sentence.
    """
    test_sentence = "I am a text for analysis and without results."

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.ENGLISH)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    assert not result


def test_text_analyzer_find_weak_words_en():
    """
    Test case for the TextAnalyzer class detecting weak words in an English sentence.
    """
    test_sentence = "I am a text for analysis with the weak word, accordingly."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.WEAKWORD
    expected_finding_count = 1
    expected_finding_message_content = "accordingly"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.ENGLISH)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be weakword
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 weakword should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain the weakword
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_complexity_en():
    """
    Test case for the TextAnalyzer class detecting complexity in an English sentence.
    """
    test_sentence = (
        "I am a long and complex text for analysis without any meaning, besides beeing long and tedious to read, but with many words, which make it only difficult, and some subordinate clauses, to add complexity and confuse the reader."
    )

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.COMPLEX
    expected_finding_count = 1
    expected_finding_message_content = "too complex"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.ENGLISH)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be complex
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 complexity finding should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain "too complex"
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_comparative_en():
    """
    Test case for the TextAnalyzer class detecting comparative in an English sentence.
    """
    test_sentence = "I am a text for analysis with a comparative that compares that apples are better then pears."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.COMPARATIVE
    expected_finding_count = 1
    expected_finding_message_content = f"{MatcherId.COMPARATIVE_MATCHER_ID.value} better"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.ENGLISH)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be comparative
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 comparative should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain the comparative word
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_superlative_en():
    """
    Test case for the TextAnalyzer class detecting superlative in an English sentence.
    """
    test_sentence = "I am a text for analysis with a superlative that apples are the best of all fruits."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.COMPARATIVE
    expected_finding_count = 1
    expected_finding_message_content = f"{MatcherId.SUPERLATIVE_MATCHER_ID.value} best"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.ENGLISH)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be comparative
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 comparative should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain the comparative word
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_passive_en():
    """
    Test case for the TextAnalyzer class detecting passive voice in an English sentence.
    """
    test_sentence = "This is a text for analysis that is written with a passive voice."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.PASSIVE
    expected_finding_count = 1
    expected_finding_message_content = ""

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.ENGLISH)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be passive
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 passive voice sentence should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message currently has only a range (should maybe be reworked)
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


######################################################
# TESTS FOR GERMAN
######################################################


def test_text_analyzer_find_nothing_de():
    """
    Test case for the TextAnalyzer class when no issues are detected in a German sentence.
    """
    test_sentence = "Ich bin ein Text zur Analyse ohne Ergebnisse."

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.GERMAN)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    assert not result


def test_text_analyzer_find_weak_words_de():
    """
    Test case for the TextAnalyzer class detecting weak words in a German sentence.
    """
    test_sentence = "Ich bin ein Text zur Analyse mit einem Weakword, entsprechend."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.WEAKWORD
    expected_finding_count = 1
    expected_finding_message_content = "entsprechend"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.GERMAN)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be weakword
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 weakword should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain the weakword
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_complexity_de():
    """
    Test case for the TextAnalyzer class detecting complexity in a German sentence.
    """
    test_sentence = (
        "Ich bin ein komplexer und komplizierter Analysetext, voll mit Wörtern, um die Lesbarkeit zu erschweren, und Nebensätzen, "
        "die dank Ausschweifungen den Satz in die Länge ziehen, und Wiederholungen, wie das ich voll mit Wörtern bin oder viele Nebensätze habe."
    )

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.COMPLEX
    expected_finding_count = 1
    expected_finding_message_content = "too complex"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.GERMAN)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be complex
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 complexity finding should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain "too complex"
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_comparative_de():
    """
    Test case for the TextAnalyzer class detecting comparative in a German sentence.
    """
    test_sentence = "Ich bin ein Text zur Analyse mit einem Vergleich, dass Äpfel besser sind als Birnen."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.COMPARATIVE
    expected_finding_count = 1
    expected_finding_message_content = f"{MatcherId.COMPARATIVE_MATCHER_ID.value} besser"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.GERMAN)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be comparative
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 comparative should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain the comparative word
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_superlative_de():
    """
    Test case for the TextAnalyzer class detecting superlative in a German sentence.
    """
    test_sentence = "Ich bin ein Analysetext mit dem Superlativ, dass Äpfel die besten aller Früchte sind."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.COMPARATIVE
    expected_finding_count = 1
    expected_finding_message_content = f"{MatcherId.SUPERLATIVE_MATCHER_ID.value} besten"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.GERMAN)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be comparative
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 comparative should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain the comparative word
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_passive_de():
    """
    Test case for the TextAnalyzer class detecting passive voice in a German sentence.
    """
    test_sentence = "Dies ist ein Analysetext, der im Passiv geschrieben ist."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.PASSIVE
    expected_finding_count = 1
    expected_finding_message_content = ""

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.GERMAN)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_DESCRIPTION_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be passive
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 passive voice sentence should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message currently has only a range (should maybe be reworked)
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


def test_text_analyzer_find_processword_de():
    """
    Test case for the TextAnalyzer class detecting a process word in a German sentence.
    """
    test_sentence = "Ich bin ein Analysetext, mit einem Processwort zum Auswählen."

    # init expected result
    expected_result_count = 1
    expected_finding_type = FindingType.PROCESS
    expected_finding_count = 1
    expected_finding_message_content = "auswählen"

    # run method
    test_analyzer = text_analyzer.TextAnalyzer(constants.GERMAN)
    result = test_analyzer.analyze_text(test_sentence, constants.DEFAULT_TITLE_CHECKS)

    # check results
    # only 1 finding should be found
    assert len(result) == expected_result_count

    # finding should be process word
    result_tuple = result[0]
    assert expected_finding_type == result_tuple.finding_type

    # only 1 process word should be found
    result_finding_count = result_tuple.finding_count
    assert result_finding_count == expected_finding_count

    # finding message should contain the process word (only lower case)
    result_finding_desc = result_tuple.finding_desc
    assert expected_finding_message_content in result_finding_desc


if __name__ == "__main__":
    test_text_analyzer_find_weak_words_en()
