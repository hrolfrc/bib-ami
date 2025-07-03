Architecture
============

Overview
--------

The `bib-ami` tool is a Python-based command-line application designed to process BibTeX files efficiently, with a focus on modularity, extensibility, and robustness. Built to handle the challenges of AI-generated references, it leverages industry-standard libraries and APIs to merge, deduplicate, and clean BibTeX files. The architecture is structured to support both researchers (via a simple CLI) and developers (via a modular codebase), ensuring compatibility with LaTeX, Zotero, and JabRef workflows.

Components
----------

1. **Command-Line Interface (CLI)**:
   - **Implementation**: Uses Python’s `argparse` module to define three arguments: `--input-dir` (directory for `.bib` files), `--output-file` (output `.bib` file), and `--merge-only` (flag to limit to merging).
   - **Purpose**: Provides an intuitive interface for users to run `bib-ami` with commands like `bib-ami --input-dir bibs --output-file cleaned.bib`.
   - **Design**: Ensures simplicity for non-technical users while allowing flexibility for advanced workflows.

2. **File Handling**:
   - **Library**: `pathlib` for cross-platform file and directory operations.
   - **Functions**: `merge_bib_files` scans a directory for `.bib` files and concatenates them with newlines to prevent parsing errors.
   - **Purpose**: Ensures robust handling of input files, supporting diverse BibTeX sources (e.g., AI-generated, Zotero exports).

3. **BibTeX Parsing**:
   - **Library**: `bibtexparser` for parsing and writing BibTeX files.
   - **Function**: `load_bib_file` parses a `.bib` file into a `BibDatabase` object, supporting common strings and non-standard entry types.
   - **Purpose**: Converts raw BibTeX text into a structured format for deduplication and metadata processing.

4. **Deduplication**:
   - **Libraries**: `fuzzywuzzy` for fuzzy matching, `python-Levenshtein` for performance optimization.
   - **Function**: `deduplicate_bibtex` compares entries based on title and author similarity (default threshold: 90/100), retaining the entry with more metadata.
   - **Purpose**: Removes duplicates, common in AI-generated references, ensuring a concise bibliography.

5. **DOI Processing**:
   - **Library**: ``requests`` for HTTP requests to the CrossRef API.
   - **Functions**:
      - ``validate_doi``: Sends GET requests to ``https://api.crossref.org/works/{doi}`` to check DOI validity.
      - ``scrape_doi``: Queries ``https://api.crossref.org/works`` with title/author to find missing DOIs.
      - ``refresh_metadata``: Retrieves updated metadata (title, author, journal, year) for valid DOIs.
   - **Purpose**: Ensures accurate, verifiable DOIs and complete metadata, critical for academic citations.

6. **Summary Reporting**:
   - **Library**: Python’s `logging` module for console output.
   - **Function**: `process_bibtex` generates a report on files merged, duplicates removed, DOIs validated/added, and entries refreshed.
   - **Purpose**: Provides transparency and auditability for users, aiding debugging and verification.

7. **Output**:
   - **Library**: `bibtexparser`’s `BibTexWriter` for writing formatted BibTeX.
   - **Function**: `process_bibtex` writes the cleaned `BibDatabase` to the output file.
   - **Purpose**: Produces a publication-ready `.bib` file.

Design Principles
-----------------

- **Modularity**: Each function (`merge_bib_files`, `deduplicate_bibtex`, etc.) is independent, allowing developers to reuse or extend components (e.g., adding DataCite API support).
- **Error Handling**: Robust try-except blocks and logging ensure the tool continues processing despite file or API errors, critical for handling unreliable AI-generated data.
- **Performance**: Uses `python-Levenshtein` for fast fuzzy matching and optimizes API calls with timeouts (5 seconds) to handle CrossRef rate limits.
- **Extensibility**: Designed to support future features like ISBN validation or cloud-based reference management, aligning with potential interdisciplinary applications (e.g., computational biology, machine learning).

Dependencies
------------

- `bibtexparser>=1.4.1`: For parsing and writing BibTeX files.
- `requests>=2.31.0`: For CrossRef API requests.
- `fuzzywuzzy>=0.18.0`: For fuzzy matching in deduplication.
- `python-Levenshtein>=0.25.0`: For performance optimization in fuzzy matching.
- `pytest>=7.4.0`, `pytest-cov>=4.1.0`: For unit testing and coverage.
- `twine>=4.0.2`: For PyPI uploads.
- `sphinx>=7.0.0`, `sphinx_rtd_theme>=1.3.0`: For RTD documentation.

Notes
-----

- **Scalability**: The architecture supports small to medium-sized BibTeX files (e.g., hundreds of entries). For large datasets, consider batching API calls or caching responses.
- **Future Enhancements**: Planned features include integration with DataCite, ISBN validation, and a configuration file for custom thresholds.
- **Compatibility**: Tested with Python 3.7+, ensuring broad compatibility for academic users.

This architecture balances usability for researchers and extensibility for developers, making `bib-ami` a robust tool for managing BibTeX references in academic workflows.