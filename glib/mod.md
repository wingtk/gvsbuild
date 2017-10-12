 * In `build\win32\vs12\glib-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot Condition="'$(Configuration)'=='Release_BundledPCRE'">..\..\..\..\..\..\..\gtk\$(Platform)\Release</GlibEtcInstallRoot>`
`<GlibEtcInstallRoot Condition="'$(Configuration)'=='Debug_BundledPCRE'">..\..\..\..\..\..\..\gtk\$(Platform)\Debug</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\glib-rel</CopyDir>`
	* `<GlibSeparateVSDllSuffix>-2-vs$(VSVer)</GlibSeparateVSDllSuffix>` with
`<GlibSeparateVSDllSuffix>-2.0</GlibSeparateVSDllSuffix>`
 * In `build\win32\vs14\glib-version-paths.props`, replace:
  * Add `<GlibEtcInstallRoot>..\..\..\..\..\..\..\gtk\$(Platform)\$(Configuration)</GlibEtcInstallRoot>` to `<PropertyGroup Label="UserMacros">` section