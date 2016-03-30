 * In `build\win32\vs12\gtk3-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk3-rel</CopyDir>`
	* `<GtkSeparateVSDllSuffix>-3-vs$(VSVer)</GtkSeparateVSDllSuffix>` with
`<GtkSeparateVSDllSuffix>-3.0</GtkSeparateVSDllSuffix>`
 * In `build\win32\vs12\gtk3-install.props`, remove:
 	* `echo "Generating icon cache......"`
`$(CopyDir)\bin\gtk-update-icon-cache.exe --ignore-theme-index --force "$(CopyDir)\share\icons\hicolor"`
