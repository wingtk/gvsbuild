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

"""Various builders (meson, CMake, ...) class."""

import shutil
import sys
from pathlib import Path

from .base_project import Project
from .simple_ui import log
from .utils import _rmtree_error_handler


class Meson(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)
        self._ensure_params()

    def _ensure_params(self):
        if not hasattr(self, "params"):
            self.params = []

    def add_param(self, par):
        self._ensure_params()
        self.params.append(par)

    def build(
        self,
        meson_params: list[str] | None = None,
        make_tests: bool = False,
        add_path=None,
    ):
        # where we build, with ninja, the library
        ninja_build = Path(self.build_dir) / "_gvsbuild-meson"

        # First we check if we need to generate the meson build files
        if not (ninja_build / "build.ninja").is_file():
            self._setup_meson_and_ninja(ninja_build, meson_params, add_path)
        if make_tests:
            # Run ninja to build all (library, ....
            self.builder.exec_ninja(working_dir=ninja_build)
            # .. run the tests ...
            self.builder.exec_ninja(params=["test"], working_dir=ninja_build)
            # .. and finally install everything
        # if we don't make the tests we simply run 'ninja install' that takes care of everything,
        # running explicitly from the build dir
        self.builder.exec_ninja(params=["install"], working_dir=ninja_build)

    def _setup_meson_and_ninja(
        self, ninja_build, meson_params: list[str] | None, add_path
    ):
        log.start_verbose("Generating meson directory")
        self.builder.make_dir(ninja_build)
        self._ensure_params()
        build_type = self.builder.opts.configuration
        if self.builder.opts.release_configuration_is_actually_debug_optimized:
            build_type = "debugoptimized"

        meson = Project.get_tool_executable("meson")
        cmd = [
            sys.executable,
            meson,
            "setup",
            self._get_working_dir(),
            ninja_build,
            "--prefix",
            self.builder.gtk_dir,
            "--buildtype",
            build_type,
        ]
        cmd += self.params
        if meson_params:
            cmd += meson_params
        if self.extra_opts:
            cmd += self.extra_opts

        # build the ninja file to do everything (build the library, create the .pc file, install it, ...)
        self.exec_vs(cmd, add_path=add_path)
        log.end()


class CmakeProject(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(
        self,
        cmake_params: list[str] | None = None,
        use_ninja: bool = False,
        make_tests: bool = False,
        do_install: bool = True,
        out_of_source: bool | None = None,
        source_part: str | None = None,
    ):
        cmake_gen = "Ninja" if use_ninja else "NMake Makefiles"

        cmake_config = (
            "Debug" if self.builder.opts.configuration == "debug" else "Release"
        )
        if self.builder.opts.release_configuration_is_actually_debug_optimized:
            cmake_config = "RelWithDebInfo"
        # Create the command for cmake
        cmd = [
            "cmake",
            "-G",
            cmake_gen,
            f"-DCMAKE_INSTALL_PREFIX={self.pkg_dir}",
            f"-DGTK_DIR={self.builder.gtk_dir}",
            f"-DCMAKE_BUILD_TYPE={cmake_config}",
        ]
        if cmake_params:
            cmd += cmake_params
        if self.extra_opts:
            cmd += self.extra_opts
        if use_ninja and out_of_source is None:
            # For ninja the default is build out of source
            out_of_source = True

        if out_of_source:
            cmake_dir = Path(self.build_dir) / "_gvsbuild-cmake"
            self.builder.make_dir(cmake_dir)
            src_full = (
                Path(self.build_dir) / source_part
                if source_part
                else Path(self.build_dir)
            )
            cmd += ["-B", str(cmake_dir), "-S", str(src_full)]
            work_dir = cmake_dir
        else:
            work_dir = self._get_working_dir()

        # Generate the files used to build
        log.start_verbose("Generating/updating cmake files")
        self.builder.exec_vs(cmd, working_dir=work_dir)
        log.end()
        # Build
        if use_ninja:
            if make_tests:
                self.builder.exec_ninja(working_dir=work_dir)
                self.builder.exec_ninja(params=["test"], working_dir=work_dir)
                if do_install:
                    self.builder.exec_ninja(params=["install"], working_dir=work_dir)
            elif do_install:
                self.builder.exec_ninja(params=["install"], working_dir=work_dir)
            else:
                self.builder.exec_ninja(working_dir=work_dir)
        else:
            self.builder.exec_vs(["nmake", "/nologo"], working_dir=work_dir)
            if do_install:
                self.builder.exec_vs(
                    ["nmake", "/nologo", "install"], working_dir=work_dir
                )


class Rust(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)
        self._ensure_params()

    def _ensure_params(self):
        if not hasattr(self, "params"):
            self.params = []

    def add_param(self, par):
        self._ensure_params()
        self.params.append(par)

    def build(self, cargo_params=None, make_tests=False):
        rustc_opts = {}

        params = cargo_params[:] if cargo_params else []
        if self.builder.opts.configuration == "release":
            # add debug symbols anyway
            rustc_opts["RUSTFLAGS"] = "-g"
            params.append("--release")
            folder = "release"
        else:
            folder = "debug"

        if self.extra_opts:
            params.extend(self.extra_opts)

        cargo_build = Path(self.build_dir) / "cargo-build"

        params.append(f"--target-dir={cargo_build}")

        if self.clean and cargo_build.exists():
            log.debug(f"Removing cargo build dir '{cargo_build}'")
            shutil.rmtree(cargo_build, onerror=_rmtree_error_handler)

        # build
        self.builder.exec_cargo(
            params=["build"] + params,
            working_dir=self.build_dir,
            rustc_opts=rustc_opts,
            rust_version=self.version,
        )

        # test
        if make_tests:
            self.builder.exec_cargo(
                params=["test"] + params,
                working_dir=self.build_dir,
                rustc_opts=rustc_opts,
                rust_version=self.version,
            )

        shutil.copytree(cargo_build / folder, cargo_build / "lib")


class MakeGir:
    """Class to build, with nmake, a single project .gir/.typelib files for the
    gobject-introspection support, used where the meson script is not present
    (gtk2 % gtk3) or not update the handle it."""

    def make_single_gir(self, prj_name, prj_dir=None):
        if not prj_dir:
            prj_dir = prj_name

        b_dir = Path(self.builder.working_dir) / prj_dir / "build" / "win32"
        if not (b_dir / "detectenv-msvc.mak").is_file():
            b_dir = Path(self.builder.working_dir) / prj_dir / "win32"
            if not (b_dir / "detectenv-msvc.mak").is_file():
                log.message(f"Unable to find detectenv-msvc.mak for {prj_name}")
                return

        python = Project.get_tool_executable("python")
        cmd = [
            "nmake",
            "-f",
            f"{prj_name}-introspection-msvc.mak",
            f"CFG={self.builder.opts.configuration}",
            f"PREFIX={self.builder.gtk_dir}",
            f"PYTHON={python}",
            "install-introspection",
        ]

        self.push_location(b_dir)
        self.exec_vs(cmd)
        self.pop_location()
