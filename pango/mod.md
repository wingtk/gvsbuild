 * Download [Pango 1.36.8](http://ftp.gnome.org/pub/GNOME/sources/pango/1.36/pango-1.36.8.tar.xz)
 * Patch with `patch -p1 -i pango-synthesize-all-fonts.patch`
 * In all vcxproj files,
	* add `<Import Project="..\..\..\..\stack.props" />`
	* remove all `<Optimization>` lines
 * In `build\win32\vs12\pango-build-defines.props`, replace:
	* `intl.lib` with `libintl.lib`
	* `<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;%(PreprocessorDefinitions)</PreprocessorDefinitions>` with
`<PreprocessorDefinitions>HAVE_CONFIG_H;G_DISABLE_SINGLE_INCLUDES;WIN32;%(PreprocessorDefinitions)</PreprocessorDefinitions>`
 * In `build\win32\vs12\pango-install-bin.props`, replace:
	* Add to `PangoDoInstallBin`:
```
copy $(Configuration)\$(Platform)\bin\$(PangoDllPrefix)pangoft2.pdb $(CopyDir)\bin

copy $(Configuration)\$(Platform)\bin\$(PangoDllPrefix)pangocairo.pdb $(CopyDir)\bin

if "$(Configuration)" == "Release_FC" copy $(SolutionDir)\Release\$(Platform)\bin\$(PangoDllPrefix)pango.pdb $(CopyDir)\bin

if "$(Configuration)" == "Release_FC" copy $(SolutionDir)\Release\$(Platform)\bin\$(PangoDllPrefix)pangowin32.pdb $(CopyDir)\bin
```
 * In `build\win32\vs12\pango-version-paths.props`, replace:
	* `<GlibEtcInstallRoot>$(SolutionDir)\..\..\..\..\vs$(VSVer)\$(Platform)</GlibEtcInstallRoot>` with
`<GlibEtcInstallRoot>..\..\..\..\..\..\gtk\$(Platform)</GlibEtcInstallRoot>`
	* `<CopyDir>$(GlibEtcInstallRoot)</CopyDir>` with
`<CopyDir>..\..\..\..\pango-rel</CopyDir>`
	* `<PangoSeparateVSDllSuffix>-1-vs$(VSVer)</PangoSeparateVSDllSuffix>` with
`<PangoSeparateVSDllSuffix>-1.0</PangoSeparateVSDllSuffix>`
 * In `build\win32\vs12\pangoft2.vcxproj`, replace:
	* `<AdditionalDependencies>fontconfig.lib;freetype.lib;%(AdditionalDependencies)</AdditionalDependencies>` with
`<AdditionalDependencies>fontconfig.lib;freetype.lib;harfbuzz.lib;%(AdditionalDependencies)</AdditionalDependencies>`
