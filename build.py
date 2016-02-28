import argparse
import glob
import os
import re
import shutil
import subprocess
import sys

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

    def exec_vs(self, cmd, add_path=None):
        self.builder.exec_vs(cmd, working_dir=self._get_working_dir(), add_path=add_path)

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

class Project_atk(Project):
    def __init__(self):
        Project.__init__(self,
            'atk',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.18/atk-2.18.0.tar.xz',
            dependencies = ['glib'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\atk.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.install(r'.\COPYING share\doc\atk')

Project.add(Project_atk())

class Project_cairo(Project):
    def __init__(self):
        Project.__init__(self,
            'cairo',
            archive_url = 'http://cairographics.org/snapshots/cairo-1.15.2.tar.xz',
            dependencies = ['fontconfig', 'glib', 'pixman'],
            )

    def build(self):
        self.exec_vs(r'msbuild msvc\vc%(vs_ver)s\cairo.sln /p:Platform=%(platform)s /p:Configuration=Release_FC /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.install(r'.\COPYING share\doc\cairo')

Project.add(Project_cairo())

class Project_cyrus_sasl(Project):
    def __init__(self):
        Project.__init__(self,
            'cyrus-sasl',
            archive_url = 'https://github.com/wingtk/cyrus-sasl/releases/download/cyrus-sasl-lmdb-2.1.27/cyrus-sasl-2.1.27.tar.gz',
            dependencies = ['lmdb', 'openssl'],
            )

    def build(self):
        #Exec nmake /f NTMakefile clean
        self.exec_vs(r'nmake /f NTMakefile SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s"')
        self.exec_vs(r'nmake /f NTMakefile install SASLDB="LMDB" LMDB_INCLUDE="%(gtk_dir)s\include" LMDB_LIBPATH="%(gtk_dir)s\lib" ' +
                     r'OPENSSL_INCLUDE="%(gtk_dir)s\include" OPENSSL_LIBPATH="%(gtk_dir)s\lib" prefix="%(pkg_dir)s"')

Project.add(Project_cyrus_sasl())

class Project_enchant(Project):
    def __init__(self):
        Project.__init__(self,
            'enchant',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/enchant-1.6.0.tar.gz',
            dependencies = ['glib'],
            )

    def build(self):
        raise NotImplementedError()
        comment = """
        $packageDestination = "$PWD-$filenameArch"
        Remove-Item -Recurse $packageDestination -ErrorAction Ignore

        Push-Location .\src

        $originalEnvironment = Swap-Environment $vcvarsEnvironment

        #Exec nmake -f makefile.mak clean
        Exec nmake -f makefile.mak DLL=1 $(if ($filenameArch -eq 'x64') { 'X64=1' }) MFLAGS=-MD GLIBDIR=..\..\..\..\gtk\%(platform)s\include\glib-2.0

        [void] (Swap-Environment $originalEnvironment)

        Pop-Location

        write-host $packageDestination\bin
        New-Item -Type Directory $packageDestination\bin
        Copy-Item `
                .\bin\%(configuration)s\enchant.exe, `
                .\bin\%(configuration)s\pdb\enchant.pdb, `
                .\bin\%(configuration)s\enchant-lsmod.exe, `
                .\bin\%(configuration)s\pdb\enchant-lsmod.pdb, `
                .\bin\%(configuration)s\test-enchant.exe, `
                .\bin\%(configuration)s\pdb\test-enchant.pdb, `
                .\bin\%(configuration)s\libenchant.dll, `
                .\bin\%(configuration)s\pdb\libenchant.pdb `
                $packageDestination\bin

        New-Item -Type Directory $packageDestination\etc\fonts
        Copy-Item `
                .\fonts.conf, `
                .\fonts.dtd `
                $packageDestination\etc\fonts

        New-Item -Type Directory $packageDestination\include\enchant
        Copy-Item `
                .\src\enchant.h, `
                .\src\enchant++.h, `
                .\src\enchant-provider.h `
                $packageDestination\include\enchant

        New-Item -Type Directory $packageDestination\lib\enchant
        Copy-Item `
                .\bin\%(configuration)s\libenchant.lib `
                $packageDestination\lib
        Copy-Item `
                .\bin\%(configuration)s\libenchant_ispell.dll, `
                .\bin\%(configuration)s\libenchant_ispell.lib, `
                .\bin\%(configuration)s\pdb\libenchant_ispell.pdb, `
                .\bin\%(configuration)s\libenchant_myspell.dll, `
                .\bin\%(configuration)s\libenchant_myspell.lib, `
                .\bin\%(configuration)s\pdb\libenchant_myspell.pdb `
                $packageDestination\lib\enchant

        New-Item -Type Directory $packageDestination\share\doc\enchant
        Copy-Item .\COPYING.LIB $packageDestination\share\doc\enchant\COPYING

        Package $packageDestination
        """

Project.add(Project_enchant())

class Project_ffmpeg(Project):
    def __init__(self):
        Project.__init__(self,
            'ffmpeg',
            archive_url = 'http://ffmpeg.org/releases/ffmpeg-2.8.4.tar.bz2',
            )

    def build(self):
        raise NotImplementedError()
        comment = """
        $packageDestination = "$PWD-$filenameArch"
        Remove-Item -Recurse $packageDestination -ErrorAction Ignore
        New-Item -Type Directory $packageDestination

        Remove-Item -Recurse build\install -ErrorAction Ignore
        New-Item -Type Directory build\install

        $originalEnvironment = Swap-Environment $vcvarsEnvironment

        $env:PATH += ";$Msys2Directory\usr\bin"

        Exec $Msys2Directory\usr\bin\bash build\build.sh build\install

        [void] (Swap-Environment $originalEnvironment)

        Copy-Item `
                build\install\include `
                $packageDestination `
                -Recurse

        New-Item -Type Directory $packageDestination\bin
        Copy-Item `
                build\install\bin\*.dll `
                $packageDestination\bin

        New-Item -Type Directory $packageDestination\lib
        Copy-Item `
                build\install\bin\*.lib `
                $packageDestination\lib

        New-Item -Type Directory $packageDestination\share\doc\ffmpeg
        Copy-Item `
                COPYING.LGPLv2.1, `
                COPYING.LGPLv3 `
                $packageDestination\share\doc\ffmpeg

        Package $packageDestination
        """

Project.add(Project_ffmpeg())

class Project_fontconfig(Project):
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

        self.exec_vs('msbuild fontconfig.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /t:build /nodeReuse:True %(msbuild_opts)s')

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

class Project_freetype(Project):
    def __init__(self):
        Project.__init__(self,
            'freetype',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/freetype-2.6.tar.bz2',
            )

    def build(self):
        self.exec_vs(r'msbuild builds\windows\vc%(vs_ver)s\freetype.vcxproj /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.install_dir(r'.\include')
        self.install(r'.\objs\%(platform)s\freetype.lib lib')
        self.install(r'.\docs\LICENSE.TXT share\doc\freetype')

Project.add(Project_freetype())

class Project_gdk_pixbuf(Project):
    def __init__(self):
        Project.__init__(self,
            'gdk-pixbuf',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.32/gdk-pixbuf-2.32.3.tar.xz',
            dependencies = ['glib', 'libpng'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\gdk-pixbuf.sln /p:Platform=%(platform)s /p:Configuration=Release_GDI+ /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.install(r'.\COPYING share\doc\gdk-pixbuf')

Project.add(Project_gdk_pixbuf())

class Project_gettext(Project):
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
        self.exec_vs(r'nmake', add_path=self.builder.opts.cmake_path)
        self.exec_vs(r'nmake install', add_path=self.builder.opts.cmake_path)
        #Exec nmake clean

        self.install(r'.\COPYING share\doc\gettext')

Project.add(Project_gettext())

class Project_glib(Project):
    def __init__(self):
        Project.__init__(self,
            'glib',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.46/glib-2.46.2.tar.xz',
            dependencies = ['gettext-runtime', 'libffi', 'zlib'],
            patches = ['glib-if_nametoindex.patch',
                       'glib-package-installation-directory.patch',
                       '0001-Change-message-system-to-use-fputs-instead-of-write.patch',
                       'Add-gsystemthreadsetname-implementation-for-W32-th.patch'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\glib.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.install(r'.\COPYING share\doc\glib')

Project.add(Project_glib())

class Project_glib_networking(Project):
    def __init__(self):
        Project.__init__(self,
            'glib-networking',
            archive_url = 'https://github.com/wingtk/glib-networking/releases/download/2.46.3-openssl/glib-networking-2.46.3.tar.xz',
            dependencies = ['gsettings-desktop-schemas', 'openssl'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\glib-networking.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

Project.add(Project_glib_networking())

class Project_gsettings_desktop_schemas(Project):
    def __init__(self):
        Project.__init__(self,
            'gsettings-desktop-schemas',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gsettings-desktop-schemas/3.18/gsettings-desktop-schemas-3.18.1.tar.xz',
            dependencies = ['glib'],
            )

    def build(self):
        self.push_location(r'.\build\win32')
        #Exec nmake /f gsettings-desktop-schemas-msvc.mak clean
        self.exec_vs(r'nmake /f gsettings-desktop-schemas-msvc.mak PYTHON="%(python_dir)s\python.exe" PYTHON2="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s"')
        self.exec_vs(r'nmake /f gsettings-desktop-schemas-msvc.mak install PREFIX="%(gtk_dir)s"')
        self.pop_location()

Project.add(Project_gsettings_desktop_schemas())

class Project_gtk_base(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\gtk+.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

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
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/gtk+-2.24.29.tar.xz',
            dependencies = ['atk', 'gdk-pixbuf', 'pango'],
            patches = ['gtk-revert-scrolldc-commit.patch', 'gtk-bgimg.patch', 'gtk-accel.patch', 'gtk-multimonitor.patch', 'gdk-window.patch'],
            )

Project.add(Project_gtk())

class Project_gtk3(Project_gtk_base):
    def __init__(self):
        Project_gtk_base.__init__(self,
            'gtk3',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.18/gtk+-3.18.6.tar.xz',
            dependencies = ['atk', 'gdk-pixbuf', 'pango', 'libepoxy'],
            )

Project.add(Project_gtk3())

class Project_harfbuzz(Project):
    def __init__(self):
        Project.__init__(self,
            'harfbuzz',
            archive_url = 'https://github.com/wingtk/harfbuzz/releases/download/1.1.2.msvc/harfbuzz-1.1.2.tar.bz2',
            dependencies = ['freetype', 'glib'],
            )

    def build(self):
        self.push_location(r'.\build\win32')
        #Exec nmake /f Makefile.vc clean CFG=%(configuration)s
        self.exec_vs(r'nmake /f Makefile.vc CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.exec_vs(r'nmake /f Makefile.vc install CFG=%(configuration)s PYTHON="%(python_dir)s\python.exe" PERL="%(perl_dir)s\bin\perl.exe" PREFIX="%(gtk_dir)s" FREETYPE=1 GOBJECT=1')
        self.pop_location()

Project.add(Project_harfbuzz())

class Project_hicolor_icon_theme(Project):
    def __init__(self):
        Project.__init__(self,
            'hicolor-icon-theme',
            archive_url = 'http://icon-theme.freedesktop.org/releases/hicolor-icon-theme-0.15.tar.xz',
            )

    def build(self):
        self.install(r'.\index.theme share\icons\hicolor')

Project.add(Project_hicolor_icon_theme())

class Project_libcroco(Project):
    def __init__(self):
        Project.__init__(self,
            'libcroco',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libcroco/0.6/libcroco-0.6.11.tar.xz',
            dependencies = ['glib', 'libxml2'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\libcroco.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.install(r'.\COPYING share\doc\libcroco')

Project.add(Project_libcroco())

class Project_libepoxy(Project):
    def __init__(self):
        Project.__init__(self,
            'libepoxy',
            archive_url = 'https://github.com/anholt/libepoxy/releases/download/v1.3.1/libepoxy-1.3.1.tar.bz2',
            patches = '0001-MSVC-Builds-Support-PACKED.patch',
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\epoxy.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

Project.add(Project_libepoxy())

class Project_libffi(Project):
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

        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\libffi.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

        self.install(r'.\\' + build_dest + r'\include\ffi.h', r'.\src\x86\ffitarget.h', 'include')
        self.install(r'LICENSE share\doc\libffi')

Project.add(Project_libffi())

class Project_libpng(Project):
    def __init__(self):
        Project.__init__(self,
            'libpng',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/libpng-1.6.21.tar.xz',
            dependencies = ['zlib'],
            )

    def build(self):
        self.exec_vs(r'msbuild projects\vc%(vs_ver)s\pnglibconf\pnglibconf.vcxproj /p:Platform=%(platform)s /p:Configuration=%(configuration)s /p:SolutionDir=%(build_dir)s\projects\vc%(vs_ver)s\ /nodeReuse:True %(msbuild_opts)s')
        self.exec_vs(r'msbuild projects\vc%(vs_ver)s\libpng\libpng.vcxproj /p:Platform=%(platform)s /p:Configuration=%(configuration)s /p:SolutionDir=%(build_dir)s\projects\vc%(vs_ver)s\ /nodeReuse:True %(msbuild_opts)s')

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

class Project_librsvg(Project):
    def __init__(self):
        Project.__init__(self,
            'librsvg',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/librsvg/2.40/librsvg-2.40.12.tar.xz',
            dependencies = ['libcroco', 'cairo', 'pango', 'gdk-pixbuf', 'gtk3'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\librsvg.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.install(r'.\COPYING share\doc\librsvg')

Project.add(Project_librsvg())

class Project_libsoup(Project):
    def __init__(self):
        Project.__init__(self,
            'libsoup',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/libsoup/2.52/libsoup-2.52.1.tar.xz',
            dependencies = ['libxml2', 'glib-networking'],
            patches = ['0001-Provide-a-_SOUP_EXTERN-so-we-ensure-the-methods-get-.patch',
                       '0002-Mark-externalized-methods-with-SOUP_AVAILABLE_IN_2_4.patch',
                       '0003-Properly-handle-the-visibility-of-the-methods.patch',
                       '0001-Declare-a-SOUP_VAR-to-externalize-variables.patch'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\soup.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

Project.add(Project_libsoup())

class Project_libxml2(Project):
    def __init__(self):
        Project.__init__(self,
            'libxml2',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/libxml2-2.9.3.tar.gz',
            dependencies = ['win-iconv'],
            )

    def build(self):
        self.exec_vs(r'msbuild win32\vc%(vs_ver)s\libxml2.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

        self.install(r'.\lib\libxml2.dll .\lib\libxml2.pdb .\lib\runsuite.exe .\lib\runsuite.pdb bin')
        self.install(r'.\win32\VC12\config.h .\include\wsockcompat.h .\include\libxml\*.h include\libxml')
        self.install(r'.\lib\libxml2.lib lib')
        self.install(r'.\COPYING share\doc\libxml2')

Project.add(Project_libxml2())

class Project_lmdb(Project):
    def __init__(self):
        Project.__init__(self,
            'lmdb',
            archive_url = 'https://github.com/wingtk/lmdb/archive/LMDB_MSVC_0.9.15.tar.gz',
            )

    def build(self):
        self.exec_vs(r'msbuild libraries\liblmdb\lmdb.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

        self.install(r'.\libraries\liblmdb\lmdb.h include')
        self.install(r'.\libraries\liblmdb\%(platform)s\%(configuration)s\lmdb.lib lib')
        self.install(r'.\libraries\liblmdb\LICENSE share\doc\lmdb')

Project.add(Project_lmdb())

class Project_openssl(Project):
    def __init__(self):
        Project.__init__(self,
            'openssl',
            archive_url = 'ftp://ftp.openssl.org/source/openssl-1.0.2f.tar.gz',
            )

    def build(self):
        raise NotImplementedError()
        comment = """
        $packageDestination = "$PWD-$filenameArch"
        Remove-Item -Recurse $packageDestination -ErrorAction Ignore

        $originalEnvironment = Swap-Environment $vcvarsEnvironment

        $env:PATH += ";$PerlDirectory\bin;$Msys2Directory\usr\bin"

        switch ($filenameArch) {
                'x86' {
                        Exec perl Configure VC-WIN32 no-ssl2 no-ssl3 no-comp --openssldir=./
                        Exec ms\do_nasm
                }

                'x64' {
                        Exec perl Configure VC-WIN64A no-ssl2 no-ssl3 no-comp --openssldir=./
                        Exec ms\do_win64a
                }
        }

        # nmake returns error code 2 because it fails to find build outputs to delete
        try { Exec nmake -f ms\ntdll.mak vclean } catch { }

        Exec nmake -f ms\ntdll.mak

        Exec nmake -f ms\ntdll.mak test

        Exec perl mk-ca-bundle.pl -n cert.pem
        Move-Item .\include .\include-orig

        Exec nmake -f ms\ntdll.mak install

        [void] (Swap-Environment $originalEnvironment)

        New-Item -Type Directory $packageDestination

        Move-Item .\bin $packageDestination
        Copy-Item `
                .\out32dll\libeay32.pdb, `
                .\out32dll\openssl.pdb, `
                .\out32dll\ssleay32.pdb `
                $packageDestination\bin
        Move-Item .\cert.pem $packageDestination\bin

        Move-Item .\include $packageDestination
        Move-Item .\include-orig .\include

        Move-Item .\lib $packageDestination
        Copy-Item `
                .\out32dll\4758cca.pdb, `
                .\out32dll\aep.pdb, `
                .\out32dll\atalla.pdb, `
                .\out32dll\capi.pdb, `
                .\out32dll\chil.pdb, `
                .\out32dll\cswift.pdb, `
                .\out32dll\gmp.pdb, `
                .\out32dll\gost.pdb, `
                .\out32dll\nuron.pdb, `
                .\out32dll\padlock.pdb, `
                .\out32dll\sureware.pdb, `
                .\out32dll\ubsec.pdb `
                $packageDestination\lib\engines

        New-Item -Type Directory $packageDestination\share\doc\openssl
        Move-Item .\openssl.cnf $packageDestination\share\openssl.cnf.example
        Copy-Item .\LICENSE $packageDestination\share\doc\openssl\COPYING

        Package $packageDestination
        """

Project.add(Project_openssl())

class Project_pango(Project):
    def __init__(self):
        Project.__init__(self,
            'pango',
            archive_url = 'http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.38/pango-1.38.1.tar.xz',
            dependencies = ['cairo', 'harfbuzz'],
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\pango.sln /p:Platform=%(platform)s /p:Configuration=Release_FC /nodeReuse:True %(msbuild_opts)s')
        self.install(r'COPYING share\doc\pango')

Project.add(Project_pango())

class Project_pixman(Project):
    def __init__(self):
        Project.__init__(self,
            'pixman',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/pixman-0.32.6.tar.gz',
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
        
        self.exec_vs(r'msbuild build\win32\vc%(vs_ver)s\pixman.vcxproj /p:Platform=%(platform)s /p:Configuration=%(configuration)s /p:SolutionDir=%(build_dir)s\build\win32\vc%(vs_ver)s\ /maxcpucount /nodeReuse:True %(msbuild_opts)s')
        self.exec_vs(r'msbuild build\win32\vc%(vs_ver)s\install.vcxproj /p:Platform=%(platform)s /p:Configuration=%(configuration)s /p:SolutionDir=%(build_dir)s\build\win32\vc%(vs_ver)s\ /maxcpucount /nodeReuse:True %(msbuild_opts)s')

        self.install(r'.\COPYING share\doc\pixman')

Project.add(Project_pixman())

class Project_win_iconv(Project):
    def __init__(self):
        Project.__init__(self,
            'win-iconv',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.7.tar.gz',
            patches = ['missing-endif.patch'],
            )

    def build(self):
        #Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

        self.exec_vs('cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DCMAKE_BUILD_TYPE=%(configuration)s', add_path=self.builder.opts.cmake_path)
        #Exec nmake clean
        self.exec_vs('nmake', add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake install', add_path=self.builder.opts.cmake_path)
        #Exec nmake clean

        self.install(r'.\COPYING share\doc\win-iconv')

Project.add(Project_win_iconv())

class Project_zlib(Project):
    def __init__(self):
        Project.__init__(self,
            'zlib',
            archive_url = 'http://dl.hexchat.net/gtk-win32/src/zlib-1.2.8.tar.xz',
            )

    def build(self):
        self.exec_vs(r'msbuild build\win32\vs%(vs_ver)s\zlib.sln /p:Platform=%(platform)s /p:Configuration=%(configuration)s /maxcpucount /nodeReuse:True %(msbuild_opts)s')

        self.push_location(r'.\build\vs%(vs_ver)s\%(configuration)s\%(platform)s')

        self.install(r'.\include\zlib.h .\include\zconf.h include')
        self.install(r'.\bin\zlib1.dll .\bin\zlib1.pdb bin')
        self.install(r'.\lib\zlib1.lib .\bin\zlib1.pdb lib')

        self.pop_location()

        self.install(r'.\README share\doc\zlib')

Project.add(Project_zlib())




class CmakeProject(Project):
    def __init__(self, name, **kwargs):
        Project.__init__(self, name, **kwargs)

    def build(self):
        cmake_config = 'Debug' if self.builder.opts.configuration == 'debug' else 'RelWithDebInfo'
        self.exec_vs('cmake -G "NMake Makefiles" -DCMAKE_INSTALL_PREFIX="%(pkg_dir)s" -DGTK_DIR="%(gtk_dir)s" -DCMAKE_BUILD_TYPE=' + cmake_config, add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake', add_path=self.builder.opts.cmake_path)
        self.exec_vs('nmake install', add_path=self.builder.opts.cmake_path)

Project.add(CmakeProject('pycairo', dependencies = ['cairo']))
Project.add(CmakeProject('pygobject', dependencies = ['glib']))
Project.add(CmakeProject('pygtk', dependencies = ['pygobject', 'gtk']))
    

#========================================================================================================================================================

global_verbose = False
global_debug = False

def print_log(msg):
    if global_verbose:
        print msg

def print_debug(msg):
    if global_debug:
        print "Debug:", msg

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
        self.vs_env['PythonPath'] = opts.python_dir

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
            self.__build_one(p)

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
        print_log("Building project %s" % (proj.name,))
        self.__prepare_build_dir(proj)

        proj.pkg_dir = proj.build_dir + "-rel"
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)
        os.makedirs(proj.pkg_dir)

        proj.builder = self
        self.__project = proj

        proj.patch()
        proj.build()

        proj.builder = None
        self.__project = None

        print_debug("copying %s to %s" % (proj.pkg_dir, self.gtk_dir))
        self.__copy_all(proj.pkg_dir, self.gtk_dir)
        shutil.rmtree(proj.pkg_dir, ignore_errors=True)

    def make_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __copy_all(self, srcdir, destdir):
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

    def __prepare_build_dir(self, proj):
        if self.opts.clean and os.path.exists(proj.build_dir):
            shutil.rmtree(proj.build_dir)

        if self.__unpack(proj) and os.path.exists(proj.patch_dir):
            print_log("Copying files from %s to %s" % (proj.patch_dir, proj.build_dir))
            self.__copy_all(proj.patch_dir, proj.build_dir)

    def __unpack(self, proj):
        if os.path.exists(proj.build_dir):
            print_debug("directory %s already exists" % (proj.build_dir,))
            return False

        print_log('Extracting %s to %s' % (proj.archive_file, self.working_dir))

        if proj.name != 'gettext-runtime':
            self.exec_msys([self.tar, 'ixf', self.__convert_to_msys(proj.archive_file), '-C', self.__convert_to_msys(self.working_dir)])
            archive_name = os.path.basename(proj.archive_file)
            out_dir = re.match(r'(.*)\.tar', archive_name).group(1)
            if not os.path.exists(os.path.join(self.working_dir, out_dir)):
                out_dir = proj.name + '-' + out_dir
            shutil.move(os.path.join(self.working_dir, out_dir), proj.build_dir)
	else:
            # gettext-runtime is a tarbomb
            os.makedirs(proj.build_dir)
            self.exec_msys([self.tar, 'ixf', self.__convert_to_msys(proj.archive_file), '-C', self.__convert_to_msys(proj.build_dir)])

        print_log('Extracted %s' % (proj.archive_file,))
        return True

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
                     gtk_dir=self.gtk_dir, python_dir=self.opts.python_dir, perl_dir=self.opts.perl_dir, msbuild_opts=self.opts.msbuild_opts)
            if self.__project is not None:
                d['pkg_dir'] = self.__project.pkg_dir
                d['build_dir'] = self.__project.build_dir
            return s % d
        else:
            return s

    def exec_vs(self, cmd, working_dir=None, add_path=None):
        self.__execute(self.__sub_vars(cmd), working_dir=working_dir, add_path=add_path, env=self.vs_env)

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
        self.__copy_all(src, dest)

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
        env[key] = folder + ';' + env[key]

    def __convert_to_msys(self, path):
        path = path
        if path[1] != ':':
            raise Exception('oops')
        path = '/' + path[0] + path[2:].replace('\\', '/')
        return path

def __get_projects_to_build(opts):
    to_build = ordered_set()
    for p in opts.projects:
        for dep in p.all_dependencies:
            to_build.add(dep)
        to_build.add(p)
    for p in opts.projects_no_deps:
        to_build.add(p)
    return to_build

def build_main():
    opts = get_options()
    print_debug("Options are: %s" % (get_options().__dict__,))
    builder = Builder(opts)
    builder.preprocess()

    to_build = __get_projects_to_build(opts)
    if not to_build:
        error_exit("nothing to do. Use --build or --build-one to specify projects to build, use --list to list available projects")
    print_log("Building %s" % ([p.name for p in to_build],))

    builder.build(to_build)

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Build GTK and friends',
    epilog=
"""
Examples:
    build.py
        Default paths. x86 build.

    build.py -p x64
        Default paths. x64 build.

    build.py --msys-directory D:\msys64 --archives-download-directory C:\hexchat-deps
        Custom paths. x86 build.

    build.py --build libpng --build libffi
        Only builds libpng, libffi, and their dependencies (zlib).

    build.py --build-one glib
        Only builds glib.

    build.py --vs-ver 10 -vs-install-path "C:\Program Files (x86)\Microsoft Visual Studio 10.0" --build gtk3
        Builds gtk3 and its dependencies using VS2010

See also:
    http://hexchat.github.io/gtk-win32/
""")

parser.add_argument('-l', '--list', default=False, action='store_true',
                    help='List available projects and exit.')

parser.add_argument('-p', '--platform', default='x86', choices=['x86', 'x64'],
                    help='Platform to build for, x86 or x64. Default is x86.')
parser.add_argument('-c', '--configuration', default='release', choices=['release', 'debug'],
                    help='Configuration to build, release or debug. Default is release.')
parser.add_argument('--build-dir', default=r'C:\gtk-build',
                    help='The directory where the sources will be downloaded and built.')
parser.add_argument('--msys-dir', default=r'C:\Msys64',
                    help='The directory where you installed msys2.')
parser.add_argument('--archives-download-dir',
                    help="The directory to download the source archives to. It will be created. " +
                         "If a source archive already exists here, it won't be downloaded again. " +
                         "Default is $(build-dir)\\src.")
parser.add_argument('--patches-root-dir',
                    help="The directory where you checked out https://github.com/wingtk/gtk-win32.git. Default is $(build-dir)\\github\\gtk-win32.")
parser.add_argument('--vs-ver', default='12',
                    help="Visual Studio version 10,12, etc. Default is 12.")
parser.add_argument('--vs-install-path',
                    help=r"The directory where you installed Visual Studio. Default is 'C:\Program Files (x86)\Microsoft Visual Studio $(build-ver).0'")
parser.add_argument('--cmake-path', default=r'C:\Program Files (x86)\CMake\bin',
                    help="The directory where you installed cmake.")
parser.add_argument('--perl-dir', default=r'C:\Perl',
                    help="The directory where you installed perl.")
parser.add_argument('--python-dir', default=r'c:\Python27',
                    help="The directory where you installed perl.")

def check_project(p):
    if not p in Project.get_names():
        raise argparse.ArgumentTypeError(
            p + " is not a valid project name, available projects are:\n\t" + "\n\t".join(Project.get_names()))
    return p

parser.add_argument('--build', action='append', default=[], type=check_project, metavar='PROJECT',
                    help="Project(s) you want to be built together with their dependencies")
parser.add_argument('--build-one', action='append', default=[], type=check_project, metavar='PROJECT',
                    help="Project(s) you want to be built without with their dependencies")

parser.add_argument('--clean', default=False, action='store_true',
                    help='Build the project(s) from scratch')

parser.add_argument('-v', '--verbose', default=False, action='store_true',
                    help='Print lots of stuff.')
parser.add_argument('-d', '--debug', default=False, action='store_true',
                    help='Print even more stuff.')
parser.add_argument('--msbuild-opts', default='',
                    help='Command line options to pass to msbuild.')

class Options(object):
    pass

def get_options():
    args = parser.parse_args()

    global global_verbose
    global global_debug

    if args.verbose:
        global_verbose = True
    if args.debug:
        global_verbose = True
        global_debug = True

    if args.list:
        print "Available projects:\n\t" + "\n\t".join(Project.get_names())
        sys.exit(0)

    opts = Options()

    opts.platform = args.platform
    opts.configuration = args.configuration
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

    if not opts.archives_download_dir:
        opts.archives_download_dir = os.path.join(args.build_dir, 'src')
    if not opts.patches_root_dir:
        opts.patches_root_dir = os.path.join(args.build_dir, 'github', 'gtk-win32')
    if not opts.vs_install_path:
        opts.vs_install_path = r'C:\Program Files (x86)\Microsoft Visual Studio %s.0' % (opts.vs_ver,)

    opts.projects = [Project.get_project(x) for x in args.build]
    opts.projects_no_deps = [Project.get_project(x) for x in args.build_one]

    return opts

build_main()
