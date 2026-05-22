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

from pathlib import Path

from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Kerberos(Tarball, Project):
    def __init__(self):
        Project.__init__(
            self,
            "mit-kerberos",
            version="1.22.2",
            repository="https://github.com/krb5/krb5",
            archive_url="https://github.com/krb5/krb5/archive/refs/tags/krb5-{version}-final.tar.gz",
            hash="289f5bb81d1f2f8d5eecebe56a056aeed95d35fd9bb4a7071c5dd7ad4b3fe888",
            dependencies=[
                "perl",
            ],
        )

    def build(self):
        nodebug = "1" if self.builder.opts.configuration != "debug" else "0"
        add_path = Path(self.builder.opts.msys_dir) / "usr" / "bin"
        krb_install = f"KRB_INSTALL_DIR={self.builder.gtk_dir}"

        self.push_location("src")
        self.exec_vs(
            ["nmake", "-f", "Makefile.in", "prep-windows", "NO_LEASH=1", krb_install],
            add_path=add_path,
        )
        self.exec_vs(
            ["nmake", f"NODEBUG={nodebug}", "NO_LEASH=1", krb_install],
            add_path=add_path,
        )
        self.exec_vs(
            ["nmake", "install", f"NODEBUG={nodebug}", "NO_LEASH=1", krb_install],
            add_path=add_path,
        )
        self.pop_location()

        self.install(r".\NOTICE share\doc\mit-kerberos")
