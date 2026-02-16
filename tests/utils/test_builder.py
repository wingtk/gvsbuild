#  Copyright (C) 2026 The Gvsbuild Authors
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
from subprocess import CalledProcessError

import pytest

from gvsbuild.utils.base_project import Options
from gvsbuild.utils.builder import Builder, CheckVsInstallError


def test_vs_check_error_if_version_not_matching():
    opts = Options()
    opts.vs_ver = "17"
    builder = Builder.__new__(Builder)
    builder.opts = opts
    builder.vs_ver_year = "vs2022"

    with pytest.raises(
        CheckVsInstallError, match="Doesn't match target Visual Studio version of 17"
    ):
        builder._Builder__check_vs_install(
            opts, r"C:\Program Files\Microsoft Visual Studio\18\Community", True
        )


def test_vs_check_error_if_not_vcvars_exists(tmp_path):
    opts = Options()
    opts.platform = "x64"
    builder = Builder.__new__(Builder)
    builder.opts = opts

    with pytest.raises(CheckVsInstallError, match="vcvars64.bat could not be found"):
        builder._Builder__check_vs_install(opts, str(tmp_path), False)


def test_vs_check_error_if_vcvars_fails(tmp_path):
    opts = Options()
    opts.platform = "x64"
    builder = Builder.__new__(Builder)
    builder.opts = opts
    vcvars_path = tmp_path / "VC" / "Auxiliary" / "Build" / "vcvars64.bat"
    vcvars_path.parent.mkdir(parents=True)
    vcvars_path.write_text("exit 1")

    with pytest.raises(CalledProcessError):
        builder._Builder__check_vs_install(opts, str(tmp_path), False)


def test_vs_check_error_if_vcvars_no_env(tmp_path):
    opts = Options()
    opts.platform = "x64"
    builder = Builder.__new__(Builder)
    builder.opts = opts
    vcvars_path = tmp_path / "VC" / "Auxiliary" / "Build" / "vcvars64.bat"
    vcvars_path.parent.mkdir(parents=True)
    vcvars_path.write_text("exit 0")

    with pytest.raises(
        CheckVsInstallError, match="did not export environment variables properly"
    ):
        builder._Builder__check_vs_install(opts, str(tmp_path), False)


def test_vs_check_success(tmp_path):
    opts = Options()
    opts.platform = "x64"
    builder = Builder.__new__(Builder)
    builder.opts = opts
    vcvars_path = tmp_path / "VC" / "Auxiliary" / "Build" / "vcvars64.bat"
    vcvars_path.parent.mkdir(parents=True)
    vcvars_path.write_text("SET FOO=BAR")
    builder._Builder__check_vs_install(opts, str(tmp_path), False)
