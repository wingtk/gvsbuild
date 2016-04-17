 * In `build\win32\vs12\atk-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GLibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\atk-rel</CopyDir>`
	* `<AtkSeparateVSDllSuffix>-1-vs$(VSVer)</AtkSeparateVSDllSuffix>` with
`<AtkSeparateVSDllSuffix>-1.0</AtkSeparateVSDllSuffix>`
 * In `build\win32`:
  * Copy `vs12` directory and rename to `vs14`
 * In `build\win32\vs14\atk.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 12.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio 2013` with
    `# Visual Studio 14`
 * In `build\win32\vs14` all `*.vcxproj` files, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`
 * In `build\win32\vs14\atk-version-paths.props`, replace:
  * `<VSVer>12</VSVer>` with
    `<VSVer>14</VSVer>`
 * In `build\win32\vs14\README.txt`, replace:
  * Replace all `vs12` on `vs14`