Workflow
========

Overview
--------

The `bib-ami` tool follows a structured workflow to consolidate, clean, and enhance BibTeX files, addressing common issues such as duplicates, invalid DOIs, and incomplete metadata. This workflow is designed to be intuitive for researchers, students, and academics who use BibTeX in LaTeX, Zotero, or JabRef workflows, particularly when dealing with error-prone AI-generated references. The process is automated to minimize manual effort, ensuring high-quality citations suitable for publication in journals like *eLife*.

Step-by-Step Workflow
---------------------

1. **Merging BibTeX Files**:
   - **Input**: A directory containing one or more `.bib` files, which may come from various sources (e.g., AI tools, manual exports from Zotero or JabRef).
   - **Process**: `bib-ami` scans the specified directory (default: current directory) using Python’s `pathlib` module to identify all `.bib` files. These files are concatenated into a single temporary `.bib` file, with newlines added to prevent parsing issues. If the `--merge-only` flag is used, this temporary file is saved as the output, and the workflow stops here.
   - **Purpose**: Consolidation simplifies subsequent processing by working with a single file, reducing complexity for users managing multiple reference sources.

2. **Parsing BibTeX**:
   - **Input**: The merged `.bib` file.
   - **Process**: The file is parsed into a `BibDatabase` object using the `bibtexparser` library, which handles BibTeX syntax and supports common strings and non-standard entry types. Parsing ensures that entries are structured for further processing (e.g., deduplication, DOI validation).
   - **Purpose**: Converts raw text into a structured format, enabling programmatic manipulation of entries.

3. **Deduplication**:
   - **Input**: The parsed `BibDatabase`.
   - **Process**: Entries are compared using `fuzzywuzzy` for fuzzy matching on title and author fields, with a default similarity threshold of 90 (out of 100). Entries with matching titles and authors are considered duplicates, and the entry with more metadata (e.g., a DOI) or more fields is retained. Duplicates are removed, and the count is tracked for the summary report.
   - **Purpose**: Eliminates redundant entries, common in AI-generated references due to variations in formatting, ensuring a concise bibliography.

4. **DOI Validation**:
   - **Input**: Entries with DOIs in the `BibDatabase`.
   - **Process**: Each DOI is validated by sending a GET request to the CrossRef API (`https://api.crossref.org/works/{doi}`). A status code of 200 indicates a valid DOI; otherwise, it’s marked invalid. Invalid DOIs are flagged for potential replacement in the next step.
   - **Purpose**: Ensures DOIs resolve to actual publications, critical for verifiable citations in academic work.

5. **DOI Scraping**:
   - **Input**: Entries without DOIs or with invalid DOIs.
   - **Process**: For each entry, a query is sent to the CrossRef API (`https://api.crossref.org/works`) using the entry’s title and first author. The API returns the most relevant match, and if a DOI is found, it’s added to the entry. This step addresses missing or incorrect DOIs in AI-generated references.
   - **Purpose**: Enhances citation completeness by adding valid DOIs, improving access to source materials.

6. **Metadata Refreshing**:
   - **Input**: Entries with valid or newly scraped DOIs.
   - **Process**: For each valid DOI, a GET request to the CrossRef API retrieves updated metadata (e.g., title, author, journal, year). The entry is updated with this data, preserving existing fields if the API request fails.
   - **Purpose**: Ensures metadata accuracy, correcting inconsistencies in AI-generated or manually created entries.

7. **Summary Reporting**:
   - **Input**: Results from all previous steps.
   - **Process**: A summary report is generated, logging the number of files merged, duplicates removed, DOIs validated (valid/invalid), DOIs added, and entries refreshed. The report is output to the console and can be redirected to a file for record-keeping.
   - **Purpose**: Provides transparency on actions taken, helping users verify the cleaning process and track changes.

8. **Output**:
   - **Process**: The processed `BibDatabase` is written to the specified output file (default: `output.bib`) using `bibtexparser`’s `BibTexWriter`, ensuring proper BibTeX formatting. The temporary merged file is deleted.
   - **Purpose**: Produces a clean, consolidated `.bib` file ready for use in LaTeX, Zotero, or JabRef.

Example Workflow
----------------

Consider a directory `bibs/` with two `.bib` files containing AI-generated references:

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

Running:

.. code-block:: bash

   bib-ami --input-dir bibs --output-file cleaned.bib

- **Step 1**: Merges `file1.bib` and `file2.bib` into a temporary file.
- **Step 2**: Parses the temporary file into a `BibDatabase`.
- **Step 3**: Identifies `smith2020` and `smith2020_duplicate` as duplicates (high title/author similarity), keeps `smith2020` (has DOI).
- **Step 4**: Validates `10.1000/invalid` (fails).
- **Step 5**: Scrapes a new DOI (e.g., `10.1000/xyz123`) for `smith2020` using CrossRef.
- **Step 6**: Refreshes metadata for `smith2020` with CrossRef data (e.g., updates journal to `Journal of AI`).
- **Step 7**: Logs summary: 2 files merged, 1 duplicate removed, 0 DOIs valid, 1 DOI invalid, 1 DOI added, 1 entry refreshed.
- **Step 8**: Writes `cleaned.bib` with the single, updated entry.

Benefits
--------

This workflow saves researchers significant time by automating tedious tasks, ensures citation accuracy for publication, and addresses common issues with AI-generated references. It is particularly valuable for interdisciplinary research (e.g., computational biology, machine learning applied to medicine), where diverse references must be meticulously managed to meet journal standards.

Notes
-----

- **Error Handling**: The workflow includes robust error handling for file operations and API requests, logging issues without halting execution.
- **API Rate Limits**: CrossRef API has rate limits (e.g., 50 requests/second). Heavy usage may require API keys or caching.
- **Future Enhancements**: Planned features include ISBN validation, DataCite API support, and advanced deduplication options.