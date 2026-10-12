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

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Openldap(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "openldap",
            version="2.7.0",
            repository="https://github.com/openldap/openldap",
            archive_url="https://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-{version}.tgz",
            hash="9e86f37da375aa948a1b478dd76fe87b02090e47c21facae19223588e3407922",
            dependencies=["openssl", "cyrus-sasl"],
        )

    def build(self):
        configuration = (
            "Debug" if self.builder.opts.configuration == "debug" else "Release"
        )
        common_params = [
            "/nologo",
            "/f",
            "Makefile.win",
            f"PREFIX={self.pkg_dir}",
            f"CFG={configuration}",
        ]
        self.exec_vs(["nmake"] + common_params + ["buildall"])
        self.exec_vs(["nmake"] + common_params + ["installall"])

        self.install(r".\COPYRIGHT share\doc\openldap")
        self.install(r".\LICENSE share\doc\openldap")
        self.install_pc_files()
