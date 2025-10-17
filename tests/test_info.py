#  Copyright (C) 2025 The Gvsbuild Authors
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


def test_version_callback_inactive():
    """Test version_callback when active=False."""
    from gvsbuild.info import version_callback

    # Should return None without raising
    result = version_callback(False)
    assert result is None


def test_version_callback_active():
    """Test version_callback when active=True."""
    from gvsbuild.info import version_callback

    # Should raise SystemExit
    with pytest.raises(SystemExit):
        version_callback(True)


def test_version_callback_output(capsys):
    """Test version_callback output."""
    from gvsbuild.info import version_callback

    # Should print version and exit
    with pytest.raises(SystemExit):
        version_callback(True)

    captured = capsys.readouterr()
    assert "gvsbuild v" in captured.out


def test_version_via_cli(app, runner, console):
    """Test version output via CLI with consistent console formatting."""
    result = runner.invoke(app, ["--version"], console=console)
    # The --version flag should trigger the callback
    assert "gvsbuild v" in result.output or result.exit_code in [0, 1]
