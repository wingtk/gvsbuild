* Download [libssh 0.7.2](https://red.libssh.org/attachments/download/177/libssh-0.7.2.tar.xz)
* Prepare zlib and openssh
* For libssh, using the cmake-gui to create a msvc project.
  * setting libssh path
  * setting msvc project path for creating
  * setting platform( x64 or Win32)
  * setting dependence lib
    *for example like Win32
      ZLIB_INCLUDE_DIR=C:\gtk-build\gtk\Win32\release\include
      ZLIB_LIBRARY=C:\gtk-build\gtk\Win32\release\lib
      OPENSSL_INCLUDE_DIR=C:\gtk-build\gtk\Win32\release\include
      OPENSSL_ROOT_DIR=C:\gtk-build\gtk\Win32\release\x64
      SSL_EAY_DEBUG=C:\gtk-build\gtk\Win32\release\lib\ssleay32.lib
      SSL_EAY_RELEASE=C:\gtk-build\gtk\Win32\release\lib\ssleay32.lib
      LIB_EAY_DEBUG=C:\gtk-build\gtk\Win32\release\lib\libeay32.lib
      LIB_EAY_RELEASE=C:\gtk-build\gtk\Win32\releaselib\libeay32.lib
  * clicked `Generate`

* after creating msvc project, setting library in msvc projects
    *library path
      C:\gtk-build\gtk\Win32\release\lib;
    *library
      libeay32.lib;ssleay32.lib;zlib1.lib;