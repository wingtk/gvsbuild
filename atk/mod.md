 * Download [ATK 2.18.0](http://ftp.acc.umu.se/pub/GNOME/sources/atk/2.18/atk-2.18.0.tar.xz)
 * In `build\win32\vs12\atk-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\atk-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GLibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\atk-rel</CopyDir>`
	* `<AtkSeparateVSDllSuffix>-1-vs$(VSVer)</AtkSeparateVSDllSuffix>` with
`<AtkSeparateVSDllSuffix>-1.0</AtkSeparateVSDllSuffix>`
 * In `build\win32\vs12\atk.vcxproj`:
	*  add `<Import Project="..\..\..\..\stack.props" />`
	* Remove all `<Optimization>` lines
 * In `build\win32\vs12\install.vcxproj`:
	* replace `AtkEtcInstallRoot` with `GlibEtcInstallRoot`
