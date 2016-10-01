 * In `build\win32\vc12\gdk-pixbuf-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\..\gtk\$(Platform)\$(Configuration)</GlibEtcInstallRoot>`
`<GlibEtcInstallRoot Condition="'$(Configuration)'=='Release_GDI+'">$(SolutionDir)\..\..\..\..\..\..\..\gtk\$(Platform)\Release</GlibEtcInstallRoot>`
`<GlibEtcInstallRoot Condition="'$(Configuration)'=='Debug_GDI+'">$(SolutionDir)\..\..\..\..\..\..\..\gtk\$(Platform)\Debug</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gdk-pixbuf-rel</CopyDir>`
	* `<GdkPixbufSeparateVSDllSuffix>-2-vs$(VSVer)</GdkPixbufSeparateVSDllSuffix>` with
`<GdkPixbufSeparateVSDllSuffix>-2.0</GdkPixbufSeparateVSDllSuffix>`
