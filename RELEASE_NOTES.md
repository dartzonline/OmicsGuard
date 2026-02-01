# Release Notes - v0.1.0

## Initial Release: OmicsGuard

We are proud to announce the first production-ready release of **OmicsGuard**, a lightweight, serverless-optimized metadata validator designed for high-throughput bioinformatics pipelines. 

This release focuses on solving the "Schema-on-Write" challenge in genomic data lakes, ensuring strict adherence to GA4GH standards (like Phenopackets) without the operational overhead of heavy frameworks or containers.

### Key Highlights

#### 1. Serverless-First Architecture
*   **Zero-Dependency Core**: Built primarily on the standard library and `jsonschema` to ensure sub-second cold starts in AWS Lambda and Google Cloud Functions.
*   **Minimal Footprint**: Package size is optimized for rapid deployment in ephemeral compute environments.

#### 2. Extensible Validation Engine
*   **Plugin System**: Introducing a dynamic plugin architecture allows teams to inject custom business logic (written in pure Python) alongside structural schema validation. 
    *   *Use Case*: Validate that a `sample_id` matches an internal LIMS regex pattern while still conforming to the global GA4GH standard.
*   **Schema Extension**: Support for "Overlay Schemas" enables organizations to add proprietary fields (e.g., `hospital_code`, `billing_id`) to standard schemas without forking or breaking compatibility.

#### 3. Intelligent Registry & Caching
*   **Standard Registry**: Built-in support for known standards (e.g., `ga4gh-phenopacket-v2`).
*   **Smart Caching**: The `SchemaLoader` transparently handles remote schema lookups, caching them locally (`~/.omicsguard/schemas`) to eliminate network latency during high-volume processing.
*   **CLI Pull**: New `pull` command allows pre-warming the cache during container build times.

#### 4. Developer & Clinician Experience
*   **Human-Readable Reports**: The validator now generates rich HTML and Markdown reports, making it easier for non-technical stakeholders (clinicians, biologists) to understand data rejection reasons.
*   **Pipeline Ready**: CLI returns standard exit codes (0/1) for seamless integration with Nextflow, Cromwell, and Snakemake.

### Technical Implementation
*   **Pythonic Refactor**: The codebase has been fully refactored to adhere to idiomatic Python standards, including comprehensive type hinting (`typing`), clean modular separation (`loader`, `validator`, `reporter`), and context-aware logging.
*   **Robust Error Handling**: Network and File I/O operations are wrapped in specific exception handlers to prevent silent failures in production pipelines.

### Installation

```bash
pip install omicsguard
```

### Contributors
*   **Dart** (Independent Researcher) - Lead Maintainer

---
*For a full list of changes, please refer to the Git log.*
