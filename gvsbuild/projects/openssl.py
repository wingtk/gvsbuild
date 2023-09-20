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
            version="3.1.3",
            archive_url="https://www.openssl.org/source/openssl-{version}.tar.gz",
            hash="f0316a2ebd89e7f2352976445458689f80302093788c466692fb2a188b2eacf6",
            dependencies=[
                "perl",
                "nasm",
                "msys2",
            ],
        )

    def build(self):
        common_options = r"no-ssl2 no-ssl3 no-comp --openssldir=%(gtk_dir)s/etc/ssl --prefix=%(gtk_dir)s"

        debug_option = "debug-" if self.builder.opts.configuration == "debug" else ""
        # Note that we want to give priority to the system perl version.
        # Using the msys2 one might endup giving us a broken build
        #        add_path = ';'.join([os.path.join(self.builder.perl_dir, 'bin'),
        #                             os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')])
        add_path = None

        if self.builder.x86:
            self.exec_vs(
                r"%(perl_dir)s\bin\perl.exe Configure "
                + debug_option
                + "VC-WIN32 "
                + common_options
            )
        else:
            self.exec_vs(
                r"%(perl_dir)s\bin\perl.exe Configure "
                + debug_option
                + "VC-WIN64A "
                + common_options
            )

        with contextlib.suppress(Exception):
            self.exec_vs(r"nmake /nologo clean", add_path=add_path)
        self.exec_vs(r"nmake /nologo", add_path=add_path)
        self.exec_vs(r"%(perl_dir)s\bin\perl.exe mk-ca-bundle.pl -n cert.pem")
        self.exec_vs(r"nmake /nologo install", add_path=add_path)

        self.install(r".\cert.pem bin")
        self.install(r".\LICENSE share\doc\openssl")
        self.install_pc_files()
