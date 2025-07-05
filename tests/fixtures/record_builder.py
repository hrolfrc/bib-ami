import logging

import uuid
from typing import Dict, Any, Optional, Self

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# ==============================================================================
# File: tests/fixtures/record_builder.py
# A factory for creating BibTeX record dictionaries for tests.
# ==============================================================================

class RecordBuilder:
    """
    A factory for creating structured test data (BibTeX records as dicts).

    This uses a fluent (builder) pattern to make test setup clean and readable.
    Example:
        record = RecordBuilder("my_id").with_title("My Title").with_doi("10.1/1").build()
    """

    def __init__(self, entry_id: Optional[str] = None):
        if entry_id is None:
            entry_id = f"rec_{uuid.uuid4().hex[:8]}"

        self._record: Dict[str, Any] = {
            "ENTRYTYPE": "article",
            "ID": entry_id,
        }

    def with_title(self, title: str) -> Self:
        self._record["title"] = title
        return self

    def with_author(self, author: str) -> Self:
        self._record["author"] = author
        return self

    def with_year(self, year: int) -> Self:
        self._record["year"] = str(year)
        return self

    def with_doi(self, doi: str) -> Self:
        self._record["doi"] = doi
        return self

    def with_note(self, note: str) -> Self:
        self._record["note"] = note
        return self

    def as_book(self) -> Self:
        self._record["ENTRYTYPE"] = "book"
        return self

    def build(self) -> Dict[str, Any]:
        """Returns the final dictionary representing the BibTeX entry."""
        return self._record
