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
from typer.testing import CliRunner


@pytest.fixture
def typer_app():
    from gvsbuild.main import app

    yield app
    del app


@pytest.fixture(scope="session")
def tmp_dir(tmp_path_factory):
    return tmp_path_factory.mktemp("gtk-build")


@pytest.fixture
def runner():
    return CliRunner()
