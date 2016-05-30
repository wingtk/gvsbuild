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
 * In `build\win32`:
  * Copy `vs12` directory and rename to `vs14`
 * In `build\win32\vs14\zlib.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 13.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio 2013` with
    `# Visual Studio 14`
 * In `build\win32\vs14` all `*.vcxproj` files, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`
 * In `build\win32\vs14\zlib-version-paths.props`, replace:
  * `<VSVer>12</VSVer>` with
    `<VSVer>14</VSVer>`