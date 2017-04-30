## Goals

This python script helps you build a full GTK+ library stack for Windows using Visual Studio.

The powershell script was originally [developed by the HexChat developers](https://github.com/hexchat/gtk-win32), make sure to check their page for more information about the original script.

HexChat developers decided that their script should focus on their specific needs, this fork tries to be a bit more generic, in particular it pursues the following goals

1. Build GTK+ 3 - we want to focus on the current version of GTK
1. Support multiple version of Visual Studio - at the moment we are focusing on VS 2013, but we include projects for other versions and we gladly accept patches
1. We try to follow as much as possible the conventions of the upstream MSVC projects by Fan Chun-wei - [Compiling the GTK+ (and Clutter) stack using Visual C++ 2008 and later](https://wiki.gnome.org/action/show/Projects/GTK+/Win32/MSVCCompilationOfGTKStack).
1. We are pretty liberal about adding more libraries to the script - at some point we will need to make the set of libraries that are built configurable and easily extensible, but right now we are ok with adding libraries that are useful to the users of this script
1. We try to fetch tarballs from their original locations - if patches are needed we try to fork the project on github and host a patched tarball there
1. We try to download the tools needed and using them from a local directory, without any installation. Actually we use directly cmake, meson, ninja, nuget and perl.

## Building

1. Install the following build tools and dependencies:

    * [Visual Studio for Windows Desktop](http://www.visualstudio.com/downloads) - 2013 and 2015 are currently supported.
    * [msys2](https://msys2.github.io/)
    * [Python 3.4](https://www.python.org/ftp/python/2.7.9/python-2.7.9.amd64.msi) (install in C:\Python34), or other package like [Miniconda 3.4](https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe)

1. Follow the instructions on the msys2 page to update the core packages.

1. Install needed packages in the msys2 shell

    ```bash
    pacman -S nasm patch gettext make coreutils diffutils wget yasm pkg-config
    ```

1. Clone [this repository](https://github.com/wingtk/gvsbuild) to _C:\gtk-build\gvsbuild_ It contains the build script, project files and patches.
   
    ```mkdir gtk-build
    cd gtk-build
    git clone https://github.com/wingtk/gvsbuild
    ```

1. Now start a command-line window as a regular user. Go to the _gvsbuild_ directory and start building with the script. For example, to build 32-bit GTK+ 3 and its dependencies, run:

    ```
    cd C:\gtk-build\gvsbuild
    python .\build.py build gtk3
    ```

    To build the 64-bit version, run:

    ```
    cd C:\gtk-build\gvsbuild
    python .\build.py build -p x64 gtk3
    ```

    For more information about the possible commands. Run

    ```
    python .\build.py --help
    ```

1. When the script is done, your GTK+ stack will be found under _C:\gtk-build\gtk_. Enjoy!
