# ==============================================================================
# This is a self-contained test suite for bib-ami.
# It includes the application classes and the test classes in one file
# to demonstrate a complete, working, and testable system.
# ==============================================================================
import logging
import random

# --- Configure Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import argparse
import unittest

# ==============================================================================
# SECTION 3: TEST CASES
# ==============================================================================
from tests.mocks.api_client import MockCrossRefClient
from tests.fixtures.bibtex_test_directory import BibTexTestDirectory
from tests.fixtures.record_builder import RecordBuilder
from bib_ami.bibtex_manager import BibTexManager


# ==============================================================================
# SECTION 3: TEST CASES
# ==============================================================================


class TestRandomizedRun(unittest.TestCase):
    def test_randomized_workflow_does_not_crash(self):
        """Runs the full workflow with random data to check for robustness."""
        for i in range(3):
            with BibTexTestDirectory(f"random_test_{i}") as manager_dir:
                num_files, entries_per_file = random.randint(1, 2), random.randint(2, 4)
                for j in range(num_files):
                    entries = [RecordBuilder().with_title(f"Random Paper {k}").build() for k in range(entries_per_file)]
                    manager_dir.add_bib_file(f"random_source_{j}.bib", entries)

                settings = argparse.Namespace(
                    input_dir=manager_dir.path,
                    output_file=manager_dir.path / "final.bib",
                    suspect_file=manager_dir.path / "suspect.bib",
                    email="test@example.com",
                    filter_validated=False
                )

                mock_client = MockCrossRefClient(settings.email)
                main_manager = BibTexManager(settings, client=mock_client)

                main_manager.process_bibliography()
                self.assertTrue(True, f"Run {i + 1} completed without errors.")


if __name__ == '__main__':
    unittest.main()
