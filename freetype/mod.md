 * Download [FreeType 2.5.0.1](http://download.savannah.gnu.org/releases/freetype/freetype-2.5.0.1.tar.bz2)
 * Extract to `C:\mozilla-build\hexchat`
 * In `builds\win32\vc11\freetype.vcxproj`, add:
	* `<ClCompile Include="..\..\..\src\base\ftbdf.c" />`
	* `<Import Project="..\..\..\..\stack.props" />` at the end
 * Delete `<Optimization>` lines in all `*.vcxproj` files
 * Open `builds\win32\vc11\freetype.sln` with VS
 * Change output directory to `.\..\..\..\objs\win32\vc11\` under _Configuration Properties_ `->` _General_
 * Add x64 solution configuration.
 * Open project properties and set Output Directory for *|x64 to `.\..\..\..\objs\x64\vc11\`
 * Set Intermediate Directory for *|x64 to the corresponding one from |Win32.
 * Change Target Name to `freetype` under _Configuration Properties_ `->` _General_ for Release|*
 * Set configuration to Release|Win32.
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
