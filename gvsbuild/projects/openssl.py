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

import contextlib
from pathlib import Path

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class OpenSSL(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "openssl",
            version="3.6.1",
            repository="https://github.com/openssl/openssl",
            archive_url="https://github.com/openssl/openssl/releases/download/openssl-{version}/openssl-{version}.tar.gz",
            hash="b1bfedcd5b289ff22aee87c9d600f515767ebf45f77168cb6d64f231f518a82e",
            dependencies=[
                "perl",
                "nasm",
                "msys2",
            ],
        )

    def build(self):
        perl_exe = (
            Path(Project.get_tool_base_dir(Project.get_project("perl")))
            / "bin"
            / "perl.exe"
        )
        gtk_dir = Path(self.builder.gtk_dir)
        debug_option = "debug-" if self.builder.opts.configuration == "debug" else ""
        target = "VC-WIN32" if self.builder.x86 else "VC-WIN64A"
        configure_target = f"{debug_option}{target}"

        self.exec_vs(
            [
                perl_exe,
                "Configure",
                configure_target,
                "enable-fips",
                "no-comp",
                "no-docs",
                "no-ssl3",
                f"--openssldir={gtk_dir / 'etc' / 'ssl'}",
                f"--prefix={gtk_dir}",
            ]
        )

        with contextlib.suppress(Exception):
            self.exec_vs(["nmake", "/nologo", "clean"])
        self.exec_vs(["nmake", "/nologo"])
        self.exec_vs([perl_exe, "mk-ca-bundle.pl", "-n", "cert.pem"])
        self.exec_vs(["nmake", "/nologo", "install"])

        self.install(r".\cert.pem bin")
        self.install(r".\LICENSE share\doc\openssl")
        self.install_pc_files()


@project_add
class OpenSSLFips(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "openssl-fips",
            version="3.6.1",
            repository="https://github.com/openssl/openssl",
            archive_url="https://www.openssl.org/source/old/{major}.{minor}/openssl-{version}.tar.gz",
            hash="b1bfedcd5b289ff22aee87c9d600f515767ebf45f77168cb6d64f231f518a82e",
            dependencies=[
                "openssl",
            ],
        )

    def build(self):
        perl_exe = (
            Path(Project.get_tool_base_dir(Project.get_project("perl")))
            / "bin"
            / "perl.exe"
        )
        gtk_dir = Path(self.builder.gtk_dir)
        debug_option = "debug-" if self.builder.opts.configuration == "debug" else ""
        target = "VC-WIN32" if self.builder.x86 else "VC-WIN64A"
        configure_target = f"{debug_option}{target}"

        self.exec_vs(
            [
                perl_exe,
                "Configure",
                configure_target,
                "enable-fips",
                "no-ssl3",
                "no-comp",
                f"--openssldir={gtk_dir / 'etc' / 'ssl'}",
                f"--prefix={gtk_dir}",
            ]
        )

        with contextlib.suppress(Exception):
            self.exec_vs(["nmake", "/nologo", "clean"])
        self.exec_vs(["nmake", "/nologo"])
        self.exec_vs(["nmake", "/nologo", "install_fips"])
