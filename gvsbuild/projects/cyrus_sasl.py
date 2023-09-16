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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class CyrusSasl(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "cyrus-sasl",
            version="2.1.28",
            hash="9e8035c12d419209ea60584d5efa51d042c3ed44b450b9d173d5504b222df9f1",
            archive_url="https://github.com/wingtk/cyrus-sasl/releases/download/cyrus-sasl-lmdb-{version}/cyrus-sasl-{version}.tar.xz",
            dependencies=["lmdb", "openssl", "mit-kerberos"],
            patches=[
                "0001-fix-snprintf-macro.patch",
                "0001-Add-MIT-Kerberos-as-GSSAPI-provider.patch",
                "0002-Provide-a-compile-option-for-32-64-gssapi.patch",
                "0001-Fix-openssl-libs-to-point-to-the-new-openssl-1.1.1-n.patch",
            ],
        )

    def build(self):
        configuration = (
            "Debug" if self.builder.opts.configuration == "debug" else "Release"
        )
        gssapilib = "gssapi32.lib" if self.builder.x86 else "gssapi64.lib"
        self.exec_vs(
            r'nmake /nologo /f NTMakefile SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" '
            + r'GSSAPI="MITKerberos" GSSAPILIB="'
            + gssapilib
            + r'" GSSAPI_INCLUDE="%(gtk_dir)s\include" GSSAPI_LIBPATH="%(gtk_dir)s\lib" '
            + r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s" CFG='
            + configuration
        )
        self.exec_vs(
            r'nmake /nologo /f NTMakefile install SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" '
            + r'GSSAPI="MITKerberos" GSSAPILIB="'
            + gssapilib
            + r'" GSSAPI_INCLUDE="%(gtk_dir)s\include" GSSAPI_LIBPATH="%(gtk_dir)s\lib" '
            + r'LMDB_LIBPATH="%(gtk_dir)s\lib" OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s" CFG='
            + configuration
        )

        self.install(r".\COPYING share\doc\cyrus-sasl")
        self.install_pc_files()
