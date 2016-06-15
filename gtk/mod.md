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
`<GlibEtcInstallRoot>..\..\..\..\..\..\..\gtk\$(Platform)\$(Configuration)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk-rel</CopyDir>`
	* `<GtkSeparateVSDllSuffix>-2-vs$(VSVer)</GtkSeparateVSDllSuffix>` with
`<GtkSeparateVSDllSuffix>-2.0</GtkSeparateVSDllSuffix>`
 * Delete `<Optimization>` lines in all `*.vcxproj` files
