Here you can download a GTK+ 2 bundle (and a few additional libraries) built with Visual Studio 2013. HexChat for Windows is built using this bundle.


## GTK+ Bundle

This is the bundle built by us containing all the GTK+ binaries, headers and import libraries. If you just want to use GTK+ for your application and don't want to build it yourself, download this. You will also need the Visual C++ redistributable to be able to run applications that use this bundle.

<table>
    <tr>
        <td>GTK+ bundle</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/vc12/x86/gtk-Win32.7z">32-bit</a></td>
        <td><a href="https://dl.hexchat.net/gtk-win32/vc12/x64/gtk-x64.7z">64-bit</a></td>
    </tr>
    <tr>
        <td><a href="https://www.microsoft.com/en-us/download/details.aspx?id=40784">Microsoft Visual C++ Redistributable Package for Visual Studio 2013</a></td>
        <td>vcredist_x86.exe - 32-bit</a></td>
        <td>vcredist_x64.exe - 64-bit</a></td>
    </tr>
</table>

These are the libraries in the bundle:

<table>
    <tr>
        <td>ATK</td>
        <td>2.14.0</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/atk-2.14.0.tar.xz">Source</a></td>
    </tr>
    <tr>
        <td>Cairo</td>
        <td>1.14.0</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/cairo-1.14.0.tar.xz">Source</a></td>
    </tr>
    <tr>
        <td>Enchant</td>
        <td>1.6.0</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/enchant-1.6.0.tar.gz">Source</a></td>
    </tr>
    <tr>
        <td>Fontconfig</td>
        <td>2.8.0</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/fontconfig-2.8.0.tar.gz">Source</a></td>
    </tr>
    <tr>
        <td>FreeType</td>
        <td>2.5.5</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/freetype-2.5.5.tar.baz">Source</a></td>
    </tr>
    <tr>
        <td>GDK-PixBuf</td>
        <td>2.30.8</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/gdk-pixbuf-2.30.8.tar.xz">Source</a></td>
    </tr>
    <tr>
        <td>gettext-runtime</td>
        <td>0.18</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/gettext-runtime-0.18.7z">Source</a></td>
    </tr>
    <tr>
        <td>GLib</td>
        <td>2.42.2</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/glib-2.42.2.tar.xz">Source</a></td>
    </tr>
    <tr>
        <td>GTK+</td>
        <td>2.24.27</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/gtk+-2.24.27.tar.xz">Source</a></td>
    </tr>
    <tr>
        <td>HarfBuzz</td>
        <td>0.9.39</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/harfbuzz-0.9.39.tar.bz2">Source</a></td>
    </tr>
    <tr>
        <td>libffi</td>
        <td>3.0.13</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/libffi-3.0.13.tar.gz">Source</a></td>
    </tr>
    <tr>
        <td>libpng</td>
        <td>1.6.16</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/libpng-1.6.16.tar.xz">Source</a></td>
    </tr>
    <tr>
        <td>libxml2</td>
        <td>2.9.1</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/libxml2-2.9.1.7z">Source</a></td>
    </tr>
    <tr>
        <td>OpenSSL</td>
        <td>1.0.1l</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/openssl-1.0.1l.tar.gz">Source</a></td>
    </tr>
    <tr>
        <td>Pango</td>
        <td>1.36.8</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/pango-1.36.8.tar.xz">Source</a></td>
    </tr>
    <tr>
        <td>Pixman</td>
        <td>0.32.6</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/pixman-0.32.6.tar.gz">Source</a></td>
    </tr>
    <tr>
        <td>win-iconv</td>
        <td>0.0.6</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.6.7z">Source</a></td>
    </tr>
    <tr>
        <td>zlib</td>
        <td>1.2.8</td>
        <td><a href="https://dl.hexchat.net/gtk-win32/src/zlib-1.2.8.tar.xz">Source</a></td>
    </tr>
</table>


## Building from Source

If you want to build the bundle from source yourself, we have a PowerShell script that will download the sources, apply some patches and run the build. It is largely based on Fan Chun-wei's [Compiling the GTK+ (and Clutter) stack using Visual C++ 2008 and later](https://wiki.gnome.org/action/show/Projects/GTK+/Win32/MSVCCompilationOfGTKStack).

1. Install the following build tools and dependencies:

    * [Visual Studio 2013 Express for Windows Desktop](http://www.visualstudio.com/downloads/download-visual-studio-vs#d-2013-express)
    * [Windows Management Framework 4.0](https://www.microsoft.com/en-us/download/details.aspx?id=40855) - Not needed for Windows 8.1 and above
    * [7-Zip](http://www.7-zip.org/download.html) (install to _C:\Program Files\7-Zip_)
    * [CMake 3.0.2](http://www.cmake.org/download/)
    * [msys2](https://msys2.github.io/)
    * Perl 5.20 [x86](https://dl.hexchat.net/misc/perl/perl-5.20.0-x86.7z) or [x64](https://dl.hexchat.net/misc/perl/perl-5.20.0-x64.7z) (extract to _C:\gtk-build\perl-5.20\Win32_ or _C:\gtk-build\perl-5.20\x64_)
    * [Python 2.7](https://www.python.org/downloads/windows/) (install to _C:\gtk-build\python-2.7\Win32_ or _C:\gtk-build\python-2.7\x64_)
    * [msgfmt](https://dl.hexchat.net/gtk-win32/msgfmt-0.18.1.7z) (extract to _C:\gtk-build_)
    * [Ragel](https://dl.hexchat.net/gtk-win32/ragel-6.8.7z) (extract to _C:\gtk-build_)

1. Follow the instructions on the msys2 page to update the core packages.

1. Install needed packages in the msys2 shell

    ```bash
    pacman -S gzip nasm patch tar xz
    ```

1. Clone [this repository](https://github.com/hexchat/gtk-win32) repository to _C:\gtk-build\github\gtk-win32_ This repository contains the build script, project files and patches.

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

![GTK+ 2 dependency graph](https://hexchat.github.io/gtk-win32/img/dependency-graph.png)
