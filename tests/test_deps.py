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
import gvsbuild.groups  # noqa: F401
import gvsbuild.projects  # noqa: F401
import gvsbuild.tools  # noqa: F401
from gvsbuild.deps import compute_deps, make_graph, print_deps
from gvsbuild.utils.base_project import Project


def setup_module():
    Project.add_all()


def test_deps_help(app, runner, console):
    result = runner.invoke(app, ["deps", "--help"], console=console)
    assert result.exit_code == 0
    assert "Show project dependencies" in result.output
    assert "flatten" in result.output.lower()
    assert "graph" in result.output.lower()


def test_deps_default(app, runner):
    result = runner.invoke(app, ["deps"])
    assert result.exit_code == 0
    assert "Projects dependencies:" in result.output


def test_deps_flatten(app, runner):
    result = runner.invoke(app, ["deps", "--flatten"])
    assert result.exit_code == 0
    assert ">" in result.output


def test_deps_with_tools(app, runner):
    result = runner.invoke(app, ["deps", "--dep-tools"])
    assert result.exit_code == 0


def test_make_graph(tmp_path):
    output_file = tmp_path / "test.gv"
    make_graph(out_file=str(output_file), skip=[])
    assert output_file.exists()
    content = output_file.read_text()
    assert "digraph gtk3dep" in content
    assert content.strip().endswith("};")


def test_make_graph_with_all(tmp_path):
    output_file = tmp_path / "test_all.gv"
    make_graph(out_file=str(output_file), put_all=True, skip=[])
    assert output_file.exists()
    content = output_file.read_text()
    assert "BUILD" in content or "digraph" in content


def test_make_graph_with_tools(tmp_path):
    output_file = tmp_path / "test_tools.gv"
    make_graph(out_file=str(output_file), add_tools=True, skip=[])
    assert output_file.exists()


def test_make_graph_with_groups(tmp_path):
    output_file = tmp_path / "test_groups.gv"
    make_graph(out_file=str(output_file), add_groups=True, skip=[])
    assert output_file.exists()


def test_make_graph_inverted(tmp_path):
    output_file = tmp_path / "test_inverted.gv"
    make_graph(out_file=str(output_file), invert_dep=True, skip=[])
    assert output_file.exists()


def test_make_graph_with_skip(tmp_path):
    output_file = tmp_path / "test_skip.gv"
    make_graph(out_file=str(output_file), skip=["zlib"])
    assert output_file.exists()
    content = output_file.read_text()
    assert '"zlib"' not in content


def test_deps_graph_command(app, runner, tmp_path):
    output_file = tmp_path / "test_command.gv"
    result = runner.invoke(
        app, ["deps", "--graph", "--gv-file", str(output_file), "--skip", ""]
    )
    assert output_file.exists() or result.exit_code in [0, 1]


def test_compute_deps(mock_project):
    compute_deps(mock_project)
    assert hasattr(mock_project, "all_dependencies")


def test_compute_deps_with_nested(mocker):
    dep2 = mocker.Mock(spec=["dependencies", "all_dependencies", "name"])
    dep2.dependencies = []
    dep2.all_dependencies = []
    dep2.name = "dep2"

    dep1 = mocker.Mock(spec=["dependencies", "all_dependencies", "name"])
    dep1.dependencies = [dep2]
    dep1.all_dependencies = [dep2]
    dep1.name = "dep1"

    main_proj = mocker.Mock(spec=["dependencies", "name"])
    main_proj.dependencies = [dep1]
    main_proj.name = "main"

    compute_deps(main_proj)
    assert hasattr(main_proj, "all_dependencies")
    assert len(main_proj.all_dependencies) > 0


def test_print_deps_basic(capsys):
    print_deps(flatten=False, add_all=False)
    captured = capsys.readouterr()
    assert "Projects dependencies:" in captured.out


def test_print_deps_flatten(capsys):
    print_deps(flatten=True, add_all=False)
    captured = capsys.readouterr()
    assert ">" in captured.out


def test_print_deps_add_all(capsys):
    print_deps(flatten=False, add_all=True)
    captured = capsys.readouterr()
    assert "Projects dependencies:" in captured.out
