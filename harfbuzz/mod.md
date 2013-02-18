 * Download [HarfBuzz 0.9.12](http://cgit.freedesktop.org/harfbuzz/snapshot/harfbuzz-0.9.12.zip)
 * Download [blinkseb's HarfBuzz solution](https://github.com/blinkseb/harfbuzz)
 * Extract to `C:\mozilla-build\hexchat`
 * Rename `hb-version.h.in` to `hb-version.h` and fix the following macros:
	* `HB_VERSION_MAJOR` (0)
	* `HB_VERSION_MINOR` (9)
	* `HB_VERSION_MICRO` (12)
	* `HB_VERSION_STRING` ("0.9.12")
 * Open `win32\harfbuzz.sln` with VS
 * Add to _Additional Include Directories_ under _Configuration Properties_ `->` _C/C++_ `->` _General_:
	<pre>..\\..\\build\\$(Platform)\\include
..\\..\\build\\$(Platform)\\include\\glib-2.0
..\\..\\build\\$(Platform)\\lib\\glib-2.0\\include</pre>
 * Change to DLL
 * Add lib path and fix freetype name
 * Generate .def file with `nm -D -g --defined-only .libs/libharfbuzz.so | cut -d ' ' -f 3 | egrep -v '^(__bss_start|_edata|_end)' | sort > actual-abi`
 * Add .def file in VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
