"""
Summary of all application constants
"""

from python_requirements_inspector.type_definitions import FindingType, RequirementsInspectorResponseItem

# Complexity threshold for when a text is too complex
TOO_LONG = 38
TOO_MUCH = 19

# Language Ids
GERMAN = "de"
ENGLISH = "en"
SUPPORTED_LANGUAGES = [GERMAN, ENGLISH]

DEFAULT_DESCRIPTION_CHECKS = [FindingType.COMPLEX, FindingType.PASSIVE, FindingType.WEAKWORD, FindingType.COMPARATIVE]
DEFAULT_TITLE_CHECKS = [FindingType.PROCESS]


INITIALIZED_DATA_FRAME = RequirementsInspectorResponseItem(
    id="",
    language="",
    smellDescription="",
    smellComplex=0,
    smellPassive=0,
    smellWeakword=0,
    smellComparative=0,
    missingProcessword=False,
)
