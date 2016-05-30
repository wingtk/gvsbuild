 * Download [libcroco 1.38.1](http://ftp.acc.umu.se/pub/GNOME/sources/libcroco/0.6/libcroco-0.6.11.tar.xz)
 * In `build\win32\vs12\croco-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\libcroco-rel</CopyDir>`
	* `<LibCrocoSeparateVSDllSuffix>-$(ApiVersion)-vs$(VSVer)</LibCrocoSeparateVSDllSuffix>` with
`<LibCrocoSeparateVSDllSuffix>-$(ApiVersion)</LibCrocoSeparateVSDllSuffix>`
 * In `build\win32`:
  * Copy `vs12` directory and rename to `vs14`
 * In `build\win32\vs14\croco-version-paths.props`, replace:
  * `<VSVer>12</VSVer>` with
    `<VSVer>14</VSVer>`