<#

.SYNOPSIS
This is a build script to build GTK+ and openssl.


.DESCRIPTION
1. Install mozilla-build, cmake, nasm, perl, msgfmt as per http://gtk.hexchat.org/
2. Clone https://github.com/hexchat/gtk-win32.git
3. Run this script. Set the parameters, if needed.


.PARAMETER Configuration
The configuration to be built. One of the following:
x86       - 32-bit build.
x86_amd64 - 64-bit build using the 32-bit cross-compiler. Use this if you have VS Express.
x64       - 64-bit build using the native 64-bit compiler. Not available in VS Express.


.PARAMETER DisableParallelBuild
Setting this to $true forces the items to be built one after the other.


.PARAMETER MozillaBuildDirectory
The directory where you installed Mozilla Build.


.PARAMETER ArchivesDownloadDirectory
The directory to download the source archives to. It will be created. If a source archive already exists here, it won't be downloaded again.


.PARAMETER PatchesRootDirectory
The directory where you checked out https://github.com/hexchat/gtk-win32.git


.PARAMETER VSInstallPath
The directory where you installed Visual Studio.


.PARAMETER Wget
The path to any downloader. It is invoked as &$Wget "$url" and should output a file in the current directory.


.PARAMETER Patch
The path to a patch.exe binary.


.PARAMETER SevenZip
The path to a 7-zip executable. Do not use the one provided by Mozilla Build as it's too old and will not work.


.PARAMETER CMakePath
The directory where you installed cmake.


.PARAMETER OnlyBuild
A subset of the items you want built.


.EXAMPLE
build.ps1
Default paths. x86 build.


.EXAMPLE
build.ps1 -Configuration x86_amd64
Default paths. x64 build using the x64 cross compiler.


.EXAMPLE
build.ps1 -Configuration x64
Default paths. x64 build using the x64 native compiler.


.EXAMPLE
build.ps1 -DisableParallelBuild
Default paths. Items are built one at a time. x86 build.


.EXAMPLE
build.ps1 -MozillaBuildDirectory D:\mozilla-build -ArchivesDownloadDirectory C:\hexchat-deps -SevenZip C:\Downloads\7-Zip\7za.exe
Custom paths. x86 build.


.EXAMPLE
build.ps1 -OnlyBuild openssl
Only builds openssl and its dependencies (zlib).


.LINK
http://gtk.hexchat.org/

#>

#========================================================================================================================================================
# Parameters begin here
#========================================================================================================================================================

param (
	[string][ValidateSet('x86', 'x86_amd64', 'x64')]
	$Configuration = 'x86',

	[switch]
	$DisableParallelBuild = $false,

	[string]
	$MozillaBuildDirectory = 'C:\mozilla-build',

	[string]
	$ArchivesDownloadDirectory = 'C:\mozilla-build\hexchat\src',

	[string]
	$PatchesRootDirectory = 'C:\mozilla-build\hexchat\github\gtk-win32',

	[string]
	$VSInstallPath = 'C:\Program Files (x86)\Microsoft Visual Studio 12.0',

	[string]
	$Wget = "$MozillaBuildDirectory\wget\wget.exe",

	[string]
	$Patch = "$MozillaBuildDirectory\msys\bin\patch.exe",

	[string]
	$SevenZip = 'C:\Program Files\7-Zip\7z.exe',

	[string]
	$CMakePath = 'C:\Program Files (x86)\CMake 2.8\bin',

	[string[]][ValidateSet('atk', 'cairo', 'enchant', 'fontconfig', 'freetype', 'gdk-pixbuf', 'gettext-runtime', 'glib', 'gtk', 'harfbuzz', 'libffi', 'libpng', 'libxml2', 'openssl', 'pango', 'pixman', 'win-iconv', 'zlib')]
	$OnlyBuild = @()
)

#========================================================================================================================================================
# Parameters end here
#========================================================================================================================================================

#========================================================================================================================================================
# Source URLs begin here
#========================================================================================================================================================

