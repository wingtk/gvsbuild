from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_builders import CmakeProject
import os

@project_add
class Libcbor(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            'libcbor',
            repo_url = 'https://github.com/PJK/libcbor.git',
            tag = 'v0.10.2',
            fetch_submodules = False,
            dependencies=[
            "cmake",
            "ninja"],
            )

    def build(self):
        # If do_install is True, the build fails
        CmakeProject.build(self, use_ninja=True, do_install=False)
        self.install(r"_gvsbuild-cmake\src\cbor.lib lib")
        self.install(r"_gvsbuild-cmake\src\cbor\*.h include\cbor")
        self.install(r"_gvsbuild-cmake\cbor\*.h include\cbor")
        self.install(r"src\cbor.h include")
        self.install(r"src\cbor\*.h include\cbor")