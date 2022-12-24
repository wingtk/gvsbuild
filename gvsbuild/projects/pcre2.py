from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pcre2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "pcre2",
            version="10.42",
            archive_url="https://github.com/PCRE2Project/pcre2/releases/download/pcre2-{version}/pcre2-{version}.tar.gz",
            hash="c33b418e3b936ee3153de2c61cc638e7e4fe3156022a5c77d0711bcbb9d64f1f",
            dependencies=["ninja", "meson", "pkgconf"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\pcre2")
