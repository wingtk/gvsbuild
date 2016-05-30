 * Download [FreeType 2.6.3](http://download.savannah.gnu.org/releases/freetype/freetype-2.6.3.tar.bz2)
 * Copy `builds\windows\vc2010` to `builds\windows\vc2013`
 * In `builds\windows\vc2013\freetype.vcxproj`:
	* Replace `<PlatformToolset>v100</PlatformToolset>` with `<PlatformToolset>v120</PlatformToolset>`
	* Replace all `vc2010` in `<OutDir>` and `<IntDir>` with `vc2013`
	* Replace
`
    <TargetName Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">freetype26</TargetName>
    <TargetName Condition="'$(Configuration)|$(Platform)'=='Release|x64'">freetype26</TargetName>
` with
`
    <TargetName Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">freetype</TargetName>
    <TargetName Condition="'$(Configuration)|$(Platform)'=='Release|x64'">freetype</TargetName>
`
	* Add `<ClCompile Include="..\..\..\src\base\ftbdf.c" />`
	* Add `<Import Project="..\..\..\..\stack.props" />` at the end
	* Delete `<Optimization>` lines
 * In `builds\windows`:
  * Copy `vc12` directory and rename to `vc14`
 * In `builds\windows\vc14\freetype.sln`, replace:
  * `Microsoft Visual Studio Solution File, Format Version 11.00` with
    `Microsoft Visual Studio Solution File, Format Version 14.00`
  * `# Visual Studio Express 2012 for Windows Desktop` with
    `# Visual Studio 14`
 * In `builds\windows\vc14\freetype.vcxproj`, replace:
  * `<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">` with
    `<Project DefaultTargets="Build" ToolsVersion="14.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">`
  * `<PlatformToolset>v120</PlatformToolset>` with
    `<PlatformToolset>v140</PlatformToolset>`