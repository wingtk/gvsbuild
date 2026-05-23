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

"""Tests for Meson._setup_meson_and_ninja and CmakeProject.build command construction."""

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from gvsbuild.utils.base_builders import CmakeProject, Meson
from gvsbuild.utils.simple_ui import log


@pytest.fixture(autouse=True)
def silence_log(mocker):
    """Prevent log.start_verbose / log.end from touching uninitialised Log state."""
    mocker.patch.object(log, "start_verbose")
    mocker.patch.object(log, "end")


@pytest.fixture
def meson_project(mocker, tmp_path):
    """A minimal Meson project instance with all external dependencies mocked."""
    proj = Meson.__new__(Meson)
    proj.params = []
    proj.extra_opts = None
    proj.build_dir = str(tmp_path / "build")

    builder = mocker.Mock()
    builder.opts.configuration = "release"
    builder.opts.release_configuration_is_actually_debug_optimized = False
    builder.gtk_dir = str(tmp_path / "gtk")
    proj.builder = builder

    mocker.patch.object(proj, "_get_working_dir", return_value=str(tmp_path / "src"))
    mocker.patch.object(proj, "exec_vs")

    return proj


def _captured_cmd(proj):
    """Return the cmd list that was passed to exec_vs."""
    proj.exec_vs.assert_called_once()
    return proj.exec_vs.call_args[0][0]


def test_meson_params_none_adds_nothing(meson_project, tmp_path):
    """No extra args are appended when meson_params is None."""
    ninja_build = tmp_path / "ninja"
    with patch(
        "gvsbuild.utils.base_builders.Project.get_tool_executable",
        return_value="meson.py",
    ):
        meson_project._setup_meson_and_ninja(ninja_build, None, None)

    cmd = _captured_cmd(meson_project)
    assert cmd[0] == sys.executable
    assert "meson.py" in cmd
    assert "setup" in cmd
    # python, meson.py, setup, src, ninja_build, --prefix, gtk_dir, --buildtype, <buildtype_value>
    assert len(cmd) == 9


def test_meson_params_empty_list_adds_nothing(meson_project, tmp_path):
    """An empty list behaves the same as None."""
    ninja_build = tmp_path / "ninja"
    with patch(
        "gvsbuild.utils.base_builders.Project.get_tool_executable",
        return_value="meson.py",
    ):
        meson_project._setup_meson_and_ninja(ninja_build, [], None)

    cmd = _captured_cmd(meson_project)
    assert len(cmd) == 9


def test_meson_params_single_flag(meson_project, tmp_path):
    """A single-element list appends exactly that one flag."""
    ninja_build = tmp_path / "ninja"
    with patch(
        "gvsbuild.utils.base_builders.Project.get_tool_executable",
        return_value="meson.py",
    ):
        meson_project._setup_meson_and_ninja(ninja_build, ["-Dtests=false"], None)

    cmd = _captured_cmd(meson_project)
    assert "-Dtests=false" in cmd
    assert len(cmd) == 10


def test_meson_params_multiple_flags_order_preserved(meson_project, tmp_path):
    """Multiple flags are appended in order."""
    ninja_build = tmp_path / "ninja"
    with patch(
        "gvsbuild.utils.base_builders.Project.get_tool_executable",
        return_value="meson.py",
    ):
        meson_project._setup_meson_and_ninja(ninja_build, ["-Da=x", "-Db=y"], None)

    cmd = _captured_cmd(meson_project)
    a_idx = cmd.index("-Da=x")
    b_idx = cmd.index("-Db=y")
    assert a_idx < b_idx


def test_meson_params_path_with_spaces_is_single_element(meson_project, tmp_path):
    """A path containing spaces is passed as one argv element, not split."""
    ninja_build = tmp_path / "ninja"
    path_with_spaces = r"C:\Users\my user\python.exe"
    param = f"-Dpython={path_with_spaces}"
    with patch(
        "gvsbuild.utils.base_builders.Project.get_tool_executable",
        return_value="meson.py",
    ):
        meson_project._setup_meson_and_ninja(ninja_build, [param], None)

    cmd = _captured_cmd(meson_project)
    assert param in cmd
    # The path must NOT have been word-split into multiple elements
    assert path_with_spaces not in cmd
    assert f"-Dpython={path_with_spaces.split()[0]}" not in cmd


