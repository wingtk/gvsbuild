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


def test_main_help(typer_app, runner):
    result = runner.invoke(typer_app, ["--help"])
    assert result.exit_code == 0
    assert "build" in result.stdout
    assert "outdated" in result.stdout
    assert "deps" in result.stdout
    assert "list" in result.stdout


def test_wrong_command(typer_app, runner):
    result = runner.invoke(typer_app, ["builds"])
    assert result.exit_code == 2
    assert "No such command" in result.stdout
