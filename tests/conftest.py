#  Copyright (C) 2016 The Gvsbuild Authors
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>.

import pytest


class CycloptsRunner:
    """Test runner for Cyclopts apps."""

    class Result:
        def __init__(self, exit_code, stdout, stderr):
            self.exit_code = exit_code
            self.output = stdout
            self.stdout = stdout
            self.stderr = stderr

    def invoke(self, app, args, console=None, **kwargs):
        """Invoke a Cyclopts app with given arguments.

        Args:
            app: The Cyclopts App instance to invoke
            args: List of command-line arguments
            console: Optional Rich Console for consistent output formatting
            **kwargs: Additional keyword arguments (ignored for compatibility)

        Returns:
            Result object with exit_code, output, stdout, and stderr
        """

        exit_code = 0

        # Capture stdout and stderr using pytest's capsys
        # We'll call the app and catch SystemExit
        try:
            # Capture output
            import io
            import sys as _sys

            stdout = io.StringIO()
            stderr = io.StringIO()

            old_stdout = _sys.stdout
            old_stderr = _sys.stderr

            try:
                _sys.stdout = stdout
                _sys.stderr = stderr

                # Call app with args list (not empty call to avoid warning)
                # Pass console if provided for consistent Rich formatting
                if console:
                    app(args if args else [], console=console)
                else:
                    app(args if args else [])

            except SystemExit as e:
                exit_code = e.code if e.code is not None else 0
            except Exception as e:
                import traceback

                stderr.write(str(e) + "\n")
                stderr.write(traceback.format_exc())
                exit_code = 1
            finally:
                _sys.stdout = old_stdout
                _sys.stderr = old_stderr

        except Exception as e:
            # Fallback error handling
            import traceback

            exit_code = 1
            stderr = io.StringIO(str(e) + "\n" + traceback.format_exc())
            stdout = io.StringIO()

        return self.Result(
            exit_code,
            stdout.getvalue() if hasattr(stdout, "getvalue") else "",
            stderr.getvalue() if hasattr(stderr, "getvalue") else "",
        )


@pytest.fixture
def app():
    """Fixture providing the gvsbuild Cyclopts app instance."""
    from gvsbuild.main import app as gvsbuild_app

    yield gvsbuild_app


@pytest.fixture(scope="session")
def tmp_dir(tmp_path_factory):
    """Fixture providing a temporary directory for testing."""
    return tmp_path_factory.mktemp("gtk-build")


@pytest.fixture
def runner():
    """Fixture providing a CycloptsRunner for testing."""
    return CycloptsRunner()


@pytest.fixture
def console():
    """Fixture providing a Rich console with consistent settings for testing."""
    from rich.console import Console

    return Console(
        width=80,
        force_terminal=True,
        highlight=False,
        color_system=None,
        legacy_windows=False,
    )
