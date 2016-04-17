 * In `build\win32\vs12\glib-networking-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\glib-networking-rel</CopyDir>`
 * In `build\win32`:
  * Copy `vs12` directory and rename to `vs14`
 * In `build\win32\glib-networking.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 12.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio 2013` with
    `# Visual Studio 14`
  * In `build\win32\vs14` all `*.vcxproj` files, replace:
   * `<Project DefaultTargets="Build" ToolsVersion="12.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
     `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
   * `<PlatformToolset>v120</PlatformToolset>` with
     `<PlatformToolset>v140</PlatformToolset>`
  * In `build\win32\vs14\glib-networking-version-paths.props`, replace:
   * `<VSVer>12</VSVer>` with
     `<VSVer>14</VSVer>`