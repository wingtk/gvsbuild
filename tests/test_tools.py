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
import sys
from unittest.mock import Mock

import pytest

from gvsbuild.utils.base_project import Project, ProjectType


def test_tools_registered():
    """Test that all tools are properly registered."""
    Project.add_all()
    tools = [p for p in Project._projects if p.type == ProjectType.TOOL]

    # Check that we have the expected tools
    tool_names = [t.name for t in tools]
    assert "cmake" in tool_names
    assert "meson" in tool_names
    assert "ninja" in tool_names
    assert "perl" in tool_names
    assert "nasm" in tool_names
    assert "cargo" in tool_names
    assert "go" in tool_names
    assert "msys2" in tool_names


def test_cmake_tool():
    """Test CMake tool initialization."""
    from gvsbuild.tools import ToolCmake

    cmake = ToolCmake()
    assert cmake.name == "cmake"
    assert cmake.version is not None
    assert cmake.archive_url is not None


def test_meson_tool():
    """Test Meson tool initialization."""
    from gvsbuild.tools import ToolMeson

    meson = ToolMeson()
    assert meson.name == "meson"
    assert meson.version is not None
    assert meson.exe_name == "meson.py"


def test_ninja_tool():
    """Test Ninja tool initialization."""
    from gvsbuild.tools import ToolNinja

    ninja = ToolNinja()
    assert ninja.name == "ninja"
    assert ninja.version is not None
    assert ninja.exe_name == "ninja.exe"


def test_perl_tool():
    """Test Perl tool initialization."""
    from gvsbuild.tools import ToolPerl

    perl = ToolPerl()
    assert perl.name == "perl"
    assert perl.version is not None


def test_nasm_tool():
    """Test NASM tool initialization."""
    from gvsbuild.tools import ToolNasm

    nasm = ToolNasm()
    assert nasm.name == "nasm"
    assert nasm.version is not None
    assert nasm.exe_name == "nasm.exe"


def test_cargo_tool():
    """Test Cargo tool initialization."""
    from gvsbuild.tools import ToolCargo

    cargo = ToolCargo()
    assert cargo.name == "cargo"
    assert cargo.version is not None
    assert cargo.exe_name == "cargo.exe"


def test_go_tool():
    """Test Go tool initialization."""
    from gvsbuild.tools import ToolGo

    go = ToolGo()
    assert go.name == "go"
    assert go.version is not None


def test_msys2_tool():
    """Test MSYS2 tool initialization."""
    from gvsbuild.tools import ToolMsys2

    msys2 = ToolMsys2()
    assert msys2.name == "msys2"
    assert msys2.internal is True


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="Windows-specific tool test"
)
def test_cmake_load_defaults():
    """Test CMake load_defaults method."""
    from gvsbuild.tools import ToolCmake

    cmake = ToolCmake()
    mock_opts = Mock()
    mock_opts.tools_root_dir = "C:\\tools"
    cmake.opts = mock_opts

    cmake.load_defaults()
    assert cmake.full_exe is not None
    assert cmake.tool_path is not None


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="Windows-specific tool test"
)
def test_perl_load_defaults():
    """Test Perl load_defaults method."""
    from gvsbuild.tools import ToolPerl

    perl = ToolPerl()
    mock_opts = Mock()
    mock_opts.tools_root_dir = "C:\\tools"
    perl.opts = mock_opts

    perl.load_defaults()
    assert perl.full_exe is not None
    assert perl.tool_path is not None
    assert perl.base_dir is not None


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="Windows-specific tool test"
)
def test_perl_get_base_dir():
    """Test Perl get_base_dir method."""
    from gvsbuild.tools import ToolPerl

    perl = ToolPerl()
    mock_opts = Mock()
    mock_opts.tools_root_dir = "C:\\tools"
    perl.opts = mock_opts
    perl.load_defaults()

    base_dir = perl.get_base_dir()
    assert base_dir is not None


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="Windows-specific tool test"
)
def test_msys2_get_path():
    """Test MSYS2 get_path method."""
    from gvsbuild.tools import ToolMsys2

    msys2 = ToolMsys2()
    mock_opts = Mock()
    mock_opts.msys_dir = "C:\\msys64"
    mock_opts.tools_root_dir = "C:\\tools"
    msys2.opts = mock_opts
    msys2.load_defaults()

    result = msys2.get_path()
    assert result is not None
    assert isinstance(result, tuple)
    assert result[0] is None  # First element should be None for msys2


@pytest.mark.skipif(
    not sys.platform.startswith("win"), reason="Windows-specific tool test"
)
def test_cargo_load_defaults():
    """Test Cargo load_defaults method."""
    from gvsbuild.tools import ToolCargo

    cargo = ToolCargo()
    mock_opts = Mock()
    mock_opts.tools_root_dir = "C:\\tools"
    cargo.opts = mock_opts
    cargo.build_dir = "C:\\tools\\cargo"

    cargo.load_defaults()
    assert cargo.full_exe is not None
    # Check if extra_env attribute exists and has expected structure
    if hasattr(cargo, "extra_env"):
        assert len(cargo.extra_env) > 0
