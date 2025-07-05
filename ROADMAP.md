# bib-ami: Future Development Plan

This document outlines the remaining features required to complete the current vision, as well as potential enhancements for future versions.

---

## Priority 1: Completing the Current Vision

This is the one remaining feature required to fully realize the "enriched" and "auditable" goals we set out in the project's philosophy.

### Implement Full Metadata Refreshing

* **Goal:** To ensure that every "golden record" is not just verified but also enriched with the most accurate and complete metadata available.
* **Implementation Steps:**
    1.  **Enhance `CrossRefClient`:** Add a new method, `get_metadata_by_doi(doi)`, that takes a verified DOI and fetches the full bibliographic record from the CrossRef API.
    2.  **Create `MetadataRefresher` Class:** Create a new component whose single responsibility is to refresh entries. Its main method would take a record with a `verified_doi`.
    3.  **Update Core Fields:** The refresher will use the data from the API to overwrite the entry's core descriptive fields (`title`, `author`, `year`, `journal`, etc.), ensuring they are canonical.
    4.  **Update Audit Trail:** The refresher must log its actions to the entry's `audit_info` dictionary (e.g., `"Refreshed metadata from CrossRef."`).
    5.  **Integrate into `BibTexManager`:** Add this as a new step in the main workflow, occurring right after validation and before reconciliation.

---

## Priority 2: High-Value Future Enhancements

These features would provide the most significant improvements in coverage and usability for a future `v1.0` release.

### 1. Add DataCite API Support

* **Problem:** CrossRef primarily covers journal articles and conference papers. Datasets, software, and many technical reports are registered with DataCite.
* **Solution:** Create a `DataCiteClient` that mirrors the `CrossRefClient`. The `Validator` would first query CrossRef; if no match is found, it would then query DataCite as a fallback. This would dramatically increase the tool's coverage.

### 2. Add ISBN Validation for Books

* **Problem:** Books are a common entry type but often lack DOIs, making them "Suspect" by default.
* **Solution:** For entries of type `@book`, use the `isbn` field to query an external source like the **Google Books API** or **Open Library API**. A successful match would allow the book to be validated and its metadata refreshed.

### 3. Implement API Caching

* **Problem:** Running the tool multiple times on the same library results in many redundant API calls, which is slow and unfriendly to the API providers.
* **Solution:** Implement a simple local file-based cache. Before making an API call, check if the query has been made recently. If so, use the cached result. This would provide a performance boost for iterative runs.

---

## Priority 3: Robustness and Quality-of-Life Improvements

These are smaller features that would make the tool more professional and easier to use.

* **Interactive "Gleaning" Mode:** For the `suspect.bib` file, an interactive mode could present each suspect entry to the user and ask them to `[k]eep`, `[d]iscard`, or `[s]earch again with new metadata?`.
* **Configurable Triage Rules:** Move the rules for what constitutes an "Accepted" entry (e.g., `@book`, `@techreport`) into the `bib_ami_config.json` file, allowing users to customize the triage logic.
* **Parallel API Requests:** The validation phase is the main bottleneck. Refactor the `Validator` to use Python's `concurrent.futures` to make multiple API requests in parallel, speeding up the process for large bibliographies.