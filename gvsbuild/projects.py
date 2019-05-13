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
from .utils.base_expanders import Tarball, GitRepo
from .utils.base_expanders import NullExpander
from .utils.base_project import Project, project_add
from .utils.base_project import GVSBUILD_IGNORE
from .utils.base_builders import Meson, MercurialCmakeProject, CmakeProject

@project_add
class Project_adwaita_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'adwaita-icon-theme',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/adwaita-icon-theme/3.32/adwaita-icon-theme-3.32.0.tar.xz',
            hash = '698db6e407bb987baec736c6a30216dfc0317e3ca2403c7adf3a5aa46c193286',
            dependencies = ['librsvg', 'python', ],
            )

    def build(self):
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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.32/atk-2.32.0.tar.xz',
            hash = 'cb41feda7fe4ef0daa024471438ea0219592baf7c291347e5a858bb64e4091cc',
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

        self.install(r'.\pc-files\* lib\pkgconfig')

        self.install(r'.\COPYING share\doc\cairo')

@project_add
class Project_clutter(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'clutter',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/clutter/1.26/clutter-1.26.2.tar.xz',
            hash = 'e7233314983055e9018f94f56882e29e7fc34d8d35de030789fdcd9b2d0e2e56',
            dependencies = ['atk','cogl','json-glib'],
            )

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'clutter.sln')

        self.install(r'.\COPYING share\doc\clutter')

@project_add
class Project_cogl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cogl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/cogl/1.22/cogl-1.22.2.tar.xz',
            hash = '39a718cdb64ea45225a7e94f88dddec1869ab37a21b339ad058a9d898782c00d',
            dependencies = ['python', 'glib','cairo','pango','gdk-pixbuf'],
            patches = ['001-cogl-missing-symbols.patch',
                       '002-cogl-pango-missing-symbols.patch'],
            )

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'cogl.sln')

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
                       '0002-Provide-a-compile-option-for-32-64-gssapi.patch'],
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
            archive_url = 'https://www.ffmpeg.org/releases/ffmpeg-4.1.3.tar.xz',
            hash = '0c3020452880581a8face91595b239198078645e7d7184273b8bcc7758beb63d',
            dependencies = [ 'yasm', 'msys2', ],
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
                    # For now is the same as the vs2017 ...
                    fixme = r'141'
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

        self.install(r'.\fontconfig.pc lib\pkgconfig')
        self.install(r'.\COPYING share\doc\fontconfig')

@project_add
class Project_freetype(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'freetype',
            archive_url = 'http://git.savannah.gnu.org/cgit/freetype/freetype2.git/snapshot/freetype2-098dd70cb1845b8c325ef4801c5f2e09e476b1ed.tar.gz',
            hash = 'c891891164a716acbcf7137585c2ef1bc27599d2815b3c099a31d6a5a2e67a72',
            dependencies = ['pkg-config', 'ninja', 'libpng'],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DWITH_ZLIB=ON -DWITH_PNG=ON -DDISABLE_FORCE_DEBUG_POSTFIX=ON -DBUILD_SHARED_LIBS=ON', use_ninja=True)
        self.install(r'.\pc-files\* lib\pkgconfig')
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
class Project_gdk_pixbuf(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'gdk-pixbuf',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.38/gdk-pixbuf-2.38.1.tar.xz',
            hash = 'f19ff836ba991031610dcc53774e8ca436160f7d981867c8c3a37acfe493ab3a',
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
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'true'
        else:
            enable_gi = 'false'

        self.add_param('-Djasper=true')
        self.add_param('-Dnative_windows_loaders=true')
        self.add_param('-Dgir=%s' % (enable_gi, ))
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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.60/glib-2.60.1.tar.xz',
            hash = '89f884f5d5c6126140ec868cef184c42ce72902c13cd08f36e660371779b5560',
            dependencies = ['ninja', 'meson', 'pkg-config', 'gettext', 'libffi', 'zlib'],
            patches = ['glib-package-installation-directory.patch'],
            )

    def build(self):
        Meson.build(self, meson_params='-Dinternal_pcre=true')
        self.install(r'.\COPYING share\doc\glib')

@project_add
class Project_glib_networking(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib-networking',
            archive_url = 'https://github.com/wingtk/glib-networking/releases/download/2.50.0-openssl/glib-networking-2.50.0.tar.xz',
            hash = 'ca116a5b9435001d0dd8cfab3743f9a5d0003dbdc99a407c66858b183f07192b',
            dependencies = ['gsettings-desktop-schemas', 'openssl'],
            )

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'glib-networking.sln')
        self.install(r'.\COPYING share\doc\glib-networking')

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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gobject-introspection/1.60/gobject-introspection-1.60.0.tar.xz',
            hash = '9efe4090cb59717126701e97062e784773f800b8d47af14c4d278ebf194df35d',
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

        Meson.build(self, meson_params='-Dpython=%s\\python.exe -Dcairo-libname=cairo-gobject.dll' % (py_dir, ))

