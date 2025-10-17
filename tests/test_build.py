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
import sys

import pytest


def test_build_help(app, runner, console):
    """Test build command help output with consistent console formatting."""
    result = runner.invoke(app, ["build", "--help"], console=console)
    assert result.exit_code == 0
    assert "Build a project or a list of projects" in result.output
    assert "PROJECTS" in result.output
    assert "--platform" in result.output


def test_wrong_project_name(app, runner):
    result = runner.invoke(app, ["build", "bad-name"], color=True)
    assert result.exit_code == 1
    full_output = result.output + result.stderr
    assert "not a valid project name" in full_output


def test_no_project(app, runner):
    result = runner.invoke(app, ["build"])
    # Cyclopts returns exit code 1 for errors
    assert result.exit_code in [1, 2]
    full_output = result.output + result.stderr
    assert (
        "requires an argument" in full_output.lower()
        or "required" in full_output.lower()
        or "missing" in full_output.lower()
        or "at least one project" in full_output.lower()
    )


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="windll only available on Windows"
)
def test_platform(tmp_dir, app, runner):
    # This test just ensures the command can be invoked with platform argument
    # Actual building may fail due to missing tools/dependencies in test environment
    assert tmp_dir.exists()
    result = runner.invoke(
        app,
        [
            "build",
            "--build-dir",
            tmp_dir,
            "--platform",
            "x86",
            "hello-world",
        ],
    )
    # Exit code may be 0 (success) or 1 (build error), but should not be 2 (argument error)
    assert result.exit_code in [0, 1]
