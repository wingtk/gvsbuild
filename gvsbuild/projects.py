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

from .utils.simple_ui import print_debug
from .utils.utils import convert_to_msys
from .utils.base_expanders import Tarball, GitRepo
from .utils.base_project import Project, project_add
from .utils.base_builders import Meson, MercurialCmakeProject

@project_add
class Project_adwaita_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'adwaita-icon-theme',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/adwaita-icon-theme/3.24/adwaita-icon-theme-3.24.0.tar.xz',
            hash = 'ccf79ff3bd340254737ce4d28b87f0ccee4b3358cd3cd5cd11dc7b42f41b272a',
            dependencies = ['librsvg'],
            )

    def build(self):
        self.push_location(r'.\win32')
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.pop_location()

        self.install(r'.\COPYING_CCBYSA3 share\doc\adwaita-icon-theme')

@project_add
class Project_atk(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'atk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.24/atk-2.24.0.tar.xz',
            hash = 'bb2daa9a808c73a7a79d2983f333e0ba74be42fc51e3ba1faf2551a636487a49',
            dependencies = ['glib'],
            )

    def build(self):
        self.exec_msbuild(r'win32\vs%(vs_ver)s\atk.sln')
        self.install(r'.\COPYING share\doc\atk')

@project_add
class Project_cairo(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cairo',
            archive_url = 'http://cairographics.org/snapshots/cairo-1.15.2.tar.xz',
            hash = '268cc265a7f807403582f440643064bf52896556766890c8df7bad02d230f6c9',
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
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\clutter.sln')

        self.install(r'.\COPYING share\doc\clutter')

@project_add
class Project_cogl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cogl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/cogl/1.22/cogl-1.22.2.tar.xz',
            hash = '39a718cdb64ea45225a7e94f88dddec1869ab37a21b339ad058a9d898782c00d',
            dependencies = ['glib','cairo','pango','gdk-pixbuf'],
            patches = ['001-cogl-missing-symbols.patch',
                       '002-cogl-pango-missing-symbols.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\cogl.sln')

        self.install(r'.\COPYING share\doc\cogl')

@project_add
class Project_cyrus_sasl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cyrus-sasl',
            hash = '9e8035c12d419209ea60584d5efa51d042c3ed44b450b9d173d5504b222df9f1',
            archive_url = 'https://github.com/wingtk/cyrus-sasl/releases/download/cyrus-sasl-lmdb-2.1.28/cyrus-sasl-2.1.28.tar.xz',
            dependencies = ['lmdb', 'openssl'],
            )

    def build(self):
        configuration = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        self.exec_vs(r'nmake /nologo /f NTMakefile SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s" CFG=' + configuration)
        self.exec_vs(r'nmake /nologo /f NTMakefile install SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" ' +
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
            )

    def build(self):
        Meson.build(self, meson_params='-Denable-introspection=false -Denable-gtk-doc=false')
        self.install(r'.\COPYING.txt share\doc\emeus')

