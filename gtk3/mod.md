 * Download [GTK+ 3.14.8](http://ftp.gnome.org/pub/gnome/sources/gtk+/3.14/gtk+-3.14.8.tar.xz)
 * Extract to `C:\mozilla-build\gtk`
 * Patch with `patch -p1 -i gtk-revert-scrolldc-commit.patch`
 * Patch with `patch -p1 -i gtk-bgimg.patch`
 * Patch with `patch -p1 -i gtk-statusicon.patch`
 * Patch with `patch -p1 -i gtk-accel.patch`
 * In `build\win32\vs12\gtk-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\gtk-install.props`:
	* Add `;$(BinDir)\libpixmap.dll` to `<InstalledDlls>`
	* Replace `copy $(BinDir)\*-vs$(VSVer).dll $(CopyDir)\bin` with
`copy $(BinDir)\*-2.0.dll $(CopyDir)\bin`
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
 * Open `build\win32\vs12\gtk+.sln` with VS
 * Select `Release|Win32` configuration
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
