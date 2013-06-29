:: run this from a command prompt
@echo off

SET PACKAGE_NAME=harfbuzz-0.9.18

set HARFBUZZ_SRC=%cd%
set HARFBUZZ_DEST=%cd%-x86
echo.Press return when ready to install!
pause

rmdir /q /s %HARFBUZZ_DEST%
mkdir %HARFBUZZ_DEST%
mkdir %HARFBUZZ_DEST%\bin
mkdir %HARFBUZZ_DEST%\include
mkdir %HARFBUZZ_DEST%\lib
mkdir %HARFBUZZ_DEST%\share
mkdir %HARFBUZZ_DEST%\share\doc
mkdir %HARFBUZZ_DEST%\share\doc\harfbuzz
copy win32\libs\Release\harfbuzz.dll %HARFBUZZ_DEST%\bin
copy win32\libs\Release\harfbuzz.pdb %HARFBUZZ_DEST%\bin
copy src\*.h %HARFBUZZ_DEST%\include
copy win32\libs\harfbuzz\Release\harfbuzz.lib %HARFBUZZ_DEST%\lib
copy COPYING %HARFBUZZ_DEST%\share\doc\harfbuzz

cd %HARFBUZZ_DEST%
set PATH=%PATH%;%ProgramFiles%\7-zip
del ..\%PACKAGE_NAME%-x86.7z
7z a ..\%PACKAGE_NAME%-x86.7z *
cd %HARFBUZZ_SRC%
rmdir /q /s %HARFBUZZ_DEST%

echo.Finished!
pause
