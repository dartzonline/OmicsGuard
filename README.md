# OmicsGuard

**A Serverless-Ready Metadata Validator for GA4GH Genomic Standards.**

## Overview

In the era of petabyte-scale genomics, data integrity is a bottleneck. OmicsGuard is a lightweight, Python-based validation engine designed to enforce "Schema-on-Write" for genomic metadata. It supports GA4GH standards (like Phenopackets) and is optimized for serverless environments (AWS Lambda, etc.).

## Features

- **Lightweight**: Minimal dependencies, fast startup for serverless.
- **Standards Compliant**: Built on `jsonschema` for compatibility with GA4GH standards.
- **Flexible**: Load schemas from local files or URLs.
- **Extensible**: Support for custom schema extensions.

## Installation

```bash
# Install from source
pip install .

# Or for development (editable mode)
pip install -e .
```

## Usage

### CLI

OmicsGuard now validates data and outputs `true` or `false` (errors are printed to stderr).

```bash
# Validate using the bundled default schema (Phenopackets)
omicsguard --data path/to/data.json
# Output: true

# Validate using a custom schema
omicsguard --schema path/to/schema.json --data path/to/data.json
```

### Python API

```python
from omicsguard.validator import validate_metadata

errors = validate_metadata(data, schema)
if errors:
    print("Validation failed:", errors)
```
