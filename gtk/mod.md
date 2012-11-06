 * Download [GTK+ HEAD](http://git.gnome.org/browse/gtk+/log/?h=gtk-2-24)
 * Extract to `C:\mozilla-build\hexchat`
 * Patch with `patch -p1 -i gtk.patch`
 * In `build\win32\vs10\gtk+.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with  
`<GlibEtcInstallRoot>..\..\..\..\build\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with  
`<CopyDir>..\..\..\..\gtk-2.24.13-rel</CopyDir>`
	* `<GtkSeparateVS10DllSuffix>-2-vs10</GtkSeparateVS10DllSuffix>` with  
`<GtkSeparateVS10DllSuffix>-2.0</GtkSeparateVS10DllSuffix>`
	* `;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>` with  
`;..\..\..\gdk;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>`
	* `<ClCompile>` with  
`<ClCompile><MultiProcessorCompilation>true</MultiProcessorCompilation>`
	* `<AdditionalLibraryDirectories>$(GlibEtcInstallRoot)\lib;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>` with  
`<AdditionalLibraryDirectories>$(GlibEtcInstallRoot)\lib;$(OutDir)..;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>`
 * Open `build\win32\vs10\gtk+.sln` with VS
 * Set up _libwimp_ as a dependency of _install_
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
