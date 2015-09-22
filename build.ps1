<#

.SYNOPSIS
This is a build script to build GTK+ 2 and openssl.


.DESCRIPTION
1. Install the requirements mentioned in the README
2. Run this script. Set the parameters, if needed.


.PARAMETER Configuration
The configuration to be built. One of the following:
x86       - 32-bit build.
x64       - 64-bit build. Uses the 32-bit cross-compiler with VS Express or the native 64-bit compiler with VS Professional and up.


.PARAMETER DisableParallelBuild
Setting this to $true forces the items to be built one after the other.


.PARAMETER BuildDirectory
The directory where the sources will be downloaded and built.


.PARAMETER Msys2Directory
The directory where you installed msys2.


.PARAMETER ArchivesDownloadDirectory
The directory to download the source archives to. It will be created. If a source archive already exists here, it won't be downloaded again.


.PARAMETER PatchesRootDirectory
The directory where you checked out https://github.com/nice-software/gtk-win32.git


.PARAMETER VSInstallPath
The directory where you installed Visual Studio.


.PARAMETER VSVer
Visual Studio version 10,12, etc

.PARAMETER CMakePath
The directory where you installed cmake.


.PARAMETER PerlDirectory
The directory where you installed perl.


.PARAMETER OnlyBuild
A subset of the items you want built.


.EXAMPLE
build.ps1
Default paths. x86 build.


.EXAMPLE
build.ps1 -Configuration x64
Default paths. x64 build.


.EXAMPLE
build.ps1 -DisableParallelBuild
Default paths. Items are built one at a time. x86 build.


.EXAMPLE
build.ps1 -Msys2Directory D:\msys64 -ArchivesDownloadDirectory C:\hexchat-deps
Custom paths. x86 build.


.EXAMPLE
build.ps1 -OnlyBuild libpng
Only builds libpng and its dependencies (zlib).

.EXAMPLE
.\build.ps1 -VSVer 10 -VSInstallPath 'C:\Program Files (x86)\Microsoft Visual Studio 10.0' -OnlyBuild gtk3
Builds gtk3 and its dependencies using VS2010

.LINK
http://hexchat.github.io/gtk-win32/

#>

#Requires -version 4.0

#========================================================================================================================================================
# Parameters begin here
#========================================================================================================================================================

param (
	[string][ValidateSet('x86', 'x64')]
	$Configuration = 'x86',

	[switch]
	$DisableParallelBuild = $false,

	[string]
	$BuildDirectory = 'C:\gtk-build',

	[string]
	$Msys2Directory = 'C:\msys64',

	[string]
	$ArchivesDownloadDirectory = "$BuildDirectory\src",

	[string]
	$PatchesRootDirectory = "$BuildDirectory\github\gtk-win32",

	[string]
	$VSInstallPath = 'C:\Program Files (x86)\Microsoft Visual Studio 12.0',

	[string]
	$CMakePath = 'C:\Program Files (x86)\CMake\bin',

	[string]
	$VSVer = '12',

	[string]
	$PerlDirectory = "$BuildDirectory\perl-5.20",

	[string[]][ValidateSet('atk', 'cairo', 'enchant', 'fontconfig', 'freetype', 'gdk-pixbuf', 'gettext-runtime', 'glib', 'gtk', 'gtk3', 'harfbuzz', 'libffi', 'libpng', 'libxml2', 'openssl', 'pango', 'pixman', 'win-iconv', 'zlib', 'libdb', 'cyrus-sasl')]
	$OnlyBuild = @()
)

#========================================================================================================================================================
# Parameters end here
#========================================================================================================================================================

#========================================================================================================================================================
# Source URLs begin here
#========================================================================================================================================================

