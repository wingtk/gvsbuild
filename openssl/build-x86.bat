:: run this from a VS x86 command prompt
@echo off

SET PACKAGE_NAME=openssl-1.0.1e

set OPENSSL_SRC=%cd%
set OPENSSL_DEST=%cd%-x86
set PERL_PATH=c:\mozilla-build\perl-5.18\Win32\bin
set NASM_PATH=c:\mozilla-build\nasm
set INCLUDE=%INCLUDE%;%OPENSSL_SRC%\..\..\..\gtk\Win32\include
set LIB=%LIB%;%OPENSSL_SRC%\..\..\..\gtk\Win32\lib
set PATH=%PATH%;%PERL_PATH%;%NASM_PATH%;%OPENSSL_SRC%\..\..\..\gtk\Win32\bin
perl Configure VC-WIN32 enable-camellia zlib-dynamic --openssldir=./
call ms\do_nasm
@echo off
nmake -f ms\ntdll.mak vclean
nmake -f ms\ntdll.mak
nmake -f ms\ntdll.mak test
perl mk-ca-bundle.pl -n
echo.Press return when ready to install!
pause

:: hack to have . as openssldir which is required for having OpenSSL load cert.pem from .
move include include-orig
nmake -f ms\ntdll.mak install
rmdir /q /s %OPENSSL_DEST%
mkdir %OPENSSL_DEST%
move bin %OPENSSL_DEST%
copy out32dll\libeay32.pdb %OPENSSL_DEST%\bin
copy out32dll\openssl.pdb %OPENSSL_DEST%\bin
copy out32dll\ssleay32.pdb %OPENSSL_DEST%\bin
move include %OPENSSL_DEST%
move lib %OPENSSL_DEST%
copy out32dll\4758cca.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\aep.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\atalla.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\capi.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\chil.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\cswift.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\gmp.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\gost.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\nuron.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\padlock.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\sureware.pdb %OPENSSL_DEST%\lib\engines
copy out32dll\ubsec.pdb %OPENSSL_DEST%\lib\engines
mkdir %OPENSSL_DEST%\share
mkdir %OPENSSL_DEST%\share\doc
mkdir %OPENSSL_DEST%\share\doc\openssl
move openssl.cnf %OPENSSL_DEST%\share\openssl.cnf.example
move include-orig include
move cert.pem %OPENSSL_DEST%\bin
copy LICENSE %OPENSSL_DEST%\share\doc\openssl\COPYING

cd %OPENSSL_DEST%
set PATH=%PATH%;%ProgramFiles%\7-zip
del ..\%PACKAGE_NAME%-x86.7z
7z a ..\%PACKAGE_NAME%-x86.7z *
cd %OPENSSL_SRC%
rmdir /q /s %OPENSSL_DEST%

echo.Finished!
pause