@project_add
class Project_enchant(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'enchant',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/enchant-1.6.0.tar.gz',
            hash = '2fac9e7be7e9424b2c5570d8affe568db39f7572c10ed48d4e13cddf03f7097f',
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
            archive_url = 'http://ffmpeg.org/releases/ffmpeg-3.3.tar.xz',
            hash = '599e7f7c017221c22011c4037b88bdcd1c47cd40c1e466838bc3c465f3e9569d',
            dependencies = [ 'yasm', 'x264' ],
            patches = [ '0001-lavc-mpegvideo_enc-allow-low_delay-for-non-MPEG2-cod.patch' ]
        )

    def build(self):
        self.exec_vs(r'bash build\build.sh %s %s %s' % (self.pkg_dir, self.builder.gtk_dir, self.builder.opts.configuration),
                     add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))

        self.install(r'.\COPYING.LGPLv2.1 ' \
                     r'.\COPYING.LGPLv3 ' \
                     r'.\COPYING.GPLv2 ' \
                     r'share\doc\ffmpeg')

    def post_install(self):
        self.builder.exec_msys(['mv', 'avcodec.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'avutil.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'postproc.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))
        self.builder.exec_msys(['mv', 'swscale.lib', '../lib/'], working_dir=os.path.join(self.builder.gtk_dir, 'bin'))

@project_add
class Project_fontconfig(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'fontconfig',
            archive_url = 'https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.1.tar.gz',
            hash = 'a9f42d03949f948a3a4f762287dbc16e53a927c91a07ee64207ebd90a9e5e292',
            dependencies = ['freetype', 'libxml2'],
            patches = ['fontconfig.patch'],
            )

    def build(self):
        #make the fontconfig files work on other compatible vs versions
        for proj in glob.glob(r'%s\*.vcxproj' % (self.build_dir,)):
            with open(proj, 'r') as f:
                content = f.read()
            if content.find('<PlatformToolset>FIXME</PlatformToolset>') >= 0:
                print_debug('patching project file %s' % (proj,))
                content = content.replace('<PlatformToolset>FIXME</PlatformToolset>', '<PlatformToolset>v%s0</PlatformToolset>' % (self.builder.opts.vs_ver))
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

        self.install(r'.\COPYING share\doc\fontconfig')

@project_add
class Project_freetype(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'freetype',
            archive_url = 'http://download.savannah.gnu.org/releases/freetype/freetype-2.7.1.tar.gz',
            hash = '162ef25aa64480b1189cdb261228e6c5c44f212aac4b4621e28cf2157efb59f5',
            )

    def build(self):
        self.exec_msbuild(r'builds\windows\vc%(vs_ver)s\freetype.vcxproj')
        self.install_dir(r'.\include')
        self.install(r'.\objs\%(platform)s\freetype.lib lib')
        self.install(r'.\docs\LICENSE.TXT share\doc\freetype')

@project_add
class Project_gdk_pixbuf(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gdk-pixbuf',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.36/gdk-pixbuf-2.36.7.tar.xz',
            hash = '1b6e5eef09d98f05f383014ecd3503e25dfb03d7e5b5f5904e5a65b049a6a4d8',
            dependencies = ['glib', 'libpng'],
            )

    def build(self):
        configuration = 'Release_GDI+'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_GDI+'

        self.exec_msbuild(r'win32\vs%(vs_ver)s\gdk-pixbuf.sln', configuration=configuration)
        self.install(r'.\COPYING share\doc\gdk-pixbuf')

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
                       '0005-gettext-runtime-intl-printf-parse.c-Fix-build-on-Vis.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gettext.sln')

        self.install(r'.\gettext-tools\its\*.its share\gettext\its')
        self.install(r'.\gettext-tools\its\*.loc share\gettext\its')
        self.install(r'.\COPYING share\doc\gettext')

@project_add
class Project_glib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.52/glib-2.52.2.tar.xz',
            hash = 'f00e5d9e2a2948b1da25fcba734a6b7a40f556de8bc9f528a53f6569969ac5d0',
            dependencies = ['gettext', 'libffi', 'zlib'],
            patches = ['glib-if_nametoindex.patch',
                       'glib-package-installation-directory.patch',
                       'glib-mkenums_perl_path.patch'],
            )

    def build(self):
        configuration = 'Release_BundledPCRE'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_BundledPCRE'

        self.exec_msbuild(r'win32\vs%(vs_ver)s\glib.sln', configuration=configuration)
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
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\glib-networking.sln')
        self.install(r'.\COPYING share\doc\glib-networking')

@project_add
class Project_glib_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib-openssl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib-openssl/2.50/glib-openssl-2.50.2.tar.xz',
            hash = '1a381fce3a932f66ff3d6acab40b6153f8fe4db7371834fae182aec7cc8b62ae',
            dependencies = ['glib', 'openssl'],
            )

    def build(self):
        self.exec_msbuild(r'win32\vs%(vs_ver)s\glib-openssl.sln')
        self.install(r'.\COPYING share\doc\glib-openssl')
        self.install(r'.\LICENSE_EXCEPTION share\doc\glib-openssl')

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

    def build(self):
        Meson.build(self)
        self.install(r'.\LICENSE share\doc\graphene')

