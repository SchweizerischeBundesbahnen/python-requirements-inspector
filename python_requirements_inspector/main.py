"""
Application entry point
"""

import argparse
import json
import tempfile
from pathlib import Path

from python_requirements_inspector.workitem_analyzer import WorkitemAnalyzer


def main(json_path: str) -> str:
    """
    Main function for analyzing workitem data from a JSON file.
    Writes all findings to another jsonfile and prints the path.

    Parameters:
        json_path (str): Path to the JSON file containing workitem data.
    Returns:
        str: Path to the generated output JSON file.
    """

    # Read input data from the provided JSON file
    with Path(json_path).open(encoding="utf-8") as json_file:
        input_data = json.load(json_file)

    workitem_analyzer = WorkitemAnalyzer()

    # Process all workitems
    for workitem in input_data:
        workitem_analyzer.analyze_workitem(workitem)

    output_data = workitem_analyzer.get_collected_data()

    # Write data back to stdout in csv format.
    with tempfile.NamedTemporaryFile(prefix="output_", suffix=".json", delete=False, mode="w+", encoding="utf-8") as output_file:
        json.dump(output_data, output_file)
        output_file.flush()

    return output_file.name


def run() -> None:
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="Analyses workitem data provided by a json file.")
    parser.add_argument("jsonfile", type=str, help="path to the json file")

    # Parse the command-line arguments
    args = parser.parse_args()
    json_file_path = args.jsonfile

    print(main(json_file_path))


if __name__ == "__main__":
    run()
