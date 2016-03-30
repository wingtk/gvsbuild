Please do not build this package in a path that contains spaces to avoid
possible problems during the build or during the usage of the library.

Please refer to the following GNOME Live! page for more detailed
instructions on building ATK and its dependencies with Visual C++:

https://live.gnome.org/GTK%2B/Win32/MSVCCompilationOfGTKStack

This VS12 solution and the projects it includes are intented to be used
in a ATK source tree unpacked from a tarball. In a git checkout you
first need to use some Unix-like environment or manual work to expand
the .in files needed, mainly config.h.win32.in into config.h.win32.
You will also need to expand atk.vcxprojin and atk.vcxproj.filtersin here
into atk.vcxproj and atk.vcxproj.filters respectively.

The dependencies for this package are gettext-runtime (libintl), GLib*
and ZLib.

a) look for all of the dependencies (except GLib*) under

   http://ftp.gnome.org/pub/GNOME/binaries/win32/dependencies/ (32-bit) -OR-
   http://ftp.gnome.org/pub/GNOME/binaries/win64/dependencies/ (64-bit)

   Please use the latest versions of these libraries that are available there,
   these are packaged by Tor Lillqvist, which are built with MinGW/GCC.
   Please see b) below regarding the build of  GLib*

-OR-

b) Build them yourself with VS12 (but you may most probably wish to get
   gettext-runtime from the URL(s) mentioned in a)).  Use the latest
   stable versions for them (you may need to get the latest unstable version of
   GLib if you are using an unstable version of ATK):

   GLib*:   Grab the latest sources from http://www.gtk.org under "Download"
            (stable only-please make a search for the latest unstable versions)
   ZLib:   http://www.zlib.net

   The above 2 packages all have supported mechanisms (Makefiles and/or Project
   Files) for building under VS12 (upgrade the Project Files from earlier VS
   versions will do for these, when applicable)

* This GLib refers to a build that is built by VS12

Set up the source tree as follows under some arbitrary top
folder <root>:

<root>\atk\<this-atk-source-tree>
<root>\vs12\<PlatformName>

*this* file you are now reading is thus located at
<root>\atk\<this-atk-source-tree>\build\win32\vs12\README.

<PlatformName> is either Win32 or x64, as in VS12 project files.

You should unpack the <dependent-package>-dev and <dependent-packge> (runtime)
into <root>\vs12\<PlatformName>, if you download any of the packages from

http://ftp.gnome.org/pub/GNOME/binaries/win32/dependencies/ (32-bit) -OR-
http://ftp.gnome.org/pub/GNOME/binaries/win64/dependencies/ (64-bit)

so that for instance libintl.h end up at 
<root>\vs12\<PlatformName>\include\libintl.h.

If you build any of the dependencies yourselves, copy the: 
-DLLs and EXEs into <root>\vs12\<PlatformName>\bin
-headers into <root>\vs12\<PlatformName>\include\
-LIBs into <root>\vs12\<PlatformName>\lib

If you have not built GLib with VS12 and placed the LIBs and headers in a
place where VS12 can find them automatically, you should also uncompress
your GLib sources in <root>\ and build it from there, following the
instructions in <root>\glib<-version>\build\win32\vs12, so that the required
headers, EXEs, DLLs and LIBs will end up in
<root>\vs12\<PlatformName>\include\glib-2.0 (headers)
<root>\vs12\<PlatformName>\lib (LIBs, also glib-2.0/include/glibocnfig.h)
<root>\vs12\<PlatformName>\bin (EXEs/DLLs)
respectively.

After the build of ATK, the "install" project will copy build results
and headers into their appropriate location under <root>\vs12\<PlatformName>.
For instance, built DLLs go into <root>\vs12\<PlatformName>\bin, built LIBs into
<root>\vs12\<PlatformName>\lib and atk headers into
<root>\vs12\<PlatformName>\include\atk-1.0. This is then from where
project files higher in the stack are supposed to look for them, not
from a specific ATK source tree.

--Chun-wei Fan <fanc999@yahoo.com.tw>
--(adapted from the GLib VS9 README.txt file originally written by Tor Lillqvist)
