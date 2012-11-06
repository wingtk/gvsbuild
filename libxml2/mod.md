 * Download [libxml2 2.9.0](ftp://xmlsoft.org/libxml2/libxml2-2.9.0.tar.gz)
 * Extract to `C:\mozilla-build\hexchat`
 * Open `win32\VC10\libxml2.sln` with VS
 * For all projects:
	* Change _Configuration Type_ to _Dynamic Library (.dll)_ under _Configuration Properties_ `->` _General_
 * For the libxml2 project:
	* Add `..\..\include;..\..\..\build\$(Platform)\include` to _Additional Include Directories_ under _Configuration Properties_ `->` _C/C++_ `->` _General_
	* Add `..\..\..\build\$(Platform)\lib` to _Additional Library Directories_ under _Configuration Properties_ `->` _Linker_ `->` _General_
	* Add `ws2_32.lib;iconv.lib` to _Additional Dependencies_ under _Configuration Properties_ `->` _Linker_ `->` _Input_
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
