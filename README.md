# gvsbuild

[![CI](https://github.com/wingtk/gvsbuild/actions/workflows/ci.yml/badge.svg)](https://github.com/wingtk/gvsbuild/actions/workflows/ci.yml)

This python script helps you build a full [GTK](https://www.gtk.org/) library stack for Windows using Visual Studio.

The script supports multiple versions of Visual Studio - at the moment we are focusing on VS 2017, but we include projects for other versions and we gladly accept patches.

The script focuses on GTK and the surrounding ecosystem (e.g. GStreamer), however we are pretty liberal about adding more libraries to the script, with the disclaimer that each contributor is responsible for keeping the additional libraries up to date.
For now the list of projects is simply defined in the [projects.py](https://github.com/wingtk/gvsbuild/blob/master/gvsbuild/projects.py) file. If the number of libraries increases, we will consider making this more configurable and easily extensible.

The script requires a working installation of [Visual Studio for Windows Desktop](http://www.visualstudio.com), [Python 3](https://www.python.org) and [msys2](https://msys2.github.io).
The script will download any additional tools required to build the libraries and will use them from a local directory, without any installation. As of today these tools include cmake, meson, ninja, nuget and perl.

The script fetches source tarballs for the projects from their original locations, however in some cases it might be necessary to host a patched tarball on github.
To ensure integrity of the downloaded files, the script checks the SHA256 hash of each download. Downloads are done using TLS, using SSL certificates provided by the system, but in case of error the download is tried again ignoring certificate errors.

## Prerequisites

Download and install the following build tools and dependencies:

1. [Visual Studio for Windows Desktop](http://www.visualstudio.com/downloads)

    The following Visual Studio versions are supported: 2013 (not for all projects), 2015, 2017 and 2019

1. [Python 3](https://www.python.org/downloads/windows/)

    We suggest to install Python in C:\Python3x, for example C:\Python310. Alternatively you can use the `--python-dir` option to tell the script the correct location of your Python installation.
    Other Python distributions like [Miniconda 3](https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe) should also work.

1. [msys2](https://msys2.github.io/)

    Follow the instructions on the msys2 page to update the core packages. The packages by the build script (make, diffutils, ...) are download and installed automatically if not presents in the msys2 installation.

## Building

1. Clone [this repository](https://github.com/wingtk/gvsbuild) to _C:\gtk-build\github\gvsbuild_ It contains the build script, project files and patches.

1. Now start a command-line window as a regular user. Go to the _gvsbuild_ directory and start building with the script. For example, to build 32-bit GTK+ 3 and its dependencies with Visual Studio 2013 (the default), run:

    ```
    cd C:\gtk-build\github\gvsbuild
    python .\build.py build gtk3
    ```

    To build the 64-bit version, run:

    ```
    cd C:\gtk-build\github\gvsbuild
    python .\build.py build -p x64 gtk3
    ```

    To build the 64-bit version with the Visual Studio 2017 (version 15) you need also to tell the script the visual studio version, run:

    ```
    cd C:\gtk-build\github\gvsbuild
    python .\build.py build -p x64 --vs-ver 15 gtk3
    ```

    For more information about the possible commands run:

    ```
    python .\build.py --help
    ```

    To get detailed help on the build command run:

    ```
    python .\build.py build --help
    ```

    Is possible to set some parameters from a file, e.g. vs2015-release.pro, putting the @ character before the file name. The file contains the option, one per line, separated by a carriage return:

    ```
    --vs-ver
    14
    --win-sdk
    8.1
    -c
    release
    ```

    Even if the format is not the easier to write or read in this way we eliminate the problem of escaping spaces is file names and directories. Then you can use it:

    ```
    python .\build.py build @vs2015-release.pro gtk3-full
    ```

1. When the script is done, your GTK+ stack will be found under _C:\gtk-build\gtk_. Enjoy!


For a complete list of the options accepted by the build command, run:

```
python .\build.py build --help
```

## Troubleshooting

If the download of a tarball fails a partial file will not pass the hash check. Delete the file and try again.

## Dependency Graph

To see and analyze the dependency between the various projects, in text or in a Graphviz format, use the script deps.py:

    ```
    cd C:\gtk-build\github\gvsbuild
    python .\deps.py -g -o test.gv
    ```

Without option a simple dependency of all the projects is printed, as usual with --help a summary of the options/commands is printed.

## License

This build script is licensed under the GPL2.0 license, see the COPYING file for the full text.

The binaries produced by the build script are licensed under the license terms of the project that gets built (ie glib is LGPL so you can use glib.dll built with this script under the terms of LGPL).

Patches included in the repository are licensed under the license terms of the project they apply to.

## Credits

This tool originated from a powershell [developed by the HexChat developers](https://github.com/hexchat/gtk-win32), make sure to check their page for more information about the original script.

Compiling the GTK stack on MSVC would not be possible without the incredible work by Fan Chun-wei - Check the [Compiling the GTK+ (and Clutter) stack using Visual C++ 2008 and later](https://wiki.gnome.org/Projects/GTK/Win32/MSVCCompilationOfGTKStack) for more information on how this works.

