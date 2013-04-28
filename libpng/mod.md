 * Download [libpng 1.6.2](ftp://ftp.simplesystems.org/pub/libpng/png/src/libpng-1.6.2.tar.xz)
 * Extract to `C:\mozilla-build\hexchat`
 * Add to `projects\vstudio\zlib.props`:
<pre>
	&lt;ItemDefinitionGroup>
		&lt;ClCompile>
			&lt;AdditionalIncludeDirectories>..\..\..\..\..\..\gtk\$(Platform)\include&lt;/AdditionalIncludeDirectories>
		&lt;/ClCompile>
		&lt;Link>
			&lt;!--AdditionalDependencies>zdll.lib&lt;/AdditionalDependencies-->
			&lt;AdditionalLibraryDirectories>..\..\..\..\..\..\gtk\$(Platform)\lib&lt;/AdditionalLibraryDirectories>
		&lt;/Link>
	&lt;/ItemDefinitionGroup>
</pre>
 * Replace `zlib.lib` with `zdll.lib` in:
	* `projects\vstudio\libpng\libpng.vcxproj`
	* `projects\vstudio\pngstest\pngstest.vcxproj`
	* `projects\vstudio\pngtest\pngtest.vcxproj`
	* `projects\vstudio\pngunknown\pngunknown.vcxproj`
	* `projects\vstudio\pngvalid\pngvalid.vcxproj`
 * Replace `</AdditionalLibraryDirectories>` with `;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>` in:
	* `projects\vstudio\libpng\libpng.vcxproj`
	* `projects\vstudio\pngstest\pngstest.vcxproj`
	* `projects\vstudio\pngtest\pngtest.vcxproj`
	* `projects\vstudio\pngunknown\pngunknown.vcxproj`
	* `projects\vstudio\pngvalid\pngvalid.vcxproj`
 * Open `projects\vstudio\vstudio.sln` with VS
 * Remove the _zlib_ project
 * For _pngtest_, add to _Command Line_ beginning under _Configuration Properties_ `->` _Custom Build Step_ `->` _General_:
	<pre>copy ..\..\..\..\..\..\gtk\$(Platform)\bin\zlib1.dll $(OutDir)</pre>
 * Under solution properties, make _pngvalid_ depend on _pngtest_
 * Make a new _x64_ solution platform based on _Win32_
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