$items = @{
	'atk'              = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/atk-2.9.3.7z';            'Dependencies' = @('glib')                              };
	'cairo'            = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/cairo-1.12.14.7z';        'Dependencies' = @('fontconfig', 'glib', 'pixman')      };
	'enchant'          = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/enchant-1.6.0.7z';        'Dependencies' = @('glib')                              };
	'fontconfig'       = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/fontconfig-2.8.0.7z';     'Dependencies' = @('freetype', 'libxml2')               };
	'freetype'         = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/freetype-2.5.0.1.7z';     'Dependencies' = @()                                    };
	'gdk-pixbuf'       = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gdk-pixbuf-2.28.1.7z';    'Dependencies' = @('glib', 'libpng')                    };
	'gettext-runtime'  = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gettext-runtime-0.18.7z'; 'Dependencies' = @('win-iconv')                         };
	'glib'             = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/glib-2.36.2.7z';          'Dependencies' = @('gettext-runtime', 'libffi', 'zlib') };
	'gtk'              = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gtk-2.24.19.7z';          'Dependencies' = @('atk', 'gdk-pixbuf', 'pango')        };
	'harfbuzz'         = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/harfbuzz-0.9.18.7z';      'Dependencies' = @('freetype', 'glib')                  };
	'libffi'           = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libffi-3.0.13.7z';        'Dependencies' = @()                                    };
	'libpng'           = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libpng-1.6.2.7z';         'Dependencies' = @('zlib')                              };
	'libxml2'          = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libxml2-2.9.1.7z';        'Dependencies' = @('win-iconv')                         };
	'openssl'          = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/openssl-1.0.1e.7z';       'Dependencies' = @('zlib')                              };
	'pango'            = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/pango-1.32.5.7z';         'Dependencies' = @('cairo', 'harfbuzz')                 };
	'pixman'           = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/pixman-0.30.2.7z';        'Dependencies' = @('libpng')                            };
	'win-iconv'        = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.6.7z';      'Dependencies' = @()                                    };
	'zlib'             = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/zlib-1.2.8.7z';           'Dependencies' = @()                                    };
}

#========================================================================================================================================================
# Source URLs end here
#========================================================================================================================================================

#========================================================================================================================================================
# Build steps begin here
#========================================================================================================================================================

$items['atk']['BuildScript'] = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'atk' `
		"msbuild build\win32\vc12\atk.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"

	New-Item -Type Directory $packageDestination\share\doc\atk
	Copy-Item .\COPYING $packageDestination\share\doc\atk

	Package $packageDestination
}

$items['cairo']['BuildScript'] = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'cairo' `
		"msbuild msvc\vc12\cairo.sln /p:Platform=$platform /p:Configuration=Release_FC /maxcpucount /nodeReuse:True"

	New-Item -Type Directory $packageDestination\share\doc\cairo
	Copy-Item .\COPYING $packageDestination\share\doc\cairo

	Package $packageDestination
}

$items['enchant']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Push-Location .\src
	VSPrompt -Name 'enchant' `
		'nmake -f makefile.mak clean' `
		"nmake -f makefile.mak DLL=1 $(if ($filenameArch -eq 'x64') { 'X64=1 ' })MFLAGS=-MD GLIBDIR=..\..\..\..\gtk\$platform\include\glib-2.0"
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

$items['fontconfig']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	&$Patch -p1 -i fontconfig.patch

	VSPrompt -Name 'fontconfig' `
		"msbuild fontconfig.sln /p:Platform=$platform /p:Configuration=Release /t:build /nodeReuse:True"


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

$items['freetype']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'freetype' `
		"msbuild builds\win32\vc12\freetype.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"

	New-Item -Type Directory $packageDestination\include
	Copy-Item -Recurse `
		.\include\* `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		".\objs\$platform\vc12\freetype.lib" `
		$packageDestination\lib

	New-Item -Type Directory $packageDestination\share\doc\freetype
	Copy-Item .\docs\LICENSE.TXT $packageDestination\share\doc\freetype\COPYING

	Package $packageDestination
}

$items['gdk-pixbuf']['BuildScript'] = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	&$Patch -p1 -i gdk-pixbuf.patch

	VSPrompt -Name 'gdk-pixbuf' `
		"msbuild build\win32\vc12\gdk-pixbuf.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"

	New-Item -Type Directory $packageDestination\share\doc\gdk-pixbuf
	Copy-Item .\COPYING $packageDestination\share\doc\gdk-pixbuf

	Package $packageDestination
}

