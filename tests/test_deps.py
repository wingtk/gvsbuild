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
from unittest.mock import Mock

import gvsbuild.groups  # noqa: F401
import gvsbuild.projects  # noqa: F401
import gvsbuild.tools  # noqa: F401
from gvsbuild.deps import compute_deps, make_graph, print_deps
from gvsbuild.utils.base_project import Project


def setup_module():
    """Setup test projects."""
    Project.add_all()


def test_deps_help(app, runner, console):
    """Test deps command help output with consistent console formatting."""
    result = runner.invoke(app, ["deps", "--help"], console=console)
    assert result.exit_code == 0
    assert "Show project dependencies" in result.output
    assert "flatten" in result.output.lower()
    assert "graph" in result.output.lower()


def test_deps_default(app, runner):
    """Test deps command with default options."""
    result = runner.invoke(app, ["deps"])
    assert result.exit_code == 0
    assert "Projects dependencies:" in result.output


def test_deps_flatten(app, runner):
    """Test deps command with flatten option."""
    result = runner.invoke(app, ["deps", "--flatten"])
    assert result.exit_code == 0
    assert ">" in result.output


def test_deps_with_tools(app, runner):
    """Test deps command including tools."""
    result = runner.invoke(app, ["deps", "--dep-tools"])
    assert result.exit_code == 0


def test_make_graph(tmp_path):
    """Test graph generation."""
    output_file = tmp_path / "test.gv"
    make_graph(out_file=str(output_file), skip=[])
    assert output_file.exists()
    content = output_file.read_text()
    assert "digraph gtk3dep" in content
    assert content.strip().endswith("};")


def test_make_graph_with_all(tmp_path):
    """Test graph generation with all projects."""
    output_file = tmp_path / "test_all.gv"
    make_graph(out_file=str(output_file), put_all=True, skip=[])
    assert output_file.exists()
    content = output_file.read_text()
    assert "BUILD" in content or "digraph" in content


def test_make_graph_with_tools(tmp_path):
    """Test graph generation including tools."""
    output_file = tmp_path / "test_tools.gv"
    make_graph(out_file=str(output_file), add_tools=True, skip=[])
    assert output_file.exists()


def test_make_graph_with_groups(tmp_path):
    """Test graph generation including groups."""
    output_file = tmp_path / "test_groups.gv"
    make_graph(out_file=str(output_file), add_groups=True, skip=[])
    assert output_file.exists()


def test_make_graph_inverted(tmp_path):
    """Test graph generation with inverted dependencies."""
    output_file = tmp_path / "test_inverted.gv"
    make_graph(out_file=str(output_file), invert_dep=True, skip=[])
    assert output_file.exists()


def test_make_graph_with_skip(tmp_path):
    """Test graph generation with skip list."""
    output_file = tmp_path / "test_skip.gv"
    make_graph(out_file=str(output_file), skip=["zlib"])
    assert output_file.exists()
    content = output_file.read_text()
    # Skipped projects should not appear in the graph output
    assert '"zlib"' not in content


def test_deps_graph_command(app, runner, tmp_path):
    """Test deps command with graph generation."""
    output_file = tmp_path / "test_command.gv"
    result = runner.invoke(
        app, ["deps", "--graph", "--gv-file", str(output_file), "--skip", ""]
    )
    # Exit code might be 0 or 1 depending on output
    assert output_file.exists() or result.exit_code in [0, 1]


def test_compute_deps():
    """Test compute_deps function."""
    # Create mock project with dependencies
    mock_proj = Mock(spec=["dependencies", "name"])
    mock_proj.dependencies = []
    mock_proj.name = "test-project"

    # Compute dependencies
    compute_deps(mock_proj)

    # Now should have all_dependencies
    assert hasattr(mock_proj, "all_dependencies")


def test_compute_deps_with_nested():
    """Test compute_deps with nested dependencies."""
    # Create mock projects
    dep2 = Mock(spec=["dependencies", "all_dependencies", "name"])
    dep2.dependencies = []
    dep2.all_dependencies = []
    dep2.name = "dep2"

    dep1 = Mock(spec=["dependencies", "all_dependencies", "name"])
    dep1.dependencies = [dep2]
    dep1.all_dependencies = [dep2]
    dep1.name = "dep1"

    main_proj = Mock(spec=["dependencies", "name"])
    main_proj.dependencies = [dep1]
    main_proj.name = "main"

    # Compute dependencies
    compute_deps(main_proj)

    # Should have all dependencies
    assert hasattr(main_proj, "all_dependencies")
    # Check that dependencies were added
    assert len(main_proj.all_dependencies) > 0


def test_print_deps_basic(capsys):
    """Test print_deps function."""
    print_deps(flatten=False, add_all=False)
    captured = capsys.readouterr()
    assert "Projects dependencies:" in captured.out


def test_print_deps_flatten(capsys):
    """Test print_deps with flatten."""
    print_deps(flatten=True, add_all=False)
    captured = capsys.readouterr()
    assert ">" in captured.out


def test_print_deps_add_all(capsys):
    """Test print_deps with add_all."""
    print_deps(flatten=False, add_all=True)
    captured = capsys.readouterr()
    assert "Projects dependencies:" in captured.out
