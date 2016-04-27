 * In `build\win32\vs12\atk-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GLibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\atk-rel</CopyDir>`
	* `<AtkSeparateVSDllSuffix>-1-vs$(VSVer)</AtkSeparateVSDllSuffix>` with
`<AtkSeparateVSDllSuffix>-1.0</AtkSeparateVSDllSuffix>`
 * Add to `build\win32\vs14` directory