$items['gettext-runtime']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	&$Patch -p1 -i gettext-runtime.patch

	Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

	VSPrompt -Name 'gettext-runtime' `
		"SET PATH=%PATH%;$CMakePath" `
		"cmake -G `"NMake Makefiles`" -DCMAKE_INSTALL_PREFIX=`"$packageDestination`" -DCMAKE_BUILD_TYPE=Release -DICONV_INCLUDE_DIR=`"$packageDestination\..\..\..\gtk\$platform\include`" -DICONV_LIBRARIES=`"$packageDestination\..\..\..\gtk\$platform\lib\iconv.lib`"" `
		'nmake clean' `
		'nmake' `
		'nmake install'

	New-Item -Type Directory $packageDestination\share\doc\gettext
	Copy-Item .\COPYING $packageDestination\share\doc\gettext

	VSPrompt -Name 'gettext-runtime-2' `
		'nmake clean'

	Package $packageDestination
}

$items['glib']['BuildScript'] = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'glib' `
		"msbuild build\win32\vc12\glib.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"

	New-Item -Type Directory $packageDestination\share\doc\glib
	Copy-Item .\COPYING $packageDestination\share\doc\glib

	Package $packageDestination
}

$items['gtk']['BuildScript'] = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	&$Patch -p1 -i gtk-revert-scrolldc-commit.patch
	&$Patch -p1 -i gtk-pixmap.patch
	&$Patch -p1 -i gtk-bgimg.patch
	&$Patch -p1 -i gtk-statusicon.patch

	VSPrompt -Name 'gtk' `
		"msbuild build\win32\vc12\gtk+.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"

	Remove-Item -Recurse $packageDestination\share\locale
	New-Item -Type Directory $packageDestination\share\locale

	$oldPath = $env:Path
	$env:Path = "${env:Path};..\..\..\..\..\msgfmt"
	Push-Location .\po
	Get-ChildItem *.po | %{
		New-Item -Type Directory "$packageDestination\share\locale\$($_.BaseName)\LC_MESSAGES"
		&msgfmt -co "$packageDestination\share\locale\$($_.BaseName)\LC_MESSAGES\gtk20.mo" $_.Name
	}
	Pop-Location
	$env:Path = $oldPath

	New-Item -Type Directory $packageDestination\share\doc\gtk
	Copy-Item .\COPYING $packageDestination\share\doc\gtk

	Package $packageDestination
}

$items['harfbuzz']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'harfbuzz' `
		"msbuild win32\harfbuzz.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"


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

$items['libffi']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	switch ($filenameArch) {
		'x86' {
			$buildDestination = 'i686-pc-mingw32'
			$configureCommand = "./configure CC=`$(pwd)/msvcc.sh LD=link CPP='cl -nologo -EP' CFLAGS='-O2' --build=$buildDestination"
		}

		'x64' {
			$buildDestination = 'x86_64-w64-mingw32'
			$configureCommand = "./configure CC=`"`$(pwd)/msvcc.sh -m64`" LD=link CPP='cl -nologo -EP' CFLAGS='-O2' --build=$buildDestination"
		}
	}

	$currentPwd = $PWD
	Push-Location ..\..
	echo "cd $($currentPwd -replace '\\', '\\') && $configureCommand && make clean && make" | &$mozillaBuildStartVC
	Pop-Location

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		.\$buildDestination\.libs\libffi-6.dll `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\include
	Copy-Item `
		.\$buildDestination\include\ffi.h, `
		.\$buildDestination\include\ffitarget.h `
		$packageDestination\include

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		.\$buildDestination\.libs\libffi_convenience.lib `
		$packageDestination\lib\libffi.lib

	New-Item -Type Directory $packageDestination\share\doc\libffi
	Copy-Item .\LICENSE $packageDestination\share\doc\libffi

	Package $packageDestination
}

$items['libpng']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'libpng' `
		"msbuild projects\vc12\vstudio.sln /p:Platform=$platform /p:Configuration=Release /nodeReuse:True"

	switch ($filenameArch) {
		'x86' {
			$releaseDirectory = '.\projects\vc12\Release'
		}

		'x64' {
			$releaseDirectory = '.\projects\vc12\x64\Release'
		}
	}

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		$releaseDirectory\libpng16.dll, `
		$releaseDirectory\libpng16.pdb, `
		$releaseDirectory\pngstest.exe, `
		$releaseDirectory\pngstest.pdb, `
		$releaseDirectory\pngtest.exe, `
		$releaseDirectory\pngtest.pdb, `
		$releaseDirectory\pngunknown.exe, `
		$releaseDirectory\pngunknown.pdb, `
		$releaseDirectory\pngvalid.exe, `
		$releaseDirectory\pngvalid.pdb `
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

