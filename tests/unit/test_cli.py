# tests/unit/test_cli.py

import unittest
from unittest.mock import patch
from pathlib import Path

# Assuming your source code is structured in a way that allows this import
from bib_ami.cli import CLIParser


class TestCLIParser(unittest.TestCase):
    """
    Unit tests for the command-line interface parser (CLIParser).
    """

    @patch('sys.argv',
           ['__main__', '--input-dir', 'in', '--output-file', 'out/final.bib', '--email', 'test@example.com'])
    def test_get_settings_generates_default_suspect_file(self):
        """
        Test Case 1: Verify that a default suspect_file path is created
        when one is not provided.
        """
        # Arrange
        parser = CLIParser()
        expected_suspect_path = Path("out/final.suspect.bib")

        # Act
        settings = parser.get_settings()

        # Assert
        self.assertIsNotNone(settings.suspect_file)
        self.assertEqual(settings.suspect_file, expected_suspect_path)

    @patch('sys.argv',
           ['__main__', '--input-dir', 'in', '--output-file', 'out.bib', '--suspect-file', 'custom/explicit.bib',
            '--email', 'test@example.com'])
    def test_get_settings_respects_provided_suspect_file(self):
        """
        Test Case 2: Verify that a user-provided suspect_file path is
        used and not overwritten by the default logic.
        """
        # Arrange
        parser = CLIParser()
        expected_suspect_path = Path("custom/explicit.bib")

        # Act
        settings = parser.get_settings()

        # Assert
        self.assertEqual(settings.suspect_file, expected_suspect_path)

    @patch('sys.argv', ['__main__', '--input-dir', 'in', '--output-file', 'out.bib'])
    def test_get_settings_errors_without_email(self):
        """
        Test Case 3: Verify that the parser correctly exits if the required
        --email argument is not provided.
        """
        # Arrange
        parser = CLIParser()

        # Act & Assert
        # The parser.error() method raises a SystemExit, so we test for that
        with self.assertRaises(SystemExit):
            parser.get_settings()


if __name__ == '__main__':
    unittest.main(verbosity=2)
