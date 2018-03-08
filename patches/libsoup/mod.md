 * In `build\win32\vs12\soup-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\libsoup-rel</CopyDir>`
	* `<SoupSeparateVSDllSuffix>-$(ApiVersion)-vs$(VSVer)</SoupSeparateVSDllSuffix>` with
`<SoupSeparateVSDllSuffix>-$(ApiVersion)</SoupSeparateVSDllSuffix>`
