 * Download [libcroco 1.38.1](https://download.gnome.org/sources/libcroco/0.6/libcroco-0.6.11.tar.xz)
 * In `build\win32\vs12\croco-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\..\gtk\$(Platform)\$(Configuration)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\libcroco-rel</CopyDir>`
	* `<LibCrocoSeparateVSDllSuffix>-$(ApiVersion)-vs$(VSVer)</LibCrocoSeparateVSDllSuffix>` with
`<LibCrocoSeparateVSDllSuffix>-$(ApiVersion)</LibCrocoSeparateVSDllSuffix>`
