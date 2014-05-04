 * Download [GTK+ 2.24.23](http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.23.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * Patch with `patch -p1 -i gtk-revert-scrolldc-commit.patch`
 * Patch with `patch -p1 -i gtk-bgimg.patch`
 * Patch with `patch -p1 -i gtk-statusicon.patch`
 * Patch with `patch -p1 -i gtk-accel.patch`
 * In `build\win32\vc12\gtk+.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<GlibEtcInstallRoot>..\..\..\..\vs10\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\gtk-2.24.23-rel</CopyDir>`
	* `<GtkSeparateVS10DllSuffix>-2-vs10</GtkSeparateVS10DllSuffix>` with
`<GtkSeparateVS10DllSuffix>-2.0</GtkSeparateVS10DllSuffix>`
	* `<ClCompile>` with
`<ClCompile><MultiProcessorCompilation>true</MultiProcessorCompilation>`
	* `*-vs10.dll` with `*-2.0.dll`
	* Add to `GtkDoInstall`:
`copy $(Configuration)\$(Platform)\bin\*.pdb $(CopyDir)\bin`
 * In `build\win32\vc12\gtk+.props`, add `<Import Project="..\..\..\..\stack.props" />` at the end
 * Delete `<Optimization>` lines in all `*.vcxproj` files
 * Open `build\win32\vc12\gtk+.sln` with VS
 * Select `Release|Win32` configuration
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
