#  Copyright (C) 2016 - Yevgen Muntyan
#  Copyright (C) 2016 - Ignacio Casal Quinteiro
#  Copyright (C) 2016 - Arnavion
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

"""
Default projects to build
"""

import os
import glob
import shutil

from .utils.simple_ui import log
from .utils.utils import convert_to_msys
from .utils.utils import file_replace
from .utils.utils import python_find_libs_dir
from .utils.base_expanders import Tarball, GitRepo, GClientRepo
from .utils.base_expanders import NullExpander
from .utils.base_project import Project, project_add
from .utils.base_project import GVSBUILD_IGNORE
from .utils.base_builders import Meson, MercurialCmakeProject, CmakeProject, Rust


@project_add
class Project_adwaita_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'adwaita-icon-theme',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/adwaita-icon-theme/40/adwaita-icon-theme-40.0.tar.xz',
            hash = '1f2bca34f60357ab91b7db91c5e919ad36775e094138dffc870bb5f97b0dbbb2',
            dependencies = ['librsvg', 'python', ],
            )

    def build(self):
        # Create the destination dir, before the build
        os.makedirs(os.path.join(self.builder.gtk_dir, 'share', 'icons', 'Adwaita'), exist_ok=True)
        
        self.push_location(r'.\win32')
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.pop_location()

        self.install(r'.\COPYING_CCBYSA3 share\doc\adwaita-icon-theme')

