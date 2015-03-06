Building from Source
====================

If you want to build the bundle from source yourself, we have a PowerShell script that will download the sources, apply some patches and run the build. It is largely based on Fan Chun-wei’s [Compiling the GTK+ (and Clutter) stack using Visual C++ 2008 and later.](https://wiki.gnome.org/action/show/Projects/GTK+/Win32/MSVCCompilationOfGTKStack)

1. Install the following build tools and dependencies:
  * [Visual Studio 2013 Express for Windows Desktop](http://www.microsoft.com/visualstudio/eng/2013-downloads#d-2013-express)
  * [Windows Management Framework 4.0](http://www.microsoft.com/en-us/download/details.aspx?id=40855) - Not needed for Windows 8.1 and above
  * [7-Zip](http://www.7-zip.org/download.html) (install to C:\Program Files\7-Zip)
  * [CMake 3.0.2](http://www.cmake.org/cmake/resources/software.html)
  * [msys2](https://msys2.github.io/) use pacman to install base-devel and mingw-w64-x86_64-toolchain
  * Perl 5.20 [x86](http://dl.hexchat.net/misc/perl/perl-5.20.0-x86.7z) or [x64](http://dl.hexchat.net/misc/perl/perl-5.20.0-x64.7z) (extract to C:\gtk-build\perl-5.20\Win32 or C:\gtk-build\perl-5.20\x64) - Really needed?
  * [NASM](http://www.nasm.us/pub/nasm/releasebuilds/?C=M;O=D) (extract to C:\gtk-build\nasm) - Really needed?
  * [msgfmt](http://dl.hexchat.net/gtk-win32/msgfmt-0.18.1.7z) (extract to C:\gtk-build) - Really needed?
  * [Ragel](http://dl.hexchat.net/gtk-win32/ragel-6.8.7z) (extract to C:\gtk-build) - Needed for harfbuzz
  * [Python 2.7](https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi) (install in C:\Python27)

2. Clone the [gtk-win32](https://github.com/nice-software/gtk-win32) repository to C:\gtk-build\gtk\github\gtk-win32 This repository contains the build script, project files and patches.

3. Now you have to allow PowerShell scripts to be run on your system. Open a PowerShell prompt as Administrator and run the following command:

  `Set-ExecutionPolicy RemoteSigned`

4. Now start a new PowerShell window as a regular user. Go to the gtk-win32 directory and start building with the script:

  * To build the 32-bit bundle, run:

  ```
  cd C:\gtk-build\hexchat\github\gtk-win32
  .\build.ps1
  ```

  * To build the 64-bit bundle, run:

  ```
  cd C:\gtk-build\hexchat\github\gtk-win32
  .\build.ps1 -Configuration x64
  ```

5. When the script is done, your GTK+ stack will be found under C:\gtk-build\gtk\gtk. Enjoy!