$items = @{
	'atk' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/atk-2.16.0.tar.xz'
		'Dependencies' = @('glib')
	};

	'cairo' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/cairo-1.14.2.tar.xz'
		'Dependencies' = @('fontconfig', 'glib', 'pixman')
	};

	'enchant' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/enchant-1.6.0.tar.gz'
		'Dependencies' = @('glib')
	};

	'fontconfig' = @{
		'ArchiveUrl' = 'http://fontconfig.org/release/fontconfig-2.11.1.tar.gz'
		'Dependencies' = @('freetype', 'libxml2')
	};

	'freetype' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/freetype-2.6.tar.bz2'
		'Dependencies' = @()
	};

	'gdk-pixbuf' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gdk-pixbuf-2.30.8.tar.xz'
		'Dependencies' = @('glib', 'libpng')
	};

	'gettext-runtime' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gettext-vc100-0.18-src.tar.bz2'
		'Dependencies' = @('win-iconv')
	};

	'glib' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/glib-2.44.1.tar.xz'
		'Dependencies' = @('gettext-runtime', 'libffi', 'zlib')
	};

	'gtk' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gtk+-2.24.28.tar.xz'
		'Dependencies' = @('atk', 'gdk-pixbuf', 'pango')
	};

	'gtk3' = @{
		'ArchiveUrl' = 'http://ftp.acc.umu.se/pub/gnome/sources/gtk+/3.14/gtk+-3.14.11.tar.xz';
		'Dependencies' = @('atk', 'gdk-pixbuf', 'pango')
	};

	'harfbuzz' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/harfbuzz-0.9.41.tar.bz2'
		'Dependencies' = @('freetype', 'glib')
	};

	'libffi' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libffi-3.2.1.tar.gz'
		'Dependencies' = @()
	};

	'libpng' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libpng-1.6.17.tar.xz'
		'Dependencies' = @('zlib')
	};

	'libxml2' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libxml2-2.9.2.tar.gz'
		'Dependencies' = @('win-iconv')
	};

	'openssl' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/openssl-1.0.2d.tar.gz'
		'Dependencies' = @()
	};

	'pango' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/pango-1.36.8.tar.xz'
		'Dependencies' = @('cairo', 'harfbuzz')
	};

	'pixman' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/pixman-0.32.6.tar.gz'
		'Dependencies' = @('libpng')
	};

	'win-iconv' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.6.tar.bz2'
		'Dependencies' = @()
	};

	'zlib' = @{
		'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/zlib-1.2.8.tar.xz'
		'Dependencies' = @()
	};

	'libdb' = @{
		'ArchiveUrl' = 'http://download.oracle.com/berkeley-db/db-5.3.28.tar.gz'
		'Dependencies' = @()
	};

	'cyrus-sasl' = @{
		'ArchiveUrl' = 'ftp://ftp.cyrusimap.org/cyrus-sasl/cyrus-sasl-2.1.26.tar.gz'
		'Dependencies' = @('libdb', 'openssl')
	};
}

#========================================================================================================================================================
# Source URLs end here
#========================================================================================================================================================

#========================================================================================================================================================
# Build steps begin here
#========================================================================================================================================================

$items['atk'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vs$VSVer\atk.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\atk
	Copy-Item .\COPYING $packageDestination\share\doc\atk

	Package $packageDestination
}

$items['cairo'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild msvc\vc$VSVer\cairo.sln /p:Platform=$platform /p:Configuration=Release_FC /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\cairo
	Copy-Item .\COPYING $packageDestination\share\doc\cairo

	Package $packageDestination
}

$items['enchant'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Push-Location .\src

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec nmake -f makefile.mak clean
	Exec nmake -f makefile.mak DLL=1 $(if ($filenameArch -eq 'x64') { 'X64=1' }) MFLAGS=-MD GLIBDIR=..\..\..\..\gtk\$platform\include\glib-2.0

	[void] (Swap-Environment $originalEnvironment)

	Pop-Location

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		.\bin\release\enchant.exe, `
		.\bin\release\pdb\enchant.pdb, `
		.\bin\release\enchant-lsmod.exe, `
		.\bin\release\pdb\enchant-lsmod.pdb, `
		.\bin\release\test-enchant.exe, `
		.\bin\release\pdb\test-enchant.pdb, `
		.\bin\release\libenchant.dll, `
		.\bin\release\pdb\libenchant.pdb `
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
		.\bin\release\libenchant.lib `
		$packageDestination\lib
	Copy-Item `
		.\bin\release\libenchant_ispell.dll, `
		.\bin\release\libenchant_ispell.lib, `
		.\bin\release\pdb\libenchant_ispell.pdb, `
		.\bin\release\libenchant_myspell.dll, `
		.\bin\release\libenchant_myspell.lib, `
		.\bin\release\pdb\libenchant_myspell.pdb `
		$packageDestination\lib\enchant

	New-Item -Type Directory $packageDestination\share\doc\enchant
	Copy-Item .\COPYING.LIB $packageDestination\share\doc\enchant\COPYING

	Package $packageDestination
}