@project_add
class Project_graphene(GitRepo, Meson):
    def __init__(self):
        Meson.__init__(self,
            'graphene',
            repo_url = 'https://github.com/ebassi/graphene',
            fetch_submodules = False,
            tag = None,
            dependencies = ['ninja', 'meson', 'pkg-config', 'glib'],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'true'
        else:
            enable_gi = 'false'

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
            dependencies = ['go', 'nuget', 'protobuf', 'perl', 'zlib', 'yasm'],
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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gsettings-desktop-schemas/3.32/gsettings-desktop-schemas-3.32.0.tar.xz',
            hash = '2d59b4b3a548859dfae46314ee4666787a00d5c82db382e97df7aa9d0e310a35',
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
        self.exec_msbuild_gen(r'build\win32', 'gtk+.sln')

        self.make_all_mo()

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))
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
class Project_gtk3_24(Project_gtk_base):
    def __init__(self):
        if self.opts.gtk3_ver != '3.24':
            self.ignore()
            return

        Project.__init__(self,
            'gtk3',
            prj_dir='gtk3-24',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.24/gtk+-3.24.7.tar.xz',
            hash = '52121144a2df4babed75eb5f34de130a46420101fde3ae216d3142df8a481520',
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
            self.make_single_gir('gtk', prj_dir='gtk3-24')

        self.exec_cmd(r'%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas')
        self.exec_cmd(r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"')

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
        self.exec_msbuild_gen(r'build\win32', 'gtksourceview.sln')

        self.install(r'.\COPYING share\doc\gtksourceview3')

    def post_install(self):
        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\gtk-3.0' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))
            self.make_single_gir('gtksourceview', prj_dir='gtksourceview3')

@project_add
class Project_harfbuzz(Tarball, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'harfbuzz',
            archive_url = 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-2.3.0.tar.bz2',
            hash = '3b314db655a41d19481e18312465fa25fca6f63382217f08062f126059f96764',
            dependencies = ['python', 'freetype', 'pkg-config', 'glib'],
            )

    def build(self):
        CmakeProject.build(self, cmake_params='-DHB_HAVE_FREETYPE=ON -DHB_HAVE_GLIB=ON -DHB_HAVE_GOBJECT=ON', use_ninja=True)

        self.install(r'.\pc-files\* lib\pkgconfig')
        self.install(r'.\COPYING share\doc\harfbuzz')

@project_add
class Project_hicolor_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'hicolor-icon-theme',
            archive_url = 'http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.15.tar.xz',
            hash = '9cc45ac3318c31212ea2d8cb99e64020732393ee7630fa6c1810af5f987033cc',
            )

    def build(self):
        self.install(r'.\index.theme share\icons\hicolor')

@project_add
class Project_icu(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'icu',
            archive_url = 'http://download.icu-project.org/files/icu4c/63.1/icu4c-63_1-src.zip',
            hash = '3d957deabf75e96c35918355eac4da3e728fc222b9b4bdb2663652f76ee51772',
            version='63.1',
            )

    def build(self):
        bindir = r'.\bin'
        libdir = r'.\lib'
        if not self.builder.x86:
            bindir += '64'
            libdir += '64'

        self.exec_msbuild(r'source\allinone\allinone.sln /t:cal')

        if self.builder.opts.configuration == 'debug':
            self.install(r'.\pc-files-debug\* lib\pkgconfig')
        else:
            self.install(r'.\pc-files\* lib\pkgconfig')

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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/json-glib/1.4/json-glib-1.4.4.tar.xz',
            hash = '720c5f4379513dc11fd97dc75336eb0c0d3338c53128044d9fabec4374f4bc47',
            dependencies = ['meson', 'ninja', 'pkg-config', 'python', 'glib'],
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
            archive_url = 'https://libarchive.org/downloads/libarchive-3.3.3.tar.gz',
            hash = 'ba7eb1781c9fbbae178c4c6bad1c6eb08edab9a1496c64833d1715d022b30e2e',
            dependencies = ['cmake', 'ninja', 'win-iconv', 'zlib', 'lz4', 'openssl', 'libxml2'],
            patches = ['0001-Do-not-try-to-compile-with-warnings-as-errors-on-deb.patch'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)
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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libcroco/0.6/libcroco-0.6.11.tar.xz',
            hash = '132b528a948586b0dfa05d7e9e059901bca5a3be675b6071a90a90b81ae5a056',
            dependencies = ['glib', 'libxml2'],
            )

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'libcroco.sln')
        self.install(r'.\COPYING share\doc\libcroco')

