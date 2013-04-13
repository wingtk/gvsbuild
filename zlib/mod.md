 * Download [zlib 1.2.7](http://zlib.net/zlib127.zip)
 * Extract to `C:\mozilla-build\hexchat`
 * Remove `Optimization` settings in `contrib\vc11\*.vcxproj`
 * In `contrib\vc11\zlibvc.sln`:
	* Remove `Itanium` platform
	* Change `Configuration` to `ReleaseWithoutAsm`
	* Add `stack.props` to each project
	* Select all projects to be built
	* For `miniunz`, `minizip` and `testzlibdll`, change:
		* `Additional Library Directories` to `$(OutDir)..\ZlibDllReleaseWithoutAsm`
		* `Additional Dependencies` to `zlibwapi.lib;%(AdditionalDependencies)`
	* Correct `Output Directory` and `Intermediate Directory` for `minizip` on `x64`
	* Fix runtime libraries (`/MT` for static libraries, `/MD` for DLL builds)
	* Select `Generate Debug Info` for `zlibvc` and for `testzlib` on `x64`
 * Build with `build-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
