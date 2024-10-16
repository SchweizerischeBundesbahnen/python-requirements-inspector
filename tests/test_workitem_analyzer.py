"""Tests."""

from python_requirements_inspector import workitem_analyzer
from python_requirements_inspector.type_definitions import FindingType, WorkItem, WorkItemFields


def test_workitem_analyzer_with_findings_en():
    """
    Test the workitem analyzer with findings for English workitems.
    """

    # init test workitem
    test_workitem = WorkItem(
        id="test-123",
        description="I'm a description for testing with a weakword accordingly",
        title="I'm a title without a processword",
        language="en",
    )

    # init expected result
    expected_result_count = 1
    expected_result_id = test_workitem["id"]
    expected_finding_count = 2
    expected_finding_types = [FindingType.WEAKWORD.value, FindingType.PROCESS.value]
    expected_finding_sections = [WorkItemFields.DESCRIPTION.value.upper(), WorkItemFields.TITLE.value.upper()]
    expected_finding_values = {
        FindingType.WEAKWORD.value: 1,
        FindingType.COMPLEX.value: 0,
        FindingType.COMPARATIVE.value: 0,
        FindingType.PASSIVE.value: 0,
        FindingType.PROCESS.value: True,
    }

    # run method
    test_workitem_analyzer = workitem_analyzer.WorkitemAnalyzer()
    test_workitem_analyzer.analyze_workitem(test_workitem)
    results = test_workitem_analyzer.get_collected_data()

    # check results
    # only 1 workitem was given so only one result should be returned
    assert len(results) == expected_result_count

    # check if the workitem id of the result is equal to the given one
    result_dict = results[0]
    assert result_dict["id"] == expected_result_id

    # split Smell description in a list of entries
    result_smell_description_list = result_dict["smellDescription"].split("\n")
    result_smell_description_list = list(filter(None, result_smell_description_list))  # remove empty entries
    # check if only 2 findings where found
    assert len(result_smell_description_list) == expected_finding_count

    # check if the findings are of the expected types
    for expected_type in expected_finding_types:
        assert any(expected_type in line for line in result_smell_description_list)

    # check if the findings are marked for the expected sections
    for expected_section in expected_finding_sections:
        assert any(expected_section in line for line in result_smell_description_list)

    # check if all values are set to the expected values
    for key, expected_value in expected_finding_values.items():
        assert result_dict[key] == expected_value


def test_workitem_analyzer_with_findings_de():
    """
    Test the workitem analyzer with findings for German workitems.
    """

    # init test workitem
    test_workitem = WorkItem(
        id="test-234",
        description="Ich bin eine Beschreibung mit dem Weakword entsprechend.",
        title="Ich bin ein Titel ohne Processwort",
        language="de",
    )

    # init expected result
    expected_result_count = 1
    expected_result_id = test_workitem["id"]
    expected_finding_count = 2
    expected_finding_types = [FindingType.WEAKWORD.value, FindingType.PROCESS.value]
    expected_finding_sections = ["DESCRIPTION", "TITLE"]
    expected_finding_values = {
        FindingType.WEAKWORD.value: 1,
        FindingType.COMPLEX.value: 0,
        FindingType.COMPARATIVE.value: 0,
        FindingType.PASSIVE.value: 0,
        FindingType.PROCESS.value: True,
    }

    # run method
    test_workitem_analyzer = workitem_analyzer.WorkitemAnalyzer()
    test_workitem_analyzer.analyze_workitem(test_workitem)
    results = test_workitem_analyzer.get_collected_data()

    # check results
    # only 1 workitem was given so only one result should be returned
    assert len(results) == expected_result_count

    # check if the workitem id of the result is equal to the given one
    result_dict = results[0]
    assert result_dict["id"] == expected_result_id

    # split Smell description in a list of entries
    result_smell_description_list = result_dict["smellDescription"].split("\n")
    result_smell_description_list = list(filter(None, result_smell_description_list))  # remove empty entries
    # check if only 2 findings where found
    assert len(result_smell_description_list) == expected_finding_count

    # check if the findings are of the expected types
    for expected_type in expected_finding_types:
        assert any(expected_type in line for line in result_smell_description_list)

    # check if the findings are marked for the expected sections
    for expected_section in expected_finding_sections:
        assert any(expected_section in line for line in result_smell_description_list)

    # check if all values are set to the expected values
    for key, expected_value in expected_finding_values.items():
        assert result_dict[key] == expected_value