@project_add
class Project_libepoxy(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libepoxy',
            archive_url = 'https://github.com/anholt/libepoxy/releases/download/1.5.3/libepoxy-1.5.3.tar.xz',
            hash = '002958c5528321edd53440235d3c44e71b5b1e09b9177e8daf677450b6c4433d',
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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libgxps/0.3/libgxps-0.3.1.tar.xz',
            hash = '1a939fc8fcea9471b7eca46b1ac90cff89a30d26f65c7c9a375a4bf91223fa94',
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
            archive_url = 'https://sourceforge.net/projects/libjpeg-turbo/files/2.0.2/libjpeg-turbo-2.0.2.tar.gz',
            hash = 'acb8599fe5399af114287ee5907aea4456f8f2c1cc96d26c28aebfdf5ee82fed',
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
            archive_url = 'http://prdownloads.sourceforge.net/libpng/libpng-1.6.36.tar.xz',
            hash = 'eceb924c1fa6b79172fdfd008d335f0e59172a86a66481e09d4089df872aa319',
            dependencies = ['cmake', 'ninja', 'zlib'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\pc-files\* lib\pkgconfig')
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
class Project_librsvg(Tarball, Project, _MakeGir):
    def __init__(self):
        Project.__init__(self,
            'librsvg',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.40/librsvg-2.40.20.tar.xz',
            hash = 'cff4dd3c3b78bfe99d8fcfad3b8ba1eee3289a0823c0e118d78106be6b84c92b',
            dependencies = ['libcroco', 'cairo', 'pango', 'gdk-pixbuf', 'gtk3'],
            )
        if Project.opts.enable_gi:
            self.add_dependency('gobject-introspection')

    def build(self):
        self.exec_msbuild_gen(r'build\win32', 'librsvg.sln')

        if Project.opts.enable_gi:
            self.builder.mod_env('INCLUDE', '%s\\include\\glib-2.0' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\lib\\glib-2.0\include' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\include\\gdk-pixbuf-2.0' % (self.builder.gtk_dir, ))
            self.builder.mod_env('INCLUDE', '%s\\include\\cairo' % (self.builder.gtk_dir, ))

            self.make_single_gir('rsvg', prj_dir='librsvg')

        self.install(r'.\COPYING share\doc\librsvg')

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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libsoup/2.66/libsoup-2.66.1.tar.xz',
            hash = '4a2cb6c1174540af13661636035992c2b179dfcb39f4d3fa7bee3c7e355c43ff',
            dependencies = ['libxml2', 'glib-openssl', 'sqlite', 'libpsl', 'mit-kerberos'],
            patches = ['fix-build.patch'],
            )

        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'true'
        else:
            enable_gi = 'false'

        self.add_param('-Dintrospection=%s' % (enable_gi, ))
        self.add_param('-Dvapi=false')

    def build(self):
        Meson.build(self)

        self.install(r'.\COPYING share\doc\libsoup')

@project_add
class Project_libssh(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libssh',
            archive_url = 'https://www.libssh.org/files/0.7/libssh-0.7.5.tar.xz',
            hash = '54e86dd5dc20e5367e58f3caab337ce37675f863f80df85b6b1614966a337095',
            dependencies = ['zlib','openssl'],
            )

    def build(self):
        self.exec_msbuild_gen(r'build', 'libssh-library.sln')

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
            archive_url = 'http://download.osgeo.org/libtiff/tiff-4.0.10.tar.gz',
            hash = '2c52d11ccaf767457db0c46795d9c7d1a8d8f76f68b0b800a3dfe45786b996e4',
            dependencies = ['cmake', 'ninja', 'libjpeg-turbo', ],
            patches = ['remove-postfix.patch'],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\COPYRIGHT share\doc\tiff')

@project_add
class Project_libuv(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libuv',
            archive_url = 'https://github.com/libuv/libuv/archive/v1.11.0.tar.gz',
            archive_file_name = 'libuv-1.11.0.tar.gz',
            hash = '6ec7eec6ecc24b1a8ffedebedb2fe9313fffb5410de89aaf784dd01080411c7a',
            )

    def build(self):
        rel_dir = r'Release'
        if self.builder.opts.configuration == 'debug':
            rel_dir = r'Debug'

        platform = r'x86'
        if self.builder.x64:
            platform = r'x64'

        tmp_python = os.getenv('PYTHON')
        os.environ["PYTHON"] = 'c:\python27\python'
        os.system(r'%s\vcbuild.bat build static %s %s' % (self._get_working_dir(), self.builder.opts.configuration, platform))
        if tmp_python != None:
            os.environ["PYTHON"] = tmp_python

        self.install(r'include\pthread-barrier.h include\libuv')
        self.install(r'include\stdint-msvc2008.h include\libuv')
        self.install(r'include\tree.h include\libuv')
        self.install(r'include\uv.h include\libuv')
        self.install(r'include\uv-aix.h include\libuv')
        self.install(r'include\uv-bsd.h include\libuv')
        self.install(r'include\uv-darwin.h include\libuv')
        self.install(r'include\uv-errno.h include\libuv')
        self.install(r'include\uv-linux.h include\libuv')
        self.install(r'include\uv-sunos.h include\libuv')
        self.install(r'include\uv-threadpool.h include\libuv')
        self.install(r'include\uv-unix.h include\libuv')
        self.install(r'include\uv-version.h include\libuv')
        self.install(r'include\uv-win.h include\libuv')

        self.push_location(rel_dir)
        self.install(r'run-benchmarks' + '.exe' + ' bin')
        self.install(r'run-tests' + '.exe' + ' bin')
        self.install(r'lib\libuv' + '.lib' + ' lib')
        self.pop_location()

        self.install(r'.\LICENSE share\doc\libuv')

@project_add
class Project_libxml2(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libxml2',
            archive_url = 'http://xmlsoft.org/sources/libxml2-2.9.9.tar.gz',
            hash = '94fb70890143e3c6549f265cee93ec064c80a84c42ad0f23e85ee1fd6540a871',
            dependencies = ['win-iconv', 'meson', 'ninja'],
            )

    def build(self):
        Meson.build(self)
        self.install(r'.\pc-files\* lib\pkgconfig')
        self.install(r'.\COPYING share\doc\libxml2')

@project_add
class Project_libyuv(GitRepo, CmakeProject):
    def __init__(self):
        Project.__init__(self,
            'libyuv',
            repo_url = 'https://chromium.googlesource.com/libyuv/libyuv',
            fetch_submodules = False,
            tag = None,
            dependencies = ['cmake', 'ninja', 'libjpeg-turbo', ],
            patches = [
                '001-win-build.patch',
                ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True)

        self.install(r'.\pc-files\* lib\pkgconfig')
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
            tag = 'meson',
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
            archive_url = 'https://github.com/lz4/lz4/archive/v1.8.3.tar.gz',
            archive_file_name = 'lz4-1.8.3.tar.gz',
            hash = '33af5936ac06536805f9745e0b6d61da606a1f8b4cc5c04dd3cbaca3b9b4fc43',
            )

    def build(self):
        self.exec_msbuild_gen(r'visual', 'lz4.sln')

        self.install(r'visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.dll visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.pdb bin')
        self.install(r'.\lib\lz4.h .\lib\lz4hc.h .\lib\lz4frame.h include')
        self.install(r'visual\%(vs_ver_year)s\bin\%(platform)s_%(configuration)s\liblz4.lib lib')

        self.install(r'.\lib\LICENSE share\doc\lz4')

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
class Project_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'openssl',
            archive_url = 'https://www.openssl.org/source/openssl-1.0.2r.tar.gz',
            hash = 'ae51d08bba8a83958e894946f15303ff894d75c2b8bbd44a852b64e3fe11d0d6',
            dependencies = ['perl', 'nasm', 'msys2', ],
            )

    def build(self):
        common_options = r'no-ssl2 no-ssl3 no-comp --openssldir=./'

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
            self.exec_vs(r'ms\do_nasm', add_path=add_path)
        else:
            self.exec_vs(r'%(perl_dir)s\bin\perl.exe Configure ' + debug_option + 'VC-WIN64A ' + common_options)
            self.exec_vs(r'ms\do_win64a', add_path=add_path)

        try:
            self.exec_vs(r'nmake /nologo -f ms\ntdll.mak vclean', add_path=add_path)
        except:
            pass

        self.exec_vs(r'nmake /nologo -f ms\ntdll.mak', add_path=add_path)
        self.exec_vs(r'nmake /nologo -f ms\ntdll.mak test', add_path=add_path)
        self.exec_vs(r'%(perl_dir)s\bin\perl.exe mk-ca-bundle.pl -n cert.pem')
        self.exec_vs(r'nmake /nologo -f ms\ntdll.mak install', add_path=add_path)

        self.install(r'.\bin\* .\cert.pem bin')
        self.install(r'.\LICENSE share\doc\openssl')
        self.install(r'.\pc-files\* lib\pkgconfig')
        self.install(r'include\* include')

        self.install(r'lib\* lib')

        self.push_location(r'.\out32dll')
        self.install('libeay32.pdb openssl.pdb ssleay32.pdb bin')
        self.install(r'''.\out32dll\4758cca.pdb .\out32dll\aep.pdb .\out32dll\atalla.pdb .\out32dll\capi.pdb
                         .\out32dll\chil.pdb lib\engines .\out32dll\cswift.pdb .\out32dll\gmp.pdb
                         .\out32dll\gost.pdb .\out32dll\nuron.pdb .\out32dll\padlock.pdb .\out32dll\sureware.pdb
                     .\out32dll\ubsec.pdb lib\engines''')
        self.pop_location()

