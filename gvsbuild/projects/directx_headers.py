#  Copyright (C) 2025 The Gvsbuild Authors
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

import os

from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class DirectXHeaders(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "directx-headers",
            repository="https://github.com/microsoft/DirectX-Headers",
            version="1.618.2",
            archive_url="https://github.com/microsoft/DirectX-Headers/archive/refs/tags/v{version}.tar.gz",
            archive_filename="directx-headers-v{version}.tar.gz",
            hash="62004f45e2ab00cbb5c7f03c47262632c22fbce0a237383fc458d9324c44cf36",
            dependencies=["meson", "ninja"],
            patches=[],
        )

    def build(self):
        Meson.build(self, meson_params="-Dbuild-test=false")
        self.install(r".\LICENSE share\doc\directx-headers")

    def post_install(self):
        lib_dir = os.path.join(self.builder.gtk_dir, "lib")
        self.builder.exec_msys(
            ["mv", "libd3dx12-format-properties.a", "d3dx12-format-properties.lib"],
            working_dir=lib_dir,
        )
        self.builder.exec_msys(
            ["mv", "libDirectX-Guids.a", "DirectX-Guids.lib"],
            working_dir=lib_dir,
        )
