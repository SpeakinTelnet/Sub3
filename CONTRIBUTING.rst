
============
Contributing
============

Contributions are welcome, either in the form of reports or fixes. Refer to the 
`GitHub repo <https://github.com/SpeakinTelnet/Sub3>`_ for issues and
pull requests.


Report Bugs
-----------

If you are reporting a bug, please include:

* Your operating system.
* Detailed steps to reproduce the bug.


Enhancement Guidelines
----------------------

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

Pull Request Guidelines
-----------------------

Your pull request should pass the ``nox`` test. 

nox will run:

.. code-block:: console
    
    $ pytest # Test suite
    $ black sub3 tests noxfile.py # Linting
    $ flake8 sub3 tests noxfile.py # General fomarting check
    $ sphinx-build -W -b html -v docs/ docs/_build/html # Regenerate the docs

Deploying
---------

A reminder for the maintainers on how to deploy.
Make sure all your changes are committed (including an entry in HISTORY.rst).
Then run

.. code-block:: console

    $ nox -s release -- patch

    #  "major", "minor", "patch"
    #     \____,   |   ,___|
    #          1 . 0 . 0


CircleCI will then deploy to PyPI if tests pass.
