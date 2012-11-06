 * Download [Pango 1.30.1](http://ftp.gnome.org/pub/GNOME/sources/pango/1.30/pango-1.30.1.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * In `build\win32\vs10\pango.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with  
`<GlibEtcInstallRoot>..\..\..\..\build\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with  
`<CopyDir>..\..\..\..\pango-1.32.1-rel</CopyDir>`
	* `<PangoSeparateVS10DllSuffix>-1-vs10</PangoSeparateVS10DllSuffix>` with  
`<PangoSeparateVS10DllSuffix>-1.0</PangoSeparateVS10DllSuffix>`
	* `<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;%(PreprocessorDefinitions)</PreprocessorDefinitions>` with  
`<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;WIN32%(PreprocessorDefinitions)</PreprocessorDefinitions>`
 * Replace `zlib1.lib` with `zdll.lib` in `build\win32\vs10\gdk-pixbuf.vcxproj`
 * Open `build\win32\vs10\gdk-pixbuf.sln` with VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
