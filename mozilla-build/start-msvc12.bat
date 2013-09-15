@echo off

SETLOCAL
SET MOZ_MSVCVERSION=12
SET MOZBUILDDIR=%~dp0
SET MOZILLABUILD=%MOZBUILDDIR%

echo "Mozilla tools directory: %MOZBUILDDIR%"

REM Get MSVC paths
call "%MOZBUILDDIR%guess-msvc.bat"

REM Use the "new" moztools-static
set MOZ_TOOLS=%MOZBUILDDIR%moztools

rem append moztools to PATH
SET PATH=%PATH%;%MOZ_TOOLS%\bin

if "%VC12DIR%"=="" (
    ECHO "Microsoft Visual C++ version 12 (2013) was not found. Exiting."
    pause
    EXIT /B 1
) else (
    rem Prepend MSVC paths
    rem The Win7 SDK (or newer) should automatically integrate itself into vcvars32.bat
    ECHO Using VC 2013 built-in SDK
    call "%VC12DIR%\bin\vcvars32.bat"
)

if "%VC12DIR%"=="" (
    rem Prepend SDK paths - Don't use the SDK SetEnv.cmd because it pulls in
    rem random VC paths which we don't want.
    rem Add the atlthunk compat library to the end of our LIB
    set "PATH=%SDKDIR%\bin;%PATH%"
    set "LIB=%SDKDIR%\lib;%LIB%;%MOZBUILDDIR%atlthunk_compat"

    if "%USEPSDKATL%"=="1" (
        if "%USEPSDKIDL%"=="1" (
            set "INCLUDE=%SDKDIR%\include;%PSDKDIR%\include\atl;%PSDKDIR%\include;%INCLUDE%"
        ) else (
            set "INCLUDE=%SDKDIR%\include;%PSDKDIR%\include\atl;%INCLUDE%"
        )
    ) else (
        if "%USEPSDKIDL%"=="1" (
            set "INCLUDE=%SDKDIR%\include;%SDKDIR%\include\atl;%PSDKDIR%\include;%INCLUDE%"
        ) else (
            set "INCLUDE=%SDKDIR%\include;%SDKDIR%\include\atl;%INCLUDE%"
        )
    )
)

cd "%USERPROFILE%"

"%MOZILLABUILD%\msys\bin\bash" --login -i
