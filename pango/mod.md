 * Download [Pango 1.36.5](http://ftp.gnome.org/pub/GNOME/sources/pango/1.36/pango-1.36.5.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * Patch with `patch -p1 -i pango-synthesize-all-fonts.patch`
 * In `build\win32\vc12\pango-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;%(PreprocessorDefinitions)</PreprocessorDefinitions>` with
`<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;WIN32;%(PreprocessorDefinitions)</PreprocessorDefinitions>`
 * In `build\win32\vc12\pango-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\pango-1.36.5-rel</CopyDir>`
	* `<PangoSeparateVSDllSuffix>-1-vs$(VSVer)</PangoSeparateVSDllSuffix>` with
`<PangoSeparateVSDllSuffix>-1.0</PangoSeparateVSDllSuffix>`
 * In `build\win32\vc12\pango-install-bin.props`, replace:
	* Add to `PangoDoInstall`:
`copy $(Configuration)\$(Platform)\bin\*.pdb $(CopyDir)\bin`
 * In `build\win32\vc12\pangooft2.vcxproj`, replace:
	* `<AdditionalDependencies>fontconfig.lib;freetype.lib;%(AdditionalDependencies)</AdditionalDependencies>` with
`<AdditionalDependencies>fontconfig.lib;freetype.lib;harfbuzz.lib;%(AdditionalDependencies)</AdditionalDependencies>`
 * Open `build\win32\vc12\pango_fc.sln` with VS
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
