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

class Tarball(object):
    def unpack(self):
        print_log('Extracting %s to %s' % (self.archive_file, self.builder.working_dir))

        if self.name != 'gettext-runtime':
            self.builder.exec_msys([self.builder.tar, 'ixf', self.__convert_to_msys(self.archive_file), '-C', self.__convert_to_msys(self.builder.working_dir)])
            archive_name = os.path.basename(self.archive_file)
            out_dir = re.match(r'(.*)\.tar', archive_name).group(1)
            if not os.path.exists(os.path.join(self.builder.working_dir, out_dir)):
                out_dir = self.name + '-' + out_dir
            shutil.move(os.path.join(self.builder.working_dir, out_dir), self.build_dir)
        else:
            # gettext-runtime is a tarbomb
            os.makedirs(self.build_dir)
            self.builder.exec_msys([self.builder.tar, 'ixf', self.__convert_to_msys(self.archive_file), '-C', self.__convert_to_msys(self.build_dir)])

        print_log('Extracted %s' % (self.archive_file,))

    def __convert_to_msys(self, path):
        path = path
        if path[1] != ':':
            raise Exception('oops')
        path = '/' + path[0] + path[2:].replace('\\', '/')
        return path

class MercurialRepo(object):
    def unpack(self):
        print_log('Cloning %s to %s' % (self.repo_url, self.build_dir))
        self.exec_cmd('hg clone %s %s-tmp' % (self.repo_url, self.build_dir))
        shutil.move(self.build_dir + '-tmp', self.build_dir)
        print_log('Cloned %s to %s' % (self.repo_url, self.build_dir))

    def update_build_dir(self):
        print_log('Updating directory %s' % (self.build_dir,))
        self.exec_cmd('hg pull -u', working_dir=self.build_dir)

class Project(object):
    def __init__(self, name, **kwargs):
        object.__init__(self)
        self.name = name
        self.dependencies = []
        self.patches = []
        self.archive_url = None
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

    def exec_cmd(self, cmd, working_dir=None, add_path=None):
        self.builder.exec_cmd(cmd, working_dir=working_dir, add_path=add_path)

    def exec_vs(self, cmd, add_path=None):
        self.builder.exec_vs(cmd, working_dir=self._get_working_dir(), add_path=add_path)

    def exec_msbuild(self, cmd, configuration=None):
        if not configuration:
            configuration = '%(configuration)s'
        self.exec_vs('msbuild ' + cmd + ' /p:Configuration=' + configuration + ' %(msbuild_opts)s')

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

class Project_atk(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'atk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.20/atk-2.20.0.tar.xz',
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
            dependencies = ['fontconfig', 'glib', 'pixman'],
            )

    def build(self):
        self.exec_msbuild(r'msvc\vc%(vs_ver)s\cairo.sln', configuration='Release_FC')
        self.install(r'.\COPYING share\doc\cairo')

Project.add(Project_cairo())

class Project_cyrus_sasl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'cyrus-sasl',
            archive_url = 'https://github.com/wingtk/cyrus-sasl/releases/download/cyrus-sasl-lmdb-2.1.27/cyrus-sasl-2.1.27.tar.gz',
            dependencies = ['lmdb', 'openssl'],
            )

    def build(self):
        #Exec nmake /nologo /f NTMakefile clean
        self.exec_vs(r'nmake /nologo /f NTMakefile SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s"')
        self.exec_vs(r'nmake /nologo /f NTMakefile install SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s"')

Project.add(Project_cyrus_sasl())

class Project_enchant(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'enchant',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/enchant-1.6.0.tar.gz',
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
            archive_url = 'http://ffmpeg.org/releases/ffmpeg-2.8.4.tar.bz2',
            )

    def build(self):
        self.exec_vs(r'bash build\build.sh %(pkg_dir)s', add_path=os.path.join(self.builder.opts.msys_dir, 'usr', 'bin'))

        self.install(r'.\COPYING.LGPLv2.1 ' \
                     r'.\COPYING.LGPLv3 ' \
                     r'share\doc\ffmpeg')

Project.add(Project_ffmpeg())

