 * Download [libepoxy 1.3.1](https://github.com/anholt/libepoxy/releases/download/v1.3.1/libepoxy-1.3.1.tar.bz2)
 * In `build\win32\vs12\epoxy-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\libepoxy-rel</CopyDir>`
	* `<EpoxySeparateVSDllSuffix>-vs$(VSVer)</EpoxySeparateVSDllSuffix>` with
<EpoxySeparateVSDllSuffix>-0</EpoxySeparateVSDllSuffix>
	* `<PythonPath>c:\python34</PythonPath>` with
<PythonPath>c:\python27</PythonPath>
 * In `build/win32/vs12/wgl_core_and_exts.vcxproj`, remove:
	* `<Command>$(TargetPath)</Command>`
 * In `build/win32/vs12/wgl_per_context_funcptrs.vcxproj`, remove:
	* `<Command>$(TargetPath)</Command>`
 * In `build/win32/vs12/wgl_usefontbitmaps.vcxproj`, remove:
	* `<Command>$(TargetPath)</Command>`
 * In `build\win32`:
  * Copy `vs12` directory and rename to `vs14`
 * In `build\win32\vs14\epoxy.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 13.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio 2013` with
    `# Visual Studio 14`
 * In `build\win32\vs14` all `*.vcxproj` files, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="12.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`
 * In `build\win32\vs14\epoxy-version-paths.props`, replace:
  * `<VSVer>12</VSVer>` with
    `<VSVer>14</VSVer>`