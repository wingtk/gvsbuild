 * Download [libpng 1.5.13](ftp://ftp.simplesystems.org/pub/libpng/png/src/lpng1513.zip)
 * Extract to `C:\mozilla-build\hexchat`
 * Add to `projects\vstudio\zlib.props`:
<pre>
	&lt;ItemDefinitionGroup>
		&lt;ClCompile>
			&lt;AdditionalIncludeDirectories>..\..\..\..\build\$(Platform)\include</AdditionalIncludeDirectories>
		&lt;/ClCompile>
		&lt;Link>
			&lt;!--AdditionalDependencies>zdll.lib</AdditionalDependencies-->
			&lt;AdditionalLibraryDirectories>..\..\..\..\build\$(Platform)\lib</AdditionalLibraryDirectories>
		&lt;/Link>
	&lt;/ItemDefinitionGroup>
</pre>
 * Replace `zlib.lib` with `zdll.lib` in:
	* `projects\vstudio\libpng\libpng.vcxproj`
	* `projects\vstudio\pngtest\pngtest.vcxproj`
	* `projects\vstudio\pngvalid\pngvalid.vcxproj`
 * Replace `</AdditionalLibraryDirectories>` with `;%(AdditionalLibraryDirectories)</AdditionalLibraryDirectories>` in:
	* `projects\vstudio\libpng\libpng.vcxproj`
	* `projects\vstudio\pngtest\pngtest.vcxproj`
	* `projects\vstudio\pngvalid\pngvalid.vcxproj`
 * Open `projects\vstudio\vstudio.sln` with VS
 * Remove zlib project
 * For _pngtest_, add to _Command Line_ beginning under _Configuration Properties_ `->` _Custom Build Step_ `->` _General_:
	<pre>copy ..\..\..\..\build\$(Platform)\bin\zlib1.dll $(OutDir)</pre>
 * Under solution properties, make _pngvalid_ depend on _pngtest_
 * Build in VS
 * Release with `release-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
