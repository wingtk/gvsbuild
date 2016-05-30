 * Download [Pixman 0.34.0](http://cairographics.org/releases/pixman-0.34.0.tar.gz)
 * Get project files from [Chun-Wei's bug](https://bugs.freedesktop.org/attachment.cgi?id=58220)
 * In `build\win32\vc12\pixman.props`, replace:
	* `<PixmanEtcInstallRoot>..\..\..\..\vs10\$(PlatformName)</PixmanEtcInstallRoot>` with `<PixmanEtcInstallRoot>..\..\..\..\..\..\gtk\$(PlatformName)</PixmanEtcInstallRoot>`
	* `<CopyDir>$(PixmanEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\pixman-rel</CopyDir>`
 * In `build\win32\vc12\pixman.props`, add to `PixmanDoInstall`
`copy $(SolutionDir)$(Configuration)\$(Platform)\bin\*.exe $(CopyDir)\bin`
`copy $(SolutionDir)$(Configuration)\$(Platform)\bin\*.pdb $(CopyDir)\bin`
 * Build `build\win32\vc12\pixman.vcxproj` and `build\win32\vc12\install.vcxproj`
 * In `build\win32`:
  * Copy `vc12` directory and rename to `vc14`
 * In `build\win32\vc14` all `*.vcxproj` files, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="12.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`