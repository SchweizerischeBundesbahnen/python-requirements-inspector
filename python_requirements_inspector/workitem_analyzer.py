"""
Implementation of workitem analyzer
"""

from python_requirements_inspector import constants
from python_requirements_inspector.lang_detector import LangDetector
from python_requirements_inspector.text_analyzer import TextAnalyzer
from python_requirements_inspector.type_definitions import Finding, FindingType, RequirementsInspectorResponseItem, WorkItem, WorkItemFields


class WorkitemAnalyzer:
    """
    A class for analyzing workitems and generating a dataframes of all findings.
    """

    def __init__(self) -> None:
        """
        Initializes a WorkitemAnalyzer object.
        """

        self.__available_text_analyzer: dict[str, TextAnalyzer] = {}
        for lang in constants.SUPPORTED_LANGUAGES:
            self.__available_text_analyzer[lang] = TextAnalyzer(lang)
        self.__language_detector = LangDetector()
        self.__text_checks = constants.DEFAULT_DESCRIPTION_CHECKS
        self.__data: list[RequirementsInspectorResponseItem] = []

    def __validate_language(self, workitem: WorkItem) -> None:
        """
        Validates the language of the workitem using language detection if not provided.

        Parameters:
            workitem (dict): A dictionary representing the workitem.

        """

        lang = workitem.get("language")
        desc = workitem.get("description")
        if not lang:
            lang = self.__language_detector.detect_language(desc)
            workitem["language"] = lang

    @staticmethod
    def __get_initialized_data_frame(workitem: WorkItem) -> RequirementsInspectorResponseItem:
        """
        Returns an initialized data frame for a given workitem.

        Parameters:
            workitem (dict): A dictionary representing the workitem data.

        Returns:
            dict: An initialized data frame.

        """
        data_frame = constants.INITIALIZED_DATA_FRAME.copy()
        data_frame["id"] = workitem.get("id")
        data_frame["language"] = workitem.get("language")
        return data_frame

    def __process_findings(self, data_frame: RequirementsInspectorResponseItem, findings: list[Finding], text_section: str) -> None:
        """
        Processes the findings returned by the analyse_text method and updates the data frame.

        Parameters:
            data_frame (dict): A data frame representing the analyzed workitem.
            findings (list): A list of namedtuple findings (defined in constants).
            text_section (str): The section of the workitem where analysis was performed on.

        """

        for finding in findings:
            # update smell description
            smell_desc = self.__generate_smell_description(text_section, finding)
            data_frame["smellDescription"] += smell_desc

            # update counter
            match finding.finding_type:
                case FindingType.COMPLEX:
                    data_frame["smellComplex"] += finding.finding_count
                case FindingType.WEAKWORD:
                    data_frame["smellWeakword"] += finding.finding_count
                case FindingType.PASSIVE:
                    data_frame["smellPassive"] += finding.finding_count
                case FindingType.COMPARATIVE:
                    data_frame["smellComparative"] += finding.finding_count

    def __process_title_findings(self, data_frame: RequirementsInspectorResponseItem, findings: list[Finding] | None) -> None:
        """
        Processes the findings of the title returned by the analyse_text method and updates the data frame.

        Parameters:
            data_frame (dict): A data frame representing the analyzed workitem.
            findings (list): A list of namedtuple findings (defined in constants).

        """
        if not findings:
            # generate finding
            finding = Finding(None, None, FindingType.PROCESS, 1, "Title contains no process word")

            # update smell description
            smell_desc = self.__generate_smell_description(WorkItemFields.TITLE.value, finding)
            data_frame["smellDescription"] += smell_desc

            if finding.finding_type == FindingType.PROCESS:
                data_frame["missingProcessword"] = True

    @staticmethod
    def __generate_smell_description(text_section: str, finding: Finding) -> str:
        """
        Generates a smell description based on the analysis result.

        Parameters:
            text_section (str): The section of the workitem where analysis was performed on.
            finding (namedtuple): A namedtuple representing a detected finding (defined in constants).

        Returns:
            str: The generated smell description.

        """

        if not finding.sent_num or not finding.sent_start:
            smell_desc = f"In {text_section.upper()} {finding.finding_type.value}: {finding.finding_desc}\n"
        else:
            smell_desc = f"In {text_section.upper()} Sentence {finding.sent_num} {finding.sent_start.strip()}… {finding.finding_type.value}: {finding.finding_desc}\n"
        return smell_desc

    @staticmethod
    def __get_remaining_fields(workitem: WorkItem) -> list[str]:
        """
        Get a list of fields in the workitem that are not part of the default input fields.

        Parameters:
            workitem (dict): The dictionary representing the workitem.

        Returns:
            list: A list of field names that are not part of the default input fields.

        """
        return list(set(workitem.keys()).difference(WorkItem.__annotations__.keys()))

    def analyze_workitem(self, workitem: WorkItem) -> None:
        """
        Analyzes all data from the given workitem (excluding id and language).

        Parameters:
            workitem (dict): A dictionary representing the workitem data.

        """

        self.__validate_language(workitem)
        data_frame = self.__get_initialized_data_frame(workitem)

        desc = workitem.get("description")
        title = workitem.get("title")
        lang = workitem.get("language")
        additional_fields_to_check = self.__get_remaining_fields(workitem)

        text_analyzer = self.__available_text_analyzer.get(lang) if lang is not None else None

        if text_analyzer is None:
            return

        # If title is empty doesn't analyze
        # It is empty when it is parametrized to not analyze it
        if title:
            findings = text_analyzer.analyze_text(title, constants.DEFAULT_TITLE_CHECKS)
            self.__process_title_findings(data_frame, findings)

        # If description is empty doesn't analyze
        # Can be empty if it is parametrized to not analyze it
        if desc:
            findings = text_analyzer.analyze_text(desc, self.__text_checks)
            self.__process_findings(data_frame, findings, WorkItemFields.DESCRIPTION.value)

        # check all fields that are not description or title
        for field in additional_fields_to_check:
            field_content = str(workitem.get(field))
            findings = text_analyzer.analyze_text(field_content, self.__text_checks)
            self.__process_findings(data_frame, findings, field)

        self.__data.append(data_frame)

    def get_collected_data(self) -> list[RequirementsInspectorResponseItem]:
        """
        Returns the collected analyzed data.

        Returns:
            list: A list containing data frames (dictonary) with analyzed workitem information.

        """

        return self.__data
