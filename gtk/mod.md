 * Download [GTK+ 2.24.15](http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.15.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * Patch with `patch -p1 -i gtk.patch`
 * In `build\win32\vc11\gtk+.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with  
`<GlibEtcInstallRoot>..\..\..\..\build\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with  
`<CopyDir>..\..\..\..\gtk-2.24.15-rel</CopyDir>`
	* `<GtkSeparateVS10DllSuffix>-2-vs10</GtkSeparateVS10DllSuffix>` with  
`<GtkSeparateVS10DllSuffix>-2.0</GtkSeparateVS10DllSuffix>`
	* `;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>` with  
`;..\..\..\gdk;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>`
	* `<ClCompile>` with  
`<ClCompile><MultiProcessorCompilation>true</MultiProcessorCompilation>`
	* `<AdditionalLibraryDirectories>$(GlibEtcInstallRoot)\lib;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>` with  
`<AdditionalLibraryDirectories>$(GlibEtcInstallRoot)\lib;$(OutDir)..;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>`
 * Remove `<ModuleDefinitionFile>$(IntDir)libwimp.def</ModuleDefinitionFile>` from `build\win32\vs10\libwimp.vcxproj`
 * Open `build\win32\vc11\gtk+.sln` with VS
 * Set up _libwimp_ as a dependency of _install_
 * Set up _gdk_ and _gtk_ as dependencies of _libwimp_
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