def test_workitem_analyzer_without_title():
    """
    Test the workitem analyzer with findings but without a title.
    """

    # init test workitem
    test_workitem = WorkItem(
        id="test-123",
        description="I'm a description for testing with a weakword accordingly",
        language="en",
    )

    # init expected result
    expected_finding_count = 1
    expected_finding_types = [FindingType.WEAKWORD.value]
    expected_finding_sections = ["DESCRIPTION"]
    expected_finding_values = {
        FindingType.WEAKWORD.value: 1,
        FindingType.COMPLEX.value: 0,
        FindingType.COMPARATIVE.value: 0,
        FindingType.PASSIVE.value: 0,
        FindingType.PROCESS.value: False,
    }

    # run method
    test_workitem_analyzer = workitem_analyzer.WorkitemAnalyzer()
    test_workitem_analyzer.analyze_workitem(test_workitem)
    results = test_workitem_analyzer.get_collected_data()

    # check results
    result_dict = results[0]

    # split Smell description in a list of entries
    result_smell_description = result_dict["smellDescription"]
    result_smell_description_list = result_smell_description.split("\n")
    result_smell_description_list = list(filter(None, result_smell_description_list))  # remove empty entries
    # check if only 1 finding where found
    assert len(result_smell_description_list) == expected_finding_count

    # check if the findings are of the expected types
    for expected_type in expected_finding_types:
        assert any(expected_type in line for line in result_smell_description_list)

    # check if the findings are marked for the expected sections
    for expected_section in expected_finding_sections:
        assert any(expected_section in line for line in result_smell_description_list)

    # check if all values are set to the expected values
    for key, expected_value in expected_finding_values.items():
        assert result_dict[key] == expected_value


def test_workitem_analyzer_with_additional_fields():
    """
    Test the workitem analyzer with findings in additional custom fields.
    """

    # init test workitem
    test_workitem = WorkItem(
        id="test-123",
        description="I'm a description for testing with a weakword accordingly",
        title="I'm a title without a processword",
        language="en",
    )
    test_workitem["testfield1"] = "I'm a customfield with text with a weakword automatically"
    test_workitem["testfield2"] = "I'm another customfield with text that is written with a passive voice."

    # init expected result
    expected_finding_count = 4
    expected_finding_types = [FindingType.WEAKWORD.value]
    expected_finding_sections = ["DESCRIPTION", "TITLE", "testfield1".upper(), "testfield2".upper()]
    expected_finding_values = {
        FindingType.WEAKWORD.value: 2,
        FindingType.COMPLEX.value: 0,
        FindingType.COMPARATIVE.value: 0,
        FindingType.PASSIVE.value: 1,
        FindingType.PROCESS.value: True,
    }

    # run method
    test_workitem_analyzer = workitem_analyzer.WorkitemAnalyzer()
    test_workitem_analyzer.analyze_workitem(test_workitem)
    results = test_workitem_analyzer.get_collected_data()

    # check results
    result_dict = results[0]

    # split Smell description in a list of entries
    result_smell_description = result_dict["smellDescription"]
    result_smell_description_list = result_smell_description.split("\n")
    result_smell_description_list = list(filter(None, result_smell_description_list))  # remove empty entries
    # check if only 1 finding where found
    assert len(result_smell_description_list) == expected_finding_count

    # check if the findings are of the expected types
    for expected_type in expected_finding_types:
        assert any(expected_type in line for line in result_smell_description_list)

    # check if the findings are marked for the expected sections
    for expected_section in expected_finding_sections:
        assert any(expected_section in line for line in result_smell_description_list)

    # check if all values are set to the expected values
    for key, expected_value in expected_finding_values.items():
        assert result_dict[key] == expected_value


if __name__ == "__main__":
    test_workitem_analyzer_with_findings_en()
