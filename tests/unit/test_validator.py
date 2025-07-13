# tests/unit/test_validator.py

import unittest
from unittest.mock import MagicMock

from bib_ami.validator import Validator
from tests.fixtures.record_builder import RecordBuilder  # Assuming this is available


class TestValidatorUnit(unittest.TestCase):
    """
    Focused unit tests for the private _validate_entry method in the Validator.
    """

    def setUp(self):
        """Set up a mock client and a Validator instance for each test."""
        # Create a mock client that we can control for each test case
        self.mock_client = MagicMock()
        self.validator = Validator(client=self.mock_client)

    def test_validate_entry_for_book(self):
        """
        Rule 1: Books should be treated as pre-validated and should NOT call the client.
        The method should return the book's own DOI if present.
        """
        # Arrange: Create a book entry with a DOI
        book_with_doi = RecordBuilder("book1").as_book().with_doi("10.9999/book.doi").build()

        # Act
        result = self.validator._validate_entry(book_with_doi)

        # Assert
        self.assertEqual(result, "10.9999/book.doi")
        self.mock_client.get_doi_for_entry.assert_not_called()

    def test_validate_entry_for_book_without_doi(self):
        """
        Rule 1a: A book without a DOI should also not call the client and return None.
        """
        # Arrange
        book_without_doi = RecordBuilder("book2").as_book().build()

        # Act
        result = self.validator._validate_entry(book_without_doi)

        # Assert
        self.assertIsNone(result)
        self.mock_client.get_doi_for_entry.assert_not_called()

    def test_validate_entry_for_article_with_found_doi(self):
        """
        Rule 2: A standard entry should call the client, which finds a DOI.
        """
        # Arrange
        article = RecordBuilder("article1").with_title("An Article").build()
        expected_doi = "10.1234/article.doi"
        self.mock_client.get_doi_for_entry.return_value = expected_doi

        # Act
        result = self.validator._validate_entry(article)

        # Assert
        self.assertEqual(result, expected_doi)
        self.mock_client.get_doi_for_entry.assert_called_once_with(article)

    def test_validate_entry_for_article_with_no_doi_found(self):
        """
        Rule 3: A standard entry should call the client, which does not find a DOI.
        """
        # Arrange
        article = RecordBuilder("article2").with_title("Another Article").build()
        self.mock_client.get_doi_for_entry.return_value = None

        # Act
        result = self.validator._validate_entry(article)

        # Assert
        self.assertIsNone(result)
        self.mock_client.get_doi_for_entry.assert_called_once_with(article)


if __name__ == '__main__':
    unittest.main(verbosity=2)