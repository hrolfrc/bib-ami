Usage & Configuration
=====================

This section serves as a reference guide for users who want to customize
the behavior of ``bib-ami``. It provides a detailed description of all
available command-line arguments and explains how to use a configuration
file for persistent settings.

Command-Line Reference
----------------------

The ``bib-ami`` tool is controlled via a set of command-line arguments.
The basic syntax is as follows:

.. code:: bash

   bib-ami --input-dir <path> --output-file <path> [options]

Below is a complete list of all available options.

``–input-dir <path>``
   | 
   | **(Required)** Specifies the path to the directory containing the
     source ``.bib`` files that you want to process. The tool will scan
     this directory for all files ending with the ``.bib`` extension.

``–output-file <path>``
   | 
   | **(Required)** Specifies the full path, including the filename, for
     the main cleaned and verified bibliography file. For example:
     ``output/final_library.bib``.

``–suspect-file <path>``
   | 
   | (Optional) Specifies the path for a separate file where all
     ’Suspect’ entries will be saved. A suspect entry is one that could
     not be verified (e.g., a modern journal article with no DOI). This
     option is most effective when used with ``–filter-validated``.

``–merge-only``
   | 
   | (Optional) A flag that instructs the tool to perform only the first
     phase of the workflow. It will merge all source ``.bib`` files into
     the specified output file without performing any deduplication,
     validation, or enrichment.

``–email <address>``
   | 
   | (Optional) Specifies the email address to be used for querying the
     CrossRef API. Providing an email is part of CrossRef’s "Polite
     Pool" policy, which helps them contact you if your script causes
     issues and may result in more reliable API access. This argument
     overrides any email set in the configuration file.

``–filter-validated``
   | 
   | (Optional) A flag that changes the output behavior. When this flag
     is active, only entries that are fully ’Verified’ (i.e., have a
     trusted DOI and refreshed metadata) will be saved to the main
     ``–output-file``. All other entries (’Accepted’ and ’Suspect’) will
     be saved to the file specified by ``–suspect-file``. If
     ``–suspect-file`` is not provided, non-verified entries will be
     commented out in the main output file.

Configuration File
------------------

For settings that you use frequently, such as your email address, you
can create a configuration file to avoid typing the same argument
repeatedly.

#. Create a file named ``bib_ami_config.json`` in the directory from
   which you are running the ``bib-ami`` command.

#. Add your settings to the file in JSON format. Currently, only the
   email address is supported.

::

   {
     "email": "your.name@university.edu"
   }

Order of Precedence
~~~~~~~~~~~~~~~~~~~

The tool uses the following order of precedence for settings:

#. A command-line argument (e.g., ``–email``) will **always override**
   any other setting.

#. If a command-line argument is not provided, the tool will look for
   the setting in the ``bib_ami_config.json`` file.

#. If the setting is found in neither location, a default value may be
   used, or the user may be prompted if the setting is required.
