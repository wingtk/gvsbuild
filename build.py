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

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import traceback
import hashlib

def convert_to_msys(path):
    path = path
    if path[1] != ':':
        raise Exception('oops')
    path = '/' + path[0] + path[2:].replace('\\', '/')
    return path

class Tarball(object):
    def unpack(self):
        print_log('Extracting %s to %s' % (self.archive_file, self.builder.working_dir))

        os.makedirs(self.build_dir)
        self.builder.exec_msys([self.builder.tar, 'ixf', convert_to_msys(self.archive_file), '-C', convert_to_msys(self.build_dir), '' if self.tarbomb else '--strip-components=1'])

        print_log('Extracted %s' % (self.archive_file,))

class MercurialRepo(object):
    def unpack(self):
        print_log('Cloning %s to %s' % (self.repo_url, self.build_dir))
        self.exec_cmd('hg clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)
        print_log('Cloned %s to %s' % (self.repo_url, self.build_dir))

    def update_build_dir(self):
        print_log('Updating directory %s' % (self.build_dir,))
        self.exec_cmd('hg pull -u', working_dir=self.build_dir)

class GitRepo(object):
    def unpack(self):
        print_log('Cloning %s to %s' % (self.repo_url, self.build_dir))

        self.builder.exec_msys('git clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)

        if self.fetch_submodules:
            self.builder.exec_msys('git submodule update --init',  working_dir=self.build_dir)

        if self.tag:
            self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=self.build_dir)

        print_log('Cloned %s to %s' % (self.repo_url, self.build_dir))

    def update_build_dir(self):
        print_log('Updating directory %s' % (self.build_dir,))

        # I don't like too much this, but at least we ensured it is properly cleaned up
        self.builder.exec_msys('git clean -xdf', working_dir=self.build_dir)

        if self.tag:
            self.builder.exec_msys('git fetch origin', working_dir=self.build_dir)
            self.builder.exec_msys('git checkout -f %s' % self.tag, working_dir=self.build_dir)
        else:
            self.builder.exec_msys('git checkout -f', working_dir=self.build_dir)
            self.builder.exec_msys('git pull --rebase', working_dir=self.build_dir)

        if self.fetch_submodules:
            self.builder.exec_msys('git submodule update --init', working_dir=self.build_dir)

        if os.path.exists(self.patch_dir):
            print_log("Copying files from %s to %s" % (self.patch_dir, self.build_dir))
            self.builder.copy_all(self.patch_dir, self.build_dir)

class Project(object):
    def __init__(self, name, **kwargs):
        object.__init__(self)
        self.name = name
        self.dependencies = []
        self.patches = []
        self.archive_url = None
        self.tarbomb = False
        for k in kwargs:
            setattr(self, k, kwargs[k])
        self.__working_dir = None

    _projects = []
    _names = []
    _dict = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return repr(self.name)

    def build(self):
        raise NotImplementedError()

    def post_install(self):
        pass

    def exec_cmd(self, cmd, working_dir=None, add_path=None):
        self.builder.exec_cmd(cmd, working_dir=working_dir, add_path=add_path)

    def exec_vs(self, cmd, add_path=None):
        self.builder.exec_vs(cmd, working_dir=self._get_working_dir(), add_path=add_path)

    def exec_msbuild(self, cmd, configuration=None, add_path=None):
        if not configuration:
            configuration = '%(configuration)s'
        self.exec_vs('msbuild ' + cmd + ' /p:Configuration=' + configuration + ' %(msbuild_opts)s', add_path=add_path)

    def install(self, *args):
        self.builder.install(self._get_working_dir(), self.pkg_dir, *args)

    def install_dir(self, src, dest=None):
        if not dest:
            dest = os.path.basename(src)
        self.builder.install_dir(self._get_working_dir(), self.pkg_dir, src, dest)

    def patch(self):
        for p in self.patches:
            name = os.path.basename(p)
            stamp = os.path.join(self.build_dir, name + ".patch-applied")
            if not os.path.exists(stamp):
                print_log("Applying patch %s" % (p,))
                self.builder.exec_msys(['patch', '-p1', '-i', p], working_dir=self._get_working_dir())
                with open(stamp, 'w') as stampfile:
                    stampfile.write('done')
            else:
                print_debug("patch %s already applied, skipping" % (p,))

    def _get_working_dir(self):
        if self.__working_dir:
            return os.path.join(self.build_dir, self.__working_dir)
        else:
            return self.build_dir

    def push_location(self, path):
        self.__working_dir = path

    def pop_location(self):
        self.__working_dir = None

    def prepare_build_dir(self):
        if self.builder.opts.clean and os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)

        if os.path.exists(self.build_dir):
            print_debug("directory %s already exists" % (self.build_dir,))
            self.update_build_dir()
        else:
            self.unpack()
            if os.path.exists(self.patch_dir):
                print_log("Copying files from %s to %s" % (self.patch_dir, self.build_dir))
                self.builder.copy_all(self.patch_dir, self.build_dir)

    def update_build_dir(self):
        pass

    def unpack(self):
        raise NotImplementedError("unpack")

    @staticmethod
    def add(proj):
        Project._projects.append(proj)
        Project._names.append(proj.name)
        Project._dict[proj.name] = proj

    @staticmethod
    def get_project(name):
        return Project._dict[name]

    @staticmethod
    def list_projects():
        return list(Project._projects)

    @staticmethod
    def get_names():
        return list(Project._names)

    @staticmethod
    def get_dict():
        return dict(Project._dict)

