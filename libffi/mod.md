* Download [libffi 3.0.13](ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz)

* Run in mozilla-build shell:
  x86:
    ```bash
    ./configure CC="$(pwd)/msvcc.sh" CXX="$(pwd)/msvcc.sh" LD=link CPP='cl -nologo -EP' CXXCPP="cl -nologo -EP" --build=i686-pc-mingw32 CFLAGS=-O2
    make
    ```

  x64:
    ```bash
    ./configure CC="$(pwd)/msvcc.sh -m64" CXX="$(pwd)/msvcc.sh -m64" LD=link CPP='cl -nologo -EP' CXXCPP="cl -nologo -EP" --build=x86_64-w64-mingw32 CFLAGS=-O2
    make
    ```

* Convert commands to project file
* Add to `build\win32\vs14` directory