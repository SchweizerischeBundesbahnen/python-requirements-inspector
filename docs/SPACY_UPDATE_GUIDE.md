# spaCy Update Guide

## Overview

This project uses spaCy for natural language processing with German and English language models. Due to the tight coupling between spaCy core and its language models, updates need to be coordinated.

## Dependency Structure

- **Python Version**: Must be compatible with spaCy requirements
- **spaCy Core**: Main NLP library (`spacy` package)
- **Language Models**:
  - German: `de_core_news_md`
  - English: `en_core_web_md`
- **Additional**: `spacy-language-detection` for automatic language detection

## Version Compatibility

⚠️ **Important**: All components must be compatible:

1. **Python Version**: spaCy versions have specific Python requirements
   - spaCy 3.7.x: Python >=3.7
   - spaCy 3.8.x: Python >=3.8, limited Python 3.13 support

2. **spaCy & Language Models**: Models MUST match spaCy's major.minor version
   - spaCy 3.7.x requires language models 3.7.x
   - spaCy 3.8.x requires language models 3.8.x

## Automated Updates with Renovate

The `renovate.json` configuration groups spaCy-related updates together:

1. **Package Grouping**: Python version + spaCy packages + language models grouped as "spaCy ecosystem"
2. **Custom Regex Manager**: Detects and updates language model URLs in `pyproject.toml`
3. **Coordinated Updates**: Updates all components together including Python version

### Current Limitations

- spaCy language models require matching versions with spaCy core
- Language model URLs in `pyproject.toml` need custom regex manager handling
- Python version constraints may affect compatibility
- Configuration uses modern Renovate syntax (auto-migrated)

## Manual Update Process

When Renovate cannot handle updates automatically:

### 1. Check Latest Versions

```bash
# Check latest spaCy version
curl -s https://pypi.org/pypi/spacy/json | jq -r '.info.version'

# Check available language models
curl -s "https://api.github.com/repos/explosion/spacy-models/releases?per_page=100" | \
  jq -r '.[] | select(.tag_name | test("^(de_core_news_md|en_core_web_md)-3.8")) | .tag_name'
```

### 2. Update pyproject.toml

Update the following sections:

```toml
[tool.poetry.dependencies]
python = ">=3.12,<3.14"  # Check spaCy's Python compatibility
spacy = "3.8.7"  # Update to latest version
de-core-news-md = { url = "https://github.com/explosion/spacy-models/releases/download/de_core_news_md-3.8.0/de_core_news_md-3.8.0-py3-none-any.whl" }
en-core-web-md = { url = "https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.8.0/en_core_web_md-3.8.0-py3-none-any.whl" }
```

### 3. Update Dependencies

```bash
# Update Poetry lock file
poetry lock

# Install updated dependencies
poetry install --all-extras

# Run tests
poetry run tox

# Run pre-commit hooks
poetry run pre-commit run -a
```

### 4. Verify Compatibility

```bash
# Test language detection
poetry run python -c "import spacy; nlp = spacy.load('de_core_news_md'); print(nlp('Test'))"
poetry run python -c "import spacy; nlp = spacy.load('en_core_web_md'); print(nlp('Test'))"
```

## Python Version Compatibility

### Current Status (2025)

- Python 3.12: Fully supported
- Python 3.13: Limited support (installation issues on some platforms)

As of early 2025, consider maintaining `python = ">=3.12,<3.13"` until spaCy fully supports Python 3.13. Always check the [latest spaCy compatibility documentation](https://spacy.io/usage#python) for current Python version support before updating.

## Troubleshooting

### Installation Failures

If installation fails after updating:

1. Check Python version compatibility
2. Verify language model versions match spaCy version
3. Clear Poetry cache: `poetry cache clear pypi --all`
4. Try downgrading to previous stable versions

### Model Loading Errors

If models fail to load:

1. Ensure model version matches spaCy version
2. Reinstall models: `poetry install --all-extras`
3. Check model URLs are correct in `pyproject.toml`

## References

- [spaCy Releases](https://github.com/explosion/spacy/releases)
- [spaCy Models](https://github.com/explosion/spacy-models/releases)
- [spaCy Compatibility](https://spacy.io/usage/models#model-versioning)
- [Renovate Documentation](https://docs.renovatebot.com/)
