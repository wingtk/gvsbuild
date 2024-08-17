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

"""Default tools used to build the various projects."""

import os
import subprocess

from .utils.base_expanders import extract_exec
from .utils.base_tool import Tool, tool_add


@tool_add
class ToolCargo(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "cargo",
            version="1.80.1",
            repository="rust-lang/rust",
            archive_url="https://win.rustup.rs/x86_64",
            archive_filename="rustup-init.exe",
            exe_name="cargo.exe",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "cargo.exe")

        self.add_extra_env("RUSTUP_HOME", self.build_dir)
        self.add_extra_env("CARGO_HOME", self.build_dir)

    def unpack(self):
        env = os.environ.copy()
        env["RUSTUP_HOME"] = self.build_dir
        env["CARGO_HOME"] = self.build_dir

        toolchain = (
            f'{self.version}-{"i686" if self.opts.x86 else "x86_64"}-pc-windows-msvc'
        )
        subprocess.run(
            f"{self.archive_file} --no-modify-path --default-toolchain {toolchain} -y",
            check=True,
            env=env,
        )

        self.mark_deps = True


@tool_add
class ToolCmake(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "cmake",
            version="3.30.2",
            archive_url="https://github.com/Kitware/CMake/releases/download/v{version}/cmake-{version}-windows-x86_64.zip",
            hash="48bf4b3dc2d668c578e0884cac7878e146b036ca6b5ce4f8b5572f861b004c25",
            dir_part="cmake-{version}-windows-x86_64",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "cmake.exe")

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file,
            self.opts.tools_root_dir,
            dir_part=self.dir_part,
            check_file=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolMeson(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "meson",
            version="1.5.1",
            archive_url="https://github.com/mesonbuild/meson/archive/refs/tags/{version}.tar.gz",
            archive_filename="meson-{version}.tar.gz",
            hash="55f6acd5bf72c14d4aa5a781993633f84a1d117bdf2c2057735902ced9b81390",
            dir_part="meson-{version}",
            exe_name="meson.py",
        )

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file,
            self.builder.opts.tools_root_dir,
            dir_part=self.dir_part,
            check_file=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolMsys2(Tool):
    def __init__(self):
        Tool.__init__(self, "msys2")
        self.internal = True

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.opts.msys_dir, "usr", "bin")

    def unpack(self):
        self.tool_mark()

    def get_path(self):
        # We always put msys at the end of path
        return None, self.tool_path


@tool_add
class ToolNasm(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "nasm",
            version="2.16.03",
            archive_url="https://www.nasm.us/pub/nasm/releasebuilds/{version}/win64/nasm-{version}-win64.zip",
            hash="3ee4782247bcb874378d02f7eab4e294a84d3d15f3f6ee2de2f47a46aa7226e6",
            dir_part="nasm-{version}",
            exe_name="nasm.exe",
        )

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(
            self.archive_file,
            self.builder.opts.tools_root_dir,
            dir_part=self.dir_part,
            check_file=self.full_exe,
            force_dest=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolNinja(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "ninja",
            version="1.12.1",
            archive_url="https://github.com/ninja-build/ninja/releases/download/v{version}/ninja-win.zip",
            archive_filename="ninja-win-{version}.zip",
            hash="f550fec705b6d6ff58f2db3c374c2277a37691678d6aba463adcbb129108467a",
            dir_part="ninja-{version}",
            exe_name="ninja.exe",
        )

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file, self.build_dir, check_file=self.full_exe, check_mark=True
        )


@tool_add
class ToolPerl(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "perl",
            version="5.20.0",
            archive_url="https://github.com/wingtk/gtk-win32/releases/download/Perl-{major}.{minor}/perl-{version}-x64.tar.xz",
            hash="05e01cf30bb47d3938db6169299ed49271f91c1615aeee5649174f48ff418c55",
            dir_part="perl-{version}",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        # Set the builder object to point to the path to use, when we need to pass directly the executable to *make
        self.base_dir = os.path.join(self.build_dir, "x64")
        # full path, added to the environment when needed
        self.tool_path = os.path.join(self.base_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "perl.exe")

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file, self.build_dir, check_file=self.full_exe, check_mark=True
        )

    def get_base_dir(self):
        return self.base_dir


@tool_add
class ToolGo(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "go",
            version="1.23.0",
            repository="https://github.com/golang/go",
            archive_url="https://go.dev/dl/go{version}.windows-amd64.zip",
            hash="d4be481ef73079ee0ad46081d278923aa3fd78db1b3cf147172592f73e14c1ac",
            dir_part="go-{version}",
        )

    def load_defaults(self):
        Tool.load_defaults(self)
        self.tool_path = os.path.join(self.build_dir, "bin")
        self.full_exe = os.path.join(self.tool_path, "go.exe")

    def unpack(self):
        # We download directly the exe file, so we copy it to the tool directory
        self.mark_deps = extract_exec(
            self.archive_file,
            self.build_dir,
            check_file=self.full_exe,
            check_mark=True,
            strip_one=True,
        )
