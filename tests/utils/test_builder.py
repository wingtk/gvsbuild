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

from gvsbuild.build import VsVer
from gvsbuild.utils.base_project import Options
from gvsbuild.utils.builder import VS_ZIP_PARTS, Builder, CheckVsInstallError


@pytest.fixture
def msbuild_builder(mocker):
    """Builder with opts configured for _create_msbuild_opts tests."""
    b = Builder.__new__(Builder)
    b.opts = mocker.Mock()
    b.opts.platform = "x64"
    b.opts.win_sdk_ver = None
    b.opts.net_target_framework = None
    b.opts.net_target_framework_version = None
    b.opts.msbuild_opts = None
    return b


def test_create_msbuild_opts_minimal(msbuild_builder):
    result = msbuild_builder._create_msbuild_opts(None)
    assert "/nologo" in result
    assert "/p:Platform=x64" in result
    assert not any("PythonPath" in s for s in result)


def test_create_msbuild_opts_with_python(msbuild_builder, tmp_path):
    result = msbuild_builder._create_msbuild_opts(tmp_path)
    assert f"/p:PythonPath={tmp_path}" in result
    assert f"/p:PythonDir={tmp_path}" in result


def test_create_msbuild_opts_with_sdk_ver(msbuild_builder):
    msbuild_builder.opts.win_sdk_ver = "10.0.22000.0"
    result = msbuild_builder._create_msbuild_opts(None)
    assert "/p:WindowsTargetPlatformVersion=10.0.22000.0" in result


def test_create_msbuild_opts_with_framework(msbuild_builder):
    msbuild_builder.opts.net_target_framework = "net6.0"
    result = msbuild_builder._create_msbuild_opts(None)
    assert "/p:TargetFrameworks=net6.0" in result


def test_create_msbuild_opts_extra_opts_are_split(msbuild_builder):
    msbuild_builder.opts.msbuild_opts = "/m:4 /nr:false"
    result = msbuild_builder._create_msbuild_opts(None)
    assert "/m:4" in result
    assert "/nr:false" in result


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


def test_vs_zip_parts_entries():
    assert VS_ZIP_PARTS["17"] == "vs2022"
    assert VS_ZIP_PARTS["18"] == "vs2026"
    assert all(k.isdigit() for k in VS_ZIP_PARTS)


def test_vsver_has_latest():
    assert VsVer.latest == "latest"
    assert VsVer.latest.value == "latest"


def test_extract_paths_returns_path_and_major_tuples():
    builder = Builder.__new__(Builder)
    res = [
        {
            "displayName": "Visual Studio Enterprise 2026",
            "installationPath": r"C:\VS\18\Enterprise",
            "installationVersion": "18.0.35410.57",
        },
        {
            "displayName": "Visual Studio Community 2022",
            "installationPath": r"C:\VS\17\Community",
            "installationVersion": "17.13.0.0",
        },
    ]
    result = builder._Builder__extract_paths(res)
    assert result == [
        (r"C:\VS\18\Enterprise", "18"),
        (r"C:\VS\17\Community", "17"),
    ]


def test_extract_paths_handles_missing_installation_version():
    builder = Builder.__new__(Builder)
    res = [{"displayName": "VS", "installationPath": r"C:\VS"}]
    result = builder._Builder__extract_paths(res)
    assert result == [(r"C:\VS", "0")]


_FAKE_VS_ENV = "PATH=C:\\Windows\nFOO=BAR\n"


@pytest.fixture
def latest_builder(mocker):
    """Partially constructed Builder ready for __check_vs 'latest' tests."""
    opts = Options()
    opts.vs_ver = "latest"
    opts.vs_install_path = None
    opts.platform = "x64"
    opts.win_sdk_ver = "10.0.22000.0"  # skip SDK auto-detection

    builder = Builder.__new__(Builder)
    builder.opts = opts
    builder.gtk_dir = r"C:\gtk"

    mocker.patch("gvsbuild.utils.builder.script_title")
    mocker.patch("gvsbuild.utils.builder.log")
    mocker.patch.object(builder, "add_global_env")

    return builder, opts


def test_check_vs_latest_selects_newest_install(latest_builder, mocker):
    builder, opts = latest_builder

    # vswhere returns VS 2022 first, then VS 2026 — latest should sort and pick 2026
    mocker.patch.object(
        builder,
        "_Builder__dump_vs_loc",
        return_value=[
            (r"C:\VS\17\Enterprise", "17"),
            (r"C:\VS\18\Enterprise", "18"),
        ],
    )
    mocker.patch.object(
        builder, "_Builder__check_vs_install", return_value=_FAKE_VS_ENV
    )

    builder._Builder__check_vs(opts)

    assert opts.vs_ver == "18"
    assert builder.vs_ver_year == "vs2026"


def test_check_vs_latest_falls_back_to_older_version(latest_builder, mocker):
    builder, opts = latest_builder

    mocker.patch.object(
        builder,
        "_Builder__dump_vs_loc",
        return_value=[
            (r"C:\VS\17\Enterprise", "17"),
            (r"C:\VS\18\Enterprise", "18"),
        ],
    )

    def _check_install_side_effect(_opts, path, _assert):
        if "18" in path:
            raise CheckVsInstallError("vcvars not found")
        return _FAKE_VS_ENV

    mocker.patch.object(
        builder,
        "_Builder__check_vs_install",
        side_effect=_check_install_side_effect,
    )

    builder._Builder__check_vs(opts)

    assert opts.vs_ver == "17"
    assert builder.vs_ver_year == "vs2022"


def test_check_vs_install_path_major_extracted_from_path(latest_builder, mocker):
    builder, opts = latest_builder
    opts.vs_install_path = r"C:\Program Files\Microsoft Visual Studio\18\Enterprise"

    mocker.patch.object(
        builder, "_Builder__check_vs_install", return_value=_FAKE_VS_ENV
    )

    builder._Builder__check_vs(opts)

    assert opts.vs_ver == "18"
    assert builder.vs_ver_year == "vs2026"
