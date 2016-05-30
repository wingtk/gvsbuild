 * Download [libepoxy 1.3.1](https://github.com/anholt/libepoxy/releases/download/v1.3.1/libepoxy-1.3.1.tar.bz2)
 * In `build\win32\vs12\epoxy-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\libepoxy-rel</CopyDir>`
	* `<EpoxySeparateVSDllSuffix>-vs$(VSVer)</EpoxySeparateVSDllSuffix>` with
<EpoxySeparateVSDllSuffix>-0</EpoxySeparateVSDllSuffix>
	* `<PythonPath>c:\python34</PythonPath>` with
<PythonPath>c:\python27</PythonPath>
 * In `build/win32/vs12/wgl_core_and_exts.vcxproj`, remove:
	* `<Command>$(TargetPath)</Command>`
 * In `build/win32/vs12/wgl_per_context_funcptrs.vcxproj`, remove:
	* `<Command>$(TargetPath)</Command>`
 * In `build/win32/vs12/wgl_usefontbitmaps.vcxproj`, remove:
	* `<Command>$(TargetPath)</Command>`
 * Add to `build\win32\vs14` directory