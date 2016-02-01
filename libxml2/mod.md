* Download [libxml2 2.9.3](ftp://xmlsoft.org/libxml2/libxml2-2.9.3.tar.gz)
* Copy win32\VC10 to win32\VC12
* Remove the `iconv` project and its references from `win32\VC12\libxml2.sln`, `win32\VC12\libxml2.vcxproj` and `win32\VC12\runsuite.vcxproj`
* Open `win32\VC12\libxml2.sln` with VS
* Add x64 configuration
* For the `libxml2` and `runsuite` projects:
	* Set `<AdditionalIncludeDirectories>' to `$(ProjectDir);$(ProjectDir)..\..\include;$(ProjectDir)..\..\include;$(ProjectDir)..\..\..\..\..\gtk\$(Platform)\include;%(AdditionalIncludeDirectories)`
	* Add `<DisableSpecificWarnings>4996</DisableSpecificWarnings>`
* For the `libxml2` project:
	* Change _Configuration Type_ to _Dynamic Library (.dll)_ under _Configuration Properties_ `->` _General_
	* Set `<AdditionalLibraryDirectories>` to `..\..\..\..\..\gtk\$(Platform)\lib`
	* Set `<AdditionalDependencies>` to `ws2_32.lib;iconv.lib`
	* Replace
	```
	  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
		<OutDir>$(ProjectDir)..\..\lib\</OutDir>
	  </PropertyGroup>
	  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
		<IntDir>build\$(ProjectName)$(Configuration)\</IntDir>
	  </PropertyGroup>
	```
	with
	```
	  <PropertyGroup>
		<OutDir>$(ProjectDir)..\..\lib\</OutDir>
		<IntDir>build\$(ProjectName)$(Configuration)\</IntDir>
	  </PropertyGroup>
	```
* Add to libxml2.vcxproj.filters:
	```
	<ClCompile Include="..\..\buf.c">
	  <Filter>Source Files</Filter>
	</ClCompile>
	```
* For the `runsuites` project:
	* Replace
	```
	  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
		<OutDir>$(ProjectDir)..\..\lib\</OutDir>
		<IntDir>build\$(ProjectName)$(Configuration)\</IntDir>
	  </PropertyGroup>
	```
	with
	```
	  <PropertyGroup>
		<OutDir>$(ProjectDir)..\..\lib\</OutDir>
		<IntDir>build\$(ProjectName)$(Configuration)\</IntDir>
	  </PropertyGroup>
	```
* In `win32\VC12\config.h`
	* Add
	```
	#define SEND_ARG2_CAST
	#define GETHOSTBYNAME_ARG_CAST
	```
	* Replace
	```
	#define snprintf _snprintf
	```
	with
	```
	#if _MSC_VER < 1900
	#define snprintf _snprintf
	#endif
	```
	* Add `#undef LIBXML_LZMA_ENABLED`
