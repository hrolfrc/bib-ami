# ==============================================================================
# File: bib_ami/bib_tex_manager.py
# Updated orchestrator that uses the CLI settings and reporter.
# ==============================================================================

# ==============================================================================
# File: bib_ami/bib_tex_manager.py
# Updated orchestrator that now uses the full reporting capabilities.
# ==============================================================================
import argparse
import logging

import bibtexparser
from bibtexparser.bwriter import BibTexWriter

from .cross_ref_client import CrossRefClient
# Assume other classes are defined in their respective files
from .ingestor import Ingestor
from .reconciler import Reconciler
from .reporter import SummaryReporter
from .triage import Triage
from .validator import Validator
from .writer import Writer


# noinspection PyArgumentList
class BibTexManager:
    """Orchestrates the bibliography processing workflow."""

    def __init__(self, settings: argparse.Namespace):
        self.settings = settings
        self.reporter = SummaryReporter()
        self.ingestor = Ingestor()
        self.client = CrossRefClient(email=self.settings.email)
        self.validator = Validator(client=self.client)
        self.reconciler = Reconciler()
        self.triage = Triage()
        self.writer = Writer()

    def process_bibliography(self):
        """Executes the full, integrity-first workflow."""
        # Phase 1
        database, num_files = self.ingestor.ingest_from_directory(self.settings.input_dir)
        self.reporter.update_summary("files_processed", num_files)
        self.reporter.update_summary("entries_ingested", len(database.entries))

        if self.settings.merge_only:
            # Simplified write for merge-only
            simple_writer = BibTexWriter()
            with open(self.settings.output_file, 'w', encoding='utf-8') as f:
                bibtexparser.dump(database, f, simple_writer)
            logging.info(f"Merge-only complete. Wrote {len(database.entries)} raw entries.")
            self.reporter.log_summary()
            return

        # Phase 2
        database, validated_count = self.validator.validate_all(database)
        self.reporter.update_summary("dois_validated_or_added", validated_count)

        # Phase 3
        database, duplicates_removed = self.reconciler.deduplicate(database)
        self.reporter.update_summary("duplicates_removed", duplicates_removed)

        # Phase 4
        verified_db, suspect_db = self.triage.run_triage(
            database,
            self.settings.filter_validated
        )
        self.reporter.update_summary("final_verified_count", len(verified_db.entries))
        self.reporter.update_summary("final_suspect_count", len(suspect_db.entries))
        self.writer.write_files(verified_db, suspect_db, self.settings.output_file, self.settings.suspect_file)

        logging.info("--- Workflow Complete ---")
        self.reporter.log_summary()

# NOTE: The other classes (CLIParser, Ingestor, Validator, Triage, Reporter) would also be
# imported and used by the main application entry point. This example focuses on the
# classes that needed significant changes for this step.
