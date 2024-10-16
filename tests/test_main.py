"""Tests."""

import json
import tempfile
from pathlib import Path

from python_requirements_inspector import main
from python_requirements_inspector.type_definitions import WorkItem


def test_main():
    """
    Test function for the main application logic.
    """

    # init test workitem
    test_data = [
        WorkItem(
            id="test-123",
            description="I'm a description for testing with a weakword accordingly",
            title="I'm a title without a processword",
            language="en",
        ),
        WorkItem(
            id="test-234",
            description="öüäß Ich bin eine Beschreibung mit dem Weakword entsprechend und Umlauts.",
            title="Ich bin ein Titel ohne Processwort",
            language="de",
        ),
    ]

    # write test data to json file
    with tempfile.NamedTemporaryFile(prefix="test_", suffix=".json", delete=False, mode="w+", encoding="utf-8") as input_json_file:
        json.dump(test_data, input_json_file)
        input_json_file.flush()

    # execute main with json file
    output_file_path = main.main(input_json_file.name)

    # read output json file
    with Path(output_file_path).open(encoding="utf-8") as output_json_file:
        output_data = json.load(output_json_file)

    # delete json files
    Path(input_json_file.name).unlink()
    Path(output_json_file.name).unlink()

    expected_dataset_count = 2

    # check if outfile has a entry per data set
    assert len(output_data) == expected_dataset_count
    assert "öüäß" in output_data[1]["smellDescription"]
