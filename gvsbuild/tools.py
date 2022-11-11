#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
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
            archive_url="https://win.rustup.rs/x86_64",
            archive_file_name="rustup-init.exe",
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

        rustup = os.path.join(self.build_dir, "bin", "rustup.exe")

        subprocess.check_call(
            f"{self.archive_file} --no-modify-path -y", shell=True, env=env
        )

        # add supported targets
        subprocess.check_call(
            f"{rustup} target add x86_64-pc-windows-msvc", shell=True, env=env
        )

        subprocess.check_call(
            f"{rustup} target add i686-pc-windows-msvc", shell=True, env=env
        )

        # switch to the right target
        subprocess.check_call(
            f'{rustup} default stable-{"i686" if self.opts.x86 else "x86_64"}-pc-windows-msvc',
            env=env,
        )

        self.mark_deps = True


@tool_add
class ToolCmake(Tool):
    def __init__(self):
        self.version = "3.24.2"
        Tool.__init__(
            self,
            "cmake",
            archive_url=f"https://github.com/Kitware/CMake/releases/download/v{self.version}/cmake-{self.version}-windows-x86_64.zip",
            hash="6af30354eecbb7113b0f0142d13c03d21abbc9f4dbdcddaf88df1f9ca1bc4d6f",
            dir_part=f"cmake-{self.version}-windows-x86_64",
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
        self.version = "0.63.2"
        Tool.__init__(
            self,
            "meson",
            archive_url=f"https://github.com/mesonbuild/meson/archive/refs/tags/{self.version}.tar.gz",
            archive_file_name=f"meson-{self.version}.tar.gz",
            hash="023a3f7c74e68991154c3205a6975705861eedbf8130e013d15faa1df1af216e",
            dependencies=[],
            dir_part=f"meson-{self.version}",
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
            archive_url="https://github.com/wingtk/gvsbuild/releases/download/nasm-2.15.05/nasm-2.15.05-win64.zip",
            hash="f5c93c146f52b4f1664fa3ce6579f961a910e869ab0dae431bd871bdd2584ef2",
            dir_part="nasm-2.15.05",
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
        self.version = "1.11.0"
        Tool.__init__(
            self,
            "ninja",
            archive_url=f"https://github.com/ninja-build/ninja/releases/download/v{self.version}/ninja-win.zip",
            archive_file_name=f"ninja-win-{self.version}.zip",
            hash="d0ee3da143211aa447e750085876c9b9d7bcdd637ab5b2c5b41349c617f22f3b",
            dir_part=f"ninja-{self.version}",
            exe_name="ninja.exe",
        )

    def unpack(self):
        self.mark_deps = extract_exec(
            self.archive_file, self.build_dir, check_file=self.full_exe, check_mark=True
        )


@tool_add
class ToolNuget(Tool):
    def __init__(self):
        self.version = "6.3.0"
        Tool.__init__(
            self,
            "nuget",
            archive_url=f"https://dist.nuget.org/win-x86-commandline/v{self.version}/nuget.exe",
            archive_file_name=f"nuget-{self.version}.exe",
            hash="38257f945b3662f5c81d646f2cd940365642e2c4941b34c0e5ae3f4281f9bd2d",
            dir_part=f"nuget-{self.version}",
            exe_name="nuget.exe",
        )

    def unpack(self):
        # Download the exe file and copy it on the tool directory
        self.mark_deps = extract_exec(
            self.archive_file,
            self.build_dir,
            check_file=self.full_exe,
            force_dest=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolPerl(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "perl",
            archive_url="https://github.com/wingtk/gtk-win32/releases/download/Perl-5.20/perl-5.20.0-x64.tar.xz",
            hash="05e01cf30bb47d3938db6169299ed49271f91c1615aeee5649174f48ff418c55",
            dir_part="perl-5.20.0",
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
class ToolYasm(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "yasm",
            archive_url="http://www.tortall.net/projects/yasm/releases/yasm-1.3.0-win64.exe",
            hash="d160b1d97266f3f28a71b4420a0ad2cd088a7977c2dd3b25af155652d8d8d91f",
            dir_part="yasm-1.3.0",
            exe_name="yasm.exe",
        )

    def unpack(self):
        # We download directly the exe file so we copy it on the tool directory ...
        self.mark_deps = extract_exec(
            self.archive_file,
            self.build_dir,
            check_file=self.full_exe,
            force_dest=self.full_exe,
            check_mark=True,
        )


@tool_add
class ToolGo(Tool):
    def __init__(self):
        Tool.__init__(
            self,
            "go",
            archive_url="https://go.dev/dl/go1.18.3.windows-amd64.zip",
            hash="9c46023f3ad0300fcfd1e62f2b6c2dfd9667b1f2f5c7a720b14b792af831f071",
            dir_part="go-1.18",
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