$items['libxml2']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'libxml2' `
		"msbuild win32\vc12\libxml2.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"

	switch ($filenameArch) {
		'x86' {
			$releaseDirectory = '.\win32\vc12\Release'
		}

		'x64' {
			$releaseDirectory = '.\win32\vc12\x64\Release'
		}
	}

	Copy-Item $releaseDirectory\runsuite.exe .
	&runsuite.exe
	Remove-Item .\runsuite.exe

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		$releaseDirectory\libxml2.dll, `
		$releaseDirectory\libxml2.pdb, `
		$releaseDirectory\runsuite.exe, `
		$releaseDirectory\runsuite.pdb `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\include\libxml
	Copy-Item `
		.\include\win32config.h, `
		.\include\wsockcompat.h, `
		.\include\libxml\*.h `
		$packageDestination\include\libxml

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		$releaseDirectory\libxml2.lib `
		$packageDestination\lib

	New-Item -Type Directory $packageDestination\share\doc\libxml2
	Copy-Item .\COPYING $packageDestination\share\doc\libxml2

	Package $packageDestination
}

$items['openssl']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	&$Patch -p1 -i openssl-tls-error.patch

	VSPrompt -Name 'openssl' `
		'set OPENSSL_SRC=%cd%' `
		"set OPENSSL_DEST=%cd%-$filenameArch" `
		"set PERL_PATH=$MozillaBuildDirectory\perl-5.18\$platform\bin" `
		"set NASM_PATH=$MozillaBuildDirectory\nasm" `
		"set INCLUDE=%INCLUDE%;%OPENSSL_SRC%\..\..\..\gtk\$platform\include" `
		"set LIB=%LIB%;%OPENSSL_SRC%\..\..\..\gtk\$platform\lib" `
		"set PATH=%PATH%;%PERL_PATH%;%NASM_PATH%;%OPENSSL_SRC%\..\..\..\gtk\$platform\bin" `
		"perl Configure $(if ($filenameArch -eq 'x86') { 'VC-WIN32' } else { 'VC-WIN64A' }) enable-camellia zlib-dynamic --openssldir=./" `
		"call $(if ($filenameArch -eq 'x86') { 'ms\do_nasm' } else { 'ms\do_win64a' })" `
		'nmake -f ms\ntdll.mak vclean' `
		'nmake -f ms\ntdll.mak' `
		'nmake -f ms\ntdll.mak test' `
		'perl mk-ca-bundle.pl -n' `
		'move include include-orig' `
		'nmake -f ms\ntdll.mak install'

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

$items['pango']['BuildScript'] = {
	$packageDestination = "$PWD-rel"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	# Add BOM to .\pango\pango-language-sample-table.h because cl.exe throws C2001 otherwise
	$languageSampleTableFileContents = Get-Content .\pango\pango-language-sample-table.h -Encoding UTF8
	Out-File .\pango\pango-language-sample-table.h -InputObject $languageSampleTableFileContents -Encoding UTF8

	&$Patch -p1 -i pango-defs.patch
	&$Patch -p1 -i pango-nonbmp.patch
	&$Patch -p1 -i pango-synthesize-all-fonts.patch

	VSPrompt -Name 'pango' `
		"msbuild build\win32\vc12\pango_fc.sln /p:Platform=$platform /p:Configuration=Release /nodeReuse:True"

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

	VSPrompt -Name 'pixman' `
		"msbuild build\win32\vc12\pixman.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True"

	New-Item -Type Directory $packageDestination\share\doc\pixman
	Copy-Item .\COPYING $packageDestination\share\doc\pixman

	Package $packageDestination
}

$items['win-iconv']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	Remove-Item -Recurse CMakeCache.txt, CMakeFiles -ErrorAction Ignore

	VSPrompt -Name 'win-iconv' `
		"SET PATH=%PATH%;$CMakePath" `
		"cmake -G `"NMake Makefiles`" -DCMAKE_INSTALL_PREFIX=`"$packageDestination`" -DCMAKE_BUILD_TYPE=Release" `
		'nmake clean' `
		'nmake' `
		'nmake install'

	New-Item -Type Directory $packageDestination\share\doc\win-iconv
	Copy-Item .\COPYING $packageDestination\share\doc\win-iconv

	VSPrompt -Name 'win-iconv-2' `
		'nmake clean'

	Package $packageDestination
}

