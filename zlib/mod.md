 * Download [zlib 1.2.8](http://zlib.net/zlib128.zip)
 * Remove `Optimization` settings in `contrib\vc12\*.vcxproj`
 * In `contrib\vstudio\vc12\zlibvc.sln`:
	* Remove `Itanium` platform
	* Change `Configuration` to `ReleaseWithoutAsm`
	* Add `stack.props` to each project
	* Select all projects to be built
	* For `zlibstat` and `zlibvc` remove any files that belong to `minizip`
	* Replace `contrib\vstudio\vc12\zlibvc.def` with `win32\zlib.def`
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
 * Add to `build\win32\vs14` directory