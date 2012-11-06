 * Download [gettext-runtime 0.18](http://winkde.org/pub/kde/ports/win32/repository-4.8/win32libs/gettext-vc100-0.18-src.tar.bz2) from WinKDE
 * Extract to `C:\mozilla-build\hexchat\gettext-runtime-0.18`
 * Open VS x86 command prompt
 * Convert `gettext-runtime\intl\intl.def` to Unix EOL
 * Patch with `patch -p1 -i gettext-runtime.patch`
 * Build with `build-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
