 * Download [cairo 1.15.2](http://cairographics.org/releases/cairo-1.15.2.tar.xz)
 * Download [VS solution](https://wiki.gnome.org/Projects/GTK%2B/Win32/MSVCCompilationOfGTKStack?action=AttachFile&do=get&target=cairo-vsprojects.zip)
 * In `msvc\vc12\cairo.props`, replace:
	* `<CairoEtcInstallRoot>..\..\..\vs10\$(Platform)</CairoEtcInstallRoot>` with
`<CairoEtcInstallRoot>..\..\..\..\..\gtk\$(Platform)</CairoEtcInstallRoot>`
	* `<CopyDir>$(CairoEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\cairo-rel</CopyDir>`
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
 * Open `msvc\vc12\cairo.sln` with VS and select `Release_FC` configuration
 * Make `cairo-gobject` and `install` buildable
 * Make `install` depend on `cairo-gobject`
 * In `msvc`:
  * Copy `vs12` directory and rename to `vs14`
 * in `msvc\vs14\cairo.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 11.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio 2010` with
    `# Visual Studio 14`
 * In `msvc\vs14` all `*.vcxproj` files, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="12.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`