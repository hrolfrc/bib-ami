# ==============================================================================
# File: tests/mocks/api_client.py
# Contains the mock for the CrossRefClient.
# ==============================================================================


class MockCrossRefClient:
    """
    A mock client that simulates the CrossRefClient for testing purposes.

    It returns canned responses based on the input to test different
    scenarios without making real network calls.
    """
    def __init__(self, email: str):
        # The email is stored but not used in the mock.
        self.email = email
        self.doi_map = {
            "Attention Is All You Need": "10.1234/attention.doi"
        }

    def get_doi_for_entry(self, entry: dict) -> str or None:
        """
        Simulates finding a DOI based on the entry's title.
        """
        title = entry.get("title")
        return self.doi_map.get(title)

    # noinspection PyUnusedLocal
    @staticmethod
    def get_metadata_by_doi(doi: str, original_entry: dict) -> dict or None:
        """
        FIXED: This method now accepts the 'original_entry' keyword argument
        to match the signature of the real CrossRefClient.

        It simulates returning canonical metadata for a known DOI.
        """
        # We can ignore original_entry in the mock; we just need to accept it.
        if doi == "10.1234/attention.doi":
            # This is the "canonical" data the e2e test will check for.
            return {
                "title": ["Attention Is All You Need (Canonical)"],
                "author": [{"family": "Vaswani", "given": "Ashish"}],
                "year": "2017",
                "journal": "Advances in Neural Information Processing Systems"
            }
        return None
