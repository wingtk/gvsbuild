 * Download [GDK-PixBuf 2.32.1](http://ftp.acc.umu.se/pub/GNOME/sources/gdk-pixbuf/2.32/gdk-pixbuf-2.32.1.tar.xz)
 * In `build\win32\vc12\gdk-pixbuf-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gdk-pixbuf-rel</CopyDir>`
	* `<GdkPixbufSeparateVSDllSuffix>-2-vs$(VSVer)</GdkPixbufSeparateVSDllSuffix>` with
`<GdkPixbufSeparateVSDllSuffix>-2.0</GdkPixbufSeparateVSDllSuffix>`
