 * In `build\win32\vs12\glib-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\glib-rel</CopyDir>`
	* `<GlibSeparateVSDllSuffix>-2-vs$(VSVer)</GlibSeparateVSDllSuffix>` with
`<GlibSeparateVSDllSuffix>-2.0</GlibSeparateVSDllSuffix>`
