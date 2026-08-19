"""Tests."""

import json
import sys
import tempfile
from contextlib import chdir
from pathlib import Path
from unittest.mock import patch

import pytest

from python_requirements_inspector import main
from python_requirements_inspector.type_definitions import WorkItem

TEST_DATA = [
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


def test_main():
    """
    Test function for the main application logic.
    """

    # write test data to json file
    with tempfile.NamedTemporaryFile(prefix="test_", suffix=".json", delete=False, mode="w+", encoding="utf-8") as input_json_file, chdir(Path(input_json_file.name).parent):
        json.dump(TEST_DATA, input_json_file)
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


def test_main_non_relative_path(tmp_path: Path):
    """
    Test function for the main application logic when the input path is absolute and outside the cwd.
    """

    # write test data to a json file outside the working directory
    outside_json_file = tmp_path / "outside.json"
    outside_json_file.write_text(json.dumps(TEST_DATA), encoding="utf-8")

    work_dir = tmp_path / "work"
    work_dir.mkdir()

    # execute main with the absolute path of the json file outside the working directory
    with chdir(work_dir), pytest.raises(ValueError, match="Input path not relative to CWD"):
        _ = main.main(str(outside_json_file))


def test_main_traversal_path(tmp_path: Path):
    """
    Test function for the main application logic when the input path escapes the cwd via '..'.
    """

    # write test data to a json file outside the working directory
    outside_json_file = tmp_path / "outside.json"
    outside_json_file.write_text(json.dumps(TEST_DATA), encoding="utf-8")

    work_dir = tmp_path / "work"
    work_dir.mkdir()

    # execute main with a relative path traversing out of the working directory
    with chdir(work_dir), pytest.raises(ValueError, match="Input path not relative to CWD"):
        _ = main.main(str(Path("..") / outside_json_file.name))


def test_run_reports_non_relative_path(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    """
    Test function for the command-line entry point when the input path is outside the cwd.
    """

    outside_json_file = tmp_path / "outside.json"
    outside_json_file.write_text(json.dumps(TEST_DATA), encoding="utf-8")

    work_dir = tmp_path / "work"
    work_dir.mkdir()

    # the entry point exits with argparse's usage error instead of raising a traceback
    with chdir(work_dir), patch.object(sys, "argv", ["inspect-requirements", str(outside_json_file)]), pytest.raises(SystemExit) as exit_info:
        main.run()

    expected_exit_code = 2

    assert exit_info.value.code == expected_exit_code
    assert "Input path not relative to CWD" in capsys.readouterr().err
