 * Download [GTK+ 3.18.1](http://ftp.acc.umu.se/pub/GNOME/sources/gtk+/3.18/gtk+-3.18.1.tar.xz)
 * In `build\win32\vs12\gtk-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\gtk-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk-rel</CopyDir>`
	* `<GtkSeparateVSDllSuffix>-3-vs$(VSVer)</GtkSeparateVSDllSuffix>` with
`<GtkSeparateVSDllSuffix>-3.0</GtkSeparateVSDllSuffix>`
 * Delete `<Optimization>` lines in all `*.vcxproj` files
 * In `build\win32\vs12\gtk3-install.props`, replace:
 	* `$(CopyDir)\bin\glib-compile-schemas.exe $(CopyDir)\share\glib-2.0\schemas` with:
`$(GlibEtcInstallRoot)\bin\glib-compile-schemas.exe $(CopyDir)\share\glib-2.0\schemas`
