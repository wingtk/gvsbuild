 * Download [Pango 1.38.0](http://ftp.acc.umu.se/pub/GNOME/sources/pango/1.38/pango-1.38.0.tar.xz)
 * In all vcxproj files,
	* add `<Import Project="..\..\..\..\stack.props" />`
	* remove all `<Optimization>` lines
 * In `build\win32\vs12\pango-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\pango-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\pango-rel</CopyDir>`
	* `<PangoSeparateVSDllSuffix>-1-vs$(VSVer)</PangoSeparateVSDllSuffix>` with
`<PangoSeparateVSDllSuffix>-1.0</PangoSeparateVSDllSuffix>`
 * In `build\win32\vs12\pangoft2.vcxproj`, replace:
	* `<AdditionalDependencies>fontconfig.lib;freetype.lib;%(AdditionalDependencies)</AdditionalDependencies>` with
`<AdditionalDependencies>fontconfig.lib;freetype.lib;harfbuzz.lib;%(AdditionalDependencies)</AdditionalDependencies>`
