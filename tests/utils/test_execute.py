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

"""Tests for list-arg execution — all subprocess calls use shell=False implicitly."""

import pytest

from gvsbuild.utils.base_builders import Meson, Rust
from gvsbuild.utils.base_project import Project
from gvsbuild.utils.builder import Builder

# Patch targets — always patch where the name is looked up
SUBPROCESS_CHECK_CALL = "gvsbuild.utils.builder.subprocess.check_call"
SUBPROCESS_RUN = "gvsbuild.utils.builder.subprocess.run"


@pytest.fixture
def builder(mocker):
    """Minimal Builder instance for testing execution methods."""
    b = Builder.__new__(Builder)
    b.opts = mocker.Mock()
    b.opts.capture_out = False
    b.opts.ninja_opts = None
    b.opts.msys_dir = "C:\\msys64"
    b.vs_env = {}
    b._Builder__project = None
    return b


def test_execute_list_calls_check_call(builder, mocker):
    mock_cc = mocker.patch(SUBPROCESS_CHECK_CALL)

    builder._Builder__execute(["echo", "hello"])

    mock_cc.assert_called_once_with(["echo", "hello"], cwd=None, env=None)


@pytest.mark.parametrize(
    "args",
    [
        ["nmake", "PREFIX=C:\\Program Files\\gtk"],
        # #1726: python exe with spaces in path must not be split
        [
            r"C:\Users\Mazin Marwan\AppData\Roaming\uv\tools\gvsbuild\Scripts\python.exe",
            "-m",
            "build",
            "--wheel",
        ],
        # bash invocation: path\to\bash as first element, script as second
        [r"C:\msys64\usr\bin\bash", r"build\build.sh", "/c/some path/gtk", "release"],
    ],
)
def test_execute_list_preserves_args_verbatim(builder, mocker, args):
    """List args are delivered to subprocess unchanged — no shell splitting."""
    mock_cc = mocker.patch(SUBPROCESS_CHECK_CALL)
    builder._Builder__execute(args)
    assert mock_cc.call_args[0][0] == args


def test_execute_list_capture_out_calls_run(builder, mocker):
    builder.opts.capture_out = True
    builder._Builder__project = mocker.Mock()
    builder._Builder__project.name = "test"
    mock_run = mocker.patch(SUBPROCESS_RUN, return_value=mocker.Mock(stdout=""))

    builder._Builder__execute(["ninja", "install"])

    mock_run.assert_called_once()
    assert "shell" not in mock_run.call_args[1]


def test_exec_vs_list_passed_to_execute_unchanged(builder, mocker):
    mock_exec = mocker.patch.object(builder, "_Builder__execute")

    builder.exec_vs(["nmake", "/nologo", "install"])

    assert mock_exec.call_args[0][0] == ["nmake", "/nologo", "install"]


def test_exec_vs_list_element_with_spaces_not_quoted(builder, mocker):
    mock_exec = mocker.patch.object(builder, "_Builder__execute")

    token = "PREFIX=C:\\Program Files\\build"
    builder.exec_vs(["nmake", token])

    assert mock_exec.call_args[0][0][1] == token


def test_exec_vs_python_exe_with_spaces_regression_1726(builder, mocker):
    """Regression #1726: python.exe in a path with spaces reaches subprocess verbatim."""
    mock_cc = mocker.patch(SUBPROCESS_CHECK_CALL)
    python_exe = (
        r"C:\Users\Mazin Marwan\AppData\Roaming\uv\tools\gvsbuild\Scripts\python.exe"
    )
    builder.exec_vs([python_exe, "-m", "build", "--wheel"])
    assert mock_cc.call_args[0][0][0] == python_exe


def test_exec_ninja_no_params_produces_list(builder, mocker):
    mock_exec = mocker.patch.object(builder, "_Builder__execute")

    builder.exec_ninja()

    assert mock_exec.call_args[0][0] == ["ninja"]


def test_exec_ninja_with_params_produces_list(builder, mocker):
    mock_exec = mocker.patch.object(builder, "_Builder__execute")

    builder.exec_ninja(params=["install"])

    assert mock_exec.call_args[0][0] == ["ninja", "install"]