$items['fontconfig'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Exec $patch -p1 -i fontconfig.patch

	#make the fontconfig files work on other compatible vs versions
	Get-ChildItem "$PWD" -Filter *.vcxproj | `
	Foreach-Object{
		$file = $_.FullName
		(Get-Content $file | ForEach-Object { $_ -replace "<PlatformToolset>FIXME</PlatformToolset>", "<PlatformToolset>v${VSVer}0</PlatformToolset>" } ) | Set-Content $file
	}

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild fontconfig.sln /p:Platform=$platform /p:Configuration=Release /t:build /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	switch ($filenameArch) {
		'x86' {
			$releaseDirectory = '.\Release'
		}

		'x64' {
			$releaseDirectory = '.\x64\Release'
		}
	}

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		$releaseDirectory\fontconfig.dll, `
		$releaseDirectory\fontconfig.pdb, `
		$releaseDirectory\fc-cache.exe, `
		$releaseDirectory\fc-cache.pdb, `
		$releaseDirectory\fc-cat.exe, `
		$releaseDirectory\fc-cat.pdb, `
		$releaseDirectory\fc-list.exe, `
		$releaseDirectory\fc-list.pdb, `
		$releaseDirectory\fc-match.exe, `
		$releaseDirectory\fc-match.pdb, `
		$releaseDirectory\fc-query.exe, `
		$releaseDirectory\fc-query.pdb, `
		$releaseDirectory\fc-scan.exe, `
		$releaseDirectory\fc-scan.pdb `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\etc\fonts
	Copy-Item `
		.\fonts.conf, `
		.\fonts.dtd `
		$packageDestination\etc\fonts

	New-Item -Type Directory $packageDestination\include\fontconfig
	Copy-Item `
		.\fontconfig\fcfreetype.h, `
		.\fontconfig\fcprivate.h, `
		.\fontconfig\fontconfig.h `
		$packageDestination\include\fontconfig

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		$releaseDirectory\fontconfig.lib `
		$packageDestination\lib

	New-Item -Type Directory $packageDestination\share\doc\fontconfig
	Copy-Item .\COPYING $packageDestination\share\doc\fontconfig

	Package $packageDestination
}

$items['freetype'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild builds\windows\vc$VSVer\freetype.vcxproj /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\include
	Copy-Item -Recurse `
		.\include\* `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		".\objs\$platform\freetype.lib" `
		$packageDestination\lib

	New-Item -Type Directory $packageDestination\share\doc\freetype
	Copy-Item .\docs\LICENSE.TXT $packageDestination\share\doc\freetype\COPYING

	Package $packageDestination
}

$items['gdk-pixbuf'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vc$VSVer\gdk-pixbuf.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\gdk-pixbuf
	Copy-Item .\COPYING $packageDestination\share\doc\gdk-pixbuf

	Package $packageDestination
}

$items['gettext-runtime'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Exec $patch -p1 -i gettext-runtime.patch

	Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	$env:PATH += ";$CMakePath"
	Exec cmake -G 'NMake Makefiles' "-DCMAKE_INSTALL_PREFIX=`"$packageDestination`"" -DCMAKE_BUILD_TYPE=Release "-DICONV_INCLUDE_DIR=`"$packageDestination\..\..\..\gtk\$platform\include`"" "-DICONV_LIBRARIES=`"$packageDestination\..\..\..\gtk\$platform\lib\iconv.lib`""
	Exec nmake clean
	Exec nmake
	Exec nmake install
	Exec nmake clean

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\gettext
	Copy-Item .\COPYING $packageDestination\share\doc\gettext

	Package $packageDestination
}

$items['glib'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Exec $patch -p1 -i glib-if_nametoindex.patch
	Exec $patch -p1 -i glib-package-installation-directory.patch
	Exec $patch -p1 -i g-win32-command-line-1.patch
	Exec $patch -p1 -i g-win32-command-line-2.patch
	Exec $patch -p1 -i 0001-Change-message-system-to-use-fputs-instead-of-write.patch
	Exec $patch -p1 -i Add-gsystemthreadsetname-implementation-for-W32-th.patch

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vs$VSVer\glib.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\glib
	Copy-Item .\COPYING $packageDestination\share\doc\glib

	Package $packageDestination
}

$items['gtk'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Exec $patch -p1 -i gtk-revert-scrolldc-commit.patch
	Exec $patch -p1 -i gtk-bgimg.patch
	Exec $patch -p1 -i gtk-accel.patch
	Exec $patch -p1 -i gtk-multimonitor.patch

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vs12\gtk+.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\locale

	Push-Location .\po
	Get-ChildItem *.po | %{
		New-Item -Type Directory "$packageDestination\share\locale\$($_.BaseName)\LC_MESSAGES"
		Exec $msgfmt -co "$packageDestination\share\locale\$($_.BaseName)\LC_MESSAGES\gtk20.mo" $_.Name
	}
	Pop-Location

	New-Item -Type Directory $packageDestination\share\doc\gtk
	Copy-Item .\COPYING $packageDestination\share\doc\gtk

	Package $packageDestination
}

