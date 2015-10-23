 * Download [GLib 2.46.1](http://ftp.acc.umu.se/pub/GNOME/sources/glib/2.46/glib-2.46.1.tar.xz)
 * In all vcxproj files,
	* add `<Import Project="..\..\..\..\stack.props" />`
	* remove all `<Optimization>` lines
 * In `build\win32\vs12\glib-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\glib-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\glib-rel</CopyDir>`
	* `<GlibSeparateVSDllSuffix>-2-vs$(VSVer)</GlibSeparateVSDllSuffix>` with
`<GlibSeparateVSDllSuffix>-2.0</GlibSeparateVSDllSuffix>`
	* `<PythonPath>c:\python27</PythonPath>` with
`<PythonPath>..\..\..\..\..\....\..\python-2.7\$(Platform)</PythonPath>`
