from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pcre2(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "pcre2",
            version="10.47",
            repository="https://github.com/PCRE2Project/pcre2",
            archive_url="https://github.com/PCRE2Project/pcre2/releases/download/pcre2-{version}/pcre2-{version}.tar.gz",
            hash="c08ae2388ef333e8403e670ad70c0a11f1eed021fd88308d7e02f596fcd9dc16",
            dependencies=["ninja", "meson", "pkgconf"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\pcre2")