@project_add
class Project_grpc(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'grpc',
            repo_url = 'https://github.com/grpc/grpc.git',
            fetch_submodules = True,
            tag = 'v1.0.0',
            dependencies = ['nuget', 'protobuf'],
            patches = ['0001-Remove-RuntimeLibrary-setting-from-the-projects.patch'],
            )

    def build(self):
        self.exec_cmd(self.builder.nuget + ' restore ' + os.path.join(self.build_dir, 'vsprojects', 'grpc.sln'))
        self.exec_msbuild(r'vsprojects\grpc.sln /t:grpc++')
        self.exec_msbuild(r'vsprojects\grpc_protoc_plugins.sln')

        self.install(r'.\include\grpc include\google')
        self.install(r'.\include\grpc++ include\google')

        platform = ''
        if self.builder.x64:
            platform = 'x64\\'

        bin_dir = r'.\vsprojects\%s%s' % (platform, self.builder.opts.configuration, )

        self.install(bin_dir + r'\gpr.lib lib')
        self.install(bin_dir + r'\grpc.lib lib')
        self.install(bin_dir + r'\grpc++.lib lib')

        self.install(bin_dir + r'\grpc_cpp_plugin.exe bin')
        self.install(bin_dir + r'\grpc_cpp_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_csharp_plugin.exe bin')
        self.install(bin_dir + r'\grpc_csharp_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_node_plugin.exe bin')
        self.install(bin_dir + r'\grpc_node_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_objective_c_plugin.exe bin')
        self.install(bin_dir + r'\grpc_objective_c_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_python_plugin.exe bin')
        self.install(bin_dir + r'\grpc_python_plugin.pdb bin')

        self.install(bin_dir + r'\grpc_ruby_plugin.exe bin')
        self.install(bin_dir + r'\grpc_ruby_plugin.pdb bin')

        self.install(r'.\LICENSE share\doc\grpc')

@project_add
class Project_gsettings_desktop_schemas(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gsettings-desktop-schemas',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gsettings-desktop-schemas/3.24/gsettings-desktop-schemas-3.24.0.tar.xz',
            hash = 'f6573a3f661d22ff8a001cc2421d8647717f1c0e697e342d03c6102f29bbbb90',
            dependencies = ['perl', 'glib'],
            patches = ['0001-build-win32-replace.py-Fix-replacing-items-in-files-.patch'],
            )

    def build(self):
        self.push_location(r'.\build\win32')
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s"')
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"')
        self.pop_location()

        self.install(r'.\COPYING share\doc\gsettings-desktop-schemas')

