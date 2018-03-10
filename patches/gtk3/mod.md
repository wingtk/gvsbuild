 * In `build\win32\vs12\gtk3-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\..\gtk\$(Platform)\$(Configuration)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk3-rel</CopyDir>`
	* `<GtkSeparateVSDllSuffix>-3-vs$(VSVer)</GtkSeparateVSDllSuffix>` with
`<GtkSeparateVSDllSuffix>-3.0</GtkSeparateVSDllSuffix>`