$items['zlib']['BuildScript'] = {
	$packageDestination = "$PWD-$filenameArch"
	Remove-Item -Recurse $packageDestination -ErrorAction Ignore

	VSPrompt -Name 'zlib' `
		"msbuild contrib\vstudio\vc12\zlibvc.sln /p:Platform=$platform /p:Configuration=ReleaseWithoutAsm /maxcpucount /nodeReuse:True"

	New-Item -Type Directory $packageDestination\include
	Copy-Item zlib.h, zconf.h $packageDestination\include

	Push-Location ".\contrib\vstudio\vc12\$filenameArch"

	New-Item -Type Directory $packageDestination\bin
	Copy-Item `
		.\TestZlibDllRelease\testzlibdll.exe, `
		.\TestZlibDllRelease\testzlibdll.pdb, `
		.\TestZlibReleaseWithoutAsm\testzlib.exe, `
		.\TestZlibReleaseWithoutAsm\testzlib.pdb, `
		.\ZlibDllReleaseWithoutAsm\zlib1.dll, `
		.\ZlibDllReleaseWithoutAsm\zlib1.map, `
		.\ZlibDllReleaseWithoutAsm\zlib1.pdb `
		$packageDestination\bin

	New-Item -Type Directory $packageDestination\lib
	Copy-Item `
		.\ZlibDllReleaseWithoutAsm\zlib1.lib, `
		.\ZlibStatReleaseWithoutAsm\zlibstat.lib `
		$packageDestination\lib

	Pop-Location

	New-Item -Type Directory $packageDestination\share\doc\zlib
	Copy-Item .\README $packageDestination\share\doc\zlib

	Package $packageDestination
}

#========================================================================================================================================================
# Build steps end here
#========================================================================================================================================================


# Verify VS exists at the indicated location, and that it supports the required target
switch ($Configuration) {
	'x86' {
		$vcvarsBat = "$VSInstallPath\VC\bin\vcvars32.bat"
	}

	'x86_amd64' {
		$vcvarsBat = "$VSInstallPath\VC\bin\x86_amd64\vcvarsx86_amd64.bat"
	}

	'x64' {
		$vcvarsBat = "$VSInstallPath\VC\bin\amd64\vcvars64.bat"
	}
}

if (-not $(Test-Path $vcvarsBat)) {
	throw "`"$vcvarsBat`" could not be found. Please check you have Visual Studio installed at `"$VSInstallPath`" and that it supports the configuration `"$Configuration`"."
}


switch ($Configuration) {
	'x86' {
		$platform = 'Win32'
		$filenameArch = 'x86'
		$mozillaBuildStartVC = "$MozillaBuildDirectory\start-msvc12.bat"
	}

	'x86_amd64' {
		$platform = 'x64'
		$filenameArch = 'x64'
		$mozillaBuildStartVC = "$MozillaBuildDirectory\start-msvc12-x86_amd64.bat"
	}

	'x64' {
		$platform = 'x64'
		$filenameArch = 'x64'
		$mozillaBuildStartVC = "$MozillaBuildDirectory\start-msvc12-x64.bat"
	}
}

$workingDirectory = "$MozillaBuildDirectory\hexchat\build\$platform"


