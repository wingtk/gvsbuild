 * Download [HarfBuzz 0.9.13](http://cgit.freedesktop.org/harfbuzz/snapshot/harfbuzz-0.9.13.zip)
 * Download [blinkseb's HarfBuzz solution](https://github.com/blinkseb/harfbuzz)
 * Extract to `C:\mozilla-build\hexchat`
 * Rename `src\hb-version.h.in` to `src\hb-version.h` and fix the following macros:
	* `HB_VERSION_MAJOR` (0)
	* `HB_VERSION_MINOR` (9)
	* `HB_VERSION_MICRO` (13)
	* `HB_VERSION_STRING` ("0.9.13")
 * Open `win32\harfbuzz.sln` with VS
 * Add to _Additional Include Directories_ under _Configuration Properties_ `->` _C/C++_ `->` _General_:
	<pre>..\\..\\build\\$(Platform)\\include
..\\..\\build\\$(Platform)\\include\\glib-2.0
..\\..\\build\\$(Platform)\\lib\\glib-2.0\\include</pre>
 * Change to DLL
 * Add lib path and fix freetype name
 * Generate .def file with `./autogen.sh && cd src && make harfbuzz.def`
 * Add .def file in VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
