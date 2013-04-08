 * Download [Pango 1.32.5](http://ftp.gnome.org/pub/GNOME/sources/pango/1.32/pango-1.32.5.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * Patch with `patch -p1 -i pango.patch`
 * In `build\win32\vc11\pango.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with  
`<GlibEtcInstallRoot>..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with  
`<CopyDir>..\..\..\..\pango-1.32.5-rel</CopyDir>`
	* `<PangoSeparateVS10DllSuffix>-1-vs10</PangoSeparateVS10DllSuffix>` with  
`<PangoSeparateVS10DllSuffix>-1.0</PangoSeparateVS10DllSuffix>`
	* `<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;%(PreprocessorDefinitions)</PreprocessorDefinitions>` with  
`<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;WIN32%(PreprocessorDefinitions)</PreprocessorDefinitions>`
	* Add to `PangoDoInstall`:  
`copy $(Configuration)\$(Platform)\bin\*.pdb $(CopyDir)\bin`
 * Open `build\win32\vc11\pango_fc.sln` with VS
 * Add harfbuzz.lib to pangoft2 input
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
