from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pcre2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "pcre2",
            version="10.40",
            archive_url="https://github.com/PCRE2Project/pcre2/releases/download/pcre2-{version}/pcre2-{version}.tar.gz",
            hash="ded42661cab30ada2e72ebff9e725e745b4b16ce831993635136f2ef86177724",
            dependencies=["ninja", "meson", "pkgconf"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\pcre2")
