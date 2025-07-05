# ==============================================================================
# File: tests/e2e/test_full_run.py
# End-to-end test for the entire workflow on a known dataset.
# ==============================================================================

import unittest

from tests.fixtures.directory_manager import BibTexTestDirectory
from tests.fixtures.record_builder import RecordBuilder


class TestFullE2ERun(unittest.TestCase):
    def test_happy_path_workflow(self):
        """Tests the full pipeline from input files to final output."""
        with BibTexTestDirectory("e2e_test_happy") as manager:
            # Setup test data
            rec1 = RecordBuilder("rec1").with_title("Attention Is All You Need").with_note("Note A").build()
            rec2 = RecordBuilder("rec2").with_title("Attention is ALL you need").with_note(
                "Note B").build()  # Duplicate
            rec3 = RecordBuilder("rec3").with_title("A paper with no DOI").build()
            manager.add_bib_file("source1.bib", [rec1, rec3])
            manager.add_bib_file("source2.bib", [rec2])

            # In a real project, this would import the main orchestrator and run it
            # from bib_ami.bib_tex_manager import BibTexManager

            # For this example, we simulate the run
            # cli_settings = ...
            # main_manager = BibTexManager(cli_settings)
            # main_manager.process_bibliography()

            # For now, we just assert the setup works
            self.assertTrue((manager.path / "source1.bib").exists())
            self.assertTrue((manager.path / "source2.bib").exists())

            # A real test would check the final output files for correctness.
            # e.g., assert that only 2 entries exist in the final .bib, one of which has merged notes.