$items['gtk3'].BuildScript = {
	$packageDestination = "$PWD\..\gtk-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vs$VSVer\gtk+.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\locale

	Push-Location .\po
	Get-ChildItem *.po | %{
		New-Item -Type Directory "$packageDestination\share\locale\$($_.BaseName)\LC_MESSAGES"
		Exec $msgfmt -co "$packageDestination\share\locale\$($_.BaseName)\LC_MESSAGES\gtk30.mo" $_.Name
	}
	Pop-Location

	New-Item -Type Directory $packageDestination\share\doc\gtk
	Copy-Item .\COPYING $packageDestination\share\doc\gtk

	Package $packageDestination
}

$items['harfbuzz'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	#make the fontconfig files work on other compatible vs versions
	Get-ChildItem "$PWD\win32" -Filter *.vcxproj | `
	Foreach-Object{
		$file = $_.FullName
		(Get-Content $file | ForEach-Object { $_ -replace "<PlatformToolset>FIXME</PlatformToolset>", "<PlatformToolset>v${VSVer}0</PlatformToolset>" } ) | Set-Content $file
	}

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild win32\harfbuzz.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		.\win32\libs\Release\harfbuzz.dll, `
		.\win32\libs\Release\harfbuzz.pdb `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\include
	Copy-Item `
		.\src\*.h `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		.\win32\libs\harfbuzz\Release\harfbuzz.lib `
		$packageDestination\lib

	New-Item -Type Directory $packageDestination\share\doc\harfbuzz
	Copy-Item .\COPYING $packageDestination\share\doc\harfbuzz

	Package $packageDestination
}

$items['libffi'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Exec $patch -p1 -i libffi-msvc-complex.patch
	Exec $patch -p1 -i libffi-win64-jmp.patch

	switch ($filenameArch) {
		'x86' {
			$buildDestination = 'i686-pc-mingw32'
		}

		'x64' {
			$buildDestination = 'x86_64-w64-mingw32'
		}
	}

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vs$VSVer\libffi.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\include
	Copy-Item `
		.\$buildDestination\include\ffi.h, `
		.\src\x86\ffitarget.h `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\share\doc\libffi
	Copy-Item .\LICENSE $packageDestination\share\doc\libffi

	Package $packageDestination
}

$items['libpng'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild projects\vc$VSVer\pnglibconf\pnglibconf.vcxproj /p:Platform=$platform /p:Configuration=Release /p:SolutionDir=$PWD\projects\vc$VSVer\ /nodeReuse:True
	Exec msbuild projects\vc$VSVer\libpng\libpng.vcxproj /p:Platform=$platform /p:Configuration=Release /p:SolutionDir=$PWD\projects\vc$VSVer\ /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	switch ($filenameArch) {
		'x86' {
			$releaseDirectory = ".\projects\vc$VSVer\Release"
		}

		'x64' {
			$releaseDirectory = ".\projects\vc$VSVer\x64\Release"
		}
	}

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		$releaseDirectory\libpng16.dll, `
		$releaseDirectory\libpng16.pdb `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\include
	Copy-Item `
		.\png.h, `
		.\pngconf.h, `
		.\pnglibconf.h, `
		.\pngpriv.h `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		$releaseDirectory\libpng16.lib `
		$packageDestination\lib

	New-Item -Type Directory $packageDestination\share\doc\libpng
	Copy-Item .\LICENSE $packageDestination\share\doc\libpng\COPYING

	Package $packageDestination
}

$items['libxml2'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild win32\vc$VSVer\libxml2.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		.\lib\libxml2.dll, `
		.\lib\libxml2.pdb, `
		.\lib\runsuite.exe, `
		.\lib\runsuite.pdb `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\include\libxml
	Copy-Item `
		.\win32\VC12\config.h, `
		.\include\wsockcompat.h, `
		.\include\libxml\*.h `
		$packageDestination\include\libxml

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		.\lib\libxml2.lib `
		$packageDestination\lib

	New-Item -Type Directory $packageDestination\share\doc\libxml2
	Copy-Item .\COPYING $packageDestination\share\doc\libxml2

	Package $packageDestination
}

$items['openssl'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	$env:PATH += ";$PerlDirectory\$platform\bin;$Msys2Directory\usr\bin"

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
}

$items['pango'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Exec $patch -p1 -i pango-synthesize-fonts-properly.patch

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vs$VSVer\pango.sln /p:Platform=$platform /p:Configuration=Release_FC /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\pango
	Copy-Item .\COPYING $packageDestination\share\doc\pango

	Package $packageDestination
}

