#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
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


def test_build_help(typer_app, runner):
    result = runner.invoke(typer_app, ["build", "--help"])
    assert result.exit_code == 0
    assert "--help" in result.stdout


def test_wrong_project_name(typer_app, runner):
    result = runner.invoke(typer_app, ["build", "bad-name"])
    assert result.exit_code == 1
    assert "not a valid project name" in result.stdout


def test_no_project(typer_app, runner):
    result = runner.invoke(typer_app, ["build"])
    assert result.exit_code == 2
    assert "Missing argument" in result.stdout


def test_platform(tmp_dir, typer_app, runner):
    assert tmp_dir.exists()
    result = runner.invoke(
        typer_app,
        [
            "build",
            "--build-dir",
            tmp_dir,
            "--platform",
            "x86",
            "--same-python",
            "hello-world",
        ],
    )
    assert result.exit_code == 0
    assert "x86" in result.stdout
