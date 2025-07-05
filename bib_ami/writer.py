# ==============================================================================
# File: bib_ami/writer.py
# New class responsible for writing output files.
# ==============================================================================
import logging
from pathlib import Path
from typing import Dict, Any

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter


# noinspection PyUnusedLocal
class Writer:
    """Writes BibDatabase objects to .bib files, including audit comments."""

    @staticmethod
    def _format_original_entry(entry: Dict[str, Any]) -> str:
        """Formats an original entry into a string for the audit comment."""
        temp_db = BibDatabase()
        # Create a clean copy for formatting
        original_copy = {k: v for k, v in entry.items() if
                         not k.startswith('bib_ami_') and k not in ['source_file', 'verified_doi', 'audit_info']}
        temp_db.entries = [original_copy]
        writer = BibTexWriter()
        writer.indent = '    '
        return writer.write(temp_db).strip()

    def _add_audit_fields(self, entry: Dict[str, Any], status_override: str = None):
        """Adds bib_ami_* fields to an entry based on its audit trail."""
        audit_info = entry.get('audit_info', {})

        # Determine final status
        status = status_override if status_override else audit_info.get('status', 'Unchanged')
        entry['bib_ami_status'] = status

        # Compile changes
        changes = audit_info.get('changes', [])
        if not changes:
            changes.append("No changes made.")
        entry['bib_ami_changes'] = ", ".join(changes)

        # Add original entry representation
        if 'original_entries' in audit_info:
            original_strings = [self._format_original_entry(e) for e in audit_info['original_entries']]
            entry['bib_ami_original'] = "\n% ".join(original_strings)

    @staticmethod
    def _clean_entry_for_writing(entry: Dict[str, Any]) -> Dict[str, Any]:
        """Removes internal fields and finalizes DOI before writing."""
        cleaned = entry.copy()
        if cleaned.get('verified_doi'):
            cleaned['doi'] = cleaned['verified_doi']

        # Remove all internal processing fields
        internal_fields = ['verified_doi', 'source_file', 'audit_info', 'original_entries']
        for field in internal_fields:
            if field in cleaned:
                del cleaned[field]
        return cleaned

    def write_files(
            self,
            verified_db: BibDatabase,
            suspect_db: BibDatabase,
            output_file: Path,
            suspect_file: Path,
            merge_only=False
    ):
        logging.info("--- Phase 4b: Writing Output Files with Audit Trail ---")
        writer = BibTexWriter()
        writer.indent = '  '
        writer.add_trailing_comma = True

        # Add audit fields before cleaning and writing
        for entry in verified_db.entries:
            self._add_audit_fields(entry, status_override="Verified")
        for entry in suspect_db.entries:
            self._add_audit_fields(entry, status_override="Suspect")

        try:
            verified_db.entries = [self._clean_entry_for_writing(e) for e in verified_db.entries]
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("% bib-ami output: Verified and Accepted Entries\n")
                f.write("% Users are responsible for verifying all citations before use.\n\n")
                bibtexparser.dump(verified_db, f, writer)
            logging.info(f"Wrote {len(verified_db.entries)} entries to '{output_file}'")

            if suspect_db.entries:
                suspect_db.entries = [self._clean_entry_for_writing(e) for e in suspect_db.entries]
                with open(suspect_file, 'w', encoding='utf-8') as f:
                    f.write("% bib-ami output: Suspect Entries Requiring Manual Review\n\n")
                    bibtexparser.dump(suspect_db, f, writer)
                logging.info(f"Wrote {len(suspect_db.entries)} entries to '{suspect_file}'")
        except Exception as e:
            logging.error(f"Failed to write output files: {e}", exc_info=True)
