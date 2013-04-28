 * Download [HarfBuzz 0.9.16](http://cgit.freedesktop.org/harfbuzz/snapshot/harfbuzz-0.9.16.zip)
 * Download [blinkseb's HarfBuzz solution](https://github.com/blinkseb/harfbuzz)
 * Extract to `C:\mozilla-build\hexchat`
 * Rename `src\hb-version.h.in` to `src\hb-version.h` and fix the following macros:
	* `HB_VERSION_MAJOR` (0)
	* `HB_VERSION_MINOR` (9)
	* `HB_VERSION_MICRO` (16)
	* `HB_VERSION_STRING` ("0.9.16")
 * Open `win32\harfbuzz.sln` with VS
 * Add to _Additional Include Directories_ under _Configuration Properties_ `->` _C/C++_ `->` _General_:
	<pre>..\..\..\..\gtk\$(Platform)\include
..\..\..\..\gtk\$(Platform)\include\glib-2.0
..\..\..\..\gtk\$(Platform)\lib\glib-2.0\include</pre>
 * Change to DLL
 * Add lib path and fix freetype name
 * Generate .def file with `./autogen.sh && cd src && make harfbuzz.def`
 * Add .def file in VS
 * Remove every source file and add back *.cc from ..\src, then remove:
	* hb-coretext.cc
	* hb-graphite2.cc
	* hb-icu.cc
	* hb-icu-le.cc
	* hb-old.cc
	* hb-ucdn.cc
	* main.cc
	* test-buffer-serialize.cc
	* test-size-params.cc
	* test-would-substitute.cc
	* test.cc
 * Add to Pre-Build event:
<pre>cd $(SolutionDir)\..\src
echo 2> rllist.txt

for %%a in (*.rl) do (
echo %%a >> rllist.txt
)

for /f "tokens=1 delims=." %%b in (rllist.txt) do (
..\..\..\..\..\ragel\ragel.exe -e -F1 -o %%b.hh %%b.rl
)
</pre>
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
