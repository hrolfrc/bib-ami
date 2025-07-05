# ==============================================================================
# File: bib_ami/validator.py
# New class responsible for using the API client to validate records.
# ==============================================================================
import logging

from bibtexparser.bibdatabase import BibDatabase

from .cross_ref_client import CrossRefClient


class Validator:
    """Validates each entry to find its canonical DOI."""

    def __init__(self, client: CrossRefClient):
        self.client = client

    def validate_all(self, database: BibDatabase) -> BibDatabase:
        logging.info("--- Phase 2: Validating and Enriching All Entries with DOIs ---")
        validated_count = 0
        for entry in database.entries:
            verified_doi = self.client.get_doi_for_entry(entry)
            entry['verified_doi'] = verified_doi
            if verified_doi:
                validated_count += 1
        logging.info(f"Validated or found DOIs for {validated_count} entries.")
        return database
