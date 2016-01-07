## Goals

This powershell script helps you build a full GTK+ library stack for Windows using Visual Studio.

The script was [developed by the HexChat developers](https://github.com/hexchat/gtk-win32), make sure to check their page for more information about the original script.

HexChat developers decided that their script should focus on their specific needs, this fork tries to be a bit more generic, in particular it pursues the following goals

1. Build GTK+ 3 - we want to focus on the current version of GTK
1. Support multiple version of Visual Studio - at the moment we are focusing on VS 2013, but we include projects for other versions and we gladly accept patches
1. We try to follow as much as possible the conventions of the upstream MSVC projects by Fan Chun-wei - [Compiling the GTK+ (and Clutter) stack using Visual C++ 2008 and later](https://wiki.gnome.org/action/show/Projects/GTK+/Win32/MSVCCompilationOfGTKStack).
1. We are pretty liberal about adding more libraries to the script - at some point we will need to make the set of libraries that are built configurable and easily extensible, but right now we are ok with adding libraries that are useful to the users of this script
1. We try to fetch tarballs from their original locations - if patches are needed we try to fork the project on github and host a patched tarball there

## Building

1. Install the following build tools and dependencies:

    * [Visual Studio 2013 Express for Windows Desktop](http://www.visualstudio.com/downloads/download-visual-studio-vs#d-2013-express) - Any version of VS apart from 2013 is not supported.
    * [Windows Management Framework 4.0](https://www.microsoft.com/en-us/download/details.aspx?id=40855) - Not needed for Windows 8.1 and above
    * [CMake 3.0.2](http://www.cmake.org/download/) (also works with CMake 2.8.x)
    * [msys2](https://msys2.github.io/)
    * Perl 5.20 [x86](https://dl.hexchat.net/misc/perl/perl-5.20.0-x86.7z) or [x64](https://dl.hexchat.net/misc/perl/perl-5.20.0-x64.7z) (extract to _C:\perl_)
    * [Python 2.7](https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi) (install in C:\Python27)

1. Follow the instructions on the msys2 page to update the core packages.

1. Install needed packages in the msys2 shell

    ```bash
    pacman -S gzip nasm patch tar xz gettext make coreutils diffutils
    ```

1. Clone [this repository](https://github.com/wingtk/gtk-win32) to _C:\gtk-build\github\gtk-win32_ It contains the build script, project files and patches.

1. Now you have to allow PowerShell scripts to be run on your system. Open a PowerShell prompt **as Administrator** and run the following command:

    ```powershell
    Set-ExecutionPolicy RemoteSigned
    ```

1. Now start a new PowerShell window as a regular user. Go to the _gtk-win32_ directory and start building with the script. For example, to build the 32-bit bundle, run:

    ```powershell
    cd C:\gtk-build\github\gtk-win32
    .\build.ps1
    ```

    To build the 64-bit bundle instead, run:

    ```powershell
    cd C:\gtk-build\github\gtk-win32
    .\build.ps1 -Configuration x64
    ```

    The script has some parameters you can pass in. Run

    ```powershell
    Get-Help -Full .\build.ps1
    ```

    to see the help for the parameters and examples.

1. When the script is done, your GTK+ stack will be found under _C:\gtk-build\gtk_. Enjoy!
