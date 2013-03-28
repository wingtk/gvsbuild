 * Download [GLib 2.36.0](http://ftp.acc.umu.se/pub/gnome/sources/glib/2.36/glib-2.36.0.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * In `build\win32\vs10\glib.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with  
`<GlibEtcInstallRoot>..\..\..\..\build\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with  
`<CopyDir>..\..\..\..\glib-2.36.0-rel</CopyDir>`
	* `<GlibSeparateVS10DllSuffix>-2-vs10</GlibSeparateVS10DllSuffix>` with  
`<GlibSeparateVS10DllSuffix>-2.0</GlibSeparateVS10DllSuffix>`
	* `<ClCompile>` with  
`<ClCompile><MultiProcessorCompilation>true</MultiProcessorCompilation>`
 * Replace `zlib1.lib` with `zdll.lib` in `build\win32\vs10\gio.vcxproj`
 * Open `build\win32\vs10\glib.sln` with VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
