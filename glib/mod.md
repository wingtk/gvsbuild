 * Download [GLib 2.42.2](http://ftp.acc.umu.se/pub/gnome/sources/glib/2.42/glib-2.42.2.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * In all vcxproj files,
	* add `<Import Project="..\..\..\..\stack.props" />`
	* remove all `<Optimization>` lines
 * In `build\win32\vs12\glib-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
 * In `build\win32\vs12\glib-install.props`, add to `GlibDoInstall`:
`copy $(BinDir)\*.pdb $(CopyDir)\bin
copy ..\..\..\gobject\gobjectnotifyqueue.c $(CopyDir)\include\glib-2.0\gobject\gobjectnotifyqueue.c`
 * In `build\win32\vs12\glib-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\glib-rel</CopyDir>`
	* `<GlibSeparateVS11DllSuffix>-2-vs$(VSVer)</GlibSeparateVS11DllSuffix>` with
`<GlibSeparateVS11DllSuffix>-2.0</GlibSeparateVS11DllSuffix>`
	* `<PythonPath>c:\python27</PythonPath>` with
`<PythonPath>..\..\..\..\..\....\..\python-2.7\$(Platform)</PythonPath>`
 * Open `build\win32\vs12\glib.sln` with VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
