# ==============================================================================
# File: bib_ami/__main__.py
# The final CLI entry point for the application.
# ==============================================================================
import logging
from .cli import CLIParser
from .bib_tex_manager import BibTexManager


def main():
    """Main entry point for the bib-ami application."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = CLIParser()
    settings = parser.get_settings()

    try:
        manager = BibTexManager(settings=settings)
        manager.process_bibliography()
    except Exception as e:
        logging.error(f"A critical error occurred during the workflow: {e}", exc_info=True)


if __name__ == "__main__":
    main()

# NOTE: The other classes (Ingestor, Validator, etc.) would need minor modifications
# to their method signatures to return counts for the reporter, as designed
# in the BibTexManager. For example, Ingestor.ingest_from_directory would
# return (BibDatabase, int) instead of just BibDatabase.