# Set up additional properties on the items
foreach ($element in $items.GetEnumerator()) {
	$name = $element.Key
	$item = $element.Value

	$archiveUrl = $item['ArchiveUrl']

	$filename = New-Object System.Uri $archiveUrl
	$filename = $filename.Segments[$filename.Segments.Length - 1]

	$patchDirectory = "$PatchesRootDirectory\$name"

	$archiveFile = New-Object System.IO.FileInfo "$ArchivesDownloadDirectory\$filename"

	$item = $items[$name]

	$item['Name'] = $name
	$item['ArchiveFile'] = $archiveFile
	$item['PatchDirectory'] = $(New-Object System.IO.DirectoryInfo $patchDirectory)
	$item['BuildDirectory'] = $(New-Object System.IO.DirectoryInfo "$workingDirectory\$($archiveFile.BaseName)")
	$item['BuildArchiveFile'] = $(New-Object System.IO.FileInfo "$workingDirectory\$($archiveFile.BaseName)-$filenameArch$($archiveFile.Extension)")
	$item['Dependencies'] = @($item['Dependencies'] | %{ $items[$_] })
}


# If OnlyBuild is not an empty array, only keep the items that are specified
if ($OnlyBuild.Length -gt 0) {
	$newItems = @{}

	$queue = New-Object System.Collections.Generic.Queue[string] (, $OnlyBuild)

	while ($queue.Length -gt 0) {
		$itemName = $queue.Dequeue()
		$item = $items[$itemName]

		$newItems[$itemName] = $item

		@($item['Dependencies']) | %{ $queue.Enqueue($_.Name) }
	}

	$items = $newItems
}


if (-not $(Test-Path "$MozillaBuild\start-msvc12.bat")) {
	Copy-Item $PatchesRootDirectory\mozilla-build\start-msvc12.bat $MozillaBuildDirectory
}
if (-not $(Test-Path "$MozillaBuild\start-msvc12-x64.bat")) {
	Copy-Item $PatchesRootDirectory\mozilla-build\start-msvc12-x64.bat $MozillaBuildDirectory
}
if (-not $(Test-Path "$MozillaBuild\start-msvc12-x86_amd64.bat")) {
	Copy-Item $PatchesRootDirectory\mozilla-build\start-msvc12-x86_amd64.bat $MozillaBuildDirectory
}


New-Item -Type Directory $ArchivesDownloadDirectory


New-Item -Type Directory $workingDirectory
Set-Location $workingDirectory
Copy-Item $PatchesRootDirectory\stack.props .


$logDirectory = "$workingDirectory\logs"
New-Item -Type Directory $logDirectory
Remove-Item $logDirectory\*.log


New-Item -Type Directory $workingDirectory\..\..\gtk\$platform


# For each item, start a job to download the source archives, extract them to mozilla-build, and copy over the stuff from gtk-win32
$items.GetEnumerator() | %{
	Start-Job -Name $_.Key -ArgumentList $_.Value, $ArchivesDownloadDirectory, $workingDirectory, $Wget, $SevenZip {
		param ($item, $ArchivesDownloadDirectory, $workingDirectory, $Wget, $SevenZip)

		'Beginning job to download and extract'

		if ($item['ArchiveFile'].Exists) {
			"$($item['ArchiveFile']) already exists"
		}
		else {
			"$($item['ArchiveFile']) doesn't exist"
			Set-Location $ArchivesDownloadDirectory
			&$Wget $item['ArchiveUrl'] > $null 2>&1
			"Downloaded $($item['ArchiveUrl'])"
		}

		"Extracting $($item['ArchiveFile'].Name) to $workingDirectory"
		&$SevenZip x $item['ArchiveFile'] -o"$workingDirectory" -y > $null
		"Extracted $($item['ArchiveFile'].Name)"

		Copy-Item "$($item['PatchDirectory'])\*" $item['BuildDirectory'] -Recurse -Force
		"Copied patch contents from $($item['PatchDirectory']) to $($item['BuildDirectory'])"
	} > $null
}

# While the jobs are running...
$downloadJobs = @()
do {
	# Log their output
	$downloadJobs = Get-Job | %{
		$job = $_

		[string[]] $jobOutput = Receive-Job $job
		$jobOutput | %{
			Write-Host "$($job.Name) : $_"
		}

		$job
	} | ? { $_.State -ne 'Completed' }

	# Sleep a bit and then try again
	Start-Sleep 1
} while ($downloadJobs.Length -gt 0)