def test_exec_ninja_with_opts_produces_list(builder, mocker):
    builder.opts.ninja_opts = "-j4"
    mock_exec = mocker.patch.object(builder, "_Builder__execute")

    builder.exec_ninja(params=["install"])

    assert mock_exec.call_args[0][0] == ["ninja", "-j4", "install"]


def test_exec_cmd_list_passed_unchanged(builder, mocker):
    mock_exec = mocker.patch.object(builder, "_Builder__execute")

    builder.exec_cmd(["copy", "src.exe", "dst.exe"])

    assert mock_exec.call_args[0][0] == ["copy", "src.exe", "dst.exe"]


def test_exec_msys_list_calls_check_call(builder, mocker):
    mock_cc = mocker.patch(SUBPROCESS_CHECK_CALL)

    builder.exec_msys(["git", "fetch", "origin"])

    mock_cc.assert_called_once()
    assert "shell" not in mock_cc.call_args[1]


def test_exec_msys_list_passes_args_verbatim(builder, mocker):
    """List args must not be shell-split; URLs and paths with spaces are preserved."""
    mocker.patch("gvsbuild.utils.builder.shutil.which", return_value=None)
    mock_cc = mocker.patch(SUBPROCESS_CHECK_CALL)

    dest = "C:\\Program Files\\source"
    builder.exec_msys(["git", "clone", "https://example.com/repo.git", dest])

    args = mock_cc.call_args[0][0]
    assert args == ["git", "clone", "https://example.com/repo.git", dest]


def test_exec_vs_does_not_expand_percent_substitution(builder, mocker):
    """After __sub_vars removal, %(var)s literals in list elements survive verbatim."""
    builder.gtk_dir = "C:\\gtk"
    mock_exec = mocker.patch.object(builder, "_Builder__execute")

    builder.exec_vs(["nmake", "PREFIX=%(gtk_dir)s"])

    assert mock_exec.call_args[0][0][1] == "PREFIX=%(gtk_dir)s"


@pytest.fixture
def cargo_builder(builder, mocker):
    """Builder with cargo prerequisites pre-configured."""
    builder.opts.cargo_opts = None
    builder.x86 = False
    mocker.patch(
        "gvsbuild.utils.builder.Project.get_tool_path", return_value="C:\\cargo"
    )
    return builder


def test_exec_cargo_no_params_calls_bare_cargo(cargo_builder, mocker):
    mock_exec = mocker.patch.object(cargo_builder, "_Builder__execute")
    cargo_builder.exec_cargo()
    cargo_cmd = mock_exec.call_args_list[1][0][0]
    assert cargo_cmd == ["cargo"]


def test_exec_cargo_list_params_appended(cargo_builder, mocker):
    mock_exec = mocker.patch.object(cargo_builder, "_Builder__execute")
    cargo_builder.exec_cargo(["install", "cargo-c", "--locked"])
    cargo_cmd = mock_exec.call_args_list[1][0][0]
    assert cargo_cmd == ["cargo", "install", "cargo-c", "--locked"]


def test_exec_cargo_global_opts_are_split_and_prepended(cargo_builder, mocker):
    cargo_builder.opts.cargo_opts = "--color always"
    mock_exec = mocker.patch.object(cargo_builder, "_Builder__execute")
    cargo_builder.exec_cargo(["build"])
    cargo_cmd = mock_exec.call_args_list[1][0][0]
    assert cargo_cmd == ["cargo", "--color", "always", "build"]


@pytest.fixture
def project_stub(mocker):
    """Minimal Project instance for exec_msbuild tests."""
    p = Project.__new__(Project)
    p.builder = mocker.Mock()
    p.builder.opts.configuration = "release"
    p.builder._create_msbuild_opts.return_value = [
        "/nologo",
        "/p:Platform=x64",
        "/v:minimal",
    ]
    p.build_dir = r"C:\build\myproject"
    p._Project__working_dir = None  # required by _get_working_dir
    return p


