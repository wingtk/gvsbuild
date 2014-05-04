 * Download [Pixman 0.32.4](http://cairographics.org/releases/pixman-0.32.4.tar.gz)
 * Extract to `C:\mozilla-build\hexchat`
 * Get project files from [Chun-Wei's bug](https://bugs.freedesktop.org/attachment.cgi?id=58220)
 * In `build\win32\vc12\pixman.props`, replace:
	* `<PixmanEtcInstallRoot>..\..\..\..\vs10\$(PlatformName)</PixmanEtcInstallRoot>` with `<PixmanEtcInstallRoot>..\..\..\..\..\..\gtk\$(PlatformName)</PixmanEtcInstallRoot>`
	* `<CopyDir>$(PixmanEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\pixman-0.32.4-rel</CopyDir>`
 * In `build\win32\vc12\pixman.props`, add to `PixmanDoInstall`
`copy $(SolutionDir)$(Configuration)\$(Platform)\bin\*.exe $(CopyDir)\bin`
`copy $(SolutionDir)$(Configuration)\$(Platform)\bin\*.pdb $(CopyDir)\bin`
 * In `build\win32\vc12\testpixman.vcxproj`, replace `libpng15.lib` with `libpng16.lib`
 * Build `build\win32\vc12\pixman.vcxproj` and `build\win32\vc12\install.vcxproj`
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
