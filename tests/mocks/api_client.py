# ==============================================================================
# File: tests/mocks/api_client.py
# Contains the mock for the CrossRefClient.
# ==============================================================================
from typing import Optional, Dict, Any
from fuzzywuzzy import fuzz

import shutil
import uuid
from pathlib import Path
from typing import Dict, Any, Optional, Self

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter
import random
import unittest


# Assuming the real CrossRefClient is in bib_ami.cross_ref_client
# from bib_ami.cross_ref_client import CrossRefClient

class MockCrossRefClient:  # In a real project, this would inherit from CrossRefClient
    """A mock client that simulates CrossRef API responses for testing."""

    def __init__(self, email: str):
        self.email = email
        self.doi_database = {
            "attention is all you need": "10.5555/attention",
            "compilers principles techniques and tools": "10.5555/compilers",
        }

    def get_doi_for_entry(self, entry: Dict[str, Any]) -> Optional[str]:
        title = entry.get("title", "").lower()
        for key, doi in self.doi_database.items():
            if fuzz.ratio(title, key) > 95:
                return doi
        return None
