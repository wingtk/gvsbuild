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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class OpenSSL(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "openssl",
            version="3.5.1",
            archive_url="https://github.com/openssl/openssl/releases/download/openssl-{version}/openssl-{version}.tar.gz",
            hash="529043b15cffa5f36077a4d0af83f3de399807181d607441d734196d889b641f",
            dependencies=[
                "perl",
                "nasm",
                "msys2",
            ],
        )

    def build(self):
        common_options = r"enable-fips no-comp no-docs no-ssl3 --openssldir=%(gtk_dir)s/etc/ssl --prefix=%(gtk_dir)s"
        debug_option = "debug-" if self.builder.opts.configuration == "debug" else ""
        target_option = "VC-WIN32 " if self.builder.x86 else "VC-WIN64A "

        self.exec_vs(
            r"%(perl_dir)s\bin\perl.exe Configure "
            + debug_option
            + target_option
            + common_options
        )

        with contextlib.suppress(Exception):
            self.exec_vs(r"nmake /nologo clean")
        self.exec_vs(r"nmake /nologo")
        self.exec_vs(r"%(perl_dir)s\bin\perl.exe mk-ca-bundle.pl -n cert.pem")
        self.exec_vs(r"nmake /nologo install")

        self.install(r".\cert.pem bin")
        self.install(r".\LICENSE share\doc\openssl")
        self.install_pc_files()


@project_add
class OpenSSLFips(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "openssl-fips",
            version="3.1.2",
            archive_url="https://www.openssl.org/source/old/{major}.{minor}/openssl-{version}.tar.gz",
            hash="a0ce69b8b97ea6a35b96875235aa453b966ba3cba8af2de23657d8b6767d6539",
            dependencies=[
                "openssl",
            ],
        )

    def build(self):
        common_options = "enable-fips no-ssl3 no-comp --openssldir=%(gtk_dir)s/etc/ssl --prefix=%(gtk_dir)s"
        debug_option = "debug-" if self.builder.opts.configuration == "debug" else ""
        target_option = "VC-WIN32 " if self.builder.x86 else "VC-WIN64A "

        self.exec_vs(
            r"%(perl_dir)s\bin\perl.exe Configure "
            + debug_option
            + target_option
            + common_options
        )

        with contextlib.suppress(Exception):
            self.exec_vs(r"nmake /nologo clean")
        self.exec_vs(r"nmake /nologo")
        self.exec_vs(r"nmake /nologo install_fips")
