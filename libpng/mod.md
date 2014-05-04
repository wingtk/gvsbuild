 * Download [libpng 1.6.8](ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng16/libpng-1.6.8.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * Add to `projects\vstudio\zlib.props`:
<pre>
	&lt;ItemDefinitionGroup>
		&lt;ClCompile>
			&lt;AdditionalIncludeDirectories>..\..\..\..\..\..\gtk\$(Platform)\include&lt;/AdditionalIncludeDirectories>
		&lt;/ClCompile>
		&lt;Link>
			&lt;!--AdditionalDependencies>zlib1.lib&lt;/AdditionalDependencies-->
			&lt;AdditionalLibraryDirectories>..\..\..\..\..\..\gtk\$(Platform)\lib&lt;/AdditionalLibraryDirectories>
		&lt;/Link>
	&lt;/ItemDefinitionGroup>
</pre>
 * Replace `zlib.lib` with `zlib1.lib` in `projects\vstudio\libpng\libpng.vcxproj`
 * In `projects\vstudio\libpng\libpng.vcxproj`
    * Replace `</AdditionalLibraryDirectories>` with `;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>`
    * Replace `<TreatWarningAsError>true</TreatWarningAsError>` with `<TreatWarningAsError>false</TreatWarningAsError>`
 * Build `projects\vc12\pngconflib\pngconflib.vcxproj` and `projects\vc12\libpng\libpng.vcxproj`
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
