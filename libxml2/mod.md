 * Download [libxml2 2.9.1](ftp://xmlsoft.org/libxml2/libxml2-2.9.1.tar.gz)
 * Remove the `iconv` project and its references from `win32\VC10\libxml2.sln`, `win32\VC10\libxml2.vcxproj` and `win32\VC10\runsuite.sln`
 * Open `win32\VC10\libxml2.sln` with VS
 * add `stack.props` to the solution
 * For the `libxml2` and `runsuite` projects:
	* Add `..\..\include;..\..\..\..\..\gtk\$(Platform)\include` to _Additional Include Directories_ under _Configuration Properties_ `->` _C/C++_ `->` _General_
	* Add `4996` to _Disable Specific Warnings_ under _Configuration Properties_ `->` _C/C++_ `->` _Advanced_
 * For the `libxml2` project:
	* Change _Configuration Type_ to _Dynamic Library (.dll)_ under _Configuration Properties_ `->` _General_
	* Add `..\..\..\..\..\gtk\$(Platform)\lib` to _Additional Library Directories_ under _Configuration Properties_ `->` _Linker_ `->` _General_
	* Add `ws2_32.lib;iconv.lib` to _Additional Dependencies_ under _Configuration Properties_ `->` _Linker_ `->` _Input_
