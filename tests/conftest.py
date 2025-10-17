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

import io
import sys

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
        stdout = io.StringIO()
        stderr = io.StringIO()
        exit_code = 0

        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = stdout
            sys.stderr = stderr

            # Call app with args list (not empty call to avoid warning)
            # Pass console if provided for consistent Rich formatting
            if console:
                app(args if args else [], console=console)
            else:
                app(args if args else [])

        except SystemExit as e:
            exit_code = e.code if e.code is not None else 0
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        return self.Result(exit_code, stdout.getvalue(), stderr.getvalue())


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


@pytest.fixture
def mock_opts(mocker, tmp_path):
    """Fixture providing a mock opts object with common attributes."""
    opts = mocker.Mock()
    opts.tools_root_dir = str(tmp_path / "tools")
    opts.build_dir = str(tmp_path / "build")
    opts.msys_dir = str(tmp_path / "msys64")
    opts.gtk_dir = str(tmp_path / "gtk")
    opts.archives_download_dir = str(tmp_path / "downloads")
    opts.patches_root_dir = str(tmp_path / "patches")
    return opts


@pytest.fixture
def mock_project(mocker):
    """Fixture providing a mock project with common attributes."""
    project = mocker.Mock()
    project.dependencies = []
    project.all_dependencies = []
    project.name = "test-project"
    return project