class Project_gtk_base(Tarball, Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
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
        Project_gtk_base.__init__(self,
            'gtk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/2.24/gtk+-2.24.31.tar.xz',
            hash = '68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658',
            dependencies = ['atk', 'gdk-pixbuf', 'pango'],
            patches = ['gtk-revert-scrolldc-commit.patch', 'gtk-bgimg.patch', 'gtk-accel.patch', 'gtk-multimonitor.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtk+.sln')

        super(Project_gtk, self).build()

@project_add
class Project_gtk3(Project_gtk_base):
    def __init__(self):
        Project_gtk_base.__init__(self,
            'gtk3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.22/gtk+-3.22.12.tar.xz',
            hash = '84fae0cefb6a11ee2b4e86b8ac42fe46a3d30b4ad16661d5fc51e8ae03e2a98c',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            patches = ['gtk3-clip-retry-if-opened-by-others.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtk+.sln /p:GtkPostInstall=rem')

        super(Project_gtk3, self).build()

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas')
        self.exec_cmd(r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"')

@project_add
class Project_gtksourceview3(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gtksourceview3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtksourceview/3.22/gtksourceview-3.22.2.tar.xz',
            hash = '6ce84231dd0931cc747708434ca2f344c65a092dd6e1a800283fe0748773af5e',
            dependencies = ['perl', 'gtk3'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtksourceview.sln')

        self.install(r'.\COPYING share\doc\gtksourceview3')

@project_add
class Project_harfbuzz(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'harfbuzz',
            archive_url = 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.4.5.tar.bz2',
            hash = 'd0e05438165884f21658154c709075feaf98c93ee5c694b951533ac425a9a711',
            dependencies = ['perl', 'freetype', 'glib'],
            )

    def build(self):
        self.push_location(r'.\win32')
        self.builder.make_dir(os.path.join(self.build_dir, 'build', 'win32', self.builder.opts.configuration, 'win32'))
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.exec_vs(r'nmake /nologo /f Makefile.vc install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.pop_location()

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
class Project_jsonc(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'json-c',
            archive_url = 'https://github.com/json-c/json-c/archive/json-c-0.12.1-20160607.tar.gz',
            hash = '989e09b99ded277a0a651cd18b81fcb76885fea08769d7a21b6da39fb8a34816',
            patches = ['json-c-0.12.1-20160607.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\json-c.sln')

        self.install(r'.\COPYING share\doc\json-c')

@project_add
class Project_json_glib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'json-glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/json-glib/1.2/json-glib-1.2.8.tar.xz',
            hash = 'fd55a9037d39e7a10f0db64309f5f0265fa32ec962bf85066087b83a2807f40a',
            dependencies = ['glib'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\json-glib.sln')

        self.install(r'.\COPYING share\doc\json-glib')

@project_add
class Project_leveldb(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'leveldb',
            archive_url = 'https://github.com/google/leveldb/archive/v1.20.tar.gz',
            hash = 'f5abe8b5b209c2f36560b75f32ce61412f39a2922f7045ae764a2c23335b6664',
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\leveldb.sln')

        self.install(r'.\LICENSE share\doc\leveldb')

@project_add
class Project_libarchive(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libarchive',
            archive_url = 'https://libarchive.org/downloads/libarchive-3.3.1.tar.gz',
            hash = '29ca5bd1624ca5a007aa57e16080262ab4379dbf8797f5c52f7ea74a3b0424e7',
            dependencies = ['cmake', 'win-iconv', 'zlib', 'lz4', 'openssl', 'libxml2'],
            patches = ['0001-Do-not-try-to-compile-with-warnings-as-errors-on-deb.patch'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs(r'nmake /nologo')
        self.exec_vs(r'nmake /nologo install')

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
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\libcroco.sln')
        self.install(r'.\COPYING share\doc\libcroco')

@project_add
class Project_libepoxy(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'libepoxy',
            archive_url = 'https://github.com/anholt/libepoxy/archive/1.4.2.tar.gz',
            hash = '61613b2cdc0167917229aa308d6eab2473f0408f84f3ccbd77d8677b42e89e39',
            dependencies = ['python', 'ninja', 'meson'],
            )

    def build(self):
        Meson.build(self)

        self.install(r'COPYING share\doc\libepoxy')

@project_add
class Project_libffi(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libffi',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/libffi-3.2.1.tar.gz',
            hash = 'd06ebb8e1d9a22d19e38d63fdb83954253f39bedc5d46232a05645685722ca37',
            patches = ['libffi-msvc-complex.patch', 'libffi-win64-jmp.patch', '0001-Fix-build-on-windows.patch'],
            )

    def build(self):
        if self.builder.x86:
            build_dest = 'i686-pc-mingw32'
        else:
            build_dest = 'x86_64-w64-mingw32'

        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\libffi.sln')

        self.install(r'.\\' + build_dest + r'\include\ffi.h', r'.\src\x86\ffitarget.h', 'include')
        self.install(r'LICENSE share\doc\libffi')

@project_add
class Project_libgxps(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libgxps',
            archive_url = 'https://git.gnome.org/browse/libgxps/snapshot/libgxps-84e11c4f93829a762273b7cc362d6bc9a7582ed7.tar.xz',
            hash = '1618845a59f665acfc1eeccee893b3cf27ff52588f90b9ba2c678630aeca5cf8',
            dependencies = ['glib', 'libarchive', 'cairo', 'libpng', 'libjpeg-turbo'],
            )

    def build(self):
        self.push_location(r'.\nmake')
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s PREFIX="%(gtk_dir)s" LIBPNG=1 LIBJPEG=1 CAIRO_PDF=1 CAIRO_PS=1 CAIRO_SVG=1')
        self.exec_vs(r'nmake /nologo /f Makefile.vc install CFG=%(configuration)s PREFIX="%(gtk_dir)s" LIBPNG=1 LIBJPEG=1 CAIRO_PDF=1 CAIRO_PS=1 CAIRO_SVG=1')
        self.pop_location()

        self.install(r'.\COPYING share\doc\libgxps')

@project_add
class Project_libjpeg_turbo(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libjpeg-turbo',
            archive_url = 'https://sourceforge.net/projects/libjpeg-turbo/files/1.5.1/libjpeg-turbo-1.5.1.tar.gz',
            hash = '41429d3d253017433f66e3d472b8c7d998491d2f41caa7306b8d9a6f2a2c666c',
            dependencies = ['cmake', 'nasm', ],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        add_path = os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')

        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s', add_path=add_path)
        self.exec_vs(r'nmake /nologo', add_path=add_path)
        self.exec_vs(r'nmake /nologo install', add_path=add_path)

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

        version = '13'
        if self.builder.opts.vs_ver == '14':
            version = '15'

        self.exec_msbuild(r'w32\VS20' + version + '\libmicrohttpd.sln', configuration=configuration)

        debug_option = ''
        if self.builder.opts.configuration == 'debug':
            debug_option = r'_d'

        if self.builder.x86:
            rel_dir = r'.\w32\VS20' + version + r'\Output'
        else:
            rel_dir = r'.\w32\VS20' + version + r'\Output\x64'

        self.push_location(rel_dir)
        self.install(r'microhttpd.h include')
        self.install(r'libmicrohttpd-dll' + debug_option + '.lib' + ' lib')
        self.install(r'libmicrohttpd-dll' + debug_option + '.dll' + ' bin')
        self.install(r'libmicrohttpd-dll' + debug_option + '.pdb' + ' bin')
        self.install(r'hellobrowser-dll' + debug_option + '.exe' + ' bin')
        self.pop_location()



        self.install(r'.\COPYING share\doc\libmicrohttpd')

@project_add
class Project_libpng(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libpng',
            archive_url = 'http://prdownloads.sourceforge.net/libpng/libpng-1.6.29.tar.xz',
            hash = '4245b684e8fe829ebb76186327bb37ce5a639938b219882b53d64bd3cfc5f239',
            dependencies = ['cmake', 'zlib'],
            )

    def build(self):
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DZLIB_ROOT="%(gtk_dir)s" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s')
        self.exec_vs(r'nmake /nologo')
        self.exec_vs(r'nmake /nologo install')

        self.install('LICENSE share\doc\libpng')

@project_add
class Project_librsvg(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'librsvg',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.40/librsvg-2.40.16.tar.xz',
            hash = 'd48bcf6b03fa98f07df10332fb49d8c010786ddca6ab34cbba217684f533ff2e',
            dependencies = ['libcroco', 'cairo', 'pango', 'gdk-pixbuf', 'gtk3'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\librsvg.sln')
        self.install(r'.\COPYING share\doc\librsvg')

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\gdk-pixbuf-query-loaders.exe --update-cache')

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
class Project_libcurl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libcurl',
            archive_url = 'https://github.com/curl/curl/releases/download/curl-7_54_0/curl-7.54.0.tar.gz',
            hash = 'a84b635941c74e26cce69dd817489bec687eb1f230e7d1897fc5b5f108b59adf',
            dependencies = ['cmake'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DGTK_DIR="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs(r'nmake /nologo')
        self.exec_vs(r'nmake /nologo install')

        self.install(r'.\COPYING share\doc\libcurl')

@project_add
class Project_libsoup(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libsoup',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libsoup/2.58/libsoup-2.58.1.tar.xz',
            hash = '62c669f557de745b7b20ba9d5b74d839c95e4c9cea1a5ab7f3da5531a1aeefb9',
            dependencies = ['libxml2', 'glib-openssl', 'sqlite'],
            )

    def build(self):
        self.exec_msbuild(r'win32\vs%(vs_ver)s\libsoup.sln')

        self.install(r'.\COPYING share\doc\libsoup')

@project_add
class Project_libssh(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libssh',
            archive_url = 'https://red.libssh.org/attachments/download/218/libssh-0.7.5.tar.xz',
            hash = '54e86dd5dc20e5367e58f3caab337ce37675f863f80df85b6b1614966a337095',
            dependencies = ['zlib','openssl'],
            )

    def build(self):
        self.exec_msbuild(r'build\vs%(vs_ver)s\libssh-library.sln')

        self.install(r'.\COPYING share\doc\libssh')

@project_add
class Project_libssh2(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libssh2',
            archive_url = 'https://www.libssh2.org/download/libssh2-1.8.0.tar.gz',
            hash = '39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4',
            dependencies = ['cmake'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake -G"NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DGTK_DIR="%(pkg_dir)s" -DWITH_ZLIB=ON -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs(r'nmake /nologo')
        self.exec_vs(r'nmake /nologo install')

        self.install(r'.\COPYING share\doc\libssh2')

@project_add
class Project_libuv(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libuv',
            archive_url = 'https://github.com/libuv/libuv/archive/v1.11.0.tar.gz',
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
class Project_libxml2(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libxml2',
            archive_url = 'ftp://xmlsoft.org/libxml2/libxml2-2.9.4.tar.gz',
            hash = 'ffb911191e509b966deb55de705387f14156e1a56b21824357cdf0053233633c',
            dependencies = ['win-iconv'],
            )

    def build(self):
        shutil.copy(os.path.join(self._get_working_dir(), 'include', 'win32config.h'),
                    os.path.join(self._get_working_dir(), 'config.h'))

        lib = ';'.join([self.builder.vs_env['LIB'],
                        os.path.join(self.builder.gtk_dir, 'lib')])

        nmake_config = 'DEBUG=1' if self.builder.opts.configuration == 'debug' else 'DEBUG=0'
        self.push_location(r'.\win32')
        self.exec_vs(r'nmake /nologo /f Makefile.msvc WITH_ICONV=1 LIB="%s" PREFIX="%s" %s' % (lib, self.builder.gtk_dir, nmake_config))
        self.exec_vs(r'nmake /nologo /f Makefile.msvc install LIB="%s" PREFIX="%s" %s' % (lib, self.builder.gtk_dir, nmake_config))
        self.pop_location()

        self.install(r'.\COPYING share\doc\libxml2')

@project_add
class Project_libyuv(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'libyuv',
            repo_url = 'https://chromium.googlesource.com/libyuv/libyuv',
            fetch_submodules = False,
            tag = None,
            dependencies = ['cmake'],
            )

    def build(self):
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s')
        self.exec_vs(r'nmake /nologo')
        self.exec_vs(r'nmake /nologo install')

        self.install(r'.\LICENSE share\doc\libyuv')

@project_add
class Project_libzip(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libzip',
            archive_url = 'https://nih.at/libzip/libzip-1.2.0.tar.gz',
            hash = '6cf9840e427db96ebf3936665430bab204c9ebbd0120c326459077ed9c907d9f',
            dependencies = ['cmake', 'zlib'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DGTK_DIR="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs(r'nmake /nologo')
        self.exec_vs(r'nmake /nologo install')

        self.install(r'.\LICENSE share\doc\libzip')

@project_add
class Project_lmdb(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'lmdb',
            archive_url = 'https://github.com/LMDB/lmdb/archive/LMDB_0.9.19.tar.gz',
            hash = '108532fb94c6f227558d45be3f3347b52539f0f58290a7bb31ec06c462d05326',
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\lmdb.sln')

        self.install(r'.\libraries\liblmdb\lmdb.h include')
        self.install(r'.\build\win32\vs%(vs_ver)s\%(platform)s\%(configuration)s\lmdb.lib lib')
        self.install(r'.\libraries\liblmdb\LICENSE share\doc\lmdb')

@project_add
class Project_lz4(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'lz4',
            archive_url = 'https://github.com/lz4/lz4/archive/v1.7.5.tar.gz',
            hash = '0190cacd63022ccb86f44fa5041dc6c3804407ad61550ca21c382827319e7e7e',
            )

    def build(self):
        self.exec_msbuild(r'visual\VS20%(vs_ver)s\lz4.sln')

        self.install(r'visual\VS20%(vs_ver)s\bin\%(platform)s_%(configuration)s\liblz4.dll visual\VS20%(vs_ver)s\bin\%(platform)s_%(configuration)s\liblz4.pdb bin')
        self.install(r'.\lib\lz4.h .\lib\lz4hc.h .\lib\lz4frame.h include')
        self.install(r'visual\VS20%(vs_ver)s\bin\%(platform)s_%(configuration)s\liblz4.lib lib')

        self.install(r'.\lib\LICENSE share\doc\lz4')

@project_add
class Project_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'openssl',
            archive_url = 'ftp://ftp.openssl.org/source/openssl-1.0.2l.tar.gz',
            hash = 'ce07195b659e75f4e1db43552860070061f156a98bb37b672b101ba6e3ddf30c',
            dependencies = ['perl', 'nasm', ],
            )

    def build(self):
        common_options = r'no-ssl2 no-ssl3 no-comp --prefix="%(pkg_dir)s"'
        add_path = None

        debug_option = ''
        if self.builder.opts.configuration == 'debug':
            debug_option = 'debug-'

        # Note that we want to give priority to the system perl version.
        # Using the msys2 one might endup giving us a broken build
        add_path = ';'.join([os.path.join(self.builder.perl_dir, 'bin'),
                             os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')])

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

        self.install(r'.\cert.pem bin')
        self.install(r'.\openssl.cnf share')
        self.install(r'.\LICENSE share\doc\openssl\COPYING')

@project_add
class Project_opus(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'opus',
            archive_url = 'https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz',
            hash = 'cfafd339ccd9c5ef8d6ab15d7e1a412c054bf4cb4ecbbbcc78c12ef2def70732',
            )

    def build(self):
        version = '13'
        if self.builder.opts.vs_ver == '14':
            version = '15'
        elif self.builder.opts.vs_ver == '15':
            version = '17'

        configuration = 'ReleaseDLL'
        if self.builder.opts.configuration == 'debug':
            configuration = 'DebugDLL'

        self.exec_msbuild(r'.\win32\VS20' + version + '\opus.sln', configuration=configuration)

        bin_dir = r'.\win32\VS20' + version + '\%s\%s' % (self.builder.opts.platform, configuration, )

        self.install(bin_dir + r'\opus.dll bin')
        self.install(bin_dir + r'\opus.pdb bin')

        self.install(bin_dir + r'\opus.lib lib')

        self.install(r'include\* include')

        self.install(r'COPYING share\doc\opus')

@project_add
class Project_pango(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pango',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.40/pango-1.40.5.tar.xz',
            hash = '24748140456c42360b07b2c77a1a2e1216d07c056632079557cd4e815b9d01c9',
            dependencies = ['cairo', 'harfbuzz'],
            )

    def build(self):
        configuration = 'Release_FC'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_FC'

        self.exec_msbuild(r'win32\vs%(vs_ver)s\pango.sln', configuration=configuration)
        self.install(r'COPYING share\doc\pango')

@project_add
class Project_pixman(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pixman',
            archive_url = 'http://cairographics.org/releases/pixman-0.34.0.tar.gz',
            hash = '21b6b249b51c6800dc9553b65106e1e37d0e25df942c90531d4c3997aa20a88e',
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
class Project_pkg_config(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pkg-config',
            archive_url = 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.2.tar.gz',
            hash = '6fc69c01688c9458a57eb9a1664c9aba372ccda420a02bf4429fe610e7e7d591',
            dependencies = [ 'glib', ],
            )

    def build(self):
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s GLIB_PREFIX="%(gtk_dir)s"')

        bin_dir = r'.\%s\%s' % (self.builder.opts.configuration, self.builder.opts.platform, )
        self.install(bin_dir + r'\pkg-config.exe bin')
        self.install(bin_dir + r'\pkg-config.pdb bin')

        self.install(r'.\COPYING share\doc\pkg-config')

@project_add
class Project_portaudio(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'portaudio',
            archive_url = 'http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz',
            dependencies = ['cmake'],
            patches = [ '0001-Do-not-add-suffice-to-the-library-name.patch',
                        '0001-Fix-MSVC-check.patch' ]
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DPA_DLL_LINK_WITH_STATIC_RUNTIME=off -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs(r'nmake /nologo')

        self.install(r'portaudio.dll bin')
        self.install(r'portaudio.pdb bin')
        self.install(r'portaudio.lib lib')

        self.install(r'.\include\* include')

        self.install(r'.\LICENSE.txt share\doc\portaudio')

@project_add
class Project_protobuf(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'protobuf',
            archive_url = 'https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-cpp-3.3.0.tar.gz',
            hash = '5e2587dea2f9287885e3b04d3a94ed4e8b9b2d2c5dd1f0032ceef3ea1d153bd7',
            dependencies = ['cmake', 'zlib'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        # We need to compile with STATIC_RUNTIME off since protobuf-c also compiles with it OFF
        self.exec_vs('cmake .\cmake\ -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -Dprotobuf_DEBUG_POSTFIX="" -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_WITH_ZLIB=ON -Dprotobuf_MSVC_STATIC_RUNTIME=OFF -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs('nmake /nologo')
        self.exec_vs('nmake /nologo install')

        self.install(r'.\LICENSE share\doc\protobuf')

@project_add
class Project_protobuf_c(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'protobuf-c',
            repo_url = 'https://github.com/protobuf-c/protobuf-c',
            fetch_submodules = False,
            tag = 'a8921fe7dc2455a20114130eacc6761d1354fa2c',
            dependencies = ['cmake', 'protobuf'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake .\build-cmake\ -G "NMake Makefiles" -DPROTOBUF_ROOT="%(gtk_dir)s" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config)
        self.exec_vs(r'nmake /nologo')
        self.exec_vs(r'nmake /nologo install')

        self.install(r'.\LICENSE share\doc\protobuf-c')

@project_add
class Project_win_iconv(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'win-iconv',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.8.tar.gz',
            hash = '23adea990a8303c6e69e32a64a30171efcb1b73824a1c2da1bbf576b0ae7c520',
            dependencies = ['cmake'],
            )

    def build(self):
        #Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

        self.exec_vs('cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s')
        #Exec nmake clean
        self.exec_vs('nmake /nologo')
        self.exec_vs('nmake /nologo install')
        #Exec nmake clean

        self.install(r'.\COPYING share\doc\win-iconv')

@project_add
class Project_wing(Tarball, Meson):
    def __init__(self):
        Project.__init__(self,
            'wing',
            archive_url = 'https://git.gnome.org/browse/wing/snapshot/wing-0.0.8.tar.xz',
            hash = 'f0a6e2e529914a902b557888f8665fbd53cba7817ab0900f7f2a1b7bb5d602e3',
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
            dependencies = ['yasm', ],
            tag = '97eaef2ab82a46d13ea5e00270712d6475fbe42b',
            patches = [ '0001-use-more-recent-version-of-config.guess.patch',
                        '0002-configure-recognize-the-msys-shell.patch' ]
            )
    def build(self):
        self.exec_vs(r'bash build\build.sh %s %s' % (convert_to_msys(self.builder.gtk_dir), self.builder.opts.configuration),
                     add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))

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

        self.install(r'.\README share\doc\zlib')

Project.add(MercurialCmakeProject('pycairo', repo_url='git+ssh://git@github.com:muntyan/pycairo-gtk-win32.git', dependencies = ['cmake', 'cairo']))
Project.add(MercurialCmakeProject('pygobject', repo_url='git+ssh://git@github.com:muntyan/pygobject-gtk-win32.git', dependencies = ['cmake', 'glib']))
Project.add(MercurialCmakeProject('pygtk', repo_url='git+ssh://git@github.com:muntyan/pygtk-gtk-win32.git', dependencies = ['cmake', 'gtk', 'pycairo', 'pygobject']))