@pytest.fixture
def cmake_project(mocker, tmp_path):
    """A minimal CmakeProject instance with all external dependencies mocked."""
    proj = CmakeProject.__new__(CmakeProject)
    proj.params = []
    proj.extra_opts = None
    proj.build_dir = str(tmp_path / "build")
    proj.pkg_dir = str(tmp_path / "pkg")

    builder = mocker.Mock()
    builder.opts.configuration = "release"
    builder.opts.release_configuration_is_actually_debug_optimized = False
    builder.gtk_dir = str(tmp_path / "gtk")
    proj.builder = builder

    mocker.patch.object(proj, "_get_working_dir", return_value=str(tmp_path / "src"))

    return proj


def _captured_cmake_cmd(proj):
    """Return the cmd list from the first builder.exec_vs call (the cmake configure step)."""
    assert proj.builder.exec_vs.call_count >= 1
    return proj.builder.exec_vs.call_args_list[0][0][0]


def test_cmake_params_none_adds_nothing(cmake_project):
    """No extra args are appended when cmake_params is None."""
    cmake_project.build(cmake_params=None, use_ninja=False, do_install=False)

    cmd = _captured_cmake_cmd(cmake_project)
    assert cmd[0] == "cmake"
    # base cmd: cmake, -G, <gen>, -DCMAKE_INSTALL_PREFIX=..., -DGTK_DIR=..., -DCMAKE_BUILD_TYPE=...
    assert len(cmd) == 6


def test_cmake_params_empty_list_adds_nothing(cmake_project):
    """An empty list behaves the same as None."""
    cmake_project.build(cmake_params=[], use_ninja=False, do_install=False)

    cmd = _captured_cmake_cmd(cmake_project)
    assert len(cmd) == 6


def test_cmake_params_single_flag(cmake_project):
    """A single-element list appends exactly that one flag."""
    cmake_project.build(
        cmake_params=["-DBUILD_TESTS=OFF"], use_ninja=False, do_install=False
    )

    cmd = _captured_cmake_cmd(cmake_project)
    assert "-DBUILD_TESTS=OFF" in cmd
    assert len(cmd) == 7


def test_cmake_params_multiple_flags_order_preserved(cmake_project):
    """Multiple flags are appended in order."""
    cmake_project.build(
        cmake_params=["-Da=x", "-Db=y", "-Dc=z"], use_ninja=False, do_install=False
    )

    cmd = _captured_cmake_cmd(cmake_project)
    a_idx = cmd.index("-Da=x")
    b_idx = cmd.index("-Db=y")
    c_idx = cmd.index("-Dc=z")
    assert a_idx < b_idx < c_idx


def test_cmake_params_path_with_spaces_is_single_element(cmake_project, tmp_path):
    """A path containing spaces is passed as one argv element, not split."""
    path_with_spaces = r"C:\Users\my user\include"
    param = f"-DFOO_INCLUDE_DIRS={path_with_spaces}"
    cmake_project.build(cmake_params=[param], use_ninja=False, do_install=False)

    cmd = _captured_cmake_cmd(cmake_project)
    assert param in cmd
    assert path_with_spaces not in cmd
    assert f"-DFOO_INCLUDE_DIRS={path_with_spaces.split()[0]}" not in cmd


def test_cmake_params_no_embedded_quotes(cmake_project, tmp_path):
    """No embedded quote characters appear in the cmd elements."""
    lib_dir = str(tmp_path / "lib")
    params = [f"-DFOO_LIB_DIRS={lib_dir}", "-DBUILD_SHARED_LIBS=ON"]
    cmake_project.build(cmake_params=params, use_ninja=False, do_install=False)

    cmd = _captured_cmake_cmd(cmake_project)
    for element in cmd:
        assert '"' not in str(element), f"Unexpected quote in cmd element: {element!r}"


def test_meson_params_no_embedded_quotes(meson_project, tmp_path):
    """No embedded quote characters are present in the cmd elements."""
    ninja_build = tmp_path / "ninja"
    python_path = str(Path(sys.executable).parent / "python.exe")
    with patch(
        "gvsbuild.utils.base_builders.Project.get_tool_executable",
        return_value="meson.py",
    ):
        meson_project._setup_meson_and_ninja(
            ninja_build,
            [f"-Dpython={python_path}", "-Dcairo_libname=cairo-gobject-2.dll"],
            None,
        )

    cmd = _captured_cmd(meson_project)
    for element in cmd:
        assert '"' not in str(element), f"Unexpected quote in cmd element: {element!r}"
