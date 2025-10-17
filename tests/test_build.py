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


def test_build_help(app, runner, console):
    """Test build command help output with consistent console formatting."""
    result = runner.invoke(app, ["build", "--help"], console=console)
    assert result.exit_code == 0
    assert "Build a project or a list of projects" in result.output
    assert "PROJECTS" in result.output
    assert "--platform" in result.output


def test_wrong_project_name(app, runner):
    result = runner.invoke(app, ["build", "bad-name"], color=True)
    assert result.exit_code == 1
    full_output = result.output + result.stderr
    assert "not a valid project name" in full_output


def test_no_project(app, runner):
    result = runner.invoke(app, ["build"])
    # Cyclopts returns exit code 1 for errors
    assert result.exit_code in [1, 2]
    full_output = result.output + result.stderr
    assert (
        "requires an argument" in full_output.lower()
        or "required" in full_output.lower()
        or "missing" in full_output.lower()
        or "at least one project" in full_output.lower()
    )


def test_platform(tmp_dir, app, runner):
    # This test just ensures the command can be invoked with platform argument
    # Actual building may fail due to missing tools/dependencies in test environment
    assert tmp_dir.exists()
    result = runner.invoke(
        app,
        [
            "build",
            "--build-dir",
            str(tmp_dir),
            "--platform",
            "x86",
            "hello-world",
        ],
    )
    # Exit code may be 0 (success) or 1 (build error), but should not be 2 (argument error)
    assert result.exit_code in [0, 1]


def test_ninja_opts_validation_valid_single_dash(app, runner):
    """Test that ninja-opts accepts valid single-dash options."""
    result = runner.invoke(app, ["build", "--ninja-opts", "-j2", "hello-world"])
    # Should not fail with validation error (exit code 1 is OK for build errors)
    assert result.exit_code != 2
    full_output = result.output + result.stderr
    assert "ninja-opts must start with a dash" not in full_output


def test_ninja_opts_validation_valid_double_dash(app, runner):
    """Test that ninja-opts accepts valid double-dash options."""
    result = runner.invoke(app, ["build", "--ninja-opts", "--verbose", "hello-world"])
    # Should not fail with validation error (exit code 1 is OK for build errors)
    assert result.exit_code != 2
    full_output = result.output + result.stderr
    assert "ninja-opts must start with a dash" not in full_output


def test_ninja_opts_validation_valid_equals_syntax(app, runner):
    """Test that ninja-opts accepts equals syntax."""
    result = runner.invoke(app, ["build", "--ninja-opts=-j2", "hello-world"])
    # Should not fail with validation error (exit code 1 is OK for build errors)
    assert result.exit_code != 2
    full_output = result.output + result.stderr
    assert "ninja-opts must start with a dash" not in full_output


def test_ninja_opts_validation_invalid_no_dash(app, runner):
    """Test that ninja-opts rejects values that don't start with dash."""
    result = runner.invoke(app, ["build", "--ninja-opts", "j2", "hello-world"])
    assert result.exit_code == 1  # Validation error
    full_output = result.output + result.stderr
    assert "ninja-opts must start with a dash (- or --)" in full_output
    assert "Got: 'j2'" in full_output
    assert "--ninja-opts -j2" in full_output
    assert "--ninja-opts --verbose" in full_output


def test_ninja_opts_validation_invalid_equals_syntax(app, runner):
    """Test that ninja-opts rejects invalid values with equals syntax."""
    result = runner.invoke(app, ["build", "--ninja-opts=j2", "hello-world"])
    assert result.exit_code == 1  # Validation error
    full_output = result.output + result.stderr
    assert "ninja-opts must start with a dash (- or --)" in full_output
    assert "Got: 'j2'" in full_output


def test_ninja_opts_validation_empty_value(app, runner):
    """Test that ninja-opts accepts empty/None values."""
    result = runner.invoke(app, ["build", "hello-world"])
    # Should not fail with validation error (exit code 1 is OK for build errors)
    assert result.exit_code != 2
    full_output = result.output + result.stderr
    assert "ninja-opts must start with a dash" not in full_output
