 * Download [glib-networking 2.46.0](https://github.com/nice-software/glib-networking/releases/download/2.46.0-openssl/glib-networking-2.46.0.tar.xz)
 * In `build\win32\vs12\glib-networking-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\glib-networking-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\glib-networking-rel</CopyDir>`
 * In `build\win32\vs12\glib-networking-install.props`, replase:
	* `$(CopyDir)\bin\gio-querymodules $(CopyDir)\lib\gio\modules` with
`$(GlibEtcInstallRoot)\bin\gio-querymodules $(CopyDir)\lib\gio\modules`