@project_add
class Project_atk(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'atk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.36/atk-2.36.0.tar.xz',
            hash = 'fb76247e369402be23f1f5c65d38a9639c1164d934e40f6a9cf3c9e96b652788',
            dependencies = [
                'ninja',
                'meson',
                'pkg-config',
                'glib',
            ],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')

        self.add_param('-Dintrospection=%s' % (self.opts.enable_gi, ))
        self.add_param('-Ddocs=false')

    def build(self):
        Meson.build(self, make_tests=True)
        self.install(r'.\COPYING share\doc\atk')

@project_add
class Project_cairo(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cairo',
            archive_url = 'https://cairographics.org/releases/cairo-1.16.0.tar.xz',
            hash = '5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331',
            dependencies = ['fontconfig', 'glib', 'pixman', 'libpng'],
            patches = ['0001-Fix-mask-usage-in-image-compositor.patch'],
            )

    def build(self):
        self.exec_vs(r'make -f Makefile.win32 CFG=%(configuration)s ARCH=%(platform)s', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.push_location(r'.\util\cairo-gobject')
        self.exec_vs(r'make -f Makefile.win32 CFG=%(configuration)s ARCH=%(platform)s', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.pop_location()

        self.install(r'.\src\%(configuration)s\cairo.dll bin')
        self.install(r'.\util\cairo-gobject\%(configuration)s\cairo-gobject.dll bin')

        self.install(r'.\src\%(configuration)s\cairo.lib lib')
        self.install(r'.\util\cairo-gobject\%(configuration)s\cairo-gobject.lib lib')

        self.install(r'.\src\cairo.h include\cairo')
        self.install(r'.\src\cairo-deprecated.h include\cairo')
        self.install(r'.\src\cairo-pdf.h include\cairo')
        self.install(r'.\src\cairo-ps.h include\cairo')
        self.install(r'.\src\cairo-script.h include\cairo')
        self.install(r'.\src\cairo-svg.h include\cairo')
        self.install(r'.\src\cairo-tee.h include\cairo')
        self.install(r'.\src\cairo-win32.h include\cairo')
        self.install(r'.\src\cairo-xml.h include\cairo')
        self.install(r'.\src\cairo-ft.h include\cairo')
        self.install(r'.\src\cairo-features.h include\cairo')
        self.install(r'.\util\cairo-gobject\cairo-gobject.h include\cairo')
        self.install(r'.\cairo-version.h include\cairo')

        self.install_pc_files()
        self.install(r'.\COPYING share\doc\cairo')

@project_add
class Project_clutter(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'clutter',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/clutter/1.26/clutter-1.26.4.tar.xz',
            hash = '8b48fac159843f556d0a6be3dbfc6b083fc6d9c58a20a49a6b4919ab4263c4e6',
            dependencies = ['atk','cogl','json-glib'],
            )

    def build(self):
        self.builder.mod_env('INCLUDE', '%s\\include\\harfbuzz' % (self.builder.gtk_dir, ))
        self.exec_msbuild_gen(r'build\win32', 'clutter.sln', add_pars='/p:UseEnv=True')

        self.install(r'.\COPYING share\doc\clutter')

@project_add
class Project_cogl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cogl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/cogl/1.22/cogl-1.22.6.tar.xz',
            hash = '6d134bd3e48c067507167c001200b275997fb9c68b08b48ff038211c8c251b75',
            dependencies = ['python', 'glib','cairo','pango','gdk-pixbuf'],
            patches = ['001-cogl-missing-symbols.patch',
                       '002-cogl-pango-missing-symbols.patch'],
            )

    def build(self):
        self.builder.mod_env('INCLUDE', '%s\\include\\harfbuzz' % (self.builder.gtk_dir, ))
        self.exec_msbuild_gen(r'build\win32', 'cogl.sln', add_pars='/p:UseEnv=True')

        self.install(r'.\COPYING share\doc\cogl')

@project_add
class Project_cyrus_sasl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cyrus-sasl',
            hash = '9e8035c12d419209ea60584d5efa51d042c3ed44b450b9d173d5504b222df9f1',
            archive_url = 'https://github.com/wingtk/cyrus-sasl/releases/download/cyrus-sasl-lmdb-2.1.28/cyrus-sasl-2.1.28.tar.xz',
            dependencies = ['lmdb', 'openssl', 'mit-kerberos'],
            patches = ['0001-fix-snprintf-macro.patch',
                       '0001-Add-MIT-Kerberos-as-GSSAPI-provider.patch',
                       '0002-Provide-a-compile-option-for-32-64-gssapi.patch',
                       '0001-Fix-openssl-libs-to-point-to-the-new-openssl-1.1.1-n.patch'],
            )

    def build(self):
        configuration = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        gssapilib = 'gssapi32.lib' if self.builder.x86 else 'gssapi64.lib'
        self.exec_vs(r'nmake /nologo /f NTMakefile SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'GSSAPI="MITKerberos" GSSAPILIB="' + gssapilib + '" GSSAPI_INCLUDE="%(gtk_dir)s\include" GSSAPI_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s" CFG=' + configuration)
        self.exec_vs(r'nmake /nologo /f NTMakefile install SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" ' +
                     r'GSSAPI="MITKerberos" GSSAPILIB="' + gssapilib + '" GSSAPI_INCLUDE="%(gtk_dir)s\include" GSSAPI_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'LMDB_LIBPATH="%(gtk_dir)s\lib" OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s" CFG=' + configuration)

        self.install(r'.\COPYING share\doc\cyrus-sasl')
        self.install_pc_files()


@project_add
class Project_dcv_color_primitives(Tarball, Meson):
    def __init__(self):
        Meson.__init__(self,
            'dcv-color-primitives',
            archive_url = 'https://github.com/aws/dcv-color-primitives/archive/v0.2.0.tar.gz',
            archive_file_name = 'dcv-color-primitives-0.2.0.tar.gz',
            hash = 'c492e69ef1b7117317e75fb2570ca9ad55be2cc3c55adc3806277e02a3898a29',
            dependencies = ['ninja', 'meson', 'pkg-config', 'cargo'],
            )

    def build(self):
        Meson.build(self, make_tests=False)
        self.install(r'.\LICENSE share\doc\dcv-color-primitives')

@project_add
class Project_quiche(GitRepo, Rust):
    def __init__(self):
        Rust.__init__(self,
            'quiche',
            repo_url = 'https://github.com/cloudflare/quiche',
            fetch_submodules = True,
            tag = "0.4.0",
            dependencies = ['cargo', 'perl', 'go', 'nasm', 'cmake', 'ninja'],
            patches = ['fix_boringssl_build.patch'],
            )

    def build(self):
        Rust.build(self, make_tests = True)

        self.install_pc_files()
        self.install(r'.\include\quiche.h include\quiche')
        self.install(r'.\cargo-build\lib\quiche.dll.lib lib\quiche')
        self.install(r'.\cargo-build\lib\quiche.lib lib\quiche')
        self.install(r'.\cargo-build\lib\quiche.dll bin')
        self.install(r'.\cargo-build\lib\deps\quiche.pdb bin')
        self.install(r'.\COPYING share\doc\quiche')

@project_add
class Project_emeus(GitRepo, Meson):
    def __init__(self):
        Meson.__init__(self,
            'emeus',
            repo_url = 'https://github.com/ebassi/emeus.git',
            fetch_submodules = False,
            tag = None,
            dependencies = ['ninja', 'meson', 'pkg-config', 'gtk3'],
            patches = [
                '00_win_no_script.patch'
                ],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'true'
        else:
            enable_gi = 'false'

        self.add_param('-Ddocs=false')
        self.add_param('-Dintrospection=%s' % (enable_gi, ))

    def build(self):
        Meson.build(self, make_tests=True)
        self.install(r'.\COPYING.txt share\doc\emeus')

@project_add
class Project_enchant(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'enchant',
            archive_url = 'https://dl.hexchat.net/gtk-win32/src/enchant-1.6.1.tar.xz',
            hash = 'd6cddd2621589ca8becaba1bfe8d3668f7d6592743664ef0e1a35543971fbe6e',
            dependencies = ['glib'],
            )

    def build(self):
        x64_param = ''
        if self.builder.x64:
            x64_param = 'X64=1'

        self.push_location(r'.\src')

        #Exec nmake /nologo -f makefile.mak clean
        self.exec_vs(r'nmake /nologo -f makefile.mak DLL=1 ' + x64_param + ' MFLAGS=-MD GLIBDIR=%(gtk_dir)s\include\glib-2.0')

        self.pop_location()

        self.install(r'.\bin\release\enchant.exe ' \
                     r'.\bin\release\pdb\enchant.pdb ' \
                     r'.\bin\release\enchant-lsmod.exe ' \
                     r'.\bin\release\pdb\enchant-lsmod.pdb ' \
                     r'.\bin\release\test-enchant.exe ' \
                     r'.\bin\release\pdb\test-enchant.pdb ' \
                     r'.\bin\release\libenchant.dll ' \
                     r'.\bin\release\pdb\libenchant.pdb '\
                     r'bin')

        self.install(r'.\fonts.conf ' \
                     r'.\fonts.dtd ' \
                     r'etc\fonts')

        self.install(r'.\src\enchant.h ' \
                     r'.\src\enchant++.h ' \
                     r'.\src\enchant-provider.h ' \
                     r'include\enchant')

        self.install(r'.\bin\release\libenchant.lib lib')

        self.install(r'.\bin\release\libenchant_ispell.dll ' \
                     r'.\bin\release\libenchant_ispell.lib ' \
                     r'.\bin\release\pdb\libenchant_ispell.pdb ' \
                     r'.\bin\release\libenchant_myspell.dll ' \
                     r'.\bin\release\libenchant_myspell.lib ' \
                     r'.\bin\release\pdb\libenchant_myspell.pdb ' \
                     r'lib\enchant')

        self.install(r'.\COPYING.LIB share\doc\enchant')

@project_add
class Project_ffmpeg(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'ffmpeg',
            archive_url = 'https://www.ffmpeg.org/releases/ffmpeg-4.4.tar.xz',
            hash = '06b10a183ce5371f915c6bb15b7b1fffbe046e8275099c96affc29e17645d909',
            dependencies = [ 'nasm', 'msys2', 'pkg-config', 'nv-codec-headers' ],
        )
        if self.opts.ffmpeg_enable_gpl:
            self.add_dependency('x264')

    def build(self):
        msys_path = Project.get_tool_path('msys2')
        self.exec_vs(r'%s\bash build\build.sh %s %s %s %s' % (msys_path, self.pkg_dir, self.builder.gtk_dir, self.builder.opts.configuration, "enable_gpl" if self.opts.ffmpeg_enable_gpl else "disable_gpl"),
                     add_path=msys_path)

        self.install(r'.\COPYING.LGPLv2.1 ' \
                     r'.\COPYING.LGPLv3 ' \
                     r'share\doc\ffmpeg')
        if self.opts.ffmpeg_enable_gpl:
            self.install(r'.\COPYING.GPLv2 ' \
                         r'share\doc\ffmpeg')

    def post_install(self):
        self.builder.exec_msys(['mv', 'avcodec.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'avutil.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        if self.opts.ffmpeg_enable_gpl:
            self.builder.exec_msys(['mv', 'postproc.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'swscale.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))

@project_add
class Project_fontconfig(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'fontconfig',
            archive_url = 'https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.13.0.tar.gz',
            hash = 'a6ca290637d8b2c4e1dd40549b179202977593f7481ec83ddfb1765ad90037ba',
            dependencies = ['freetype', 'libxml2'],
            patches = ['fontconfig.patch'],
            )

    def build(self):
        #make the fontconfig files work on other compatible vs versions
        for proj in glob.glob(r'%s\*.vcxproj' % (self.build_dir,)):
            with open(proj, 'r') as f:
                content = f.read()
            if content.find('<PlatformToolset>FIXME</PlatformToolset>') >= 0:
                log.debug('patching project file %s' % (proj,))
                if self.builder.opts.vs_ver == '16':
                    fixme = r'142'
                elif self.builder.opts.vs_ver == '15':
                    fixme = r'141'
                else:
                    fixme = self.builder.opts.vs_ver + r'0'
                content = content.replace('<PlatformToolset>FIXME</PlatformToolset>', '<PlatformToolset>v%s</PlatformToolset>' % (fixme))
                with open(proj, 'w') as f:
                    f.write(content)

        self.exec_msbuild('fontconfig.sln /t:build')

        if self.builder.x86:
            rel_dir = r'.\%(configuration)s'
        else:
            rel_dir = r'.\x64\%(configuration)s'

        self.push_location(rel_dir)
        self.install('fontconfig.dll', 'fontconfig.pdb', 'fc-cache.exe', 'fc-cache.pdb', 'fc-cat.exe', 'fc-cat.pdb', 'fc-list.exe', 'fc-list.pdb',
                     'fc-match.exe', 'fc-match.pdb', 'fc-query.exe', 'fc-query.pdb', 'fc-scan.exe', 'fc-scan.pdb', 'bin')
        self.pop_location()

        self.install(r'fonts.conf fonts.dtd etc\fonts')
        self.install(r'.\fontconfig\fcfreetype.h .\fontconfig\fcprivate.h .\fontconfig\fontconfig.h include\fontconfig')

        self.push_location(rel_dir)
        self.install('fontconfig.lib', 'lib')
        self.pop_location()

        self.install_pc_files()
        self.install(r'.\COPYING share\doc\fontconfig')

@project_add
class Project_freetype(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'freetype',
            archive_url = 'http://git.savannah.gnu.org/cgit/freetype/freetype2.git/snapshot/freetype2-0d5f1dd37c056b4460a460d16fd1fbb06740e891.tar.gz',
            hash = 'e768fa19ac50bb87659370b75766ad6ca150c32c736a9dbf5980cbf9017067f6',
            dependencies = ['pkg-config', 'ninja', 'libpng'],
            patches = ['0001-meson-in-shared-libraries-we-need-to-export-the-meth.patch'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\docs\LICENSE.TXT share\doc\freetype')

@project_add
class Project_fribidi(GitRepo, Meson):
    def __init__(self):
        Project.__init__(self,
            'fribidi',
            repo_url = 'https://github.com/fribidi/fribidi.git',
            fetch_submodules = False,
            tag = 'f2c9d50722cb60d0cdec3b1bafba9029770e86b4',
            dependencies = ['ninja', 'meson'],
            )

    def build(self):
        Meson.build(self, meson_params='-Ddocs=false')
        self.install(r'.\COPYING share\doc\fribidi')

@project_add
class Project_pdfium(GClientRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'pdfium',
            repo_url = 'https://pdfium.googlesource.com/pdfium.git',
            fetch_submodules = False,
            tag = 'df97b13e53d1b96151fa119e3e94db19f5df097b',
            dependencies = ['depot', 'python', 'ninja'],
            patches = ['shared_library.patch', 'relative_includes.patch'],
            subproject_patches = {'build': ['rc_compiler.patch']},
            )

    def build(self):
        self.exec_vs(r'cp ..\resources.rc .')
        self.exec_vs(r'cp ..\args.gn out')
        if self.builder.x86:
            self.exec_vs(r'echo target_cpu="x86" >> out\args.gn')
        self.exec_vs(r'gn gen out')
        self.exec_vs(r'ninja -C out pdfium')

        self.install_dir(r'public', r'include\pdfium')
        self.install(r'out\pdfium.dll.lib', r'lib\pdfium.lib')

@project_add
class Project_gdk_pixbuf(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gdk-pixbuf',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.42/gdk-pixbuf-2.42.6.tar.xz',
            hash = 'c4a6b75b7ed8f58ca48da830b9fa00ed96d668d3ab4b1f723dcf902f78bde77f',
            dependencies = [
                'ninja',
                'pkg-config',
                'meson',
                'python',
                'libtiff-4',
                'jasper',
                'glib',
                'libpng',
            ],
            patches = ['115.diff'],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'enabled'
        else:
            enable_gi = 'disabled'

        self.add_param('-Djasper=true')
        self.add_param('-Dnative_windows_loaders=true')
        self.add_param('-Dintrospection=%s' % (enable_gi, ))
        self.add_param('-Dman=false')
        self.add_param('-Dx11=false')

    def build(self):
        # We can experiment with a couple of options to give to meson:
        #    -Dbuiltin_loaders=all|windows
        #        Buld the loader inside the library
        Meson.build(self)
        self.install(r'.\COPYING share\doc\gdk-pixbuf')

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache')

@project_add
class Project_gettext(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gettext',
            archive_url = 'http://ftp.gnu.org/pub/gnu/gettext/gettext-0.19.7.tar.gz',
            hash = '5386d2a40500295783c6a52121adcf42a25519e2d23675950619c9e69558c23f',
            dependencies = ['win-iconv'],
            patches = ['0001-gettext-runtime-Add-pre-configured-headers-for-MSVC-.patch',
                       '0001-gettext-tools-Add-pre-configured-headers-and-sources.patch',
                       '0001-gettext-tools-gnulib-lib-libxml-Check-for-_WIN32-as-.patch',
                       '0001-gettext-tools-Make-private-headers-C-friendly.patch',
                       '0001-gettext-tools-src-x-lua.c-Fix-C99ism.patch',
                       '0002-gettext-tools-gnulib-lib-Declare-items-at-top-of-blo.patch',
                       '0004-gettext-runtime-intl-plural-exp.h-Match-up-declarati.patch',
                       '0005-gettext-runtime-intl-printf-parse.c-Fix-build-on-Vis.patch',
                       '0006-gettext-intrinsics.patch'],
            )

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'gettext.sln')

        self.install(r'.\gettext-tools\its\*.its share\gettext\its')
        self.install(r'.\gettext-tools\its\*.loc share\gettext\its')
        self.install(r'.\COPYING share\doc\gettext')

@project_add
class Project_glib(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.68/glib-2.68.1.tar.xz',
            hash = '241654b96bd36b88aaa12814efc4843b578e55d47440103727959ac346944333',
            dependencies = ['ninja', 'meson', 'pkg-config', 'gettext', 'libffi', 'zlib'],
            patches = ['glib-package-installation-directory.patch'],
            )

    def build(self):
        Meson.build(self, meson_params='-Dinternal_pcre=true')
        self.install(r'.\COPYING share\doc\glib')

@project_add
class Project_glib_networking(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'glib-networking',
            archive_url = 'https://ftp.acc.umu.se/pub/gnome/sources/glib-networking/2.68/glib-networking-2.68.0.tar.xz',
            hash = '0b235e85ad26b3c0d12255d0963c460e5a639c4722f78e2a03e969e224b29f6e',
            dependencies = ['pkg-config', 'ninja', 'meson', 'glib', 'openssl'],
            )

    def build(self):
        Meson.build(self, meson_params='-Dgnutls=disabled -Dopenssl=enabled')
        self.install(r'.\COPYING share\doc\glib-networking')
        self.install(r'.\LICENSE_EXCEPTION share\doc\glib-networking')

@project_add
class Project_glib_py_wrapper(NullExpander, Meson):
    def __init__(self):
        Project.__init__(self,
            'glib-py-wrapper',
            dependencies = ['glib'],
            version = '0.1.0',
            )

    def build(self):
        Meson.build(self)

@project_add
class Project_glib_openssl(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'glib-openssl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib-openssl/2.50/glib-openssl-2.50.8.tar.xz',
            hash = '869f08e4e9a719c1df411c2fb5554400f6b24a9db0cb94c4359db8dad18d185f',
            dependencies = ['pkg-config', 'ninja', 'meson', 'glib', 'openssl'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\glib-openssl')
        self.install(r'.\LICENSE_EXCEPTION share\doc\glib-openssl')

@project_add
class Project_gobject_introspection(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gobject-introspection',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gobject-introspection/1.64/gobject-introspection-1.64.1.tar.xz',
            hash = '80beae6728c134521926affff9b2e97125749b38d38744dc901f4010ee3e7fa7',
            dependencies = [
                'ninja',
                'meson',
                'msys2',
                'pkg-config',
                'glib',
                ],
            )

    def build(self):
        # For finding gobject-introspection.pc
        self.builder.mod_env('PKG_CONFIG_PATH', '.')
        # For finding & using girepository.lib/.dll
        self.builder.mod_env('LIB', r'.\girepository')
        self.builder.mod_env('PATH', r'.\girepository')
        # For linking the _giscanner.pyd extension module when using a virtualenv
        py_dir = Project.get_tool_path('python')
        py_libs = python_find_libs_dir(py_dir)
        if py_libs:
            log.debug("Python library path is [%s]" % (py_libs, ))
            self.builder.mod_env('LIB', py_libs, prepend=False)

        Meson.build(self, meson_params='-Dpython=%s\\python.exe -Dcairo_libname=cairo-gobject.dll' % (py_dir, ))

@project_add
class Project_graphene(Tarball, Meson):
    def __init__(self):
        Meson.__init__(self,
            'graphene',
            archive_url = 'https://github.com/ebassi/graphene/archive/refs/tags/1.10.4.tar.gz',
            hash = 'd73861aceda1adf13c1fbb588ce8a3b4f632bd8d41e4635d4c70e00595d85c4d',
            dependencies = ['ninja', 'meson', 'pkg-config', 'glib'],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'enabled'
        else:
            enable_gi = 'disabled'

        self.add_param('-Dbenchmarks=false')
        self.add_param('-Dintrospection=%s' % (enable_gi, ))

    def build(self):
        Meson.build(self, make_tests=True)
        self.install(r'.\LICENSE share\doc\graphene')

@project_add
class Project_grpc(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'grpc',
            repo_url = 'https://github.com/grpc/grpc.git',
            fetch_submodules = True,
            tag = 'v1.12.0',
            dependencies = ['go', 'nuget', 'protobuf', 'perl', 'zlib', 'nasm'],
            patches = ['0001-removing-extra-plugins.patch'],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DgRPC_ZLIB_PROVIDER=package -DgRPC_PROTOBUF_PROVIDER=package', use_ninja=True, out_of_source=False)
        self.install(r'.\third_party\boringssl\ssl\ssl.lib lib')
        self.install(r'.\third_party\boringssl\crypto\crypto.lib lib')
        self.install(r'.\gpr.lib lib')
        self.install(r'.\grpc.lib lib')
        self.install(r'.\grpc++.lib lib')
        self.install(r'.\grpc_cpp_plugin.exe bin')
        self.install(r'.\grpc_cpp_plugin.pdb bin')
        self.install(r'.\grpc_csharp_plugin.exe bin')
        self.install(r'.\grpc_csharp_plugin.pdb bin')
        self.install(r'.\LICENSE share\doc\grpc')

@project_add
class Project_gsettings_desktop_schemas(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gsettings-desktop-schemas',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gsettings-desktop-schemas/40/gsettings-desktop-schemas-40.0.tar.xz',
            hash = 'f1b83bf023c0261eacd0ed36066b76f4a520bbcb14bb69c402b7959257125685',
            dependencies = ['meson', 'ninja', 'pkg-config', 'python', 'glib'],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'true'
        else:
            enable_gi = 'false'

        self.add_param('-Dintrospection=%s' % (enable_gi, ))

    def build(self):
        Meson.build(self)

        self.install(r'.\COPYING share\doc\gsettings-desktop-schemas')

@project_add
class Project_gstreamer(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gstreamer',
            archive_url = 'https://gstreamer.freedesktop.org/src/gstreamer/gstreamer-1.18.4.tar.xz',
            hash = '9aeec99b38e310817012aa2d1d76573b787af47f8a725a65b833880a094dfbc5',
            dependencies = ['meson', 'ninja', 'glib', 'orc'],
            )

        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'enabled'
        else:
            enable_gi = 'disabled'

        self.add_param('-Dintrospection=%s' % (enable_gi, ))

    def build(self):
        add_path = os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')

        Meson.build(self, add_path=add_path, meson_params='-Dtests=disabled -Dexamples=disabled')
        self.install(r'.\COPYING share\doc\gstreamer')

@project_add
class Project_gst_plugins_base(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gst-plugins-base',
            archive_url = 'https://gstreamer.freedesktop.org/src/gst-plugins-base/gst-plugins-base-1.18.4.tar.xz',
            hash = '29e53229a84d01d722f6f6db13087231cdf6113dd85c25746b9b58c3d68e8323',
            dependencies = ['meson', 'ninja', 'gtk3', 'gstreamer', 'opus'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\gst-plugins-base')

@project_add
class Project_gst_plugins_good(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gst-plugins-good',
            archive_url = 'https://gstreamer.freedesktop.org/src/gst-plugins-good/gst-plugins-good-1.18.4.tar.xz',
            hash = 'b6e50e3a9bbcd56ee6ec71c33aa8332cc9c926b0c1fae995aac8b3040ebe39b0',
            dependencies = ['meson', 'ninja', 'glib', 'gstreamer', 'gst-plugins-base', 'libvpx'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\gst-plugins-good')

@project_add
class Project_gst_plugins_bad(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gst-plugins-bad',
            archive_url = 'https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-1.18.4.tar.xz',
            hash = '74e806bc5595b18c70e9ca93571e27e79dfb808e5d2e7967afa952b52e99c85f',
            dependencies = ['meson', 'ninja', 'glib', 'gstreamer', 'gst-plugins-base'],
            )
        self.add_param('-Dcurl=disabled')
        self.add_param('-Dcurl-ssh2=disabled')

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\gst-plugins-bad')

@project_add
class Project_gst_python(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gst-python',
            archive_url = 'https://gstreamer.freedesktop.org/src/gst-python/gst-python-1.16.3.tar.xz',
            hash = '36a00a256c25ccaaa9b965a6f09d6158dfb77558145ab6b25809938732c7161f',
            dependencies = ['meson', 'ninja', 'glib', 'gstreamer', 'pygobject'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\gst-python')

class _MakeGir(object):
    """
    Class to build, with nmake, a single project .gir/.typelib files for the
    gobject-introspection support, used where the meson script is not
    present (gtk % gtk3) or not update the handle it
    """
    def make_single_gir(self, prj_name, prj_dir=None):
        if not prj_dir:
            prj_dir = prj_name

        b_dir = r'%s\%s\build\win32' % (self.builder.working_dir, prj_dir, )
        if not os.path.isfile(os.path.join(b_dir, 'detectenv-msvc.mak')):
            b_dir = r'%s\%s\win32' % (self.builder.working_dir, prj_dir, )
            if not os.path.isfile(os.path.join(b_dir, 'detectenv-msvc.mak')):
                log.message('Unable to find detectenv-msvc.mak for %s' % (prj_name, ))
                return

        cmd = 'nmake -f %s-introspection-msvc.mak CFG=%s PREFIX=%s PYTHON=%s install-introspection' % (
                prj_name,
                self.builder.opts.configuration,
                self.builder.gtk_dir,
                Project.get_tool_executable('python'),
                )

        self.push_location(b_dir)
        self.exec_vs(cmd)
        self.pop_location()

class Project_gtk_base(Tarball, Project, _MakeGir):
    def make_all_mo(self):
        mo = 'gtk20.mo' if self.name == 'gtk' else 'gtk30.mo'

        localedir = os.path.join(self.pkg_dir, 'share', 'locale')
        self.push_location(r'.\po')
        for fp in glob.glob(os.path.join(self.build_dir, 'po', '*.po')):
            f = os.path.basename(fp)
            lcmsgdir = os.path.join(localedir, f[:-3], 'LC_MESSAGES')
            self.builder.make_dir(lcmsgdir)
            cmd = ' '.join(['msgfmt', '-co', os.path.join(lcmsgdir, mo), f])
            self.builder.exec_cmd(cmd, working_dir=self._get_working_dir())
        self.pop_location()

        self.install(r'.\COPYING share\doc\%s' % self.name)

@project_add
class Project_gtk(Project_gtk_base):
    def __init__(self):
        Project.__init__(self,
            'gtk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/2.24/gtk+-2.24.31.tar.xz',
            hash = '68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658',
            dependencies = ['atk', 'gdk-pixbuf', 'pango'],
            patches = ['gtk-revert-scrolldc-commit.patch', 'gtk-bgimg.patch', 'gtk-accel.patch',
                       # https://github.com/hexchat/hexchat/issues/1007
                       'gtk-multimonitor.patch',
                       # These two will be in 2.24.33
                       'bfdac2f70e005b2504cc3f4ebbdab328974d005a.patch', '61162225f712df648f38fd12bc0817cfa9f79a64.patch',
                       # https://github.com/hexchat/hexchat/issues/2077
                       '0001-GDK-W32-Remove-WS_EX_LAYERED-from-an-opaque-window.patch',
                       ],
            )
        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')

    def build(self):
        self.builder.mod_env('INCLUDE', '%s\\include\\harfbuzz' % (self.builder.gtk_dir, ))
        self.exec_msbuild_gen(r'build\win32', 'gtk+.sln', add_pars='/p:UseEnv=True')

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\include\\harfbuzz' % (self.builder.gtk_dir, ))
            self.make_single_gir('gtk', prj_dir='gtk')

@project_add
class Project_gtk3_20(Project_gtk_base):
    def __init__(self):
        if self.opts.gtk3_ver != '3.20':
            self.ignore()
            return

        Project.__init__(self,
            'gtk3',
            prj_dir='gtk3-20',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.20/gtk+-3.20.10.tar.xz',
            hash = 'e81da1af1c5c1fee87ba439770e17272fa5c06e64572939814da406859e56b70',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            patches = ['gtk3-clip-retry-if-opened-by-others.patch'],
            )
        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'gtk+.sln',  add_pars='/p:GtkPostInstall=rem')

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))
            self.make_single_gir('gtk', prj_dir='gtk3-20')

        self.exec_cmd(r'%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas')
        self.exec_cmd(r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"')

@project_add
class Project_gtk3_22(Project_gtk_base):
    def __init__(self):
        if self.opts.gtk3_ver != '3.22':
            self.ignore()
            return

        Project.__init__(self,
            'gtk3',
            prj_dir='gtk3-22',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.22/gtk+-3.22.30.tar.xz',
            hash = 'a1a4a5c12703d4e1ccda28333b87ff462741dc365131fbc94c218ae81d9a6567',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            )
        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'gtk+.sln',  add_pars='/p:GtkPostInstall=rem')

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))
            self.make_single_gir('gtk', prj_dir='gtk3-22')

        self.exec_cmd(r'%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas')
        self.exec_cmd(r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"')

@project_add
class Project_gtk3_24(Tarball, Meson):
    def __init__(self):
        if self.opts.gtk3_ver != '3.24':
            self.ignore()
            return

        Project.__init__(self,
            'gtk3',
            prj_dir='gtk3-24',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.24/gtk+-3.24.28.tar.xz',
            hash = 'b04e09763367f1ce932cd2ee3a359d4de150e1c38e7bef7d29aa72557a6b47c6',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            patches = [
                'gtk_update_icon_cache.patch',
            ],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'true'
        else:
            enable_gi = 'false'

        self.add_param('-Dintrospection=%s' % (enable_gi, ))

    def build(self):
        Meson.build(self, meson_params='-Dtests=false -Ddemos=false -Dexamples=false')

        self.install(r'.\COPYING share\doc\gtk3')

@project_add
class Project_gtksourceview3(Tarball, Project, _MakeGir):
    def __init__(self):
        Project.__init__(self,
            'gtksourceview3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtksourceview/3.22/gtksourceview-3.22.2.tar.xz',
            hash = '6ce84231dd0931cc747708434ca2f344c65a092dd6e1a800283fe0748773af5e',
            dependencies = ['perl', 'gtk3'],
            )
        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')

    def build(self):
        self.builder.mod_env('INCLUDE', '%s\\include\\harfbuzz' % (self.builder.gtk_dir, ))
        self.exec_msbuild_gen(r'build\win32', 'gtksourceview.sln', add_pars='/p:UseEnv=True')

        self.install(r'.\COPYING share\doc\gtksourceview3')

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\gtk-3.0' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))
            self.make_single_gir('gtksourceview', prj_dir='gtksourceview3')

@project_add
class Project_harfbuzz(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'harfbuzz',
            archive_url = 'https://github.com/harfbuzz/harfbuzz/releases/download/2.8.0/harfbuzz-2.8.0.tar.xz',
            hash = 'a1079fd021adaf5683351f34587a255975cc3bcadba31246ae40ebebb95ecd42',
            dependencies = ['python', 'freetype', 'pkg-config', 'glib'],
            )

        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            self.add_param('-Dintrospection=enabled')
        else:
            self.add_param('-Dintrospection=disabled')

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\harfbuzz')

@project_add
class Project_hicolor_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'hicolor-icon-theme',
            archive_url = 'http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.17.tar.xz',
            hash = '317484352271d18cbbcfac3868eab798d67fff1b8402e740baa6ff41d588a9d8',
            )

    def build(self):
        self.install(r'.\index.theme share\icons\hicolor')

@project_add
class Project_icu(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'icu',
            archive_url = 'https://github.com/unicode-org/icu/releases/download/release-63-1/icu4c-63_1-src.zip',
            hash = '3d957deabf75e96c35918355eac4da3e728fc222b9b4bdb2663652f76ee51772',
            version='63.1',
            )

    def build(self):
        bindir = r'.\bin'
        libdir = r'.\lib'
        if not self.builder.x86:
            bindir += '64'
            libdir += '64'
        if self.opts.vs_ver != '15':
            # Not Vs2017, we change the platform 
            search, replace = self._msbuild_make_search_replace(141)
            self._msbuild_copy_dir(None, os.path.join(self.build_dir, 'source', 'allinone'), search, replace)

        self.exec_msbuild(r'source\allinone\allinone.sln /t:cal')

        if self.builder.opts.configuration == 'debug':
            self.install_pc_files('pc-files-debug')
        else:
            self.install_pc_files()

        self.install(r'.\LICENSE share\doc\icu')
        self.install(bindir + r'\* bin')
        self.install(libdir + r'\* lib')
        self.install(r'.\include\* include')

@project_add
class Project_jasper(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'jasper',
            archive_url = 'http://www.ece.uvic.ca/~frodo/jasper/software/jasper-2.0.14.tar.gz',
            hash = '2a1f61e55afe8b4ce8115e1508c5d7cb314d56dfcc2dd323f90c072f88ccf57b',
            dependencies = ['cmake', 'ninja', 'libjpeg-turbo', ],
            patches = [
                    '001-dont-use-pkg-full-path.patch',
                    '002-dont-install-msvc-runtime.patch',
                ]
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\COPYRIGHT share\doc\jasper')
        self.install(r'.\LICENSE share\doc\jasper')

@project_add
class Project_jsonc(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'json-c',
            archive_url = 'https://github.com/json-c/json-c/archive/json-c-0.12.1-20160607.tar.gz',
            hash = '989e09b99ded277a0a651cd18b81fcb76885fea08769d7a21b6da39fb8a34816',
            patches = ['json-c-0.12.1-20160607.patch'],
            )

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'json-c.sln')

        self.install(r'.\COPYING share\doc\json-c')

@project_add
class Project_json_glib(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'json-glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/json-glib/1.6/json-glib-1.6.2.tar.xz',
            hash = 'a33d66c6d038bda46b910c6c6d59c4e15db014e363dc997a0414c2e07d134f24',
            dependencies = ['meson', 'ninja', 'pkg-config', 'python', 'glib'],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'enabled'
        else:
            enable_gi = 'disabled'

        self.add_param('-Dgtk_doc=disabled')
        self.add_param('-Dintrospection=%s' % (enable_gi, ))

    def build(self):
        Meson.build(self, make_tests=True)

        self.install(r'.\COPYING share\doc\json-glib')

@project_add
class Project_leveldb(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'leveldb',
            archive_url = 'https://github.com/google/leveldb/archive/v1.20.tar.gz',
            archive_file_name = 'leveldb-1.20.tar.gz',
            hash = 'f5abe8b5b209c2f36560b75f32ce61412f39a2922f7045ae764a2c23335b6664',
            )

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'leveldb.sln')

        self.install(r'.\LICENSE share\doc\leveldb')

@project_add
class Project_libarchive(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libarchive',
            archive_url = 'https://libarchive.org/downloads/libarchive-3.4.1.tar.xz',
            hash = 'bb84e02f08cc3027e08e2473fc46eb7724ba9244e9c6ef8d122f68addd6042f7',
            dependencies = ['cmake', 'ninja', 'win-iconv', 'zlib', 'lz4', 'openssl', 'libxml2'],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DENABLE_WERROR=OFF', use_ninja=True)
        # Fix the pkg-config .pc file, correcting the library's names
        file_replace(os.path.join(self.pkg_dir, 'lib', 'pkgconfig', 'libarchive.pc'),
                     [ (' -llz4',   ' -lliblz4'),
                       (' -leay32', ' -llibeay32'),
                       (' -lxml2',  ' -llibxml2'),
                       ]
                     )
        self.install(r'.\COPYING share\doc\libarchive')

@project_add
class Project_libcroco(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libcroco',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libcroco/0.6/libcroco-0.6.13.tar.xz',
            hash = '767ec234ae7aa684695b3a735548224888132e063f92db585759b422570621d4',
            dependencies = ['glib', 'libxml2'],
            )

    def build(self):
        self.exec_msbuild_gen(r'win32', 'libcroco.sln')
        self.install(r'.\COPYING share\doc\libcroco')

@project_add
class Project_libepoxy(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libepoxy',
            archive_url = 'https://github.com/anholt/libepoxy/releases/download/1.5.5/libepoxy-1.5.5.tar.xz',
            hash = '261663db21bcc1cc232b07ea683252ee6992982276536924271535875f5b0556',
            dependencies = ['python', 'ninja', 'meson'],
            )

    def build(self):
        Meson.build(self)

        self.install(r'COPYING share\doc\libepoxy')

@project_add
class Project_libffi(GitRepo, Meson):
    def __init__(self):
        Project.__init__(self,
            'libffi',
            repo_url = 'https://github.com/centricular/libffi.git',
            fetch_submodules = False,
            tag = 'meson-1.14',
            dependencies = ['python', 'ninja', 'meson'],
            patches = [
                 '001-rename-debug-to-ffi-debug.patch',
                 ],
            )

    def build(self):
        Meson.build(self)
        self.install(r'LICENSE share\doc\libffi')

@project_add
class Project_libgxps(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libgxps',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libgxps/0.3/libgxps-0.3.2.tar.xz',
            hash = '6d27867256a35ccf9b69253eb2a88a32baca3b97d5f4ef7f82e3667fa435251c',
            dependencies = ['meson', 'ninja', 'pkg-config', 'glib', 'libarchive', 'cairo', 'libpng', 'libjpeg-turbo', 'libtiff-4', 'gtk3', ],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            disable_gi = 'false'
        else:
            disable_gi = 'true'

        self.add_param('-Ddisable-introspection=%s' % (disable_gi, ))
        self.add_param('-Dwith-liblcms2=false')
        self.add_param('-Denable-test=false')

    def build(self):
        Meson.build(self)

        self.install(r'.\COPYING share\doc\libgxps')

@project_add
class Project_libjpeg_turbo(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libjpeg-turbo',
            archive_url = 'https://sourceforge.net/projects/libjpeg-turbo/files/2.0.6/libjpeg-turbo-2.0.6.tar.gz',
            hash = 'd74b92ac33b0e3657123ddcf6728788c90dc84dcb6a52013d758af3c4af481bb',
            dependencies = ['cmake', 'ninja', 'nasm', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\LICENSE.md share\doc\libjpeg-turbo')

@project_add
class Project_libmicrohttpd(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libmicrohttpd',
             archive_url = 'http://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.54.tar.gz',
             hash = 'bcc721895d4a114b0548a39d2241c35caacb9e2e072d40e11b55c60e3d5ddcbe',
             patches = ['001-remove-postsample.patch'],
            )

    def build(self):
        configuration = 'release-dll'
        if self.builder.opts.configuration == 'debug':
            configuration = 'debug-dll'

        td = self.exec_msbuild_gen(r'w32', 'libmicrohttpd.sln', configuration=configuration)
        base_dir = os.path.join('w32', td)

        debug_option = ''
        if self.builder.opts.configuration == 'debug':
            debug_option = r'_d'

        rel_dir = '.\\' + base_dir + r'\Output'
        if not self.builder.x86:
            rel_dir += r'\x64'

        self.push_location(rel_dir)
        self.install(r'microhttpd.h include')
        self.install(r'libmicrohttpd-dll' + debug_option + '.lib' + ' lib')
        self.install(r'libmicrohttpd-dll' + debug_option + '.dll' + ' bin')
        self.install(r'libmicrohttpd-dll' + debug_option + '.pdb' + ' bin')
        self.install(r'hellobrowser-dll' + debug_option + '.exe' + ' bin')
        self.pop_location()

        self.install(r'.\COPYING share\doc\libmicrohttpd')

@project_add
class Project_libpng(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libpng',
            archive_url = 'http://prdownloads.sourceforge.net/libpng/libpng-1.6.37.tar.xz',
            hash = '505e70834d35383537b6491e7ae8641f1a4bed1876dbfe361201fc80868d88ca',
            dependencies = ['cmake', 'ninja', 'zlib'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install_pc_files()
        self.install('LICENSE share\doc\libpng')

@project_add
class Project_libpsl(GitRepo, Meson):
    def __init__(self):
        Project.__init__(self,
            'libpsl',
            repo_url = 'https://github.com/rockdaboot/libpsl.git',
            fetch_submodules = True,
            tag = 'b32e81367ce91388e94bd34c54e7297063857d66',
            dependencies = ['python', 'meson', 'ninja', 'pkg-config', 'icu', ],
            )

        self.add_param('-Druntime=libicu')
        self.add_param('-Dbuiltin=libicu')

    def build(self):
        Meson.build(self)

        self.install(r'.\LICENSE share\doc\libpsl')

@project_add
class Project_librsvg_legacy(Tarball, Project, _MakeGir):
    def __init__(self):

        if not self.opts.old_rsvg:
            self.ignore()
            return

        Project.__init__(self,
            'librsvg',
            prj_dir='librsvg-legacy',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.40/librsvg-2.40.20.tar.xz',
            hash = 'cff4dd3c3b78bfe99d8fcfad3b8ba1eee3289a0823c0e118d78106be6b84c92b',
            dependencies = ['libcroco', 'cairo', 'pango', 'gdk-pixbuf', 'gtk3'],
            patches = [
                'vs2019-support.patch'
                ],
            )
        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')

    def build(self):
        self.builder.mod_env('INCLUDE', '%s\\include\\harfbuzz' % (self.builder.gtk_dir, ))
        self.exec_msbuild_gen(r'build\win32', 'librsvg.sln', add_pars='/p:UseEnv=True')

        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\glib-2.0' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\lib\\glib-2.0\include' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\include\\gdk-pixbuf-2.0' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))

            self.make_single_gir('rsvg', prj_dir='librsvg-legacy')

        self.install(r'.\COPYING share\doc\librsvg')

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache')

@project_add
class Project_librsvg(Tarball, Project):
    def __init__(self):

        if self.opts.old_rsvg:
            self.ignore()
            return

        Project.__init__(self,
            'librsvg',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.50/librsvg-2.50.3.tar.xz',
            hash = 'a4298a98e3a95fdd73c858c17d4dd018525fb09dbb13bbd668a0c2243989e958',
            dependencies = [
                'cargo',
                'cairo',
                'pango',
                'gdk-pixbuf',
            ],
            patches = [
                '0001-keep-cairo-dep.patch',
            ],
            )
        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')

    def build(self):
        self.builder.mod_env('INCLUDE', 'include\\cairo', add_gtk=True)

        b_dir = r'%s\%s\win32' % (self.builder.working_dir, self.name, )

        cmd = 'nmake -f makefile.vc CFG=%s PREFIX=%s PYTHON=%s install' % (
                self.builder.opts.configuration,
                self.builder.gtk_dir,
                Project.get_tool_executable('python'),
                )

        if Project.opts.enable_gi:
            cmd += ' INTROSPECTION=1'

        self.push_location(b_dir)
        self.exec_vs(cmd)
        self.pop_location()

        self.install(r'.\COPYING.LIB share\doc\librsvg')

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache')

@project_add
class Project_libcurl(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libcurl',
            archive_url = 'https://github.com/curl/curl/releases/download/curl-7_54_0/curl-7.54.0.tar.gz',
            hash = 'a84b635941c74e26cce69dd817489bec687eb1f230e7d1897fc5b5f108b59adf',
            dependencies = ['perl', 'cmake', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
        # Fix the pkg-config .pc file, correcting the library's names
        file_replace(os.path.join(self.pkg_dir, 'lib', 'pkgconfig', 'libcurl.pc'),
                     [ (' -lcurl', ' -llibcurl_imp'),
                       ]
                     )

        self.install(r'.\COPYING share\doc\libcurl')

@project_add
class Project_libsoup(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libsoup',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libsoup/2.72/libsoup-2.72.0.tar.xz',
            hash = '170c3f8446b0f65f8e4b93603349172b1085fb8917c181d10962f02bb85f5387',
            dependencies = ['libxml2', 'glib-networking', 'sqlite', 'libpsl', 'mit-kerberos'],
            patches = ['0001-Improve-support-for-rfc-7230.patch'],
            )

        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'enabled'
        else:
            enable_gi = 'disabled'

        self.add_param('-Dintrospection=%s' % (enable_gi, ))
        self.add_param('-Dvapi=disabled')
        self.add_param('-Dsysprof=disabled')
        self.add_param('-Dtls_check=false')
        self.add_param('-Dtests=false')

    def build(self):
        Meson.build(self)

        self.install(r'.\COPYING share\doc\libsoup')

@project_add
class Project_libssh(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libssh',
            archive_url = 'https://www.libssh.org/files/0.9/libssh-0.9.3.tar.xz',
            hash = '2c8b5f894dced58b3d629f16f3afa6562c20b4bdc894639163cf657833688f0c',
            dependencies = ['zlib','openssl', 'cmake', 'ninja'],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DWITH_ZLIB=ON', use_ninja=True)
        self.install(r'.\COPYING share\doc\libssh')

@project_add
class Project_libssh2(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libssh2',
            archive_url = 'https://www.libssh2.org/download/libssh2-1.8.0.tar.gz',
            hash = '39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4',
            dependencies = ['cmake', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DWITH_ZLIB=ON', use_ninja=True)
        self.install(r'.\COPYING share\doc\libssh2')

@project_add
class Project_libtiff4(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libtiff-4',
            archive_url = 'http://download.osgeo.org/libtiff/tiff-4.2.0.tar.gz',
            hash = 'eb0484e568ead8fa23b513e9b0041df7e327f4ee2d22db5a533929dfc19633cb',
            dependencies = ['cmake', 'ninja', 'libjpeg-turbo', ],
            patches = ['remove-postfix.patch'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\COPYRIGHT share\doc\tiff')

@project_add
class Project_libuv(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libuv',
            archive_url = 'https://github.com/libuv/libuv/archive/v1.35.0.tar.gz',
            hash = 'ff84a26c79559e511f087aa67925c3b4e0f0aac60cd8039d4d38b292f208ff58',
            dependencies = [
                'cmake', 
                'ninja',  
                ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\LICENSE share\doc\libuv')

@project_add
class Project_libvpx(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libvpx',
            archive_url = 'https://github.com/webmproject/libvpx/archive/v1.10.0.tar.gz',
            hash = '85803ccbdbdd7a3b03d930187cb055f1353596969c1f92ebec2db839fa4f834a',
            dependencies = ['yasm', 'msys2', 'libyuv', 'perl'],
            patches = ['0006-gen_msvs_vcxproj.sh-Select-current-Windows-SDK-if-av.patch',
                       '0001-Always-generate-pc-file.patch'],
            )
    def build(self):
        configure_options = "--enable-pic --as=yasm --disable-unit-tests --size-limit=16384x16384 " \
                            "--enable-postproc --enable-multi-res-encoding --enable-temporal-denoising " \
                            "--enable-vp9-temporal-denoising --enable-vp9-postproc --disable-tools " \
                            "--disable-examples --disable-docs "
        if self.builder.opts.configuration == 'debug':
            configure_options += '--enable-debug_libs'

        if self.builder.x86:
            target = 'x86-win32-vs'
        else:
            target = 'x86_64-win64-vs'

        target += self.builder.opts.vs_ver

        msys_path = Project.get_tool_path('msys2')

        self.exec_vs(r'%s\bash ./configure --target=%s --prefix=%s %s' % (msys_path, target, convert_to_msys(self.builder.gtk_dir), configure_options),
                     add_path=msys_path)
        self.exec_vs(r'make', add_path=msys_path)
        self.exec_vs(r'make install', add_path=msys_path)

        self.install(r'.\LICENSE share\doc\libvpx')

    def post_install(self):
        # LibVPX generates a static library named 'vpxmd.lib' or 'vpxmdd.lib'
        # in an unusual directory which is not the same as expected by the vpx.pc file
        if self.builder.opts.configuration == 'debug':
            lib_name = 'vpxmdd.lib'
        else:
            lib_name = 'vpxmd.lib'
        if self.builder.x86:
            lib_path = 'Win32/' + lib_name
        else:
            lib_path = 'x64/' + lib_name
        self.builder.exec_msys(['mv', lib_path, './vpx.lib'], working_dir=os.path.join(self.builder.gtk_dir, 'lib'))

@project_add
class Project_libxml2(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libxml2',
            archive_url = 'http://xmlsoft.org/sources/libxml2-2.9.12.tar.gz',
            hash = 'c8d6681e38c56f172892c85ddc0852e1fd4b53b4209e7f4ebf17f7e2eae71d92',
            dependencies = ['win-iconv', 'meson', 'ninja'],
            )

    def build(self):
        Meson.build(self)
        self.install_pc_files()
        self.install(r'.\COPYING share\doc\libxml2')

@project_add
class Project_libyuv(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libyuv',
            repo_url = 'https://chromium.googlesource.com/libyuv/libyuv',
            fetch_submodules = False,
            tag = '93b1b332cd60b56ab90aea14182755e379c28a80',
            dependencies = ['cmake', 'ninja', 'libjpeg-turbo', ],
            patches = [
                '001-win-build.patch',
                ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install_pc_files()
        self.install(r'.\LICENSE share\doc\libyuv')

@project_add
class Project_libzip(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libzip',
            archive_url = 'https://nih.at/libzip/libzip-1.2.0.tar.gz',
            hash = '6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f',
            dependencies = ['cmake', 'ninja', 'zlib'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
        self.install(r'.\LICENSE share\doc\libzip')

@project_add
class Project_lmdb(GitRepo, Meson):
    def __init__(self):
        Project.__init__(self,
            'lmdb',
            repo_url = 'https://github.com/wingtk/lmdb.git',
            fetch_submodules = False,
            tag = 'mdb.RE/0.9-meson',
            dependencies = [
                'ninja',
                'meson',
            ],
            )

    def build(self):
        self.push_location(r'.\libraries\liblmdb')
        Meson.build(self)
        self.install('LICENSE share\doc\lmdb')
        self.pop_location()

@project_add
class Project_luajit(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'luajit',
            archive_url = 'http://luajit.org/download/LuaJIT-2.1.0-beta3.tar.gz',
            hash = '1ad2e34b111c802f9d0cdf019e986909123237a28c746b21295b63c9e785d9c3',
            patches = ['set-paths.patch'],
            )

    def build(self):
        option = ''
        if self.builder.opts.configuration == 'debug':
            option = 'debug'

        self.push_location('src')

        self.exec_vs(r'.\msvcbuild ' + option)

        self.install(r'.\lua.h .\lualib.h .\luaconf.h .\lauxlib.h .\luajit.h include\luajit-2.1')
        self.install(r'.\luajit.exe .\lua51.dll .\lua51.pdb bin')
        self.install(r'.\lua51.lib lib')

        self.pop_location()

        self.install(r'.\etc\luajit.pc lib\pkgconfig')
        self.install(r'.\README .\COPYRIGHT share\doc\luajit')

@project_add
class Project_lz4(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'lz4',
            archive_url = 'https://github.com/lz4/lz4/archive/v1.9.3.tar.gz',
            archive_file_name = 'lz4-1.9.3.tar.gz',
            hash = '030644df4611007ff7dc962d981f390361e6c97a34e5cbc393ddfbe019ffe2c1',
            )

    def build(self):
        self.exec_msbuild_gen(r'visual', 'lz4.sln')

        self.install(r'visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.dll visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.pdb bin')
        self.install(r'.\lib\lz4.h .\lib\lz4hc.h .\lib\lz4frame.h include')
        self.install(r'visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.lib lib')

        self.install(r'.\lib\LICENSE share\doc\lz4')
        self.install_pc_files()

@project_add
class Project_mit_kerberos(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'mit-kerberos',
            hash = 'd46a676bd6cfe58b8684ffd881bc7ed2c9c90cb43ccfa45a9500530e84aa262b',
            archive_url = 'https://github.com/krb5/krb5/archive/krb5-1.16.1-final.tar.gz',
            dependencies = [
                'perl',
            ],
            )

    def build(self):
        configuration = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        add_path = os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')

        self.push_location('src')
        self.exec_vs(r'nmake -f Makefile.in prep-windows NO_LEASH=1 KRB_INSTALL_DIR=%(gtk_dir)s ', add_path=add_path)
        self.exec_vs(r'nmake NODEBUG=' + str(1 if configuration == 'Release' else 0) + ' NO_LEASH=1 KRB_INSTALL_DIR=%(gtk_dir)s ', add_path=add_path)
        self.exec_vs(r'nmake install NODEBUG=' + str(1 if configuration == 'Release' else 0) + ' NO_LEASH=1 KRB_INSTALL_DIR=%(gtk_dir)s ', add_path=add_path)
        self.pop_location()

        self.install(r'.\NOTICE share\doc\mit-kerberos')

@project_add
class Project_nv_codec_headers(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'nv-codec-headers',
            repo_url = 'http://git.videolan.org/git/ffmpeg/nv-codec-headers.git',
            fetch_submodules = False,
            tag = 'n9.0.18.4',
            )

    def build(self):
        add_path = os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')

        self.exec_vs(r'make install PREFIX="%(gtk_dir)s"', add_path=add_path)

@project_add
class Project_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'openssl',
            archive_url = 'https://www.openssl.org/source/openssl-1.1.1k.tar.gz',
            hash = '892a0875b9872acd04a9fde79b1f943075d5ea162415de3047c327df33fbaee5',
            dependencies = ['perl', 'nasm', 'msys2', ],
            )

    def build(self):
        common_options = r'no-ssl2 no-ssl3 no-comp --openssldir=%(gtk_dir)s/etc/ssl --prefix=%(gtk_dir)s'

        debug_option = ''
        if self.builder.opts.configuration == 'debug':
            debug_option = 'debug-'

        # Note that we want to give priority to the system perl version.
        # Using the msys2 one might endup giving us a broken build
#        add_path = ';'.join([os.path.join(self.builder.perl_dir, 'bin'),
#                             os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')])
        add_path = None

        if self.builder.x86:
            self.exec_vs(r'%(perl_dir)s\bin\perl.exe Configure ' + debug_option + 'VC-WIN32 ' + common_options)
        else:
            self.exec_vs(r'%(perl_dir)s\bin\perl.exe Configure ' + debug_option + 'VC-WIN64A ' + common_options)

        try:
            self.exec_vs(r'nmake /nologo clean', add_path=add_path)
        except:
            pass

        self.exec_vs(r'nmake /nologo', add_path=add_path)
        #self.exec_vs(r'nmake /nologo test', add_path=add_path)
        self.exec_vs(r'%(perl_dir)s\bin\perl.exe mk-ca-bundle.pl -n cert.pem')
        self.exec_vs(r'nmake /nologo install', add_path=add_path)

        self.install(r'.\cert.pem bin')
        self.install(r'.\LICENSE share\doc\openssl')
        self.install_pc_files()

@project_add
class Project_opus(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'opus',
            archive_url = 'https://archive.mozilla.org/pub/opus/opus-1.3.1.tar.gz',
            hash = '65b58e1e25b2a114157014736a3d9dfeaad8d41be1c8179866f144a2fb44ff9d',
            )

    def build(self):
        configuration = 'ReleaseDLL'
        if self.builder.opts.configuration == 'debug':
            configuration = 'DebugDLL'

        td = self.exec_msbuild_gen(r'.\win32', 'opus.sln', configuration=configuration)
        bin_dir = os.path.join(r'.\win32', td, self.builder.opts.platform, configuration)

        self.install(bin_dir + r'\opus.dll bin')
        self.install(bin_dir + r'\opus.pdb bin')

        self.install(bin_dir + r'\opus.lib lib')

        self.install(r'include\* include')

        self.install_pc_files()

        self.install(r'COPYING share\doc\opus')

@project_add
class Project_orc(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'orc',
            archive_url = 'https://gstreamer.freedesktop.org/src/orc/orc-0.4.32.tar.xz',
            hash = 'a66e3d8f2b7e65178d786a01ef61f2a0a0b4d0b8370de7ce134ba73da4af18f0',
            dependencies = [
                'ninja',
                'meson',
            ],
            )

    def build(self):
        Meson.build(self, meson_params='-Dbenchmarks=disabled -Dtools=enabled')
        self.install(r'COPYING share\doc\orc')

@project_add
class Project_pango(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'pango',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.48/pango-1.48.4.tar.xz',
            hash = '418913fb062071a075846244989d4a67aa5c80bf0eae8ee4555a092fd566a37a',
            dependencies = [
                'ninja',
                'meson',
                'cairo',
                'harfbuzz',
                'fribidi',
            ],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'enabled'
        else:
            enable_gi = 'disabled'

        self.add_param('-Dintrospection=%s' % (enable_gi, ))

    def build(self):
        Meson.build(self)
        self.install(r'COPYING share\doc\pango')

@project_add
class Project_pixman(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pixman',
            archive_url = 'http://cairographics.org/releases/pixman-0.40.0.tar.gz',
            hash = '6d200dec3740d9ec4ec8d1180e25779c00bc749f94278c8b9021f5534db223fc',
            )

    def build(self):
        optimizations = 'SSE2=on SSSE3=on'
        if self.builder.x64:
            # FIXME: cairo fails to build due to missing symbols if I enable MMX on 64bit
            optimizations += ' MMX=off'
        else:
            optimizations += ' MMX=on'

        add_path = os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')

        self.exec_vs(r'make -f Makefile.win32 pixman CFG=%(configuration)s ' + optimizations, add_path=add_path)

        self.install(r'.\pixman\%(configuration)s\pixman-1.lib lib')

        self.install(r'.\pixman\pixman.h include\pixman-1')
        self.install(r'.\pixman\pixman-version.h include\pixman-1')

        self.install(r'.\COPYING share\doc\pixman')

@project_add
class Project_pkgconf(GitRepo, Meson):
    def __init__(self):
        GitRepo.__init__(self)
        Project.__init__(self,
            'pkg-config',
            prj_dir = 'pkgconf',
            repo_url = 'https://github.com/pkgconf/pkgconf.git',
            fetch_submodules = False,
            tag = 'pkgconf-1.5.4',
            dependencies = ['ninja', 'meson'],
            patches = [ '0001-vs2013.patch',
                      ],
            )
        self.add_param('-Dtests=false')

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\pkgconf')

    def post_install(self):
        self.exec_cmd(r'copy %(gtk_dir)s\bin\pkgconf.exe %(gtk_dir)s\bin\pkg-config.exe')

@project_add
class Project_portaudio(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'portaudio',
            archive_url = 'http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz',
            dependencies = ['cmake', 'ninja', ],
            patches = [ '0001-Do-not-add-suffice-to-the-library-name.patch',
                        '0001-Fix-MSVC-check.patch' ]
            )

    def build(self):
        CmakeProject.build(self,
                           cmake_params='-DPA_DLL_LINK_WITH_STATIC_RUNTIME=off',
                           use_ninja=True,
                           do_install=False,
                           out_of_source=False)

        self.install(r'portaudio.dll bin')
        self.install(r'portaudio.pdb bin')
        self.install(r'portaudio.lib lib')

        self.install(r'.\include\* include')

        self.install(r'.\LICENSE.txt share\doc\portaudio')

@project_add
class Project_protobuf(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'protobuf',
            archive_url = 'https://github.com/protocolbuffers/protobuf/releases/download/v3.15.8/protobuf-cpp-3.15.8.tar.gz',
            hash = '9b57647b898e45253c98fae35146f6a5e9e788817d29019f9280270c951a0038',
            dependencies = ['cmake', 'zlib', 'ninja', ],
            )

    def build(self):
        # We need to compile with STATIC_RUNTIME off since protobuf-c also compiles with it OFF
        CmakeProject.build(self,
                           cmake_params=r'-Dprotobuf_DEBUG_POSTFIX="" -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_WITH_ZLIB=ON -Dprotobuf_MSVC_STATIC_RUNTIME=OFF',
                           use_ninja=True,
                           source_part='cmake')

        self.install(r'.\LICENSE share\doc\protobuf')

@project_add
class Project_protobuf_c(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'protobuf-c',
            archive_url = 'https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.3/protobuf-c-1.3.3.tar.gz',
            hash = '22956606ef50c60de1fabc13a78fbc50830a0447d780467d3c519f84ad527e78',
            dependencies = ['cmake', 'protobuf', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True, source_part='build-cmake')

        self.install(r'.\LICENSE share\doc\protobuf-c')
        self.install_pc_files()

@project_add
class Project_pycairo(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pycairo',
            archive_url = 'https://github.com/pygobject/pycairo/releases/download/v1.19.1/pycairo-1.19.1.tar.gz',
            hash = '2c143183280feb67f5beb4e543fd49990c28e7df427301ede04fc550d3562e84',
            dependencies = ['cairo', 'python'],
            patches = [
                'pycairo_py3_8_load_dll.patch',
                ],
            )

    def build(self):
        cairo_inc = os.path.join(self.builder.gtk_dir, 'include', 'cairo')
        self.builder.mod_env('INCLUDE', cairo_inc)
        self.push_location(self.build_dir)
        self.exec_vs(r'%(python_dir)s\python.exe setup.py install')
        if self.builder.opts.py_egg:
            self.exec_vs(r'%(python_dir)s\python.exe setup.py bdist_egg')
        if self.builder.opts.py_wheel:
            self.exec_vs(r'%(python_dir)s\python.exe setup.py bdist_wheel')
        if self.builder.opts.py_egg or self.builder.opts.py_wheel:
            self.install_dir('dist', 'python')
        self.install(r'.\COPYING share\doc\pycairo')
        self.install(r'.\COPYING-LGPL-2.1 share\doc\pycairo')
        self.install(r'.\COPYING-MPL-1.1 share\doc\pycairo')
        self.install_pc_files()
        self.pop_location()

@project_add
class Project_pygobject(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pygobject',
            archive_url = 'https://ftp.acc.umu.se/pub/GNOME/sources/pygobject/3.36/pygobject-3.36.0.tar.xz',
            hash = '8683d2dfb5baa9e501a9a64eeba5c2c1117eadb781ab1cd7a9d255834af6daef',
            dependencies = ['python', 'pycairo', 'gobject-introspection', 'libffi'],
            patches = [
                'pygobject_py3_8_load_dll.patch',
                ],
            )

    def build(self):
        gtk_dir = self.builder.gtk_dir
        add_inc = [
            os.path.join(gtk_dir, 'include', 'cairo'),
            os.path.join(gtk_dir, 'include', 'gobject-introspection-1.0'),
            os.path.join(gtk_dir, 'include', 'glib-2.0'),
            os.path.join(gtk_dir, 'lib', 'glib-2.0', 'include'),
        ]
        self.builder.mod_env('INCLUDE', ";".join(add_inc))
        self.push_location(self.build_dir)
        self.exec_vs(r'%(python_dir)s\python.exe setup.py install')
        if self.builder.opts.py_egg:
            self.exec_vs(r'%(python_dir)s\python.exe setup.py bdist_egg')
        if self.builder.opts.py_wheel:
            self.exec_vs(r'%(python_dir)s\python.exe setup.py bdist_wheel')
        if self.builder.opts.py_egg or self.builder.opts.py_wheel:
            self.install_dir('dist', 'python')
        self.install(r'.\COPYING share\doc\pygobject')
        self.install(r'.\gi\pygobject.h include\pygobject-3.0')
        self.install_pc_files()
        self.pop_location()

@project_add
class Project_sqlite(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'sqlite',
            archive_url = 'https://www.sqlite.org/2020/sqlite-autoconf-3310100.tar.gz',
            hash = '62284efebc05a76f909c580ffa5c008a7d22a1287285d68b7825a2b6b51949ae',
            )

    def build(self):
        nmake_debug = 'DEBUG=2' if self.builder.opts.configuration == 'debug' else 'DEBUG=0'
        self.exec_vs(r'nmake /f Makefile.msc sqlite3.dll DYNAMIC_SHELL=1 ' + nmake_debug)

        self.install('sqlite3.h include')
        self.install('sqlite3ext.h include')
        self.install('sqlite3.dll sqlite3.pdb bin')
        self.install('sqlite3.lib lib')

@project_add
class Project_win_iconv(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'win-iconv',
            archive_url = 'https://github.com/win-iconv/win-iconv/archive/v0.0.8.tar.gz',
            archive_file_name = 'win-iconv-0.0.8.tar.gz',
            hash = '23adea990a8303c6e69e32a64a30171efcb1b73824a1c2da1bbf576b0ae7c520',
            dependencies = ['cmake', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True, cmake_params='-DBUILD_TEST=1', make_tests=True)

        self.install(r'.\COPYING share\doc\win-iconv')

@project_add
class Project_wing(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'wing',
            archive_url = 'https://gitlab.gnome.org/GNOME/wing/-/archive/v0.3.6/wing-v0.3.6.tar.gz',
            hash = 'f2c9bde1292b45027c188b49f8a65d49161f50da5d28b2a8c5eeb12159e59aaf',
            dependencies = ['ninja', 'meson', 'pkg-config', 'glib'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\COPYING share\doc\wing')

@project_add
class Project_x264(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'x264',
            repo_url = 'http://git.videolan.org/git/x264.git',
            fetch_submodules = False,
            dependencies = [ 'nasm', 'msys2' ],
            tag = 'e9a5903edf8ca59ef20e6f4894c196f135af735e',
            patches = [ '0001-use-more-recent-version-of-config.guess.patch',
                        '0002-configure-recognize-the-msys-shell.patch' ]
            )

    def build(self):
        msys_path = Project.get_tool_path('msys2')
        self.exec_vs(r'%s\bash build\build.sh %s %s' % (msys_path, convert_to_msys(self.builder.gtk_dir), self.builder.opts.configuration),
                     add_path=msys_path)

        # use the path expected when building with a dependent project
        self.builder.exec_msys(['mv', 'libx264.dll.lib', 'libx264.lib'], working_dir=os.path.join(self.builder.gtk_dir, 'lib'))

        self.install(r'.\COPYING share\doc\x264')

@project_add
class Project_zlib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'zlib',
            archive_url = 'http://www.zlib.net/zlib-1.2.11.tar.xz',
            hash = '4ff941449631ace0d4d203e3483be9dbc9da454084111f97ea0a2114e19bf066',
            )

    def build(self):
        options = ''
        if self.builder.opts.configuration == 'debug':
            options = 'CFLAGS="-nologo -MDd -W3 -Od -Zi -Fd\\"zlib\\""'

        self.exec_vs(r'nmake /nologo /f win32\Makefile.msc STATICLIB=zlib-static.lib IMPLIB=zlib1.lib ' + options)

        self.install(r'.\zlib.h .\zconf.h include')
        self.install(r'.\zlib1.dll .\zlib1.pdb bin')
        self.install(r'.\zlib1.lib lib')

        self.install_pc_files()
        self.install(r'.\README share\doc\zlib')

@project_add
class Project_check_libs(NullExpander, Meson):
    def __init__(self):
        Project.__init__(self,
            'check-libs',
            dependencies = [
                    # Used to build the various tests
                    'meson',
                    'ninja',
                    'pkg-config',
                    # libraries to test, hopefully all the one we build!
                    'atk',
                    'cairo',
                    'freetype',
                    'gdk-pixbuf',
                    'glib',
                    'jasper',
                    'json-glib',
                    'libarchive',
                    'libcurl',
                    'libffi',
                    'libjpeg-turbo',
                    'libpng',
                    'libtiff-4',
                    'libxml2',
                    'libyuv',
                    'pango',
                    'zlib',

                ],
            version = '0.1.0',
            )

    def build(self):
        Meson.build(self, make_tests=True)
        self.install(r'.\COPYING share\doc\check-libs')


@project_add
class Project_lgi(GitRepo, Project):
    def __init__(self):
        GitRepo.__init__(self)
        Project.__init__(self,
            'lgi',
            repo_url='https://github.com/pavouk/lgi.git',
            fetch_submodules=False,
            tag='2dd5db9678913ba08e54931b59cd97e550c7459e',
            dependencies=['luajit', 'gobject-introspection'],
            patches=['fix-loading-non-libtool-style-libs.patch'],
        )

    def build(self):
        self.push_location('lgi')

        self.exec_vs(r'nmake -f .\Makefile-msvc.mak corelgilua51.dll version.lua PREFIX="%(gtk_dir)s')

        self.install(r'corelgilua51.dll lib\lua\lgi')
        self.install(r'.\*.lua share\lua\lgi')
        self.install(r'.\override\*.lua share\lua\lgi\override')

        self.pop_location()

        self.install(r'LICENSE share\doc\lgi')
        self.install(r'lgi.lua share\lua')


@project_add
class Project_dev_shell(Project):
    def __init__(self):
        Project.__init__(self,
            'dev-shell',
            # We may need all tools
            dependencies = [ 'tools' ],
            version = '0.1.0',
            # We don't want this project to be built with the group 'all'
            type = GVSBUILD_IGNORE,
            )
        self.meson = True

    def unpack(self):
        # Nothing to do, it's not really a project
        pass

    def finalize_dep(self, builder, deps):
        if builder.opts.skip:
            skip = builder.opts.skip.split(',')
            for s in skip:
                p = Project.get_project(s)
                if p in deps:
                    log.log('dev-shell: skip %s' % (s, ))
                    deps.remove(p)
                    if s =='meson' or s == 'python':
                        # We disable the meson management
                        self.meson = False

    def build(self):
        # Do the shell
        print("")
        print("gvsbuild dev shell. Type exit to exit :)")
        print("")
        print("The environment var GTK_BASE_DIR points to the gtk installation dir")
        print("(%s)" % (self.builder.gtk_dir, ))
        print("if you need it e.g. as a --prefix option")
        print("")
        if self.meson:
            # Add a _meson env to use it directly
            meson_path = Project.get_tool_path('meson')
            self.builder.mod_env('_MESON', 'python %s\\meson.py' % (meson_path, ))
            print("If you need to use meson you can use the _MESON environment, e.g.")
            print("%_MESON% configure")
            print("")

        # If you need to use it as a --prefix in some build test ...
        self.builder.mod_env('GTK_BASE_DIR', self.builder.gtk_dir)
        self.builder.mod_env('PROMPT', '[ gvsbuild shell ] $P $G', subst=True)
        self.builder.exec_vs("cmd", working_dir=self.builder.working_dir)

@project_add
class Project_boringssl(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'boringssl',
            repo_url='https://github.com/google/boringssl.git',
            fetch_submodules=False,
            tag='067cfd92f4d7da0edfa073b096d090b98a83b860', #commit from master-with-bazel branch
            dependencies=['cmake', 'go', 'perl', 'nasm', 'ninja'],
        )

    def build(self):
        # If do_install is True, the build fails
        CmakeProject.build(self, use_ninja=True, do_install=False)

        self.install(r'.\_gvsbuild-cmake\ssl.lib lib')
        self.install(r'.\_gvsbuild-cmake\crypto.lib lib')
        self.install(r'.\LICENSE share\doc\boringssl')
        self.install(r'.\src\include\openssl\* include\boringssl\openssl')
