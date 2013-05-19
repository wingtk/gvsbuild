 * Download [FreeType 2.4.11](http://download.savannah.gnu.org/releases/freetype/freetype-2.4.11.tar.bz2)
 * Extract to `C:\mozilla-build\hexchat`
 * Open `builds\win32\vc2010\freetype.sln` with VS
 * add `stack.props` to the solution
 * Add `src\base\ftbdf.c` to `freetype\Source Files\FT_MODULES`
 * Change target name to `freetype` under _Configuration Properties_ `->` _General_
 * Change output directory to `.\..\..\..\objs\win32\vc11\` under _Configuration Properties_ `->` _General_
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
