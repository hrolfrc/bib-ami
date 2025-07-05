.. _bib-ami-testing-strategy:

For Developers: The Testing Strategy
===================================

Goal
----

The primary goal of this test plan is to verify that the bibliography processing tool achieves its desired outcome: producing a **trustworthy, complete, auditable, and high-fidelity "golden" bibliography**. This plan ensures that every component and workflow is rigorously tested to meet the project’s core principles of data integrity.

Testing Philosophy: A Layered Approach
-------------------------------------

To ensure comprehensive coverage, we use a layered testing strategy. Each layer serves a distinct purpose, providing a safety net that catches different types of errors.

- **Unit Tests**: Fast, isolated tests to verify the internal logic of each individual class.
- **Integration Tests**: Focused tests to verify that data flows correctly between the distinct phases of the workflow (i.e., the "plumbing" works).
- **End-to-End (E2E) Tests**: Slower, comprehensive tests that run the entire application on realistic data to ensure the final output is correct.

This layered approach allows for rapid feedback during development (from unit tests) while guaranteeing the robustness of the complete system (from integration and E2E tests).

Test Environment and Helper Classes
----------------------------------

A robust testing environment is crucial for efficiency and clarity. All test code resides in a dedicated ``tests/`` directory, separate from the application source code in ``src/``. This environment is supported by a set of specialized helper classes designed to create test data and simulate external dependencies.

Helper Class Descriptions
~~~~~~~~~~~~~~~~~~~~~~~~

These classes are the foundation of our test suite, allowing us to create clean, readable, and powerful tests.

**BibTexTestDirectory**
   :Location: ``tests/fixtures/directory_manager.py``
   :Purpose: To programmatically create and clean up temporary directory structures for integration and E2E tests.
   :Responsibilities:
     - Create a temporary root directory for a single test run.
     - Provide methods to populate the directory with different types of files: well-formed ``.bib`` files, files with syntax errors, non-``.bib`` files, etc.
     - Ensure automatic cleanup of the directory and its contents after a test completes, typically by implementing the context manager protocol (``__enter__`` and ``__exit__``).

**MockCrossRefClient**
   :Location: ``tests/mocks/api_client.py``
   :Purpose: To simulate the real ``CrossRefClient`` for fast, offline unit and integration tests.
   :Responsibilities:
     - Implement the same public methods as the real client (e.g., ``get_work_by_doi``).
     - Be configurable to return specific, predefined responses based on the query it receives.
     - Track the calls made to it, so tests can assert that the correct queries were sent.

**RecordBuilder**
   :Location: ``tests/fixtures/record_builder.py``
   :Purpose: To act as a factory for creating structured test data (e.g., Python dictionaries representing BibTeX records).
   :Responsibilities:
     - Provide a clean, fluent API for generating test records (e.g., ``RecordBuilder().with_title("...").build()``).
     - Include convenience methods for common scenarios, such as ``create_duplicate_pair()`` or ``create_suspect_article()``.

Test Suite Breakdown
--------------------

Unit Tests
~~~~~~~~~~

:Goal: Verify the correctness of each class’s internal logic in complete isolation.
:How it meets the desired outcome: Ensures the core algorithms for validation, reconciliation, and triage are correct by design, which is the foundation of a **trustworthy** system.

+--------------------+-----------------------------------------------------------------------------------------------------------------+
| **Class to Test**  | **Test Method Description**                                                                                     |
+====================+=================================================================================================================+
| ``Validator``      | Using ``MockCrossRefClient`` and ``RecordBuilder``, test that the ``Validator`` correctly adds new DOIs,        |
|                    | confirms existing ones, replaces incorrect ones, and handles API failures gracefully.                           |
+--------------------+-----------------------------------------------------------------------------------------------------------------+
| ``Reconciler``     | Using ``RecordBuilder``, test that the ``Reconciler`` correctly deduplicates entries sharing a DOI, merges      |
|                    | user-specific fields like ``note`` to demonstrate **fidelity**, and uses fuzzy matching for entries that lack   |
|                    | a DOI.                                                                                                          |
+--------------------+-----------------------------------------------------------------------------------------------------------------+
| ``Triage``         | Using ``RecordBuilder``, test that the ``Triage`` class correctly classifies an ``@article`` with a DOI as      |
|                    | ``Verified``, a ``@book`` without a DOI as ``Accepted``, and a modern ``@article`` without a DOI as ``Suspect``.|
+--------------------+-----------------------------------------------------------------------------------------------------------------+

Integration Tests
~~~~~~~~~~~~~~~~

:Goal: Verify that the "plumbing" between the workflow phases is solid and that each phase can correctly process the file output from the previous one.
:How it meets the desired outcome: Guarantees the **auditability** and reproducibility of the workflow by confirming the integrity of the intermediate artifacts.

+----------------------------------+-----------------------------------------------------------------------------------------------------------------+
| **Test Case**                    | **Actions**                                                                                                     |
+==================================+=================================================================================================================+
|                                  | is created. Then, feed this file to the ``Validator`` (using a mock API) and assert that its output file        |
| ``Ingestor -> Validator``        | Use ``BibTexTestDirectory`` to create a test directory and run the ``Ingestor``. Assert that its output        |
|                                  |  contains the correct validation statuses.                                                                      |
+----------------------------------+-----------------------------------------------------------------------------------------------------------------+
| ``Validator -> Reconciler``      | Create a pre-made validated JSON file containing known duplicates. Run the ``Reconciler`` on this file and      |
|                                  | assert that its output has the correct number of deduplicated entries and that user notes have been merged      |
|                                  | correctly.                                                                                                      |
+----------------------------------+-----------------------------------------------------------------------------------------------------------------+
| ``Reconciler -> Triage & Writer``| Create a pre-made reconciled JSON file with a mix of record types. Run the final ``Triage`` and ``Writer``      |
|                                  | phases and assert that the final ``.bib`` output files are created and contain the correct entries.             |
+----------------------------------+-----------------------------------------------------------------------------------------------------------------+

End-to-End (E2E) Tests
~~~~~~~~~~~~~~~~~~~~~~

:Goal: Verify that the entire application works as a cohesive whole on realistic data, from source files to final outputs.
:How it meets the desired outcome: Demonstrates that all principles are upheld in a complete run, ensuring a **complete** and **auditable** final product.

+----------------------+-----------------------------------------------------------------------------------------------------------------+
| **Test Scenario**    | **Actions**                                                                                                     |
+======================+=================================================================================================================+
| "Happy Path" Scenario| Use ``BibTexTestDirectory`` to create a directory with several well-formed ``.bib`` files. Run the full        |
|                      | application pipeline and assert that the final output files are created correctly and the summary report is     |
|                      | accurate.                                                                                                       |
+----------------------+-----------------------------------------------------------------------------------------------------------------+
| Pathological Scenario| Use ``BibTexTestDirectory`` to create a directory with a mix of broken, duplicate, and un-verifiable entries.  |
|                      | Run the full pipeline and assert that the final output files correctly separate the valid and suspect entries,  |
|                      | and that the summary report reflects the actions taken.                                                         |
+----------------------+-----------------------------------------------------------------------------------------------------------------+