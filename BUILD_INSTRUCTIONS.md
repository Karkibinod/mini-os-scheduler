# Building and Publishing mini-os-scheduler to PyPI

This guide provides step-by-step instructions for building, testing, and publishing the `mini-os-scheduler` package to PyPI.

## Prerequisites

1. **Python 3.7+** installed
2. **pip** and **setuptools** up to date:
   ```bash
   pip install --upgrade pip setuptools wheel
   ```
3. **twine** for uploading to PyPI:
   ```bash
   pip install twine
   ```
4. **PyPI Account**: Create accounts at:
   - Test PyPI: https://test.pypi.org/account/register/
   - Production PyPI: https://pypi.org/account/register/

## Step 1: Verify Package Metadata

Verify the following in `pyproject.toml`:

1. **Author information**: Check author name and email
2. **Repository URLs**: Verify GitHub URLs are correct
3. **Version number**: Update `version = "0.1.0"` for new releases

## Step 2: Install in Development Mode

Test the package locally before building:

```bash
# Navigate to project root
cd "/Users/binod/Desktop/JOB/MINI OS CPU SCHEDULER"

# Install in editable/development mode
pip install -e .

# Test the CLI command
mini-scheduler --sample --algorithm fcfs

# Test with web dashboard (optional)
pip install -e ".[web]"
python -m mini_os_scheduler.web.app
```

## Step 3: Run Tests

Ensure all tests pass:

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=mini_os_scheduler --cov-report=html
```

## Step 4: Build the Package

Build source distribution and wheel:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build package
python -m build

# This creates:
# - dist/mini_os_scheduler-0.1.0.tar.gz (source distribution)
# - dist/mini_os_scheduler-0.1.0-py3-none-any.whl (wheel)
```

## Step 5: Verify the Build

Check the built package:

```bash
# List files in the distribution
tar -tzf dist/mini_os_scheduler-0.1.0.tar.gz

# Check the wheel contents
unzip -l dist/mini_os_scheduler-0.1.0-py3-none-any.whl
```

## Step 6: Test on Test PyPI (Recommended)

Upload to Test PyPI first to verify everything works:

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# You'll be prompted for:
# - Username: __token__
# - Password: Your Test PyPI API token (pypi-...)
```

**Get Test PyPI API Token:**
1. Go to https://test.pypi.org/manage/account/
2. Scroll to "API tokens"
3. Create a new token with scope "Entire account"
4. Copy the token (starts with `pypi-`)

**Test Installation from Test PyPI:**

```bash
# Create a clean virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ mini-os-scheduler

# Test the command
mini-scheduler --sample --algorithm all
```

## Step 7: Upload to Production PyPI

Once verified on Test PyPI, upload to production:

```bash
# Upload to PyPI
twine upload dist/*

# You'll be prompted for:
# - Username: __token__
# - Password: Your PyPI API token (pypi-...)
```

**Get PyPI API Token:**
1. Go to https://pypi.org/manage/account/
2. Scroll to "API tokens"
3. Create a new token with scope "Entire account"
4. Copy the token (starts with `pypi-`)

## Step 8: Verify Installation

Test installation from PyPI:

```bash
# Create a clean virtual environment
python -m venv verify_env
source verify_env/bin/activate  # On Windows: verify_env\Scripts\activate

# Install from PyPI
pip install mini-os-scheduler

# Test the command
mini-scheduler --sample --algorithm all

# Test with web dashboard
pip install "mini-os-scheduler[web]"
python -m mini_os_scheduler.web.app
```

## Versioning Guide

To release a new version:

1. **Update version in `pyproject.toml`**:
   ```toml
   version = "0.2.0"  # Increment as needed
   ```

2. **Update version in `mini_os_scheduler/__init__.py`**:
   ```python
   __version__ = "0.2.0"
   ```

3. **Create a git tag** (optional but recommended):
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

4. **Rebuild and upload**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   twine upload dist/*
   ```

### Version Numbering (Semantic Versioning)

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

Examples:
- `0.1.0` → `0.1.1` (bug fix)
- `0.1.1` → `0.2.0` (new feature)
- `0.2.0` → `1.0.0` (major release, stable API)

## Troubleshooting

### Common Issues

1. **"Package already exists"**
   - Version number must be unique
   - Increment version in `pyproject.toml`

2. **"Invalid distribution"**
   - Check `MANIFEST.in` includes all necessary files
   - Verify `pyproject.toml` syntax

3. **"Module not found" after installation**
   - Check package structure in `pyproject.toml`
   - Verify `__init__.py` files exist

4. **CLI command not found**
   - Verify `[project.scripts]` in `pyproject.toml`
   - Reinstall package: `pip install -e .`

## Quick Reference Commands

```bash
# Development
pip install -e .
mini-scheduler --sample --algorithm all

# Testing
pytest tests/ -v

# Building
python -m build

# Uploading to Test PyPI
twine upload --repository testpypi dist/*

# Uploading to PyPI
twine upload dist/*

# Clean build artifacts
rm -rf dist/ build/ *.egg-info
```

## Post-Publication Checklist

- [ ] Package installs successfully from PyPI
- [ ] CLI command works: `mini-scheduler --help`
- [ ] All algorithms run correctly
- [ ] Web dashboard works (if installed with `[web]` extra)
- [ ] README displays correctly on PyPI
- [ ] Update GitHub repository with PyPI badge
- [ ] Create release notes/CHANGELOG

## PyPI Badge for README

Add this to your README.md:

```markdown
[![PyPI version](https://badge.fury.io/py/mini-os-scheduler.svg)](https://badge.fury.io/py/mini-os-scheduler)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
```

