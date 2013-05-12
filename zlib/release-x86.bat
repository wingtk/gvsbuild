:: run this from a command prompt
@echo off

SET PACKAGE_NAME=zlib-1.2.8

set ZLIB_SRC=%cd%
set ZLIB_DEST=%cd%-x86
echo.Press return when ready to install!
pause

rmdir /q /s %ZLIB_DEST%
mkdir %ZLIB_DEST%
mkdir %ZLIB_DEST%\bin
mkdir %ZLIB_DEST%\include
mkdir %ZLIB_DEST%\lib
mkdir %ZLIB_DEST%\share
mkdir %ZLIB_DEST%\share\doc
mkdir %ZLIB_DEST%\share\doc\zlib
copy zlib.h %ZLIB_DEST%\include
copy zconf.h %ZLIB_DEST%\include
copy contrib\vstudio\vc11\x86\MiniUnzipRelease\miniunz.exe %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\MiniUnzipRelease\miniunz.pdb %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\MiniZipRelease\minizip.exe %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\MiniZipRelease\minizip.pdb %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\TestZlibDllRelease\testzlibdll.exe %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\TestZlibDllRelease\testzlibdll.pdb %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\TestZlibReleaseWithoutAsm\testzlib.exe %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\TestZlibReleaseWithoutAsm\testzlib.pdb %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\ZlibDllReleaseWithoutAsm\zlib1.dll %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\ZlibDllReleaseWithoutAsm\zlib1.map %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\ZlibDllReleaseWithoutAsm\zlib1.pdb %ZLIB_DEST%\bin
copy contrib\vstudio\vc11\x86\ZlibDllReleaseWithoutAsm\zdll.lib %ZLIB_DEST%\lib
copy contrib\vstudio\vc11\x86\ZlibStatReleaseWithoutAsm\zlibstat.lib %ZLIB_DEST%\lib
copy README %ZLIB_DEST%\share\doc\zlib\COPYING

cd %ZLIB_DEST%
set PATH=%PATH%;%ProgramFiles%\7-zip
del ..\%PACKAGE_NAME%-x86.7z
7z a ..\%PACKAGE_NAME%-x86.7z *
cd %ZLIB_SRC%
rmdir /q /s %ZLIB_DEST%

echo.Finished!
pause
