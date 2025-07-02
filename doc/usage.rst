Usage
=====

Install bib-clean via PyPI:

.. code-block:: bash

   pip install bib-clean

Merge all `.bib` files in a directory:

.. code-block:: bash

   bib-clean --input-dir path/to/bib/files --output-file merged.bib

Arguments:
- ``--input-dir``: Directory containing `.bib` files (default: current directory).
- ``--output-file``: Output file for merged BibTeX entries (default: ``output.bib``).

Future Features
---------------

- Deduplicate BibTeX entries.
- Validate DOIs using CrossRef/DataCite APIs.
- Refresh metadata for accurate citations.