$items['pixman']['BuildScript'] = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$exports = Get-ChildItem -Recurse *.c, *.h | Select-String -Pattern 'PIXMAN_EXPORT' -Encoding UTF8 | %{
		$content = Get-Content -Encoding UTF8 $_.Path
		"$($content[$_.LineNumber - 1]) $($content[$_.LineNumber])"
	} | ?{
		$_ -like 'PIXMAN_EXPORT *'
	} | %{
		if ($_ -match 'PIXMAN_EXPORT (?:const )?\S+ (?:\* )?(PREFIX(?: ?)\()?([^\s\(\)]+)') {
			if ($Matches[1] -eq $null) {
				$Matches[2]
			}
			else {
				"pixman_region$($Matches[2])"
				"pixman_region32$($Matches[2])"
			}
		}
	} | ? {
		-not ($_ -like '_pixman*')
	}

	$exports += 'prng_srand_r'
	$exports += 'prng_randmemset_r'

	$exports | Sort-Object -Unique | Out-File -Encoding OEM .\pixman\pixman.symbols

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vc$VSVer\pixman.vcxproj /p:Platform=$platform /p:Configuration=Release /p:SolutionDir=$PWD\build\win32\vc$VSVer\ /maxcpucount /nodeReuse:True
	Exec msbuild build\win32\vc$VSVer\install.vcxproj /p:Platform=$platform /p:Configuration=Release /p:SolutionDir=$PWD\build\win32\vc$VSVer\ /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\pixman
	Copy-Item .\COPYING $packageDestination\share\doc\pixman

	Package $packageDestination
}

$items['win-iconv'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Exec $patch -p2 -i win-iconv-r38.patch
	Exec $patch -p1 -i win-iconv-revert-r32.patch

	Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	$env:PATH += ";$CMakePath"

	Exec cmake -G 'NMake Makefiles' "-DCMAKE_INSTALL_PREFIX=`"$packageDestination`"" -DCMAKE_BUILD_TYPE=Release
	Exec nmake clean
	Exec nmake
	Exec nmake install
	Exec nmake clean

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\share\doc\win-iconv
	Copy-Item .\COPYING $packageDestination\share\doc\win-iconv

	Package $packageDestination
}

$items['zlib'].BuildScript = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build\win32\vs$VSVer\zlib.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	Push-Location ".\build\vs$VSVer\Release\$platform"

	New-Item -Type Directory $packageDestination\include
	Copy-Item `
		.\include\zlib.h, `
		.\include\zconf.h `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		.\bin\zlib1.dll, `
		.\bin\zlib1.pdb  `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\lib
	Copy-Item .\lib\zlib1.lib $packageDestination\lib

	Pop-Location

	New-Item -Type Directory $packageDestination\share\doc\zlib
	Copy-Item .\README $packageDestination\share\doc\zlib

	Package $packageDestination
}

$items['libdb'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec msbuild build_windows\Berkeley_DB_vs20$VSVer.sln /p:Platform=$platform /p:Configuration="Static Release" /maxcpucount /nodeReuse:True

	[void] (Swap-Environment $originalEnvironment)

	New-Item -Type Directory $packageDestination\include
	Copy-Item `
		.\build_windows\db.h, `
		.\build_windows\db_config.h, `
		.\build_windows\db_cxx.h, `
		.\build_windows\db_int.h, `
		.\build_windows\clib_port.h `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\lib
	Copy-Item .\build_windows\$platform\"Static Release"\* $packageDestination\lib

	Package $packageDestination
}

$items['cyrus-sasl'].BuildScript = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	$originalEnvironment = Swap-Environment $vcvarsEnvironment

	Exec nmake /f NTMakefile clean
	Exec nmake /f NTMakefile DB_INCLUDE=`"$packageDestination\..\..\..\gtk\$platform\include`" DB_LIBPATH=`"$packageDestination\..\..\..\gtk\$platform\lib`" DB_LIB=libdb53s.lib OPENSSL_INCLUDE=`"$packageDestination\..\..\..\gtk\$platform\include`" OPENSSL_LIBPATH=`"$packageDestination\..\..\..\gtk\$platform\lib`"
	Exec nmake /f NTMakefile install prefix=`"$packageDestination`"

	[void] (Swap-Environment $originalEnvironment)

	Package $packageDestination
}

#========================================================================================================================================================
# Build steps end here
#========================================================================================================================================================


$patch = "$Msys2Directory\usr\bin\patch.exe"
if (-not $(Test-Path $patch)) {
	throw "$patch not found. Please check that you installed patch in msys2 using ``pacman -S patch``"
}

