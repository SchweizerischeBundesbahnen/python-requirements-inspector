# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library for analyzing functional and non-functional requirements written in English or German. It uses spaCy for natural language processing to detect code smells in requirement texts, including:

- Complex sentences
- Weak words usage
- Non-passive voice
- Comparative/superlative language
- Missing process words

## Development Commands

### Setup
```bash
# Install dependencies (including all groups)
uv sync --all-groups
```

### Code Quality and Testing
```bash
# Run all pre-commit hooks (includes formatting, linting, type checking)
uv run pre-commit run -a

# Run tests with coverage (minimum 90% required)
uv run tox

# Run specific test environments
uv run tox -e lint    # Linting and type checking only
uv run tox -e py313   # Tests with coverage

# Manual linting and formatting
uv run ruff format
uv run ruff check
uv run mypy .
```

### Build
```bash
uv build
```

### Run the Application
```bash
uv run inspect-requirements path/to/input.json
```

## Code Architecture

### Core Components

- **WorkitemAnalyzer** (`workitem_analyzer.py`): Main orchestrator that processes workitems and coordinates analysis
- **TextAnalyzer** (`text_analyzer.py`): Handles text analysis for specific languages using spaCy
- **LangDetector** (`lang_detector.py`): Detects language of text if not provided
- **TextProcessor** (`text_processor.py`): Processes text using spaCy models

### Checker System

The `checkers/` directory contains specialized analyzers:
- **ComplexChecker**: Analyzes sentence complexity
- **WeakWordChecker**: Detects weak/filler words
- **PassiveChecker**: Identifies passive voice usage
- **ComparativeChecker**: Finds comparative/superlative language
- **ProcessWordChecker**: Validates presence of process words in titles

### Data Flow

1. JSON input with workitems (id, title, description, language)
2. Language detection if not provided
3. Text analysis using appropriate spaCy model (German/English)
4. Multiple checker passes for different smell types
5. Results aggregated in RequirementsInspectorResponseItem format
6. Output written to temporary JSON file

### Key Files

- `type_definitions.py`: TypedDict definitions for WorkItem and response structures
- `constants.py`: Configuration constants and supported languages
- `main.py`: CLI entry point with argument parsing

## Development Notes

- Python 3.13 only (strict version requirement: >=3.13,<3.14)
- Uses uv for dependency management
- Requires spaCy language models for German and English
- Pre-commit hooks enforce code quality (ruff, mypy, security checks)
- Tests require 90% minimum coverage
- SonarCloud integration for code quality monitoring

## Testing

Tests are located in `tests/` directory and use pytest. Coverage reports are generated in XML format for CI/CD integration.