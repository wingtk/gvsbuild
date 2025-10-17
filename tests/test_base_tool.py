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
import os
from unittest.mock import Mock

import pytest

from gvsbuild.utils.base_tool import Tool, tool_add


def test_tool_creation():
    """Test Tool creation."""
    tool = Tool("test-tool")
    assert tool.name == "test-tool"
    assert tool.mark_deps is False


def test_tool_with_dir_part():
    """Test Tool with dir_part."""
    tool = Tool("test-tool", version="1.0.0", dir_part="test-{version}")
    assert tool.dir_part == "test-1.0.0"


def test_tool_load_defaults_with_dir_part(tmp_path):
    """Test Tool load_defaults with dir_part."""
    tool = Tool("test-tool", version="1.0.0", dir_part="test-{version}")
    mock_opts = Mock()
    mock_opts.tools_root_dir = str(tmp_path)
    tool.opts = mock_opts

    tool.load_defaults()
    assert str(tmp_path / "test-1.0.0") in tool.build_dir


def test_tool_load_defaults_without_dir_part(tmp_path):
    """Test Tool load_defaults without dir_part."""
    tool = Tool("test-tool")
    mock_opts = Mock()
    mock_opts.tools_root_dir = str(tmp_path)
    tool.opts = mock_opts

    tool.load_defaults()
    assert str(tmp_path / "test-tool") in tool.build_dir


def test_tool_with_exe_name(tmp_path):
    """Test Tool with exe_name."""
    tool = Tool("test-tool", exe_name="test.exe")
    mock_opts = Mock()
    mock_opts.tools_root_dir = str(tmp_path)
    tool.opts = mock_opts

    tool.load_defaults()
    assert tool.full_exe is not None
    assert "test.exe" in tool.full_exe


def test_tool_mark(tmp_path):
    """Test tool_mark method."""
    tool = Tool("test-tool")
    tool.build_dir = str(tmp_path / "test-tool-mark")

    # Initially directory doesn't exist
    assert not os.path.exists(tool.build_dir)

    # Call tool_mark
    tool.tool_mark()

    # Now directory should exist
    assert os.path.exists(tool.build_dir)
    assert tool.mark_deps is True


def test_tool_mark_existing_dir(tmp_path):
    """Test tool_mark with existing directory."""
    build_dir = tmp_path / "existing"
    build_dir.mkdir()

    tool = Tool("test-tool")
    tool.build_dir = str(build_dir)
    tool.mark_deps = False

    # Call tool_mark on existing directory
    tool.tool_mark()

    # mark_deps should remain False
    assert tool.mark_deps is False


def test_tool_build_no_mark():
    """Test tool build method when mark_deps is False."""
    tool = Tool("test-tool")
    tool.mark_deps = False

    result = tool.build()
    assert result is True  # Returns not mark_deps


def test_tool_build_with_mark():
    """Test tool build method when mark_deps is True."""
    tool = Tool("test-tool")
    tool.mark_deps = True

    result = tool.build()
    assert result is False  # Returns not mark_deps


def test_tool_get_path_with_tool_path():
    """Test get_path with tool_path set."""
    tool = Tool("test-tool")
    tool.tool_path = "/path/to/tool"
    tool.build_dir = "/build/dir"

    result = tool.get_path()
    assert result == "/path/to/tool"


def test_tool_get_path_without_tool_path():
    """Test get_path without tool_path."""
    tool = Tool("test-tool")
    tool.tool_path = None
    tool.build_dir = "/build/dir"

    result = tool.get_path()
    assert result == "/build/dir"


def test_tool_get_executable():
    """Test get_executable method."""
    tool = Tool("test-tool", exe_name="test.exe")
    tool.full_exe = "/path/to/test.exe"

    result = tool.get_executable()
    assert result == "/path/to/test.exe"


def test_tool_get_executable_no_exe():
    """Test get_executable raises when no full_exe."""
    tool = Tool("test-tool")
    tool.full_exe = None

    with pytest.raises(NotImplementedError):
        tool.get_executable()


def test_tool_get_base_dir_not_implemented():
    """Test get_base_dir raises NotImplementedError."""
    tool = Tool("test-tool")

    with pytest.raises(NotImplementedError):
        tool.get_base_dir()


def test_tool_export():
    """Test export method does nothing."""
    tool = Tool("test-tool")
    result = tool.export()
    assert result is None


def test_tool_update_build_dir():
    """Test update_build_dir calls unpack."""
    tool = Tool("test-tool")
    unpack_called = False

    def mock_unpack():
        nonlocal unpack_called
        unpack_called = True

    tool.unpack = mock_unpack
    tool.update_build_dir()

    assert unpack_called is True


def test_tool_add_decorator():
    """Test tool_add decorator registers tool."""

    @tool_add
    class TestToolDecorator(Tool):
        def __init__(self):
            Tool.__init__(self, "test-tool-decorator-unique")

        def unpack(self):
            pass

    assert TestToolDecorator is not None