$tar = "$Msys2Directory\usr\bin\tar.exe"
if (-not $(Test-Path $tar)) {
	throw "$tar not found. Please check that you installed tar and other unzipping tools in msys2 using ``pacman -S gzip tar xz``"
}

$msgfmt = "$Msys2Directory\usr\bin\msgfmt.exe"
if (-not $(Test-Path $msgfmt)) {
	throw "$msgfmt not found. Please check that you installed msgfmt in msys2 using ``pacman -S gettext``"
}

# Verify VS exists at the indicated location, and that it supports the required target
switch ($Configuration) {
	'x86' {
		$vcvarsBat = "$VSInstallPath\VC\bin\vcvars32.bat"
	}

	'x64' {
		$vcvarsBat = "$VSInstallPath\VC\bin\amd64\vcvars64.bat"

		# make sure it works even with VS Express
		if (-not $(Test-Path $vcvarsBat)) {
			$vcvarsBat = "$VSInstallPath\VC\bin\x86_amd64\vcvarsx86_amd64.bat"
		}
	}
}

if (-not $(Test-Path $vcvarsBat)) {
	throw "`"$vcvarsBat`" could not be found. Please check you have Visual Studio installed at `"$VSInstallPath`" and that it supports the configuration `"$Configuration`"."
}

