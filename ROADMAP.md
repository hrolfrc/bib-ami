# bib-ami: Future Development Plan

With the core architecture implemented and tested, the project is on a solid foundation. This document outlines the remaining features required to complete the current vision, as well as potential enhancements for future versions.

---

## Foundational Priority: Code Quality & Robustness

This is an ongoing priority that should be addressed alongside all new feature development to ensure the long-term health and stability of the project.

### Increase Test Coverage to >90%

* **Goal:** To move from the current coverage level to 85--95%, ensuring all critical application logic is verified by automated tests.
* **Strategy:**
    1.  **Target Untested Logic:** Use the Codecov report to identify modules and functions with low coverage.
    2.  **Write "Unhappy Path" Tests:** Add specific unit tests for error conditions, such as file I/O errors in the `Ingestor`, API failures in the `Validator`, and malformed entries in the `Reconciler`.
    3.  **Ensure Full Branch Coverage:** Add tests to verify that all `if/else` conditions in the `Triage` and `Reconciler` classes are executed.
    4.  **Maintain Coverage:** Configure CI (e.g., with Codecov's settings) to fail a pull request if it decreases the overall test coverage.

---

## Priority 1: High-Value Future Enhancements

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

## Priority 2: Robustness and Quality-of-Life Improvements

These are smaller features that would make the tool more professional and easier to use.

* **Interactive "Gleaning" Mode:** For the `suspect.bib` file, an interactive mode could present each suspect entry to the user and ask them to `[k]eep`, `[d]iscard`, or `[s]earch again with new metadata?`.
* **Configurable Triage Rules:** Move the rules for what constitutes an "Accepted" entry (e.g., `@book`, `@techreport`) into the `bib_ami_config.json` file, allowing users to customize the triage logic.
* **Parallel API Requests:** The validation phase is the main bottleneck. Refactor the `Validator` to use Python's `concurrent.futures` to make multiple API requests in parallel, speeding up the process for large bibliographies.