def test_exec_msbuild_builds_correct_command(project_stub):
    project_stub.exec_msbuild([r"src\all.sln", "/p:SkipUWP=true"])
    cmd = project_stub.builder.exec_vs.call_args[0][0]
    assert cmd[0] == "msbuild"
    assert r"src\all.sln" in cmd
    assert "/p:SkipUWP=true" in cmd
    assert "/p:Configuration=release" in cmd
    assert "/nologo" in cmd


def test_exec_msbuild_explicit_configuration_overrides_opts(project_stub):
    project_stub.exec_msbuild([r"src\all.sln"], configuration="debug")
    cmd = project_stub.builder.exec_vs.call_args[0][0]
    assert "/p:Configuration=debug" in cmd


@pytest.fixture
def rust_project(mocker):
    """Minimal Rust project instance for cargo-params construction tests."""
    p = Rust.__new__(Rust)
    p.builder = mocker.Mock()
    p.builder.opts.configuration = "debug"
    p.build_dir = r"C:\build\librsvg"
    p.clean = False
    p.extra_opts = []
    p.version = "stable"
    # Rust.build calls shutil.copytree after exec_cargo; patch it out
    mocker.patch("gvsbuild.utils.base_builders.shutil.copytree")
    return p


def test_rust_build_debug_does_not_add_release_flag(rust_project):
    rust_project.build()
    params = rust_project.builder.exec_cargo.call_args[1]["params"]
    assert "build" in params
    assert "--release" not in params


def test_rust_build_release_adds_release_flag(rust_project):
    rust_project.builder.opts.configuration = "release"
    rust_project.build()
    params = rust_project.builder.exec_cargo.call_args[1]["params"]
    assert "--release" in params


def test_rust_build_forwards_cargo_params(rust_project):
    rust_project.build(cargo_params=["--features", "foo"])
    params = rust_project.builder.exec_cargo.call_args[1]["params"]
    assert "--features" in params
    assert "foo" in params


@pytest.fixture
def meson_project(mocker, tmp_path):
    """Minimal Meson project with a pre-existing build.ninja to skip setup."""
    p = Meson.__new__(Meson)
    p.builder = mocker.Mock()
    p.build_dir = str(tmp_path)
    p.params = []
    p.extra_opts = []
    ninja_build = tmp_path / "_gvsbuild-meson"
    ninja_build.mkdir()
    (ninja_build / "build.ninja").write_text("")
    return p


def test_meson_build_calls_ninja_install(meson_project):
    meson_project.build()
    calls = meson_project.builder.exec_ninja.call_args_list
    params = [c[1].get("params") for c in calls]
    assert ["install"] in params


def test_meson_build_with_tests_calls_ninja_test_then_install(meson_project):
    meson_project.build(make_tests=True)
    calls = meson_project.builder.exec_ninja.call_args_list
    params = [c[1].get("params") for c in calls]
    assert None in params
    assert ["test"] in params
    assert ["install"] in params


def test_execute_resolves_bare_name_via_env_path(builder, mocker):
    """Bare executable names must be resolved using env['PATH'], not the parent
    process PATH — Windows CreateProcess does not consult env for bare lookups."""
    builder.vs_env = {"PATH": r"C:\fake\tools"}
    fake_cmake = r"C:\fake\tools\cmake.exe"
    mocker.patch(
        "gvsbuild.utils.builder.shutil.which",
        side_effect=lambda name, path=None: fake_cmake if name == "cmake" else None,
    )
    mock_cc = mocker.patch(SUBPROCESS_CHECK_CALL)

    builder.exec_vs(["cmake", "-G", "Ninja"])

    resolved_args = mock_cc.call_args[0][0]
    assert resolved_args[0] == fake_cmake
    assert resolved_args[1:] == ["-G", "Ninja"]


def test_execute_absolute_path_skips_resolution(builder, mocker):
    """An absolute path in args[0] must pass through without calling shutil.which."""
    mock_which = mocker.patch("gvsbuild.utils.builder.shutil.which")
    mock_cc = mocker.patch(SUBPROCESS_CHECK_CALL)

    bash = r"C:\msys64\usr\bin\bash"
    builder.exec_vs([bash, "build.sh"])

    mock_which.assert_not_called()
    assert mock_cc.call_args[0][0][0] == bash
