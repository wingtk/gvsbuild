 * In `build\win32\vs12\gtk3-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk3-rel</CopyDir>`
	* `<GtkSeparateVSDllSuffix>-3-vs$(VSVer)</GtkSeparateVSDllSuffix>` with
`<GtkSeparateVSDllSuffix>-3.0</GtkSeparateVSDllSuffix>`
 * In `build\win32\vs12\gtk3-install.props`, remove:
 	* `echo "Generating icon cache......"`
`$(CopyDir)\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "$(CopyDir)\share\icons\hicolor"`
 * In `build\win32`:
  * Copy `vs12` directory and rename to `vs14`
 * In `build\win32\vs14\gtk+.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 12.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio 2013` with
    `# Visual Studio 14`
 * In `build\win32\vs14` all `*.vcxproj` files, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`
 * In `build\win32\vs14\gtk3-version-paths.props`, replace:
  * `<VSVer>12</VSVer>` with
    `<VSVer>14</VSVer>`
 * In `build\win32\vs14\README.txt`, replace:
  * Replace all `vs12` to `vs14`