 * Download [Pango 1.40.1](http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.40/pango-1.40.1.tar.xz)
 * In all vcxproj files,
	* add `<Import Project="..\..\..\..\stack.props" />`
	* remove all `<Optimization>` lines
 * In `build\win32\vs12\pango-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\pango-rel</CopyDir>`
	* `<PangoSeparateVSDllSuffix>-1-vs$(VSVer)</PangoSeparateVSDllSuffix>` with
`<PangoSeparateVSDllSuffix>-1.0</PangoSeparateVSDllSuffix>`
