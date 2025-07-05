# ==============================================================================
# File: bib_ami/ingestor.py
# New class responsible for file discovery and parsing.
# ==============================================================================
import logging
from pathlib import Path

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


# noinspection PyArgumentList
class Ingestor:
    """Finds and parses all .bib files from a directory."""

    @staticmethod
    def ingest_from_directory(input_dir: Path) -> BibDatabase:
        logging.info(f"--- Phase 1: Ingesting files from '{input_dir}' ---")
        database = BibDatabase()
        bib_files = list(input_dir.glob("*.bib"))

        for file_path in bib_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as bibtex_file:
                    parser = bibtexparser.bparser.BibTexParser(
                        common_strings=True,
                        ignore_nonstandard_types=False,
                        homogenise_fields=True
                    )
                    db = bibtexparser.load(bibtex_file, parser=parser)
                    for entry in db.entries:
                        entry['source_file'] = str(file_path.name)
                    database.entries.extend(db.entries)
            except Exception as e:
                logging.error(f"Failed to load or parse '{file_path}': {e}")

        logging.info(f"Ingested {len(database.entries)} entries from {len(bib_files)} files.")
        return database
