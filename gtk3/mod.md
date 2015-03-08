 * Download [GTK+ 3.14.11](http://ftp.gnome.org/pub/gnome/sources/gtk+/3.14/gtk+-3.14.11.tar.xz)
 * In `build\win32\vs12\gtk-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\gtk-install.props`:
	* Add `;$(BinDir)\libpixmap.dll` to `<InstalledDlls>`
	* Replace `copy $(BinDir)\*-vs$(VSVer).dll $(CopyDir)\bin` with
`copy $(BinDir)\*-3.0.dll $(CopyDir)\bin`
	* Add to `GtkDoInstall`:
`copy $(BinDir)\*.pdb $(CopyDir)\bin`
	* Add to `GtkDoInstall`:
`copy "$(BinDir)\libpixmap.dll" $(CopyDir)\lib\gtk-$(ApiVersion)\$(GtkHost)\engines`
 * In `build\win32\vs12\gtk-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk-rel</CopyDir>`
	* `<GtkSeparateVSDllSuffix>-3-vs$(VSVer)</GtkSeparateVSDllSuffix>` with
`<GtkSeparateVSDllSuffix>-3.0</GtkSeparateVSDllSuffix>`
 * Delete `<Optimization>` lines in all `*.vcxproj` files
