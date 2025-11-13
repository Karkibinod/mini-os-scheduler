# Package Information

## Package Name
`mini-os-scheduler`

## Author
Binod Karki

## Version
0.1.0

## Description
A comprehensive CPU scheduling simulator implementing FCFS, SJF, Priority, and Round Robin algorithms with CLI and web interfaces.

## Quick Commands

```bash
# Install
pip install -e .

# Run CLI
mini-scheduler --sample --algorithm all

# Run tests
pytest mini_os_scheduler/tests/ -v

# Build for PyPI
python -m build

# Upload to PyPI
twine upload dist/*
```

## Files Structure

- `mini_os_scheduler/` - Main package
- `pyproject.toml` - Package configuration
- `README.md` - Package documentation
- `LICENSE` - MIT License
- `BUILD_INSTRUCTIONS.md` - Build guide
- `QUICK_START.md` - Quick reference

