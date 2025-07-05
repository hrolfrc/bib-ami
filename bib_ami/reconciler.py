# ==============================================================================
# File: bib_ami/reconciler.py
# New class responsible for deduplication and merging user data.
# ==============================================================================

# ==============================================================================
# File: bib_ami/reconciler.py
# Updated to create a detailed audit trail for each merged record.
# ==============================================================================
import logging
from typing import Dict, List, Any

from bibtexparser.bibdatabase import BibDatabase


class Reconciler:
    """Deduplicates entries, merges metadata, and creates an audit trail."""

    def __init__(self, fuzzy_threshold=95):
        self.fuzzy_threshold = fuzzy_threshold

    @staticmethod
    def _create_golden_record(group: List[Dict]) -> Dict[str, Any]:
        """Merges a group of duplicate entries into a single golden record."""
        winner = max(group, key=len)
        golden_record = winner.copy()

        # --- Auditing and Merging Logic ---
        changes = []

        # 1. Merge user-specific fields like 'note'
        notes = {e.get('note') for e in group if e.get('note')}
        if len(notes) > 1:
            golden_record['note'] = " | ".join(sorted(list(notes)))
            changes.append("Merged 'note' fields from duplicates.")

        # 2. Check if a DOI was corrected
        original_dois = {e.get('doi', '').lower() for e in group if e.get('doi')}
        if golden_record.get('verified_doi') and len(original_dois) > 1:
            changes.append(f"Standardized DOI to {golden_record['verified_doi']}.")

        # 3. Store audit information directly in the record
        golden_record['audit_info'] = {
            "status": "Reconciled",
            "changes": changes,
            "original_entries": group  # Keep originals for the writer
        }
        return golden_record

    def deduplicate(self, database: BibDatabase) -> (BibDatabase, int):
        logging.info("--- Phase 3: Reconciling and Deduplicating Entries ---")
        initial_count = len(database.entries)

        # Pass 1: Deduplicate by verified DOI
        doi_map: Dict[str, List[Dict]] = {}
        no_doi_entries: List[Dict] = []
        for entry in database.entries:
            doi = entry.get('verified_doi')
            if doi:
                doi_key = doi.lower()
                if doi_key not in doi_map:
                    doi_map[doi_key] = []
                doi_map[doi_key].append(entry)
            else:
                no_doi_entries.append(entry)

        reconciled_entries: List[Dict] = []
        for group in doi_map.values():
            golden_record = self._create_golden_record(group)
            reconciled_entries.append(golden_record)

        # Pass 2: Fuzzy deduplication for entries without a DOI (simplified for now)
        reconciled_entries.extend(no_doi_entries)

        database.entries = reconciled_entries
        duplicates_removed = initial_count - len(reconciled_entries)
        logging.info(f"Removed {duplicates_removed} duplicate entries.")
        return database, duplicates_removed
