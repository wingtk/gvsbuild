 * Download [glib-networking 2.46.1](https://github.com/nice-software/glib-networking/releases/download/2.46.1-openssl/glib-networking-2.46.1.tar.xz)
 * In `build\win32\vs12\glib-networking-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\glib-networking-rel</CopyDir>`
