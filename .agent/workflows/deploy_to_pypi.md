---
description: How to release the package to PyPI
---

# Deploying to PyPI

Follow these steps to build and upload `omicsguard` to PyPI.

## Prerequisites

Ensure you have the build and upload tools installed:

```bash
pip install build twine
```

## 1. Build the Package

Run this command from the root of the repository (where `pyproject.toml` is located) to create the source distribution (`.tar.gz`) and the wheel (`.whl`).

```bash
# Clean previous builds
rm -rf dist/

# Build
python -m build
```

## 2. Verify Artifacts

Check the `dist/` directory to ensure the files were created:

```bash
ls -l dist/
```

You should see files like:
- `omicsguard-0.1.0-py3-none-any.whl`
- `omicsguard-0.1.0.tar.gz`

## 3. Upload to PyPI

### TestPyPI (Recommended for first run)
First, upload to TestPyPI to ensure everything looks right without affecting the main index.

```bash
twine upload --repository testpypi dist/*
```

### Main PyPI
Once verified, upload to the official PyPI repository.

```bash
twine upload dist/*
```

> **Note**: You will be prompted for your PyPI username and password (or API token). Use `__token__` as the username and your API token as the password.
