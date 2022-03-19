# gvsbuild

![CI](https://github.com/wingtk/gvsbuild/workflows/CI/badge.svg)

This python script helps you build a full [GTK](https://www.gtk.org/) library
stack for Windows using Visual Studio. Currently, GTK 3 (3.20, 3.22, 3.24) and
GTK 4 (4.6) are supported.

The script supports multiple versions of Visual Studio - at the moment we are
focusing on VS 2022, but we include projects for other versions, and we gladly
accept patches.

The script focuses on GTK and the surrounding ecosystem (e.g. GStreamer).
However, we are open to adding more libraries as long as the contributor takes
on the responsibility for keeping it up to date. The supported projects are
modules in the
[projects](https://github.com/wingtk/gvsbuild/blob/master/gvsbuild/projects)
directory.

The script requires a working installation of [Visual Studio for Windows
Desktop](http://www.visualstudio.com), [Python 3](https://www.python.org) and
[msys2](https://msys2.github.io). The script will download any additional tools
required to build the libraries and will use them from a local directory,
without any installation. As of today these tools include cmake, meson, ninja,
nuget and perl.

The script fetches source tarballs for the projects from their original
locations, however in some cases it might be necessary to host a patched tarball
on GitHub. To ensure integrity of the downloaded files, the script checks the
SHA256 hash of each download. Downloads are done using TLS, using SSL
certificates provided by the system, but in case of error the download is tried
again ignoring certificate errors.

## Development Environment

### Choco
We recommend using [Chocolately](https://chocolatey.org/) as a package manager
in Windows.

To install it, open PowerShell as an administrator, then execute:

```PowerShell
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
To run local scripts in follow-on steps, also execute
`Set-ExecutionPolicy RemoteSigned`. This allows for local PowerShell scripts
to run without signing, but still requires signing for remote scripts.

### Git
To setup a development environment in Windows install
[Git](https://gitforwindows.org) by executing as an administrator:

```PowerShell
choco install git
```

### MSYS2
Both of the development environments in the next steps need MSYS2 installed.

Install [MSYS2](http://www.msys2.org/):

Keep PowerShell open as administrator and execute:
```PowerShell
choco install msys2
```

### Building GTK

First we will install the gvsbuild dependencies:
1. Visual C++ build tools workload for Visual Studio 2022 Build Tools
2. Python

#### Install Visual Studio 2022
With your admin PowerShell terminal:

```PowerShell
choco install visualstudio2022-workload-vctools
```

Note: Visual Studio versions 2013 (not for all projects), 2015, 2017, 2019, and 2022 are currently supported.

#### Install the Latest Python

Download and install the latest version of Python:

1. Install from Chocolately with `choco install python` with admin PowerShell
1. Restart your PowerShell terminal as a normal user and check that `python --version` is correct.

Note: If you are going to install Python using an alternative means, like the
official Windows installers, we suggest to install Python in C:\Python3x, for
example C:\Python310. Alternatively you can use the `--python-dir` option to
tell the script the correct location of your Python installation. Other Python
distributions like [Miniconda
3](https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe)
should also work.

#### Install gvsbuild
Open a new regular user PowerShell terminal and execute:

```PowerShell
mkdir C:\gtk-build\github
cd C:\gtk-build\github
git clone https://github.com/wingtk/gvsbuild.git
```

#### Build GTK

In the same PowerShell terminal, execute:

```PowerShell
cd C:\gtk-build\github\gvsbuild
python .\build.py build -p=x64 --vs-ver=17 --msys-dir=C:\tools\msys64 --gtk3-ver=3.24 gtk3
```

Alternatively, if you want to build GTK 4, execute:
```PowerShell
cd C:\gtk-build\github\gvsbuild
python .\build.py build -p=x64 --vs-ver=17 --msys-dir=C:\tools\msys64 gtk4 
```

Grab a coffee, the build will take a few minutes to complete.

#### Add GTK to Your Path

```PowerShell
$env:Path = "C:\gtk-build\gtk\x64\release\bin;" + $env:Path
```

#### Other Options

 To build the 64-bit version with the Visual Studio 2022 (version 17) you need
 also to tell the script the visual studio version, run:

 ```
 cd C:\gtk-build\github\gvsbuild
 python .\build.py build -p x64 --vs-ver 17 gtk3
 ```

 For more information about the possible commands run:

 ```
 python .\build.py --help
 ```

 To get detailed help on the build command run:

 ```
 python .\build.py build --help
 ```

 Is possible to set some parameters from a file, e.g. vs2015-release.pro, putting
 the @ character before the file name. The file contains the option, one per
 line, separated by a carriage return:

 ```
 --vs-ver
 14
 --win-sdk
 8.1
 -c
 release
 ```

 Even if the format is not the easier to write or read in this way we eliminate
 the problem of escaping spaces is file names and directories. Then you can use
 it:

 ```
 python .\build.py build @vs2015-release.pro gtk3-full
 ```

For a complete list of the options accepted by the build command, run:

```
python .\build.py build --help
```

## Troubleshooting

If the download of a tarball fails a partial file will not pass the hash check.
Delete the file and try again.

## Dependency Graph

To see and analyze the dependency between the various projects, in text or in a
Graphviz format, use the script deps.py:

 ```
 cd C:\gtk-build\github\gvsbuild
 python .\deps.py -g -o test.gv
 ```

Without option a simple dependency of all the projects is printed, as usual with
--help a summary of the options/commands is printed.

## License

This build script is licensed under the GPL2.0 license, see the COPYING file for
the full text.

The binaries produced by the build script are licensed under the license terms
of the project that gets built (ie glib is LGPL so you can use glib.dll built
with this script under the terms of LGPL).

Patches included in the repository are licensed under the license terms of the
project they apply to.

## Credits

This tool originated from a powershell [developed by the HexChat
developers](https://github.com/hexchat/gtk-win32), make sure to check their page
for more information about the original script.

Compiling the GTK stack on MSVC would not be possible without the incredible
work by Fan Chun-wei - Check the [Compiling the GTK+ (and Clutter) stack using
Visual C++ 2008 and
later](https://wiki.gnome.org/Projects/GTK/Win32/MSVCCompilationOfGTKStack) for
more information on how this works.
