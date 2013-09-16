 * Download [ATK 2.9.3](http://ftp.gnome.org/pub/gnome/sources/atk/2.9/atk-2.9.3.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * In `build\win32\vc12\atk.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GLibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\atk-2.9.3-rel</CopyDir>`
	* `<AtkSeparateVSDllSuffix>-1-vs$(VSVer)</AtkSeparateVSDllSuffix>` with
`<AtkSeparateVSDllSuffix>-1.0</AtkSeparateVSDllSuffix>`
 * In `build\win32\vc12\atk.props`:
	*  add to `AtkDoInstall`
`copy $(SolutionDir)$(Configuration)\$(Platform)\bin\*.pdb $(CopyDir)\bin`
	*  add at the end
`<Import Project="..\..\..\..\stack.props" />`
 * In `build\win32\vc12\install.vcxproj`, replace `AtkEtcInstallRoot` with `GlibEtcInstallRoot`
 * Delete `<Optimization>` lines in all `*.vcxproj` files
 * Open `build\win32\vc12\atk.sln` with VS
 * Select `Release|Win32` configuration
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