$vcvarsEnvironment = @{}
$(&cmd /C "`"$vcvarsBat`" > NUL && SET") | %{
	$keyValuePair = $_.Split('=', 2)
	$vcvarsEnvironment[$keyValuePair[0]] = $keyValuePair[1]
}

switch ($Configuration) {
	'x86' {
		$platform = 'Win32'
		$filenameArch = 'x86'
	}

	'x64' {
		$platform = 'x64'
		$filenameArch = 'x64'
	}
}

$workingDirectory = "$BuildDirectory\build\$platform"


# Set up additional properties on the items
$items.GetEnumerator() | %{
	$name = $_.Key
	$item = $_.Value

	$archiveUrl = $item.ArchiveUrl

	$filename = New-Object System.Uri $archiveUrl
	$filename = $filename.Segments[$filename.Segments.Length - 1]

	$item = $items[$name]

	$item.Name = $name
	$item.ArchiveFile = New-Object System.IO.FileInfo "$ArchivesDownloadDirectory\$filename"
	$item.PatchDirectory = $(New-Object System.IO.DirectoryInfo "$PatchesRootDirectory\$name")
	$item.BuildDirectory = New-Object System.IO.DirectoryInfo "$workingDirectory\$name"
	$item.Dependencies = @($item.Dependencies | %{ $items[$_] })
	$item.Dependents = @()
	$item.State = ''
}

$items.GetEnumerator() | %{
	$item = $_.Value

	$item.Dependencies | %{ $items[$_.Name].Dependents += $item }
}


# If OnlyBuild is not an empty array, only keep the items that are specified
if ($OnlyBuild.Length -gt 0) {
	$newItems = @{}

	$queue = New-Object System.Collections.Generic.Queue[string] (, $OnlyBuild)

	while ($queue.Count -gt 0) {
		$itemName = $queue.Dequeue()
		$item = $items[$itemName]

		$newItems[$itemName] = $item

		$item.Dependencies | %{
			if ($newItems[$_.Name] -eq $null) {
				$queue.Enqueue($_.Name)
			}
		}
	}

	$items = $newItems
}


New-Item -Type Directory $ArchivesDownloadDirectory -ErrorAction Ignore


New-Item -Type Directory $workingDirectory -ErrorAction Ignore
Copy-Item $PatchesRootDirectory\stack.props $workingDirectory


$logDirectory = "$workingDirectory\logs"
New-Item -Type Directory $logDirectory -ErrorAction Ignore
Remove-Item $logDirectory\*.log


New-Item -Type Directory $workingDirectory\..\..\gtk\$platform -ErrorAction Ignore


# For each item, start a job to download the source archives, extract them to $workingDirectory, and copy over the stuff from gtk-win32
Write-Host "Downloading and extracting source archives to $workingDirectory"

$items.GetEnumerator() | %{
	$item = $_.Value

	$item.State = 'Downloading and extracting'

	[void] (Start-Job -Name $item.Name -InitializationScript {
		function Exec {
			$name, $arguments = @($args)
			$arguments = @($arguments | ?{ $_ -ne $null })
			&$name @arguments
			[void] ($LASTEXITCODE -and $(throw "$name $arguments exited with code $LASTEXITCODE"))
		}

		function ConvertTo-Msys2Path ([string] $Path) {
			([regex] '^([a-zA-Z]):').Replace(($Path -replace '\\', '/'), { "/$($args[0].Groups[1].Value.ToLower())" })
		}
	} -ArgumentList $item {
		param ($item)

		$ArchivesDownloadDirectory = $using:ArchivesDownloadDirectory
		$Msys2Directory = $using:Msys2Directory
		$tar = $using:tar
		$workingDirectory = $using:workingDirectory

		'Beginning job to download and extract'

		# BaseName, etc. properties of FileInfo properties are available on the PSObject. Convert it back to a FileInfo.
		$item.ArchiveFile = New-Object System.IO.FileInfo $item.ArchiveFile

		if ($item.ArchiveFile.Exists) {
			"$($item.ArchiveFile) already exists"
		}
		else {
			"$($item.ArchiveFile) doesn't exist. Downloading..."

			$ProgressPreference = 'SilentlyContinue'
			Invoke-WebRequest $item.ArchiveUrl -OutFile $item.ArchiveFile
			$ProgressPreference = 'Continue'

			"Downloaded $($item.ArchiveUrl)"
		}

		"Extracting $($item.ArchiveFile.Name) to $workingDirectory"

		$env:PATH += ";$Msys2Directory\usr\bin"

		if ($item.Name -ne 'gettext-runtime') {
			Exec $tar xf $(ConvertTo-Msys2Path $item.ArchiveFile) -C $(ConvertTo-Msys2Path $workingDirectory)

			$outputDirectoryName = [System.IO.Path]::GetFilenameWithoutExtension($item.ArchiveFile.BaseName)

			while (Test-Path "$workingDirectory\$outputDirectoryName") {
				Move-Item "$workingDirectory\$outputDirectoryName" $item.BuildDirectory
				Sleep 1
			}
		}
		else {
			# gettext-runtime is a tarbomb
			[void] (New-Item -Type Directory $item.BuildDirectory)
			Exec $tar xf $(ConvertTo-Msys2Path $item.ArchiveFile) -C $(ConvertTo-Msys2Path $item.BuildDirectory)
		}

		"Extracted $($item.ArchiveFile.Name)"

		Copy-Item "$($item.PatchDirectory)\*" $item.BuildDirectory -Recurse -Force
		"Copied patch contents from $($item.PatchDirectory) to $($item.BuildDirectory)"
	})
}

# While the jobs are running...
do {
	# Log their output
	Get-Job | %{
		$job = $_

		@(Receive-Job $job 2>&1) | %{
			if ($_ -isnot [System.Management.Automation.ErrorRecord]) {
				Write-Host "$($job.Name) : $_"
			}
			else {
				$Host.UI.WriteErrorLine("$($job.Name) : $($_.Exception.Message)")
			}
		}

		if (($job.State -eq 'Completed') -and (-not $job.HasMoreData)) {
			$items[$job.Name].State = 'Pending'

			Remove-Job $job
		}
		elseif (($job.State -eq 'Failed') -and (-not $job.HasMoreData)) {
			Write-Host "$($job.Name) : Failed"

			$items[$job.Name].State = 'Failed'

			Remove-Job $job
		}
	}

	# Sleep a bit and then try again
	Start-Sleep 1
} while (@(Get-Job).Length -gt 0)

if (@($items.GetEnumerator() | ?{ $_.Value.State -eq 'Failed' }).Length -gt 0) {
	Write-Error 'One or more source archives could not be downloaded or extracted.'
	exit 1
}

Write-Host 'Downloaded and extracted all source archives.'


# Until all items have been built
while (@($items.GetEnumerator() | ?{ ($_.Value.State -eq 'Pending') -or ($_.Value.State -eq 'Building') }).Length -gt 0) {
	# If another job can be started - either parallel build is enabled, or it's disabled and there is no running build job), and there are no failed jobs...
	if (
		(-not $DisableParallelBuild -or $(Get-Job) -eq $null) -and
		(@($items.GetEnumerator() | ?{ $_.Value.State -eq 'Failed' }).Length -eq 0)
	) {
		# Find an item which hasn't already been built, isn't being built currently, and whose dependencies have all been built
		$nextPendingItem =
			@($items.GetEnumerator() | ?{
				$item = $_.Value

				if ($item.State -ne 'Pending') {
					return $false
				}

				$remainingDependencies = @($item.Dependencies | ?{ $items[$_.Name].State -ne 'Completed' })
				return $remainingDependencies.Length -eq 0
			} | %{ $_.Value })[0]

		# If such an item exists...
		if ($nextPendingItem -ne $null) {
			$nextPendingItem.State = 'Building'

			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($nextPendingItem.Name) : Started"
			Write-Host "$($nextPendingItem.Name) : Started"

			# Start a job to build it
			[void] (Start-Job -Name $nextPendingItem.Name -InitializationScript {
				function Swap-Environment([HashTable] $newEnvironment) {
					$originalEnvironment = @{}

					Get-ChildItem Env: | %{ $originalEnvironment[$_.Name] = $_.Value }

					$originalEnvironment.GetEnumerator() | %{ Remove-Item "env:$($_.Key)" }

					$newEnvironment.GetEnumerator() | %{ [System.Environment]::SetEnvironmentVariable($_.Key, $_.Value) }

					return $originalEnvironment
				}

				function Exec {
					$name, $arguments = @($args)
					$arguments = @($arguments | ?{ $_ -ne $null })
					&$name @arguments
					[void] ($LASTEXITCODE -and $(throw "$name $arguments exited with code $LASTEXITCODE"))
				}

				# Add utf-8 BOM and execution charset pragma to the given file because cl.exe throws C4819 otherwise
				function Fix-C4819([string] $filename) {
					$contents = Get-Content $filename -Encoding UTF8
					$contents = @('#pragma execution_character_set("utf-8")', '') + $contents
					Out-File $filename -InputObject $contents -Encoding UTF8
				}

				function Package([string] $directory) {
					Copy-Item -Recurse -Force $directory\* $workingDirectory\..\..\gtk\$platform

					Remove-Item -Recurse $directory
				}
			} -ArgumentList $nextPendingItem {
				param ($item)

				$BuildDirectory = $using:BuildDirectory
				$CMakePath = $using:CMakePath
				$Configuration = $using:Configuration
				$filenameArch = $using:filenameArch
				$Msys2Directory = $using:Msys2Directory
				$patch = $using:patch
				$PerlDirectory = $using:PerlDirectory
				$platform = $using:platform
				$vcvarsEnvironment = $using:vcvarsEnvironment
				$VSInstallPath = $using:VSInstallPath
				$VSVer = $using:VSVer
				$workingDirectory = $using:workingDirectory

				Set-Location $item.BuildDirectory

				Invoke-Command ([ScriptBlock] [ScriptBlock]::Create($item.BuildScript))
			})
		}
	}

	# For each job...
	Get-Job | %{
		$job = $_

		# Log all its output
		@(Receive-Job $job 2>&1) | %{
			if ($_ -isnot [System.Management.Automation.ErrorRecord]) {
				Write-Host "$($job.Name) : $_"
			}
			else {
				$Host.UI.WriteErrorLine("$($job.Name) : $($_.Exception.Message)")
			}

			Out-File -Append -Encoding OEM -FilePath "$logDirectory\$($job.Name).log" -InputObject $_
		}

		# If the job has been completed...
		if (($job.State -eq 'Completed') -and (-not $job.HasMoreData)) {
			$items[$job.Name].State = 'Completed'

			Write-Host "$($job.Name) : Completed"
			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($job.Name) : Completed"

			# Delete the job
			Remove-Job $job
		}

		elseif (($job.State -eq 'Failed') -and (-not $job.HasMoreData)) {
			$items[$job.Name].State = 'Failed'

			$items.GetEnumerator() | %{
				$item = $_.Value

				if ($item.State -eq 'Pending') {
					$item.State = 'Cancelled'
				}
			}

			Write-Host "$($job.Name) : Failed"
			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($job.Name) : Failed"

			# Delete the job
			Remove-Job $job
		}
	}

	# Sleep a bit and then try again
	Start-Sleep 1
}

$itemStateGroups = @{}
$items.GetEnumerator() | %{ $_.Value } | Group-Object -Property { $_.State } | %{ $itemStateGroups[$_.Name] = $_.Group | Sort-Object -Property { $_.Name } }

if ($itemStateGroups.Completed.Length -gt 0) {
	Write-Host ''
	Write-Host 'The following items were successfully built:'

	$itemStateGroups.Completed | %{ Write-Host $_.Name }
}

if ($itemStateGroups.Failed.Length -gt 0) {
	Write-Host ''
	Write-Host 'The following items failed to build:'

	$itemStateGroups.Failed | %{ Write-Host $_.Name }
}

if ($itemStateGroups.Cancelled.Length -gt 0) {
	Write-Host ''
	Write-Host 'The following items were not built because one or more of the other items failed to build:'

	$itemStateGroups.Cancelled | %{ Write-Host $_.Name }
}

if ($itemStateGroups.Failed.Length -gt 0) {
	exit 1
}
