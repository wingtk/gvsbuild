 * Download [libpng 1.6.16](ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng16/libpng-1.6.16.tar.xz)
 * Copy `projects\vstudio` to `projects\vc12`. Only keep libpng and pnglibconf directories.
 * In `projects\vc12\libpng\libpng.vcxproj`:
	* Under `<ItemGroup Label="ProjectConfigurations">`, add
`
    <ProjectConfiguration Include="Release|x64">
      <Configuration>Release</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
`
	* Add `<PlatformToolset>v120</PlatformToolset>` to all `<PropertyGroup>` elements that have `Label="Configuration"`
	* Add
`
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <LinkIncremental>false</LinkIncremental>
    <CustomBuildBeforeTargets />
    <TargetName>$(ProjectName)16</TargetName>
  </PropertyGroup>
`
	* Remove all `<Optimization>` elements
	* Replace `<AdditionalDependencies>zlib.lib</AdditionalDependencies>` with `<AdditionalDependencies>zlib1.lib</AdditionalDependencies>`
	* Add
`
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <ClCompile>
      <WarningLevel>Level4</WarningLevel>
      <PrecompiledHeader>Use</PrecompiledHeader>
      <DebugInformationFormat>ProgramDatabase</DebugInformationFormat>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <PreprocessorDefinitions>WIN32;NDEBUG;_WINDOWS;_USRDLL;%(PreprocessorDefinitions)</PreprocessorDefinitions>
      <FloatingPointExceptions>false</FloatingPointExceptions>
      <TreatWChar_tAsBuiltInType>false</TreatWChar_tAsBuiltInType>
      <PrecompiledHeaderFile>pngpriv.h</PrecompiledHeaderFile>
      <BrowseInformation>true</BrowseInformation>
      <CompileAs>CompileAsC</CompileAs>
      <StringPooling>true</StringPooling>
      <MinimalRebuild>false</MinimalRebuild>
      <DisableSpecificWarnings>4996;4127</DisableSpecificWarnings>
      <AdditionalIncludeDirectories>$(ZLibSrcDir);%(AdditionalIncludeDirectories)</AdditionalIncludeDirectories>
      <TreatWarningAsError>true</TreatWarningAsError>
    </ClCompile>
    <Link>
      <SubSystem>Windows</SubSystem>
      <GenerateDebugInformation>true</GenerateDebugInformation>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
      <AdditionalDependencies>zlib1.lib</AdditionalDependencies>
      <Version>16</Version>
      <AdditionalLibraryDirectories>$(OutDir);%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>
    </Link>
  </ItemDefinitionGroup>
`
	* Under `<ClCompile Include="..\..\..\png.c">`, add `<PrecompiledHeader Condition="'$(Configuration)|$(Platform)'=='Release|x64'">Create</PrecompiledHeader>`
 * Add to `projects\vstudio\zlib.props`:
`
  <ItemDefinitionGroup>
    <ClCompile>
      <AdditionalIncludeDirectories>..\..\..\..\..\..\gtk\$(Platform)\include</AdditionalIncludeDirectories>
    </ClCompile>
    <Link>
      <!--AdditionalDependencies>zlib1.lib</AdditionalDependencies-->
      <AdditionalLibraryDirectories>..\..\..\..\..\..\gtk\$(Platform)\lib</AdditionalLibraryDirectories>
    </Link>
  </ItemDefinitionGroup>
`
