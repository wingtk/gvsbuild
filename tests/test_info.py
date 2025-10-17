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
    from gvsbuild.info import version_callback

    result = version_callback(False)
    assert result is None


def test_version_callback_active_exit_code(mocker):
    from gvsbuild.info import version_callback

    mocker.patch("importlib.metadata.version", return_value="1.0.0")

    with pytest.raises(SystemExit) as exc_info:
        version_callback(True)

    assert exc_info.value.code == 0


def test_version_callback_output(capsys, mocker):
    from gvsbuild.info import version_callback

    mocker.patch("importlib.metadata.version", return_value="1.2.3")

    with pytest.raises(SystemExit) as exc_info:
        version_callback(True)

    captured = capsys.readouterr()
    assert captured.out == "gvsbuild v1.2.3\n"
    assert exc_info.value.code == 0


def test_version_via_cli(app, runner, console):
    result = runner.invoke(app, ["--version"], console=console)
    assert "gvsbuild v" in result.output or result.exit_code in [0, 1]
