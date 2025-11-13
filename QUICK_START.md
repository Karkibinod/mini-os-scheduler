# Quick Start Guide - Publishing to PyPI

## 🚀 Fast Track to PyPI

### Step 1: Verify Package Information

Verify `pyproject.toml` has correct:
- Author name and email
- GitHub repository URLs
- Version number

### Step 2: Install Build Tools

```bash
pip install --upgrade pip setuptools wheel build twine
```

### Step 3: Test Locally

```bash
# Install in development mode
pip install -e .

# Test CLI
mini-scheduler --sample --algorithm all

# Test web dashboard (optional)
pip install -e ".[web]"
python -m mini_os_scheduler.web.app
```

### Step 4: Run Tests

```bash
pip install -e ".[dev]"
pytest mini_os_scheduler/tests/ -v
```

### Step 5: Build Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build
python -m build
```

### Step 6: Upload to Test PyPI

```bash
# Get API token from https://test.pypi.org/manage/account/
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ mini-os-scheduler
```

### Step 7: Upload to Production PyPI

```bash
# Get API token from https://pypi.org/manage/account/
twine upload dist/*
```

### Step 8: Verify

```bash
# In a clean environment
pip install mini-os-scheduler
mini-scheduler --sample --algorithm all
```

## ✅ Done!

Your package is now on PyPI! 🎉

## 📝 Version Updates

To release a new version:

1. Update `version = "0.2.0"` in `pyproject.toml`
2. Update `__version__ = "0.2.0"` in `mini_os_scheduler/__init__.py`
3. Rebuild: `python -m build`
4. Upload: `twine upload dist/*`

## 🔗 Important Links

- **Test PyPI**: https://test.pypi.org/
- **Production PyPI**: https://pypi.org/
- **API Tokens**: https://pypi.org/manage/account/ (scroll to "API tokens")

---

For detailed instructions, see `BUILD_INSTRUCTIONS.md`

