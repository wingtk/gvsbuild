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


def test_main_help(app, runner, console):
    """Test main app help output with consistent console formatting."""
    result = runner.invoke(app, ["--help"], console=console)
    assert result.exit_code == 0
    assert "Build GTK for Windows" in result.stdout
    assert "build" in result.stdout
    assert "outdated" in result.stdout
    assert "deps" in result.stdout
    assert "list" in result.stdout


def test_wrong_command(app, runner):
    result = runner.invoke(app, ["builds"])
    # Cyclopts returns exit code 1 for errors
    assert result.exit_code in [1, 2]
    # Cyclopts outputs errors to stdout
    full_output = result.stdout + result.stderr
    assert (
        "builds" in full_output
        or "command" in full_output.lower()
        or "unrecognized" in full_output.lower()
    )
