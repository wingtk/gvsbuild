from gvsbuild.utils.base_project import Project, project_add
from gvsbuild.utils.base_expanders import GitRepo
from gvsbuild.utils.base_builders import CmakeProject
import os

@project_add
class Libfido2(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(
            self,
            'libfido2',
            repo_url = 'https://github.com/Yubico/libfido2.git',
            tag = '1.13.0',
            fetch_submodules = False,
            patches = ['0001-libfido2-update-cmake-script-to-have-sdl-flag-before.patch'],
            dependencies=[
            "zlib",
            "openssl",
            "libcbor"],
            )

    def build(self):
        if self.builder.x86:
            arch = "x86"
        else:
            arch = 'x64'

        include_dirs = os.path.join(self.builder.gtk_dir, "inc")
        lib_dirs = os.path.join(self.builder.gtk_dir, "lib")
        bin_dirs = lib_dirs = os.path.join(self.builder.gtk_dir, "bin")
        #Build static libs only for libfido2
        build_params = '-DBUILD_EXAMPLES=OFF -DBUILD_MANPAGES=OFF -DBUILD_TESTS=OFF -DBUILD_TOOLS=OFF -DBUILD_SHARED_LIBS=OFF -DCMAKE_C_FLAGS_DEBUG="/MTd /D_CRT_SECURE_NO_WARNINGS /D_CRT_NONSTDC_NO_DEPRECATE" -DCMAKE_C_FLAGS_RELEASE="/MT /D_CRT_SECURE_NO_WARNINGS /D_CRT_NONSTDC_NO_DEPRECATE"'
        cmake_params = f"-DWITH_ZLIB=ON -DCBOR_INCLUDE_DIRS={include_dirs} -DCRYPTO_INCLUDE_DIRS={include_dirs} -DZLIB_INCLUDE_DIRS={include_dirs} -DCBOR_LIBRARY_DIRS={lib_dirs} -DCRYPTO_LIBRARY_DIRS={lib_dirs} -DZLIB_LIBRARY_DIRS={lib_dirs} -DCBOR_BIN_DIRS={bin_dirs} -DCRYPTO_BIN_DIRS={bin_dirs} -DZLIB_BIN_DIRS={bin_dirs} {build_params}"
        
        CmakeProject.build(self, cmake_params=cmake_params, use_ninja=True)
        self.install(r'output\%s\static\* .' % (arch))
