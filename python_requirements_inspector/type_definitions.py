from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


class WorkItem(TypedDict):
    id: str | None
    title: str
    description: str
    language: str | None


class WorkItemFields(Enum):
    ID = "id"
    TITLE = "title"
    DESCRIPTION = "description"
    LANGUAGE = "language"


class RequirementsInspectorResponseItem(TypedDict):
    id: str | None
    language: str | None
    smellComplex: int
    smellPassive: int
    smellWeakword: int
    smellComparative: int
    missingProcessword: bool
    smellDescription: str


class FindingType(Enum):
    COMPLEX = "smellComplex"
    PASSIVE = "smellPassive"
    WEAKWORD = "smellWeakword"
    COMPARATIVE = "smellComparative"
    PROCESS = "missingProcessword"


class MatcherId(Enum):
    WEAKWORD_MATCHER_ID = "Weakwords"
    PROCESSWORD_MATCHER_ID = "Processwords"
    PASSIVE_MATCHER_ID = "Passive"
    COMPARATIVE_MATCHER_ID = "Comparative"
    SUPERLATIVE_MATCHER_ID = "Superlative"
    RELEVANT_WORDS_MATCHER_ID = "Relevant"
    ALL_WORDS_MATCHER_ID = "All"


@dataclass
class Finding:
    sent_num: int | None
    sent_start: str | None
    finding_type: FindingType
    finding_count: int
    finding_desc: str


@dataclass
class PartialFinding:
    finding_type: FindingType
    finding_count: int
    finding_desc: str
