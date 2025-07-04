Introduction
============

**bib-ami** is a command-line utility for improving the integrity of
BibTeX (``.bib``) bibliographies. It is designed to help researchers,
academics, and students by automating several common data cleaning
tasks.

Managing bibliographies often involves dealing with duplicate entries,
inconsistent formatting, and missing metadata. **bib-ami** addresses
these issues by providing functionality to merge multiple ``.bib``
files, identify and remove duplicate entries, and validate or find
missing Digital Object Identifiers (DOIs) by querying the CrossRef API.
The goal is to produce a consolidated and more reliable BibTeX file,
reducing the manual effort required to manage academic references.

Getting Started
===============

This section is designed to get you up and running with **bib-ami** in
under five minutes.

Installation
------------

**bib-ami** is distributed via the Python Package Index (PyPI) and can
be installed easily using ``pip``. Ensure you have Python 3.7 or higher
installed.

.. code:: bash

   pip install bib-ami

This command will also install all necessary dependencies, including
``bibtexparser``, ``requests``, and ``fuzzywuzzy``.

Quick Start Example
-------------------

The fastest way to see **bib-ami** in action is to run it on a directory
of your existing ``.bib`` files. This single command will merge all
found files, deduplicate the entries, attempt to find missing DOIs, and
save the result to a new, clean file.

#. Create a directory (e.g., ``my_bib_files``) and place all your source
   ``.bib`` files inside it.

#. Create a second directory for the output (e.g., ``output``).

#. Run the following command from your terminal, making sure to provide
   your email address. An email is required for responsible use of the
   CrossRef API’s Polite Pool.

.. code:: bash

   bib-ami --input-dir my_bib_files --output-file output/cleaned_library.bib --email "your.name@university.edu"

After the process completes, you will find a ``cleaned_library.bib``
file in your ``output`` directory. This file contains the consolidated
and enhanced collection of your references. A summary of the actions
taken (e.g., duplicates removed, DOIs added) will be printed to your
console.
