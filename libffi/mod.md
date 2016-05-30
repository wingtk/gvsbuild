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

* In `build\win32`:
 * Copy `vs12` directory and rename to `vs14`
* In `build\win32\vs14\libffi.sln`, replace:
 * `Microsoft Visual Studio Solution File, Format Version 12.00` with
   `Microsoft Visual Studio Solution File, Format Version 14.00`
 * `# Visual Studio 2013` with
   `# Visual Studio 14`
* In `build\win32\vs14\libffi.vcxproj`, replace:
 * `<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
   `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
 * `<PlatformToolset>v120</PlatformToolset>` with
   `<PlatformToolset>v140</PlatformToolset>`