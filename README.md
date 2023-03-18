# gvsbuild

![CI](https://github.com/wingtk/gvsbuild/workflows/CI/badge.svg)

This python script helps you build a full [GTK](https://www.gtk.org/) library
stack for Windows using Visual Studio. Currently, GTK 3 and GTK 4 are supported.

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
example C:\Python310. Other Python distributions like [Miniconda
3](https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe)
should also work.

#### Install gvsbuild
The recommended way to install gvsbuild is with pipx. Open a new regular user
PowerShell terminal and execute:

```PowerShell
python -m pip install --user pipx
python -m pipx ensurepath
pipx install gvsbuild
```

Alternatively, you can also use git to clone the repository and install it.
Open a new regular user PowerShell terminal and execute:

```PowerShell
mkdir C:\gtk-build\github
cd C:\gtk-build\github
git clone https://github.com/wingtk/gvsbuild.git
cd C:\gtk-build\github\gvsbuild
python -m venv .venv
.\.venv\Scripts\activate.ps1
pip install .
```

#### Build GTK

In the same PowerShell terminal, execute:

```PowerShell
gvsbuild build gtk3
```

Alternatively, if you want to build GTK 4, execute:
```PowerShell
gvsbuild build gtk4
```

Grab a coffee, the build will take a few minutes to complete.

#### Add GTK to Your Environmental Variables

```PowerShell
$env:Path = "C:\gtk-build\gtk\x64\release\bin;" + $env:Path
$env:LIB = "C:\gtk-build\gtk\x64\release\lib;" + $env:LIB
$env:INCLUDE = "C:\gtk-build\gtk\x64\release\include;C:\gtk-build\gtk\x64\release\include\cairo;C:\gtk-build\gtk\x64\release\include\glib-2.0;C:\gtk-build\gtk\x64\release\include\gobject-introspection-1.0;C:\gtk-build\gtk\x64\release\lib\glib-2.0\include;" + $env:INCLUDE
```

#### Use PyGObject

Add the `--enable-gi` and `--py-wheel` options like:

```PowerShell
gvsbuild build --enable-gi --py-wheel gtk4 pygobject
```

Once that finishes, then you need to use the gvsbuild generated wheels with your
[Python virtualenv](https://docs.python.org/3/tutorial/venv.html) in order to
work around this [PyGObject
bug](https://gitlab.gnome.org/GNOME/pygobject/-/issues/545):

```PowerShell
pip install --force-reinstall (Resolve-Path C:\gtk-build\build\x64\release\pygobject\dist\PyGObject*.whl)
pip install --force-reinstall (Resolve-Path C:\gtk-build\build\x64\release\pycairo\dist\pycairo*.whl)
```

#### Other Options

 For more information about the possible commands run:

 ```
 gvsbuild --help
 ```

 To get detailed help on the build command run:

 ```
 gvsbuild build --help
 ```

 It is possible to set some parameters from a file, e.g. vs2015-release.pro, putting
 the @ character before the file name. The file contains the option, one per
 line, separated by a carriage return:

 ```
 --vs-ver
 14
 --win-sdk
 8.1
 --configuration
 release
 ```

 Even if the format is not the easier to write or read in this way we eliminate
 the problem of escaping spaces is file names and directories. Then you can use
 it:

 ```
 gvsbuild build @vs2015-release.pro gtk3-full
 ```

## Troubleshooting

- If a build fails, try rebuilding it with `--clean`, if that fails, try
rebuilding it with `--from-scratch`
- If the download of a tarball fails a partial file will not pass the hash check,
delete the file and try again.

## OpenSSL

In addition to the setup instructions above, to build OpenSSL you also need the
Visual C++ 2013 Redistributable Package installed. To install it, open PowerShell
as administrator and execute:

```PowerShell
choco install vcredist2013
```

Similar to other packages, you can build OpenSSL by executing:
```
gvsbuild build openssl
```

## Dependency Graph

To see and analyze the dependency between the various projects, in text or in a
Graphviz format, use the script deps.py:

 ```
gvsbuild deps --graph --gv-file test.gv
 ```

Without option a simple dependency of all the projects is printed, as usual with
--help a summary of the options/commands is printed.

## License

This build script is licensed under the GPL2.0 license, see the COPYING file for
the full text.

The binaries produced by the build script are licensed under the license terms
of the project that is built (ie glib is LGPL so you can use glib.dll built
with this script under the terms of LGPL).

Patches included in the repository are licensed under the license terms of the
project they apply to.

## Credits

This tool originated from a gtk-win32 PowerShell script created by the
[HexChat](https://hexchat.github.io/) developers for building it for Windows.
Although this project is now archived, you can explore the original project if you
are interested in the history at https://github.com/hexchat/gtk-win32.

Compiling the GTK stack on MSVC would not be possible without the incredible
work by [Fan Chun-wei](https://github.com/fanc999). If you are interested in more
details of how this works, please see [Compiling the GTK+ (and Clutter) stack using
Visual C++ 2008 and
later](https://wiki.gnome.org/Projects/GTK/Win32/MSVCCompilationOfGTKStack).
