Usage
=====

Install bib-ami via PyPI:

.. code-block:: bash

   pip install bib-ami

Merge all `.bib` files in a directory without further processing:

.. code-block:: bash

   bib-ami --input-dir path/to/bib/files --output-file merged.bib --merge-only

Merge, deduplicate, validate DOIs, scrape missing DOIs, and refresh metadata:

.. code-block:: bash

   bib-ami --input-dir path/to/bib/files --output-file cleaned.bib

Arguments
---------

- ``--input-dir``: Directory containing `.bib` files (default: current directory).
- ``--output-file``: Output file for processed BibTeX entries (default: ``output.bib``).
- ``--merge-only``: Only merge `.bib` files without deduplication or DOI processing.

Example
-------

Given two `.bib` files in ``bibs/``:

**file1.bib**:

.. code-block:: bibtex

   @article{smith2020,
     title={Machine Learning},
     author={Smith, John},
     journal={Journal of AI},
     year={2020},
     doi={10.1000/invalid}
   }

**file2.bib**:

.. code-block:: bibtex

   @article{smith2020_duplicate,
     title={Machine Learning},
     author={Smith, John},
     journal={AI Journal},
     year={2020}
   }

Run:

.. code-block:: bash

   bib-ami --input-dir bibs --output-file cleaned.bib

Output (``cleaned.bib``):

.. code-block:: bibtex

   @article{smith2020,
     title={Machine Learning},
     author={Smith, John},
     journal={Journal of AI},
     year={2020},
     doi={10.1000/xyz123}
   }

Summary (logged):

.. code-block:: text

   Files Merged: 2
   Duplicates Removed: 1
   DOIs Valid: 0
   DOIs Invalid: 1
   DOIs Added: 1
   Entries Refreshed: 1

Features
--------

- Merges multiple `.bib` files into a single file.
- Deduplicates entries using fuzzy matching on title and author.
- Validates DOIs via CrossRef API.
- Scrapes missing DOIs using CrossRef API based on title and author.
- Refreshes metadata for entries with valid DOIs.
- Generates a summary report of changes (files merged, duplicates removed, DOIs validated/added, entries refreshed).

Notes
-----

- **API Rate Limits**: CrossRef/DataCite APIs have rate limits (e.g., 50 requests/second for CrossRef). Heavy usage may require API keys or caching.
- **Future Enhancements**: Planned features include ISBN validation and support for additional APIs (e.g., DataCite).
- **Compatibility**: Works with LaTeX, Zotero, and JabRef workflows.