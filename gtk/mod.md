 * Download [GTK+ 2.24.30](http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.30.tar.xz)
 * In `build\win32\vs12\gtk-install.props`:
	* Add `;$(BinDir)\libpixmap.dll` to `<InstalledDlls>`
	* Add to `<GtkDoInstall`:
`
copy "$(BinDir)\$(GtkDllPrefix)gdk$(GtkDllSuffix).pdb" $(CopyDir)\bin
copy "$(BinDir)\libpixmap.pdb" $(CopyDir)\bin
copy "$(BinDir)\libwimp.pdb" $(CopyDir)\bin
`
	* Add to `GtkDoInstall`:
`copy $(BinDir)\*.pdb $(CopyDir)\bin`
	* Add to `GtkDoInstall`:
`copy "$(BinDir)\libpixmap.dll" $(CopyDir)\lib\gtk-$(ApiVersion)\$(GtkHost)\engines`
 * In `build\win32\vs12\gtk-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk-rel</CopyDir>`
	* `<GtkSeparateVSDllSuffix>-2-vs$(VSVer)</GtkSeparateVSDllSuffix>` with
`<GtkSeparateVSDllSuffix>-2.0</GtkSeparateVSDllSuffix>`
 * Delete `<Optimization>` lines in all `*.vcxproj` files
 * In `build\win32`:
  * Copy `vs12` directory and rename to `vs14`
 * In `build\win32\vs14\gtk+.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 13.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio 2013` with
    `# Visual Studio 14`
 * In `build\win32\vs14` all `*.vcxproj` files, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`
 * In `build\win32\vs14\gtk-version-paths.props`, replace:
  * `<VSVer>10</VSVer>` with
    `<VSVer>14</VSVer>`