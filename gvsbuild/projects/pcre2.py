from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pcre2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "pcre2",
            version="10.43",
            archive_url="https://github.com/PCRE2Project/pcre2/releases/download/pcre2-{version}/pcre2-{version}.tar.gz",
            hash="889d16be5abb8d05400b33c25e151638b8d4bac0e2d9c76e9d6923118ae8a34e",
            dependencies=["ninja", "meson", "pkgconf"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\pcre2")