# All the jobs have been completed. Delete them all.
Get-Job | Remove-Job


# Map of items that have finished building (name -> item)
$completedItems = @{}


# Until all items have been built
while ($completedItems.Count -ne $items.Count) {

	# If another job can be started (either parallel build is enabled, or it's disabled and there is no running build job)...
	if (-not $DisableParallelBuild -or $(Get-Job) -eq $null) {

		# Find an item which hasn't already been built, isn't being built currently, and whose dependencies have all been built
		[Object[]] $nextItem =
			$items.GetEnumerator() | ?{
				$completedItems[$_.Key] -eq $null -and
				(Get-Job -Name $_.Key 2>$null) -eq $null
			} | %{ $_.Value } | ?{
				[Object[]] $dependencies = @($_['Dependencies'])
				if ($dependencies.Length -gt 0) {
					[Object[]] $remainingDependencies = $dependencies | ?{ $completedItems[$_['Name']] -eq $null }
					return $remainingDependencies.Length -eq 0
				}
				else {
					return $true
				}
			}

		# If such an item exists...
		if ($nextItem.Length -gt 0) {
			$pendingItem = $nextItem[0]

			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($pendingItem['Name']) : Started"
			Write-Host "$($pendingItem['Name']) : Started"

			# Start a job to build it
			Start-Job -Name $pendingItem['Name'] -InitializationScript {
				# Runs all unnamed arguments as commands in a VS prompt
				function VSPrompt([string] $Name) {
					$tempVSPromptBatchFile = "$($env:TEMP)\hexchat-build-$Name.bat"

					Out-File -FilePath $tempVSPromptBatchFile -InputObject "@CALL `"$VSInstallPath\VC\vcvarsall.bat`" $Configuration" -Encoding OEM
					foreach ($command in $args) {
						Out-File -FilePath $tempVSPromptBatchFile -InputObject $command -Encoding OEM -Append
					}

					&$tempVSPromptBatchFile

					Remove-Item $tempVSPromptBatchFile
				}

				function Package([string] $directory) {
					$archiveFilename = "$PWD-$filenameArch.7z"

					Push-Location $directory
					Remove-Item $archiveFilename -ErrorAction Ignore
					&$SevenZip a $archiveFilename *
					Pop-Location

					Copy-Item -Recurse -Force $directory\* $workingDirectory\..\..\gtk\$platform

					Remove-Item -Recurse $directory
				}
			} -ArgumentList $pendingItem {
				param ($item)

				$MozillaBuildDirectory = $using:MozillaBuildDirectory
				$mozillaBuildStartVC = $using:mozillaBuildStartVC
				$Configuration = $using:Configuration
				$filenameArch = $using:filenameArch
				$Patch = $using:Patch
				$platform = $using:platform
				$VSInstallPath = $using:VSInstallPath
				$workingDirectory = $using:workingDirectory
				$SevenZip = $using:SevenZip
				$CMakePath = $using:CMakePath

				Set-Location $item['BuildDirectory']

				Invoke-Command ([ScriptBlock] [ScriptBlock]::Create($item['BuildScript']))
			} > $null
		}
	}

	# For each job...
	Get-Job | %{
		$job = $_

		# Log all its output
		[string[]] $jobOutput = Receive-Job $job
		$jobOutput | %{
			Out-File -Append -Encoding OEM -FilePath "$logDirectory\$($job.Name).log" -InputObject $_
			Write-Host "$($job.Name) : $_"
		}

		# If the job has been completed...
		if ($job.State -eq 'Completed') {

			# Make sure all its output has been logged
			$jobOutput = Receive-Job $job
			$jobOutput | %{
				Out-File -Append -Encoding OEM -FilePath "$logDirectory\$($job.Name).log" -InputObject $_
				Write-Host "$($job.Name) : $_"
			}

			# Add the item to the completed items map
			$completedItems[$job.Name] = $items[$job.Name]

			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($job.Name) : Completed"
			Write-Host "$($job.Name) : Completed"

			# Delete the job
			Remove-Job $job
		}
	}

	# Sleep a bit and then try again
	Start-Sleep 1
}
