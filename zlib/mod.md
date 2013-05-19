 * Download [zlib 1.2.7](http://zlib.net/zlib127.zip)
 * Extract to `C:\mozilla-build\hexchat`
 * Remove `Optimization` settings in `contrib\vc11\*.vcxproj`
 * In `contrib\vstudio\vc11\zlibvc.sln`:
	* Remove `Itanium` platform
	* Change `Configuration` to `ReleaseWithoutAsm`
	* Add `stack.props` to each project
	* Select all projects to be built
	* For `zlibstat` and `zlibvc` remove any files that belong to `minizip`
	* Replace `contrib\vstudio\vc11\zlibvc.def` with `win32\zlib.def`
	* For `miniunz`, `minizip` and `testzlibdll`, change:
		* `Additional Library Directories` to `$(OutDir)..\ZlibDllReleaseWithoutAsm`
		* `Additional Dependencies` to `zlibwapi.lib;%(AdditionalDependencies)`
	* Correct `Output Directory` and `Intermediate Directory` for `minizip` on `x64`
	* Fix runtime libraries (`/MT` for static libraries, `/MD` for DLL builds)
	* Select `Generate Debug Info` for `zlibvc` and for `testzlib` on `x64`
	* For all projects:
		* Remove `ZLIB_WINAPI` from `PreprocessorDefinitions`
		* Replace `zlibwapi.lib` with `zlib1.lib`
		* Replace `zlibwapi.dll` with `zlib1.dll`
		* Replace `zlibwapi.pdb` with `zlib1.pdb`
		* Replace `zlibwapi.map` with `zlib1.map`
	* Select `miniunz` and `minizip` not to be built
 * Patch with `patch -p1 -i zlib-minizip-win8.patch`
 * Open `contrib\vstudio\vc11\zlibvc.sln` with VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