@project_add
class Project_opus(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'opus',
            archive_url = 'https://archive.mozilla.org/pub/opus/opus-1.3.tar.gz',
            hash = '4f3d69aefdf2dbaf9825408e452a8a414ffc60494c70633560700398820dc550',
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

        self.install(r'COPYING share\doc\opus')

@project_add
class Project_pango(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'pango',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.42/pango-1.42.4.tar.xz',
            hash = '1d2b74cd63e8bd41961f2f8d952355aa0f9be6002b52c8aa7699d9f5da597c9d',
            dependencies = [
                'ninja',
                'meson',
                'cairo',
                'harfbuzz',
                'fribidi',
            ],
            patches = [
                '001-ignore-help2man.patch',
            ],
            )
        if self.opts.enable_gi:
            self.add_dependency('gobject-introspection')
            enable_gi = 'true'
        else:
            enable_gi = 'false'

        self.add_param('-Dgir=%s' % (enable_gi, ))

    def build(self):
        Meson.build(self)
        self.install(r'COPYING share\doc\pango')

@project_add
class Project_pixman(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pixman',
            archive_url = 'http://cairographics.org/releases/pixman-0.38.0.tar.gz',
            hash = 'a7592bef0156d7c27545487a52245669b00cf7e70054505381cff2136d890ca8',
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
            archive_url = 'https://github.com/google/protobuf/releases/download/v3.5.1/protobuf-cpp-3.5.1.tar.gz',
            hash = 'c28dba8782da2cfea1e11c61d335958c31a9c1bc553063546af9cbe98f204092',
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
            archive_url = 'https://github.com/protobuf-c/protobuf-c/releases/download/v1.3.1/protobuf-c-1.3.1.tar.gz',
            hash = '51472d3a191d6d7b425e32b612e477c06f73fe23e07f6a6a839b11808e9d2267',
            dependencies = ['cmake', 'protobuf', 'ninja', ],
            )

    def build(self):
        CmakeProject.build(self, use_ninja=True, source_part='build-cmake')

        self.install(r'.\LICENSE share\doc\protobuf-c')

@project_add
class Project_pycairo(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pycairo',
            archive_url = 'https://github.com/pygobject/pycairo/releases/download/v1.18.0/pycairo-1.18.0.tar.gz',
            hash = 'abd42a4c9c2069febb4c38fe74bfc4b4a9d3a89fea3bc2e4ba7baff7a20f783f',
            dependencies = ['cairo', 'python'],
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
        self.pop_location()

@project_add
class Project_pygobject(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pygobject',
            archive_url = 'https://ftp.acc.umu.se/pub/GNOME/sources/pygobject/3.32/pygobject-3.32.0.tar.xz',
            hash = '83f4d7e59fde6bc6b0d39c5e5208574802f759bc525a4cb8e7265dfcba45ef29',
            dependencies = ['python', 'pycairo', 'gobject-introspection', 'libffi'],
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
        self.pop_location()

@project_add
class Project_sqlite(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'sqlite',
            archive_url = 'https://www.sqlite.org/2016/sqlite-autoconf-3120200.tar.gz',
            hash = 'fd00770c9afd39db555c78400e52f55e8bd6568c78be23561abb472a22d09abb',
            )

    def build(self):
        nmake_debug = 'DEBUG=2' if self.builder.opts.configuration == 'debug' else 'DEBUG=0'
        self.exec_vs(r'nmake /f Makefile.msc sqlite3.dll DYNAMIC_SHELL=1 ' + nmake_debug)

        self.install('sqlite3.h include')
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
            archive_url = 'https://gitlab.gnome.org/GNOME/wing/repository/v0.1.6/archive.tar.gz',
            archive_file_name = 'wing-0.1.6.tar.gz',
            hash = '0106552c9f0cf5662fefaef978e17bbdadebe350f8c092fdbc28a121f6d9cec1',
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

        self.install(r'.\pc-files\* lib\pkgconfig')
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
