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
	<pre>..\\..\\build\\$(Platform)\\include</pre>
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