class Project_adwaita_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'adwaita-icon-theme',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/adwaita-icon-theme/3.22/adwaita-icon-theme-3.22.0.tar.xz',
            hash = 'c18bf6e26087d9819a962c77288b291efab25d0419b73d909dd771716a45dcb7',
            dependencies = ['librsvg'],
            )

    def build(self):
        self.push_location(r'.\build\win32')
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.exec_vs(r'nmake /nologo /f adwaita-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))
        self.pop_location()

        self.install(r'.\COPYING_CCBYSA3 share\doc\adwaita-icon-theme')

Project.add(Project_adwaita_icon_theme())

class Project_atk(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'atk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.22/atk-2.22.0.tar.xz',
            hash = 'd349f5ca4974c9c76a4963e5b254720523b0c78672cbc0e1a3475dbd9b3d44b6',
            dependencies = ['glib'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\atk.sln')
        self.install(r'.\COPYING share\doc\atk')

Project.add(Project_atk())

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

        self.install(r'.\COPYING share\doc\cairo')

Project.add(Project_cairo())

class Project_clutter(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'clutter',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/clutter/1.26/clutter-1.26.0.tar.xz',
            hash = '67514e7824b3feb4723164084b36d6ce1ae41cb3a9897e9f1a56c8334993ce06',
            dependencies = ['atk','cogl','json-glib'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\clutter.sln')

        self.install(r'.\COPYING share\doc\clutter')

Project.add(Project_clutter())

class Project_cogl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cogl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/cogl/1.22/cogl-1.22.0.tar.xz',
            hash = '689dfb5d14fc1106e9d2ded0f7930dcf7265d0bc84fa846b4f03941633eeaa91',
            dependencies = ['glib','cairo','pango','gdk-pixbuf'],
            patches = ['001-cogl-missing-symbols.patch',
                       '002-cogl-pango-missing-symbols.patch',
                       '003-cogl-framebuffer-missing-debug-return.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\cogl.sln')

        self.install(r'.\COPYING share\doc\cogl')

Project.add(Project_cogl())

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

Project.add(Project_cyrus_sasl())

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

Project.add(Project_enchant())

class Project_ffmpeg(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'ffmpeg',
            archive_url = 'http://ffmpeg.org/releases/ffmpeg-2.8.7.tar.bz2',
            hash = '8777ce4a335640fdd13680ba423ef6da330ff5071bfbe27cdbb452379167efe5',
            dependencies = [ 'x264' ]
        )

    def build(self):
        self.exec_vs(r'bash build\build.sh %s %s %s' % (self.pkg_dir, self.builder.gtk_dir, self.builder.opts.configuration),
                     add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))

        self.install(r'.\COPYING.LGPLv2.1 ' \
                     r'.\COPYING.LGPLv3 ' \
                     r'.\COPYING.GPLv2 ' \
                     r'share\doc\ffmpeg')

Project.add(Project_ffmpeg())

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

Project.add(Project_fontconfig())

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

Project.add(Project_freetype())

class Project_gdk_pixbuf(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gdk-pixbuf',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.36/gdk-pixbuf-2.36.1.tar.xz',
            hash = '9d5ba72070460c1b5b74115d395a3e33daeb7b7b67fb256cdccc9d7187c42a38',
            dependencies = ['glib', 'libpng'],
            )

    def build(self):
        configuration = 'Release_GDI+'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_GDI+'

        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gdk-pixbuf.sln', configuration=configuration)
        self.install(r'.\COPYING share\doc\gdk-pixbuf')

Project.add(Project_gdk_pixbuf())

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

        self.install(r'.\COPYING share\doc\gettext')

Project.add(Project_gettext())

class Project_glib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.50/glib-2.50.3.tar.xz',
            hash = '82ee94bf4c01459b6b00cb9db0545c2237921e3060c0b74cff13fbc020cfd999',
            dependencies = ['gettext', 'libffi', 'zlib'],
            patches = ['glib-if_nametoindex.patch',
                       'glib-package-installation-directory.patch'],
            )

    def build(self):
        configuration = 'Release_BundledPCRE'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_BundledPCRE'

        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\glib.sln', configuration=configuration)
        self.install(r'.\COPYING share\doc\glib')

Project.add(Project_glib())

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

Project.add(Project_glib_networking())

class Project_glib_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib-openssl',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib-openssl/2.50/glib-openssl-2.50.0.tar.xz',
            hash = '359ef30cb908d910aa06ab11038dd667d6e821819c0211ead8f210e3503d3974',
            dependencies = ['glib', 'openssl'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\glib-openssl.sln')
        self.install(r'.\COPYING share\doc\glib-openssl')
        self.install(r'.\LICENSE_EXCEPTION share\doc\glib-openssl')

Project.add(Project_glib_openssl())

class Project_grpc(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'grpc',
            repo_url = 'https://github.com/grpc/grpc.git',
            fetch_submodules = True,
            tag = 'v1.0.0',
            dependencies = ['protobuf'],
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

Project.add(Project_grpc())

class Project_gsettings_desktop_schemas(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gsettings-desktop-schemas',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gsettings-desktop-schemas/3.22/gsettings-desktop-schemas-3.22.0.tar.xz',
            hash = '0f06c7ba34c3a99e4d58b10889496133c9aaad6698ea2d8405d481c7f1a7eae1',
            dependencies = ['glib'],
            )

    def build(self):
        self.push_location(r'.\build\win32')
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s"')
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PREFIX="%(gtk_dir)s"')
        self.pop_location()

        self.install(r'.\COPYING share\doc\gsettings-desktop-schemas')

Project.add(Project_gsettings_desktop_schemas())

class Project_gtk_base(Tarball, Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
        mo = 'gtk20.mo' if self.name == 'gtk' else 'gtk30.mo'

        localedir = os.path.join(self.pkg_dir, 'share', 'locale')
        self.push_location(r'.\po')
        for f in glob.glob('*.po'):
            lcmsgdir = os.path.join(localedir, f[:-3], 'LC_MESSAGES')
            self.builder.make_dir(lcmsgdir)
            self.builder.exec_msys(['msgfmt', '-co', os.path.join(lcmsgdir, mo), f], working_dir=self._get_working_dir())
        self.pop_location()

        self.install(r'.\COPYING share\doc\%s' % self.name)

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

Project.add(Project_gtk())

class Project_gtk3(Project_gtk_base):
    def __init__(self):
        Project_gtk_base.__init__(self,
            'gtk3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.22/gtk+-3.22.6.tar.xz',
            hash = 'eba75a216a117f4391beb2971ba20ff8a1823f109893f0ab6c2eac2210ea172f',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            patches = ['gtk3-clip-retry-if-opened-by-others.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtk+.sln /p:GtkPostInstall=rem')

        super(Project_gtk3, self).build()

    def post_install(self):
        self.exec_cmd(r'%(gtk_dir)s\bin\glib-compile-schemas.exe %(gtk_dir)s\share\glib-2.0\schemas')
        self.exec_cmd(r'%(gtk_dir)s\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "%(gtk_dir)s\share\icons\hicolor"')

Project.add(Project_gtk3())

class Project_gtksourceview3(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gtksourceview3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtksourceview/3.22/gtksourceview-3.22.2.tar.xz',
            hash = '6ce84231dd0931cc747708434ca2f344c65a092dd6e1a800283fe0748773af5e',
            dependencies = ['gtk3'],
            )

    def build(self):
        add_path = os.path.join(self.builder.opts.perl_dir, 'bin')
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtksourceview.sln', add_path=add_path)

        self.install(r'.\COPYING share\doc\gtksourceview3')

Project.add(Project_gtksourceview3())

class Project_harfbuzz(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'harfbuzz',
            archive_url = 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.4.0.tar.bz2',
            hash = '8497eca976f3c4cdee7f46ffc228d755d2f0651da7c253fa6ae99d5a61ddd1b5',
            dependencies = ['freetype', 'glib'],
            )

    def build(self):
        self.push_location(r'.\win32')
        self.builder.make_dir(os.path.join(self.build_dir, 'build', 'win32', self.builder.opts.configuration, 'win32'))
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.exec_vs(r'nmake /nologo /f Makefile.vc install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.pop_location()

        self.install(r'.\COPYING share\doc\harfbuzz')

Project.add(Project_harfbuzz())

class Project_hicolor_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'hicolor-icon-theme',
            archive_url = 'http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.15.tar.xz',
            hash = '9cc45ac3318c31212ea2d8cb99e64020732393ee7630fa6c1810af5f987033cc',
            )

    def build(self):
        self.install(r'.\index.theme share\icons\hicolor')

Project.add(Project_hicolor_icon_theme())

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

Project.add(Project_jsonc())

class Project_json_glib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'json-glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/json-glib/1.2/json-glib-1.2.2.tar.xz',
            hash = 'ea128ab52a824fcd06e5448fbb2bd8d9a13740d51c66d445828edba71321a621',
            dependencies = ['glib'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\json-glib.sln')

        self.install(r'.\COPYING share\doc\json-glib')

Project.add(Project_json_glib())

class Project_leveldb(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'leveldb',
            archive_url = 'http://github.com/google/leveldb/archive/v1.18.tar.gz',
            hash = '4aa1a7479bc567b95a59ac6fb79eba49f61884d6fd400f20b7af147d54c5cee5',
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\leveldb.sln')

        self.install(r'.\LICENSE share\doc\leveldb')

Project.add(Project_leveldb())

class Project_libarchive(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libarchive',
            archive_url = 'http://www.libarchive.org/downloads/libarchive-3.2.2.tar.gz',
            hash = '691c194ee132d1f0f7a42541f091db811bc2e56f7107e9121be2bc8c04f1060f',
            dependencies = ['win-iconv', 'zlib', 'lz4', 'openssl', 'libxml2'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install(r'.\COPYING share\doc\libarchive')

Project.add(Project_libarchive())

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

Project.add(Project_libcroco())

class Project_libepoxy(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libepoxy',
            archive_url = 'https://github.com/anholt/libepoxy/releases/download/v1.3.1/libepoxy-1.3.1.tar.bz2',
            hash = '1d8668b0a259c709899e1c4bab62d756d9002d546ce4f59c9665e2fc5f001a64',
            patches = ['0001-MSVC-Builds-Support-PACKED.patch'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\epoxy.sln')

Project.add(Project_libepoxy())

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

Project.add(Project_libffi())

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

Project.add(Project_libgxps())

class Project_libjpeg_turbo(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libjpeg-turbo',
            archive_url = 'https://sourceforge.net/projects/libjpeg-turbo/files/1.5.1/libjpeg-turbo-1.5.1.tar.gz',
            hash = '41429d3d253017433f66e3d472b8c7d998491d2f41caa7306b8d9a6f2a2c666c',
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        add_path = ';'.join([self.builder.opts.cmake_path,
                             os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')])

        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s', add_path=add_path)
        self.exec_vs(r'nmake /nologo', add_path=add_path)
        self.exec_vs(r'nmake /nologo install', add_path=add_path)

        self.install(r'.\LICENSE.md share\doc\libjpeg-turbo')

Project.add(Project_libjpeg_turbo())

class Project_libmicrohttpd(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libmicrohttpd',
             archive_url = 'http://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.48.tar.gz',
             hash = '87667e158f2bf8c691a002e256ffe30885d4121a9ee4143af0320c47cdf8a2a4',
             patches = ['001-disable-w32_SetThreadName.patch'],
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
            debug_option = '_d'

        if self.builder.x86:
            rel_dir = r'w32\VS20' + version + '\Output'
        else:
            rel_dir = r'w32\VS20' + version + '\Output\x64'

        self.push_location(rel_dir)
        self.install(r'microhttpd.h include')
        self.install(r'libmicrohttpd-dll' + debug_option + '.lib' + ' lib')
        self.install(r'libmicrohttpd-dll' + debug_option + '.dll' + ' bin')
        self.install(r'libmicrohttpd-dll' + debug_option + '.pdb' + ' bin')
        self.install(r'hellobrowser-dll' + debug_option + '.exe' + ' bin')
        self.pop_location()

        self.install(r'.\COPYING share\doc\libmicrohttpd')

Project.add(Project_libmicrohttpd())

class Project_libpng(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libpng',
            archive_url = 'http://prdownloads.sourceforge.net/libpng/libpng-1.6.28.tar.xz',
            hash = 'd8d3ec9de6b5db740fefac702c37ffcf96ae46cb17c18c1544635a3852f78f7a',
            dependencies = ['zlib'],
            )

    def build(self):
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DZLIB_ROOT="%(gtk_dir)s" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install('LICENSE share\doc\libpng')

Project.add(Project_libpng())

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

Project.add(Project_librsvg())

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

Project.add(Project_sqlite())

class Project_libcurl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libcurl',
            archive_url = 'https://github.com/curl/curl/archive/curl-7_48_0.tar.gz',
            hash = '401043087d326edc74021597b9b8a60d6b5c9245fe224beaf89fa6d6c2d9178a',
            dependencies = [],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DGTK_DIR="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install(r'.\COPYING share\doc\libcurl')

Project.add(Project_libcurl())

class Project_libsoup(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libsoup',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libsoup/2.56/libsoup-2.56.0.tar.xz',
            hash = 'd8216b71de8247bc6f274ec054c08547b2e04369c1f8add713e9350c8ef81fe5',
            dependencies = ['libxml2', 'glib-openssl', 'sqlite'],
            patches = ['0001-websocket-connection-log-when-getting-a-pong-message.patch',
                       '0001-websocket-add-api-to-add-a-keepalive-interval.patch',
                       '0001-websocket-connection-avoid-sending-data-if-we-are-cl.patch']
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\libsoup.sln')

        self.install(r'.\COPYING share\doc\libsoup')

Project.add(Project_libsoup())

class Project_libssh(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libssh',
            archive_url = 'https://red.libssh.org/attachments/download/177/libssh-0.7.2.tar.xz',
            hash = 'a32c45b9674141cab4bde84ded7d53e931076c6b0f10b8fd627f3584faebae62',
            dependencies = ['zlib','openssl'],
            )

    def build(self):
        self.exec_msbuild(r'build\vs%(vs_ver)s\libssh-library.sln')

        self.install(r'.\COPYING share\doc\libssh')

Project.add(Project_libssh())

class Project_libssh2(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libssh2',
            archive_url = 'https://www.libssh2.org/download/libssh2-1.7.0.tar.gz',
            hash = 'e4561fd43a50539a8c2ceb37841691baf03ecb7daf043766da1b112e4280d584',
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake -G"NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DGTK_DIR="%(pkg_dir)s" -DWITH_ZLIB=ON -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install(r'.\COPYING share\doc\libssh2')

Project.add(Project_libssh2())

class Project_libuv(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libuv',
            archive_url = 'https://github.com/libuv/libuv/archive/v1.9.1.tar.gz',
            hash = 'a6ca9f0648973d1463f46b495ce546ddcbe7cce2f04b32e802a15539e46c57ad',
            )

    def build(self):
        rel_dir = r'Release'
        if self.builder.opts.configuration == 'debug':
            rel_dir = r'Debug'

        platform = r'x86'
        if self.builder.x64:
            platform = r'x64'

        os.system(r'%s\vcbuild.bat build static %s %s' % (self._get_working_dir(), self.builder.opts.configuration, platform))

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

Project.add(Project_libuv())

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

Project.add(Project_libxml2())

class Project_libyuv(GitRepo, Project):
    def __init__(self):
        Project.__init__(self,
            'libyuv',
            repo_url = 'https://chromium.googlesource.com/libyuv/libyuv',
            fetch_submodules = False,
            tag = None,
            )

    def build(self):
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install(r'.\LICENSE share\doc\libyuv')

Project.add(Project_libyuv())

class Project_libzip(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libzip',
            archive_url = 'http://nih.at/libzip/libzip-1.1.3.tar.gz',
            hash = '1faa5a524dd4a12c43b6344e618edce1bf8050dfdb9d0f73f3cc826929a002b0',
            dependencies = ['zlib'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DGTK_DIR="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install(r'.\LICENSE share\doc\libzip')

Project.add(Project_libzip())

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

Project.add(Project_lmdb())

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

Project.add(Project_lz4())

class Project_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'openssl',
            archive_url = 'ftp://ftp.openssl.org/source/openssl-1.0.2k.tar.gz',
            hash = '6b3977c61f2aedf0f96367dcfb5c6e578cf37e7b8d913b4ecb6643c3cb88d8c0',
            )

    def build(self):
        common_options = r'no-ssl2 no-ssl3 no-comp --prefix="%(pkg_dir)s"'
        add_path = None

        debug_option = ''
        if self.builder.opts.configuration == 'debug':
            debug_option = 'debug-'

        # Note that we want to give priority to the system perl version.
        # Using the msys2 one might endup giving us a broken build
        add_path = ';'.join([os.path.join(self.builder.opts.perl_dir, 'bin'),
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

Project.add(Project_openssl())

class Project_opus(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'opus',
            archive_url = 'http://downloads.xiph.org/releases/opus/opus-1.1.3.tar.gz',
            hash = '58b6fe802e7e30182e95d0cde890c0ace40b6f125cffc50635f0ad2eef69b633',
            )

    def build(self):
        version = '13'
        if self.builder.opts.vs_ver == '14':
            version = '15'

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

Project.add(Project_opus())

class Project_pango(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pango',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.40/pango-1.40.3.tar.xz',
            hash = 'abba8b5ce728520c3a0f1535eab19eac3c14aeef7faa5aded90017ceac2711d3',
            dependencies = ['cairo', 'harfbuzz'],
            )

    def build(self):
        configuration = 'Release_FC'
        if self.builder.opts.configuration == 'debug':
            configuration = 'Debug_FC'

        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\pango.sln', configuration=configuration)
        self.install(r'COPYING share\doc\pango')

Project.add(Project_pango())

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

Project.add(Project_pixman())

class Project_pkg_config(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pkg-config',
            archive_url = 'https://pkg-config.freedesktop.org/releases/pkg-config-0.29.1.tar.gz',
            hash = 'beb43c9e064555469bd4390dcfd8030b1536e0aa103f08d7abf7ae8cac0cb001',
            dependencies = [ 'glib', ],
            )

    def build(self):
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s GLIB_PREFIX="%(gtk_dir)s"')

        bin_dir = r'.\%s\%s' % (self.builder.opts.configuration, self.builder.opts.platform, )
        self.install(bin_dir + r'\pkg-config.exe bin')
        self.install(bin_dir + r'\pkg-config.pdb bin')

        self.install(r'.\COPYING share\doc\pkg-config')

Project.add(Project_pkg_config())

class Project_portaudio(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'portaudio',
            archive_url = 'http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz',
            patches = [ '0001-Do-not-add-suffice-to-the-library-name.patch',
                        '0001-Fix-MSVC-check.patch' ]
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        self.exec_vs(r'cmake . -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DPA_DLL_LINK_WITH_STATIC_RUNTIME=off -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)

        self.install(r'portaudio.dll bin')
        self.install(r'portaudio.pdb bin')
        self.install(r'portaudio.lib lib')

        self.install(r'.\include\* include')

        self.install(r'.\LICENSE.txt share\doc\portaudio')

Project.add(Project_portaudio())

class Project_protobuf(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'protobuf',
            archive_url = 'https://github.com/google/protobuf/archive/v3.1.0.tar.gz',
            hash = '0a0ae63cbffc274efb573bdde9a253e3f32e458c41261df51c5dbc5ad541e8f7',
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'Release'
        # We need to compile with STATIC_RUNTIME off since protobuf-c also compiles with it OFF
        self.exec_vs('cmake .\cmake\ -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -Dprotobuf_DEBUG_POSTFIX="" -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_MSVC_STATIC_RUNTIME=OFF -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install(r'.\LICENSE share\doc\protobuf')

Project.add(Project_protobuf())

class Project_protobuf_c(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'protobuf-c',
            archive_url = 'https://github.com/protobuf-c/protobuf-c/releases/download/v1.2.1/protobuf-c-1.2.1.tar.gz',
            hash = '846eb4846f19598affdc349d817a8c4c0c68fd940303e6934725c889f16f00bd',
            dependencies = ['protobuf'],
            patches = ['0001-Declare-variables-at-the-beginning-of-the-block.patch',
                       '0001-Do-not-build-tests.patch'],
            )

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs(r'cmake .\build-cmake\ -G "NMake Makefiles" -DPROTOBUF_ROOT="%(gtk_dir)s" -DCMAKE_INSTALL_PREFIX="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config,add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)

        self.install(r'.\LICENSE share\doc\protobuf-c')

Project.add(Project_protobuf_c())

class Project_win_iconv(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'win-iconv',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.8.tar.gz',
            hash = '23adea990a8303c6e69e32a64a30171efcb1b73824a1c2da1bbf576b0ae7c520',
            )

    def build(self):
        #Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

        self.exec_vs('cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s', add_path=self.builder.opts.cmake_path)
        #Exec nmake clean
        self.exec_vs('nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake /nologo install', add_path=self.builder.opts.cmake_path)
        #Exec nmake clean

        self.install(r'.\COPYING share\doc\win-iconv')

Project.add(Project_win_iconv())

class Project_wing(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'wing',
            archive_url = 'https://git.gnome.org/browse/wing/snapshot/wing-8c8ff6da28c4921f7306d7cc84ce0566a9f66e31.tar.xz',
            hash = 'cd4f5f28c5730a5512e497f326230c8d7eb74c654dce32754b493b41d010cab6',
            dependencies = ['glib'],
            )

    def build(self):
        self.push_location(r'.\nmake')
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s PREFIX="%(gtk_dir)s"')
        self.exec_vs(r'nmake /nologo /f Makefile.vc install CFG=%(configuration)s PREFIX="%(gtk_dir)s"')
        self.pop_location()

        self.install(r'.\COPYING share\doc\wing')

Project.add(Project_wing())

class Project_x264(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'x264',
            wget_opts = [ '--no-passive-ftp'],
            archive_url = 'ftp://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-20160313-2245.tar.bz2',
            hash = '65cc10e063cb38a664fbf66f536fe7c92631b7764bf6866786d3a0e702226b86',
            patches = [ '0001-use-more-recent-version-of-config.guess.patch',
                        '0002-configure-recognize-the-msys-shell.patch' ]
            )
    def build(self):
        self.exec_vs(r'bash build\build.sh %s %s' % (convert_to_msys(self.builder.gtk_dir), self.builder.opts.configuration),
                     add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))

        # use the path expected when building with a dependent project
        self.builder.exec_msys(['cp', 'libx264.lib', 'x264.lib'], working_dir=os.path.join(self.builder.gtk_dir, 'lib') )

        self.install(r'.\COPYING share\doc\x264')

Project.add(Project_x264())

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

Project.add(Project_zlib())


class CmakeProject(Tarball, Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs('cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DGTK_DIR="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake /nologo install', add_path=self.builder.opts.cmake_path)

class MercurialCmakeProject(MercurialRepo, CmakeProject):
    def __init__(self, name, **kwargs):
        CmakeProject.__init__(self, name, **kwargs)

Project.add(MercurialCmakeProject('pycairo', repo_url='git+ssh://git@github.com:muntyan/pycairo-gtk-win32.git', dependencies = ['cairo']))
Project.add(MercurialCmakeProject('pygobject', repo_url='git+ssh://git@github.com:muntyan/pygobject-gtk-win32.git', dependencies = ['glib']))
Project.add(MercurialCmakeProject('pygtk', repo_url='git+ssh://git@github.com:muntyan/pygtk-gtk-win32.git', dependencies = ['gtk', 'pycairo', 'pygobject']))


#========================================================================================================================================================

global_verbose = False
global_debug = False

def print_message(msg):
    print(msg)

def print_log(msg):
    if global_verbose:
        print(msg)

def print_debug(msg):
    if global_debug:
        print("Debug:", msg)

def error_exit(msg):
    print("Error:", msg, file=sys.stderr)
    sys.exit(1)

class ordered_set(set):
    def __init__(self):
        set.__init__(self)
        self.__list = list()

    def add(self, o):
        if not o in self:
            set.add(self, o)
            self.__list.append(o)

    def __iter__(self):
        return self.__list.__iter__()

class Builder(object):
    def __init__(self, opts):
        self.opts = opts

        self.__check_tools(opts)
        self.__check_vs(opts)

        self.working_dir = os.path.join(opts.build_dir, 'build', opts.platform, opts.configuration)
        self.gtk_dir = os.path.join(opts.build_dir, 'gtk', opts.platform, opts.configuration)

        self.x86 = opts.platform == 'Win32'
        self.x64 = not self.x86

        self.msbuild_opts = '/nologo /p:Platform=%(platform)s /p:PythonPath=%(python_dir)s %(msbuild_opts)s ' % \
            dict(platform=opts.platform, python_dir=opts.python_dir, configuration=opts.configuration, msbuild_opts=opts.msbuild_opts)

        if global_verbose:
            self.msbuild_opts += ' /v:normal'
        else:
            self.msbuild_opts += ' /v:minimal'

    def __check_tools(self, opts):
        self.patch = os.path.join(opts.msys_dir, 'usr', 'bin', 'patch.exe')
        if not os.path.exists(self.patch):
            error_exit("%s not found. Please check that you installed patch in msys2 using ``pacman -S patch``" % (self.patch,))
        print_debug("patch: %s" % (self.patch,))

        self.tar = os.path.join(opts.msys_dir, 'usr', 'bin', 'tar.exe')
        if not os.path.exists(self.tar):
            error_exit("%s not found. Please check that you installed tar and other unzipping tools in msys2 using ``pacman -S gzip tar xz``" % (self.tar,))
        print_debug("tar: %s" % (self.tar,))

        self.msgfmt = os.path.join(opts.msys_dir, 'usr', 'bin', 'msgfmt.exe')
        if not os.path.exists(self.msgfmt):
            error_exit("%s not found. Please check that you installed msgfmt in msys2 using ``pacman -S gettext``" % (self.msgfmt,))
        print_debug("msgfmt: %s" % (self.msgfmt,))

        self.wget = os.path.join(opts.msys_dir, 'usr', 'bin', 'wget.exe')
        if not os.path.exists(self.wget):
            error_exit("%s not found. Please check that you installed wget in msys2 using ``pacman -S wget``" % (self.wget,))
        print_debug("wget: %s" % (self.wget,))

        self.nuget = opts.nuget_path
        if not os.path.exists(self.nuget):
            print_log("Could not find nuget: %s" % (self.nuget,))

    def __check_vs(self, opts):
        # Verify VS exists at the indicated location, and that it supports the required target
        if opts.platform in ('Win32', 'win32', 'x86'):
            opts.platform = 'Win32'
            self.filename_arch = 'x86'
            vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'vcvars32.bat')
        elif opts.platform in ('x64', 'amd64', 'Amd64'):
            opts.platform = 'x64'
            self.filename_arch = 'x64'
            vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'amd64', 'vcvars64.bat')
            # make sure it works even with VS Express
            if not os.path.exists(vcvars_bat):
                vcvars_bat = os.path.join(opts.vs_install_path, 'VC', 'bin', 'x86_amd64', 'vcvarsx86_amd64.bat')
        else:
            raise Exception("Invalid target platform '%s'" % (opts.platform,))

        if not os.path.exists(vcvars_bat):
            raise Exception("'%s' could not be found. Please check you have Visual Studio installed at '%s' and that it supports the target platform '%s'." % (vcvars_bat, opts.vs_install_path, opts.platform))

        output = subprocess.check_output('cmd.exe /c ""%s" && set"' % (vcvars_bat,), shell=True)
        self.vs_env = {}
        for l in output.splitlines():
            k, v = l.decode('utf-8').split("=", 1)
            self.vs_env[k] = v

    def preprocess(self):
        for proj in Project.list_projects():
            if proj.archive_url:
                url = proj.archive_url
                archive = url[url.rfind('/') + 1:]
                proj.archive_file = os.path.join(self.opts.archives_download_dir, archive)
            else:
                proj.archive_file = None
            proj.patch_dir = os.path.join(self.opts.patches_root_dir, proj.name)
            proj.build_dir = os.path.join(self.working_dir, proj.name)
            proj.dependencies = [Project.get_project(dep) for dep in proj.dependencies]
            proj.dependents = []

        for proj in Project.list_projects():
            self.__compute_deps(proj)
            print_debug("%s => %s" % (proj.name, [d.name for d in proj.all_dependencies]))

    def __compute_deps(self, proj):
        if hasattr(proj, 'all_dependencies'):
            return
        deps = ordered_set()
        for dep in proj.dependencies:
            self.__compute_deps(dep)
            for p in dep.all_dependencies:
                deps.add(p)
            deps.add(dep)
        proj.all_dependencies = deps

    def build(self, projects):
        if self.__prepare_build(projects):
            return

        if self.opts.check_hash:
            return

        for p in projects:
            try:
                self.__build_one(p)
            except:
                traceback.print_exc()
                error_exit("%s build failed" % (p.name))

    def __prepare_build(self, projects):
        if not os.path.exists(self.working_dir):
            print_log("Creating working directory %s" % (self.working_dir,))
            os.makedirs(self.working_dir)

        shutil.copy(os.path.join(self.opts.patches_root_dir, 'stack.props'), self.working_dir)

        log_dir = os.path.join(self.working_dir, 'logs')
        if not os.path.exists(log_dir):
            print_log("Creating log directory %s" % (log_dir,))
            os.makedirs(log_dir)

        #Remove-Item $logDirectory\*.log

        build_dir = os.path.join(self.working_dir, '..', '..', '..', 'gtk', self.opts.platform)
        if not os.path.exists(build_dir):
            print_log("Creating directory %s" % (build_dir,))
            os.makedirs(build_dir)

        for p in projects:
            if self.__download_one(p):
                return True
        return False

    def __build_one(self, proj):
        print_message("Building project %s" % (proj.name,))

        proj.builder = self
        self.__project = proj

        proj.prepare_build_dir()

        proj.pkg_dir = proj.build_dir + "-rel"
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)
        os.makedirs(proj.pkg_dir)

        proj.patch()
        proj.build()

        print_debug("copying %s to %s" % (proj.pkg_dir, self.gtk_dir))
        self.copy_all(proj.pkg_dir, self.gtk_dir)
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)

        proj.post_install()

        proj.builder = None
        self.__project = None

    def make_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def copy_all(self, srcdir, destdir):
        self.make_dir(destdir)
        for f in glob.glob('%s\\*' % (srcdir,)):
            self.__copy_to(f, destdir)

    def __copy_to(self, src, destdir):
        #print_debug("__copy_to %s %s" % (src, destdir))
        self.make_dir(destdir)
        for f in glob.glob(src):
            if os.path.isdir(f):
                name = os.path.basename(f)
                dest_subdir = os.path.join(destdir, name)
                self.make_dir(dest_subdir)
                for item in os.listdir(f):
                    self.__copy_to(os.path.join(f, item), dest_subdir)
            else:
                shutil.copy2(f, destdir)

    def __copy(self, src, destdir):
        if os.path.isdir(src):
            dst = os.path.join(destdir, os.path.basename(src))
            print_debug("copying '%s' to '%s'" % (src, dst))
            shutil.copytree(src, dst)
        else:
            print_debug("copying '%s' to '%s'" % (src, destdir))
            shutil.copy(src, destdir)

    def __hashfile(self, file_name):
        hash_calc = hashlib.sha256()
        with open(file_name, 'rb') as fi:
            for chunk in iter(lambda: fi.read(4096), b""):
                hash_calc.update(chunk)
        return hash_calc.hexdigest()

    def __check_hash(self, proj):
        if hasattr(proj, 'hash'):
            hc = self.__hashfile(proj.archive_file)
            if hc != proj.hash:
                print_message("Hash mismatch on %s:\n  Calculated '%s'\n  Expected   '%s'\n" % (proj.archive_file, hc, proj.hash, ))
                return True

            # Print the correct hash
            if self.opts.check_hash:
                print_message("Hash ok on %s (%s)" % (proj.archive_file, hc, ))
            else:
                print_debug("Hash ok on %s (%s)" % (proj.archive_file, hc, ))
        return False

    def __download_one(self, proj):
        if not proj.archive_file:
            print_debug("archive file is not specified for project %s, skipping" % (proj.name,))
            return False

        if os.path.exists(proj.archive_file):
            print_debug("archive %s already exists" % (proj.archive_file,))
            return self.__check_hash(proj)

        if not os.path.exists(self.opts.archives_download_dir):
            print_log("Creating archives download directory %s" % (self.opts.archives_download_dir,))
            os.makedirs(self.opts.archives_download_dir)

        print_log("downloading %s" % (proj.archive_file,))
        wget_opts = [self.wget];
        if hasattr(proj, 'wget_opts'):
            wget_opts += proj.wget_opts;
        self.__execute(wget_opts + [proj.archive_url], self.opts.archives_download_dir)
        return self.__check_hash(proj)

    def __sub_vars(self, s):
        if '%' in s:
            d = dict(platform=self.opts.platform, configuration=self.opts.configuration, build_dir=self.opts.build_dir, vs_ver=self.opts.vs_ver,
                     gtk_dir=self.gtk_dir, python_dir=self.opts.python_dir, perl_dir=self.opts.perl_dir, msbuild_opts=self.msbuild_opts)
            if self.__project is not None:
                d['pkg_dir'] = self.__project.pkg_dir
                d['build_dir'] = self.__project.build_dir
            return s % d
        else:
            return s

    def exec_vs(self, cmd, working_dir=None, add_path=None):
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path, env=self.vs_env)

    def exec_cmd(self, cmd, working_dir=None, add_path=None):
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path)

    def install(self, build_dir, pkg_dir, *args):
        if len(args) == 1:
            args = args[0].split()
        dest = os.path.join(pkg_dir, self.__sub_vars(args[-1]))
        self.make_dir(dest)
        for f in args[:-1]:
            src = os.path.join(self.__sub_vars(build_dir), self.__sub_vars(f))
            print_debug("copying %s to %s" % (src, dest))
            self.__copy_to(src, dest)

    def install_dir(self, build_dir, pkg_dir, src, dest):
        src = os.path.join(build_dir, self.__sub_vars(src))
        dest = os.path.join(pkg_dir, self.__sub_vars(dest))
        print_debug("copying %s content to %s" % (src, dest))
        self.copy_all(src, dest)

    def exec_msys(self, args, working_dir=None):
        self.__execute(args, working_dir=working_dir, add_path=os.path.join(self.opts.msys_dir, 'usr', 'bin'))

    def __execute(self, args, working_dir=None, add_path=None, env=None):
        print_debug("running %s, cwd=%s, path+=%s" % (args, working_dir, add_path))
        if add_path:
            if env is not None:
                env = dict(env)
            else:
                env = dict(os.environ)
            self.__add_path(env, add_path)
        subprocess.check_call(args, cwd=working_dir, env=env, shell=True)

    def __add_path(self, env, folder):
        key = None
        for k in env:
            if k.lower() == 'path':
                key = k
                break
        env[key] = env[key] + ';' + folder

class Options(object):
    pass

def get_options(args):
    opts = Options()

    opts.platform = args.platform
    opts.configuration = getattr(args, 'configuration', 'release')
    opts.build_dir = args.build_dir
    opts.archives_download_dir = args.archives_download_dir
    opts.patches_root_dir = args.patches_root_dir
    opts.vs_ver = args.vs_ver
    opts.vs_install_path = args.vs_install_path
    opts.cmake_path = args.cmake_path
    opts.nuget_path = args.nuget_path
    opts.perl_dir = args.perl_dir
    opts.python_dir = args.python_dir
    opts.msys_dir = args.msys_dir
    opts.clean = args.clean
    opts.msbuild_opts = args.msbuild_opts
    opts.no_deps = args.no_deps
    opts.check_hash = args.check_hash

    if not opts.archives_download_dir:
        opts.archives_download_dir = os.path.join(args.build_dir, 'src')
    if not opts.nuget_path:
        opts.nuget_path = os.path.join(args.build_dir, 'nuget', 'nuget.exe')
    if not opts.patches_root_dir:
        opts.patches_root_dir = sys.path[0]
    if not opts.vs_install_path:
        opts.vs_install_path = r'C:\Program Files (x86)\Microsoft Visual Studio %s.0' % (opts.vs_ver,)

    opts.projects = args.project

    for p in opts.projects:
        if not p in Project.get_names():
            error_exit(
                p + " is not a valid project name, available projects are:\n\t" + "\n\t".join(Project.get_names()))

    return opts

def __get_projects_to_build(opts):
    to_build = ordered_set()
    for name in opts.projects:
        p = Project.get_project(name)
        if not opts.no_deps:
            for dep in p.all_dependencies:
                to_build.add(dep)
        to_build.add(p)
    return to_build

def do_build(args):
    opts = get_options(args)
    print_debug("options are: %s" % (opts.__dict__,))
    builder = Builder(opts)
    builder.preprocess()

    to_build = __get_projects_to_build(opts)
    if not to_build:
        error_exit("nothing to do")
    print_debug("building %s" % ([p.name for p in to_build],))

    builder.build(to_build)

def do_list(args):
    print("Available projects:\n\t" + "\n\t".join(Project.get_names()))
    sys.exit(0)

def handle_global_options(args):
    global global_verbose
    global global_debug
    if args.verbose:
        global_verbose = True
    if args.debug:
        global_verbose = True
        global_debug = True

#==============================================================================
# Command line parser
#==============================================================================

def create_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Jhbuild-like system for Windows to build Gtk and friends',
        epilog=
    """
Examples:
    build.py build libpng libffi
        Build libpng, libffi, and their dependencies (zlib).

    build.py build --no-deps glib
        Build glib only.
    """)

    #==============================================================================
    # Global options
    #==============================================================================

    parser.add_argument('-v', '--verbose', default=False, action='store_true',
                        help='Print lots of stuff.')
    parser.add_argument('-d', '--debug', default=False, action='store_true',
                        help='Print even more stuff.')

    subparsers = parser.add_subparsers()

    #==============================================================================
    # build
    #==============================================================================

    p_build = subparsers.add_parser('build', help='build project(s)')
    p_build.set_defaults(func=do_build)

    p_build.add_argument('-p', '--platform', default='x86', choices=['x86', 'x64'],
                         help='Platform to build for, x86 or x64. Default is x86.')
    p_build.add_argument('-c', '--configuration', default='release', choices=['release', 'debug'],
                         help='Configuration to build, release or debug. Default is release.')
    p_build.add_argument('--build-dir', default=r'C:\gtk-build',
                         help='The directory where the sources will be downloaded and built.')
    p_build.add_argument('--msys-dir', default=r'C:\Msys64',
                         help='The directory where you installed msys2.')
    p_build.add_argument('--archives-download-dir',
                         help="The directory to download the source archives to. It will be created. " +
                              "If a source archive already exists here, it won't be downloaded again. " +
                              "Default is $(build-dir)\\src.")
    p_build.add_argument('--patches-root-dir',
                         help="The directory where you checked out https://github.com/wingtk/gtk-win32.git. Default is $(build-dir)\\github\\gtk-win32.")
    p_build.add_argument('--vs-ver', default='12',
                         help="Visual Studio version 10,12,14, etc. Default is 12.")
    p_build.add_argument('--vs-install-path',
                         help=r"The directory where you installed Visual Studio. Default is 'C:\Program Files (x86)\Microsoft Visual Studio $(build-ver).0'")
    p_build.add_argument('--cmake-path', default=r'C:\Program Files (x86)\CMake\bin',
                         help="The directory where you installed cmake.")
    p_build.add_argument('--nuget-path',
                         help="The directory where you installed nuget. " +
                              "Default is $(build-dir)\\nuget\\nuget.exe")
    p_build.add_argument('--perl-dir', default=r'C:\Perl',
                         help="The directory where you installed perl.")
    p_build.add_argument('--python-dir', default=os.path.dirname(sys.executable),
                         help="The directory where you installed python.")

    p_build.add_argument('--check-hash', default=False, action='store_true',
                         help='Only check hashes of downloaded archive(s), no build')
    p_build.add_argument('--clean', default=False, action='store_true',
                         help='Build the project(s) from scratch')
    p_build.add_argument('--no-deps', default=False, action='store_true',
                         help='Do not build dependencies of the selected project(s)')

    p_build.add_argument('--msbuild-opts', default='',
                         help='Command line options to pass to msbuild.')

    p_build.add_argument('project', nargs='+',
                         help='Project(s) to build.')

    #==============================================================================
    # list
    #==============================================================================

    p_list = subparsers.add_parser('list', help='list available projects')
    p_list.set_defaults(func=do_list)

    return parser

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    handle_global_options(args)
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
        
