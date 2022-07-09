import nox
import argparse

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = True

# default to the testing sessions
nox.options.sessions = ["black", "lint", "spell_check", "tests", "docs", "wheel"]

locations = "sub3", "tests", "noxfile.py"


@nox.session(python="3.10")
def black(session):
    """Run black code formatter."""

    session.install("black")
    session.run("black", *locations)


@nox.session(python="3.10")
def lint(session):
    session.install("flake8", "black")
    session.run("flake8", "--version")
    session.run("black", "--version")
    session.run("black", "--check", *locations)
    session.run("flake8", *locations)


@nox.session(python="3.10")
def spell_check(session):
    session.install("-e", ".")
    session.install("-r", "docs/requirements.txt")

    # Generate documentation into `build/docs`
    session.run(
        "sphinx-build", "-W", "-b", "spelling", "-v", "docs/", "docs/_build/html"
    )


@nox.session(python=["3.10"])
def tests(session):
    session.install("-e", ".")
    session.install("-r", "tests/requirements.txt")
    session.run("pytest")


@nox.session(python="3.10")
def docs(session):
    session.install("-e", ".")
    session.install("-r", "docs/requirements.txt")

    # Generate documentation into `build/docs`
    session.run("sphinx-build", "-W", "-b", "html", "-v", "docs/", "docs/_build/html")


@nox.session(python="3.10")
def wheel(session):
    session.install("twine", "wheel")

    # Generate documentation into `build/docs`
    session.run("python", "setup.py", "sdist", "bdist_wheel")
    session.run("twine", "check", "dist/*")


@nox.session
def release(session: nox.Session) -> None:

    wheel(session)

    """
    Kicks off an automated release process by creating and pushing a new tag.

    Invokes bump2version with the posarg setting the version.

    Usage:
    $ nox -s release -- [major|minor|patch]
    """
    parser = argparse.ArgumentParser(description="Release a semver version.")
    parser.add_argument(
        "version",
        type=str,
        nargs=1,
        help="The type of semver release to make.",
        choices={"major", "minor", "patch"},
    )
    args: argparse.Namespace = parser.parse_args(args=session.posargs)
    version: str = args.version.pop()

    # If we get here, we should be good to go
    # Let's do a final check for safety
    confirm = input(
        f"You are about to bump the {version!r} version. Are you sure? [y/n]: "
    )

    # Abort on anything other than 'y'
    if confirm.lower().strip() != "y":
        session.error(f"You said no when prompted to bump the {version!r} version.")

    session.install("bump2version")

    session.log(f"Bumping the {version!r} version")
    session.run("bump2version", version)

    session.log("Pushing the new tag")
    session.run("git", "push", external=True)
    session.run("git", "push", "--tags", external=True)