class Project_fontconfig(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'fontconfig',
            archive_url = 'https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.11.1.tar.gz',
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
            archive_url = 'http://download.savannah.gnu.org/releases/freetype/freetype-2.6.3.tar.bz2',
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
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.32/gdk-pixbuf-2.32.3.tar.xz',
            dependencies = ['glib', 'libpng'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gdk-pixbuf.sln', configuration='Release_GDI+')
        self.install(r'.\COPYING share\doc\gdk-pixbuf')

Project.add(Project_gdk_pixbuf())

class Project_gettext(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gettext-runtime',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/gettext-vc100-0.18-src.tar.bz2',
            dependencies = ['win-iconv'],
            patches = ['gettext-runtime.patch', 'gettext-lib-prexif.patch'],
            )

    def build(self):
        #Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

        self.exec_vs(r'cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s ' +
                        r'-DICONV_INCLUDE_DIR="%(gtk_dir)s\include" -DICONV_LIBRARIES="%(gtk_dir)s\lib\iconv.lib"', add_path=self.builder.opts.cmake_path)
        #Exec nmake clean
        self.exec_vs(r'nmake /nologo', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake /nologo install', add_path=self.builder.opts.cmake_path)
        #Exec nmake clean

        self.install(r'.\COPYING share\doc\gettext')

Project.add(Project_gettext())

class Project_glib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.48/glib-2.48.0.tar.xz',
            dependencies = ['gettext-runtime', 'libffi', 'zlib'],
            patches = ['glib-if_nametoindex.patch',
                       'glib-package-installation-directory.patch',
                       'Add-gsystemthreadsetname-implementation-for-W32-th.patch'],
            )

    def build(self):
        configuration = 'Release_BundledPCRE'
        if self.builder.opts.configuration == 'debug':
            configuation = 'Debug_BundledPCRE'

        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\glib.sln /p:PythonPath=%(python_dir)s', configuration=configuration)
        self.install(r'.\COPYING share\doc\glib')

Project.add(Project_glib())

class Project_glib_networking(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'glib-networking',
            archive_url = 'https://github.com/wingtk/glib-networking/releases/download/2.46.3-openssl/glib-networking-2.46.3.tar.xz',
            dependencies = ['gsettings-desktop-schemas', 'openssl'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\glib-networking.sln')

Project.add(Project_glib_networking())

class Project_gsettings_desktop_schemas(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'gsettings-desktop-schemas',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gsettings-desktop-schemas/3.18/gsettings-desktop-schemas-3.18.1.tar.xz',
            dependencies = ['glib'],
            )

    def build(self):
        self.push_location(r'.\build\win32')
        #Exec nmake /f gsettings-desktop-schemas-msvc.mak clean
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak PYTHON="%(python_dir)s\python.exe" PYTHON2="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s"')
        self.exec_vs(r'nmake /nologo /f gsettings-desktop-schemas-msvc.mak install PREFIX="%(gtk_dir)s"')
        self.pop_location()

Project.add(Project_gsettings_desktop_schemas())

class Project_gtk_base(Tarball, Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\gtk+.sln')

        mo = 'gtk20.mo' if self.name == 'gtk' else 'gtk30.mo'

        localedir = os.path.join(self.pkg_dir, 'share', 'locale')
        self.push_location(r'.\po')
        for f in glob.glob('*.po'):
            lcmsgdir = os.path.join(localedir, f[:-3], 'LC_MESSAGES')
            self.builder.make_dir(lcmsgdir)
            self.builder.exec_msys(['msgfmt', '-co', os.path.join(lcmsgdir, mo), f], working_dir=self._get_working_dir())
        self.pop_location()

        self.install(r'.\COPYING share\doc\gtk')

class Project_gtk(Project_gtk_base):
    def __init__(self):
        Project_gtk_base.__init__(self,
            'gtk', 
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/2.24/gtk+-2.24.30.tar.xz',
            dependencies = ['atk', 'gdk-pixbuf', 'pango'],
            patches = ['gtk-revert-scrolldc-commit.patch', 'gtk-bgimg.patch', 'gtk-accel.patch', 'gtk-multimonitor.patch'],
            )

Project.add(Project_gtk())

class Project_gtk3(Project_gtk_base):
    def __init__(self):
        Project_gtk_base.__init__(self,
            'gtk3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.20/gtk+-3.20.1.tar.xz',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            )

Project.add(Project_gtk3())

class Project_harfbuzz(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'harfbuzz',
            archive_url = 'https://www.freedesktop.org/software/harfbuzz/release/harfbuzz-1.2.4.tar.bz2',
            dependencies = ['freetype', 'glib'],
            )

    def build(self):
        self.push_location(r'.\win32')
        self.builder.make_dir(os.path.join(self.build_dir, 'build', 'win32', self.builder.opts.configuration, 'win32'))
        #Exec nmake /f Makefile.vc clean CFG=%(configuration)s
        self.exec_vs(r'nmake /nologo /f Makefile.vc CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.exec_vs(r'nmake /nologo /f Makefile.vc install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.pop_location()

Project.add(Project_harfbuzz())

class Project_hicolor_icon_theme(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'hicolor-icon-theme',
            archive_url = 'http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.15.tar.xz',
            )

    def build(self):
        self.install(r'.\index.theme share\icons\hicolor')

Project.add(Project_hicolor_icon_theme())

class Project_libcroco(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libcroco',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libcroco/0.6/libcroco-0.6.11.tar.xz',
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

class Project_libpng(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libpng',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/libpng-1.6.21.tar.xz',
            dependencies = ['zlib'],
            )

    def build(self):
        self.exec_msbuild(r'projects\vc%(vs_ver)s\pnglibconf\pnglibconf.vcxproj /p:SolutionDir=%(build_dir)s\projects\vc%(vs_ver)s\ ')
        self.exec_msbuild(r'projects\vc%(vs_ver)s\libpng\libpng.vcxproj /p:SolutionDir=%(build_dir)s\projects\vc%(vs_ver)s\ ')

        if self.builder.x86:
            rel_dir = r'.\projects\vc%(vs_ver)s\%(configuration)s'
        else:
            rel_dir = r'.\projects\vc%(vs_ver)s\x64\%(configuration)s'

        self.push_location(rel_dir)
        self.install('libpng16.dll libpng16.pdb bin')
        self.install('libpng16.lib lib')
        self.pop_location()
        self.install(r'.\png.h .\pngconf.h .\pnglibconf.h .\pngpriv.h include')
        self.install('LICENSE share\doc\libpng')

Project.add(Project_libpng())

class Project_librsvg(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'librsvg',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.40/librsvg-2.40.12.tar.xz',
            dependencies = ['libcroco', 'cairo', 'pango', 'gdk-pixbuf', 'gtk3'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\librsvg.sln')
        self.install(r'.\COPYING share\doc\librsvg')

Project.add(Project_librsvg())

class Project_libsoup(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libsoup',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libsoup/2.54/libsoup-2.54.0.1.tar.xz',
            dependencies = ['libxml2', 'glib-networking'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\libsoup.sln')

Project.add(Project_libsoup())

class Project_libxml2(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'libxml2',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/libxml2-2.9.3.tar.gz',
            dependencies = ['win-iconv'],
            )

    def build(self):
        self.exec_msbuild(r'win32\vc%(vs_ver)s\libxml2.sln')

        self.install(r'.\lib\libxml2.dll .\lib\libxml2.pdb .\lib\runsuite.exe .\lib\runsuite.pdb bin')
        self.install(r'.\win32\VC12\config.h .\include\wsockcompat.h .\include\libxml\*.h include\libxml')
        self.install(r'.\lib\libxml2.lib lib')
        self.install(r'.\COPYING share\doc\libxml2')

Project.add(Project_libxml2())

class Project_lmdb(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'lmdb',
            archive_url = 'https://github.com/wingtk/lmdb/archive/LMDB_MSVC_0.9.15.tar.gz',
            )

    def build(self):
        self.exec_msbuild(r'libraries\liblmdb\lmdb.sln')

        self.install(r'.\libraries\liblmdb\lmdb.h include')
        self.install(r'.\libraries\liblmdb\%(platform)s\%(configuration)s\lmdb.lib lib')
        self.install(r'.\libraries\liblmdb\LICENSE share\doc\lmdb')

Project.add(Project_lmdb())

class Project_openssl(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'openssl',
            archive_url = 'ftp://ftp.openssl.org/source/openssl-1.0.2g.tar.gz',
            )

    def build(self):
        common_options = r'no-ssl2 no-ssl3 no-comp --prefix="%(pkg_dir)s"'
        add_path = None

        if self.builder.x86:
            self.exec_vs(r'%(perl_dir)s\bin\perl.exe Configure VC-WIN32 ' + common_options)

            # Note that we want to give priority to the system perl version.
            # Using the msys2 one might endup giving us a broken build
            add_path = ';'.join([os.path.join(self.builder.opts.perl_dir, 'bin'),
                                 os.path.join(self.builder.opts.msys_dir, 'usr', 'bin')])
            self.exec_vs(r'ms\do_nasm', add_path=add_path)
        else:
            self.exec_vs(r'%(perl_dir)s\bin\perl.exe Configure VC-WIN64A ' + common_options)
            self.exec_vs(r'ms\do_win64a')

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

class Project_pango(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pango',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.40/pango-1.40.0.tar.xz',
            dependencies = ['cairo', 'harfbuzz'],
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\pango.sln', configuration='Release_FC')
        self.install(r'COPYING share\doc\pango')

Project.add(Project_pango())

class Project_pixman(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'pixman',
            archive_url = 'http://cairographics.org/releases/pixman-0.34.0.tar.gz',
            dependencies = ['libpng'],
            )

    def __get_symbol(self, code, exports):
        # PIXMAN_EXPORT pixman_implementation_t *
        # _pixman_internal_only_get_implementation (void)
        
        # PIXMAN_EXPORT pixman_bool_t
        # PREFIX (_copy) (region_type_t *dst, region_type_t *src)

        sym = None
        m = re.match(r'PIXMAN_EXPORT\s+.*(\s|\*)(PREFIX\s*\(([a-zA-Z0-9_]+)\))\s*\(', code)
        if m:
            sym = m.group(3)
            exports.add('pixman_region32' + sym)
            exports.add('pixman_region' + sym)
        else:
            m = re.match(r'PIXMAN_EXPORT\s+.*(\s|\*)([a-zA-Z0-9_]+)\s*\(', code)
            if m:
                sym = m.group(2)
                if not sym.startswith('_pixman'):
                    exports.add(sym)

    def __get_exports(self, srcfile, exports):
        lines = open(srcfile, 'r').readlines()
        for i in xrange(len(lines)):
            if lines[i].find('PIXMAN_EXPORT') >= 0:
                self.__get_symbol(lines[i].strip() + ' ' + lines[i+1].strip(), exports)

    def __generate_sym_file(self):
        sym_file = os.path.join(self.build_dir, 'pixman', 'pixman.symbols')
        if os.path.exists(sym_file):
            print_debug('symbol file %s already exists' % (sym_file,))
            return

        print_log('Generating symbol file %s' % (sym_file,))

        exports = set(['prng_srand_r', 'prng_randmemset_r'])

        for root, dirs, files in os.walk(self.build_dir):
            for f in files:
                f = f.lower()
                if f.endswith('.c') or f.endswith('.h'):
                    self.__get_exports(os.path.join(root, f), exports)

        with open(sym_file + '.tmp', 'w') as out:
            out.write('\n'.join(sorted(exports)))
        shutil.move(sym_file + '.tmp', sym_file)

    def build(self):
        self.__generate_sym_file()

        self.exec_msbuild(r'build\win32\vc%(vs_ver)s\pixman.vcxproj /p:SolutionDir=%(build_dir)s\build\win32\vc%(vs_ver)s\ ')
        self.exec_msbuild(r'build\win32\vc%(vs_ver)s\install.vcxproj /p:SolutionDir=%(build_dir)s\build\win32\vc%(vs_ver)s\ ')

        self.install(r'.\COPYING share\doc\pixman')

Project.add(Project_pixman())

class Project_win_iconv(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'win-iconv',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.8.tar.gz',
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

class Project_zlib(Tarball, Project):
    def __init__(self):
        Project.__init__(self,
            'zlib',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/zlib-1.2.8.tar.xz',
            )

    def build(self):
        self.exec_msbuild(r'build\win32\vs%(vs_ver)s\zlib.sln')

        self.push_location(r'.\build\vs%(vs_ver)s\%(configuration)s\%(platform)s')

        self.install(r'.\include\zlib.h .\include\zconf.h include')
        self.install(r'.\bin\zlib1.dll .\bin\zlib1.pdb bin')
        self.install(r'.\lib\zlib1.lib .\bin\zlib1.pdb lib')

        self.pop_location()

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
    print>>sys.stderr, "Error:", msg
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

        self.working_dir = os.path.join(opts.build_dir, 'build', opts.platform)
        self.gtk_dir = os.path.join(opts.build_dir, 'gtk', opts.platform)

        self.x86 = opts.platform == 'Win32'
        self.x64 = not self.x86

        self.msbuild_opts = '/nologo /p:Platform=%(platform)s %(msbuild_opts)s ' % \
            dict(platform=opts.platform, configuration=opts.configuration, msbuild_opts=opts.msbuild_opts)

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
            raise Exception("'%s' could not be found. Please check you have Visual Studio installed at '%s' and that it supports the target platform '%s'." % (vsvars_bat, opts.vs_install_path, opts.platform))

        output = subprocess.check_output('cmd.exe /c ""%s" && set"' % (vcvars_bat,), shell=True)
        self.vs_env = {}
        for l in output.splitlines():
            k, v = l.split("=", 1)
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
        self.__prepare_build(projects)
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

        build_dir = os.path.join(self.working_dir, '..', '..', 'gtk', self.opts.platform)
        if not os.path.exists(build_dir):
            print_log("Creating directory %s" % (build_dir,))
            os.makedirs(build_dir)

        for p in projects:
            self.__download_one(p)

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

        proj.builder = None
        self.__project = None

        print_debug("copying %s to %s" % (proj.pkg_dir, self.gtk_dir))
        self.copy_all(proj.pkg_dir, self.gtk_dir)
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)

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

    def __download_one(self, proj):
        if not proj.archive_file:
            print_debug("archive file is not specified for project %s, skipping" % (proj.name,))
            return

        if os.path.exists(proj.archive_file):
            print_debug("archive %s already exists" % (proj.archive_file,))
            return

        if not os.path.exists(self.opts.archives_download_dir):
            print_log("Creating archives download directory %s" % (self.opts.archives_download_dir,))
            os.makedirs(self.opts.archives_download_dir)

        print_log("downloading %s" % (proj.archive_file,))
        self.__execute([self.wget, proj.archive_url], self.opts.archives_download_dir)

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

    def exec_cmd(self, args, working_dir=None, add_path=None):
        self.__execute(args, working_dir=working_dir, add_path=add_path)

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
    opts.perl_dir = args.perl_dir
    opts.python_dir = args.python_dir
    opts.msys_dir = args.msys_dir
    opts.clean = args.clean
    opts.msbuild_opts = args.msbuild_opts
    opts.no_deps = args.no_deps

    if not opts.archives_download_dir:
        opts.archives_download_dir = os.path.join(args.build_dir, 'src')
    if not opts.patches_root_dir:
        opts.patches_root_dir = os.path.join(args.build_dir, 'github', 'gtk-win32')
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
        description='Jhbuild for poor, build Gtk and friends',
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
    #p_build.add_argument('-c', '--configuration', default='release', choices=['release', 'debug'],
    #                     help='Configuration to build, release or debug. Default is release.')
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
                         help="Visual Studio version 10,12, etc. Default is 12.")
    p_build.add_argument('--vs-install-path',
                         help=r"The directory where you installed Visual Studio. Default is 'C:\Program Files (x86)\Microsoft Visual Studio $(build-ver).0'")
    p_build.add_argument('--cmake-path', default=r'C:\Program Files (x86)\CMake\bin',
                         help="The directory where you installed cmake.")
    p_build.add_argument('--perl-dir', default=r'C:\Perl',
                         help="The directory where you installed perl.")
    p_build.add_argument('--python-dir', default=r'c:\Python27',
                         help="The directory where you installed python.")

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
    args.func(args)
