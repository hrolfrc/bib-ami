import argparse
import logging
import unittest

from bib_ami.bibtex_manager import BibTexManager
from tests.fixtures.bibtex_simulator import BibTexSimulator
from tests.fixtures.bibtex_test_directory import BibTexTestDirectory
from tests.mocks.api_client import MockCrossRefClient

# --- Configure Logging ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestRandomizedRun(unittest.TestCase):
    def test_randomized_workflow_does_not_crash(self):
        for i in range(3):
            with BibTexTestDirectory(f"random_test_{i}") as manager_dir:
                simulator = BibTexSimulator(manager_dir)
                simulator.populate_directory(
                    num_files=2, entries_per_file=5, broken_ratio=0.2
                )
                settings = argparse.Namespace(
                    input_dir=manager_dir.path,
                    output_file=manager_dir.path / "final.bib",
                    suspect_file=manager_dir.path / "suspect.bib",
                    email="test@example.com",
                    filter_validated=False,
                    merge_only=False,
                )
                mock_client = MockCrossRefClient(settings.email)
                main_manager = BibTexManager(settings, client=mock_client)
                main_manager.process_bibliography()
                self.assertTrue(True, f"Run {i+1} completed without errors.")


if __name__ == "__main__":
    unittest.main()
