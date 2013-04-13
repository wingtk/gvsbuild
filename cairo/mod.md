 * Download [cairo 1.12.14](http://cairographics.org/releases/cairo-1.12.14.tar.xz)
 * Download [VS solution](https://live.gnome.org/GTK%2B/Win32/MSVCCompilationOfGTKStack?action=AttachFile&do=get&target=cairo-vsprojects.zip)
 * Extract to `C:\mozilla-build\hexchat`
 * In `msvc\vc11\cairo.props`, replace:
	* `zlib1.lib` with `zdll.lib`
	* `<CairoEtcInstallRoot>..\..\..\vs10\$(Platform)</CairoEtcInstallRoot>` with  
`<CairoEtcInstallRoot>..\..\..\..\..\gtk\$(Platform)</CairoEtcInstallRoot>`
	* `<CopyDir>$(CairoEtcInstallRoot)</CopyDir>` with  
`<CopyDir>..\..\..\cairo-1.12.14-rel</CopyDir>`
	* `<CairoSeparateVS10DllSuffix>-vs10</CairoSeparateVS10DllSuffix>` with  
`<CairoSeparateVS10DllSuffix></CairoSeparateVS10DllSuffix>`
	* `<AdditionalIncludeDirectories>.;..\..;..\..\src;$(CairoEtcInstallRoot)\include;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>` with  
`<AdditionalIncludeDirectories>.;..\..;..\..\src;$(CairoEtcInstallRoot)\include;$(CairoEtcInstallRoot)\include\pixman-1;%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>`
	* `<ClCompile>` with  
`<ClCompile><MultiProcessorCompilation>true</MultiProcessorCompilation>`
	* `$(CopyDir)\include\cairo` with  
`$(CopyDir)\include`
	* `libpng15.lib` with  
`libpng16.lib`
	* Remove  
`copy $(SolutionDir)$(Configuration)\$(Platform)\include\*.h $(CopyDir)\include\cairo`
	* Add to `CairoDoInstall`:  
`copy $(SolutionDir)$(Configuration)\$(Platform)\bin\*.pdb $(CopyDir)\bin`
 * Add `src\cairo-path-stroke-traps.c` to the `cairo` project
 * Open `msvc\vc11\cairo.sln` with VS and select `Release_FC` configuration
 * Make `cairo-gobject` and `install` buildable
 * Make `install` depend on `cairo-gobject`
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
