 * Download [GTK+ 2.24.15](http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.15.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * Patch with `patch -p1 -i gtk-pixmap.patch`
 * In `build\win32\vc11\gtk+.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with  
`<GlibEtcInstallRoot>..\..\..\..\build\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with  
`<CopyDir>..\..\..\..\gtk-2.24.17-rel</CopyDir>`
	* `<GtkSeparateVS10DllSuffix>-2-vs10</GtkSeparateVS10DllSuffix>` with  
`<GtkSeparateVS10DllSuffix>-2.0</GtkSeparateVS10DllSuffix>`
	* `<ClCompile>` with  
`<ClCompile><MultiProcessorCompilation>true</MultiProcessorCompilation>`
	* `*-vs10.dll` with `*-2.0.dll`
 * Open `build\win32\vc11\gtk+.sln` with VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
