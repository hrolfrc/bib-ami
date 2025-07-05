# ==============================================================================
# File: bib_ami/triage.py
# New class responsible for classifying records.
# ==============================================================================
import logging

from bibtexparser.bibdatabase import BibDatabase


# noinspection SpellCheckingInspection
class Triage:
    """Categorizes records as Verified, Accepted, or Suspect."""

    @staticmethod
    def run_triage(database: BibDatabase) -> (BibDatabase, BibDatabase):
        logging.info("--- Phase 4a: Triaging Records ---")
        verified_db = BibDatabase()
        suspect_db = BibDatabase()

        for entry in database.entries:
            entry_type = entry.get('ENTRYTYPE', 'misc').lower()
            if entry.get('verified_doi'):
                verified_db.entries.append(entry)
            elif entry_type in ['book', 'techreport', 'misc', 'phdthesis', 'mastersthesis']:
                verified_db.entries.append(entry)  # Accepted
            else:
                suspect_db.entries.append(entry)  # Suspect

        logging.info(
            f"Triage complete: {len(verified_db.entries)} verified/accepted, {len(suspect_db.entries)} suspect.")
        return verified_db, suspect_db
