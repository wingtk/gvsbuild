 * Download [HarfBuzz 0.9.29](http://cgit.freedesktop.org/harfbuzz/snapshot/harfbuzz-0.9.29.tar.gz)
 * Download [blinkseb's HarfBuzz solution](https://github.com/blinkseb/harfbuzz)
 * Extract to `C:\mozilla-build\hexchat`
 * Copy `src\hb-version.h.in` as `src\hb-version.h` and fix the following macros:
	* `HB_VERSION_MAJOR` (0)
	* `HB_VERSION_MINOR` (9)
	* `HB_VERSION_MICRO` (28)
	* `HB_VERSION_STRING` ("0.9.28")
 * Open `win32\harfbuzz.sln` with VS
 * Generate .def file:
	* Open solution
	* Select `Release|Win32` configuration
	* Build solution
	* Start VS2012 Command Prompt
	<pre>cd C:\mozilla-build\hexchat\build\Win32\harfbuzz-0.9.28\win32\libs\Release
powershell.exe -command "Out-File -Encoding utf8 -FilePath ..\\..\\harfbuzz.def -InputObject 'EXPORTS'; dumpbin /LINKERMEMBER harfbuzz.lib | Select-String ' .. \_(hb\_.*)$' | %{ $_.Matches[0].Groups[1].Value } | Out-File -Encoding utf8 -Append -FilePath ..\\..\\harfbuzz.def"</pre>
	* Go back to solution and change the project type to DLL.
	* Add `EXPORTS` at the top of harfbuzz.def
	* Set _Linker_ `->` _Input_ `->` _Module DefinitionFile_ to `harfbuzz.def`
 * Add lib path and fix freetype name
 * Add `<Import Project="..\..\stack.props" />`
 * Add `<Import Project="harfbuzz.props" />`
 * Select `Release|Win32` configuration
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
