from gvsbuild.utils.base_builders import CmakeProject
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class Pcre2(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            "pcre2",
            archive_url="https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.40/pcre2-10.40.tar.gz",
            hash="ded42661cab30ada2e72ebff9e725e745b4b16ce831993635136f2ef86177724",
            dependencies=["cmake", "ninja", "pkg-config"],
        )

    def build(self):
        CmakeProject.build(self, use_ninja=True, make_tests=True)
        self.install(r".\COPYING share\doc\pcre2")
