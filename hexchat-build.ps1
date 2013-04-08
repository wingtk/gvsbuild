#========================================================================================================================================================
# Instructions:-
# 1. Install mozilla-build, cmake, nasm, perl, msgfmt as per http://gtk.hexchat.org/
# 2. Install gendef, Python and ISS as per http://docs.hexchat.org/en/latest/building.html if you want to build Perl, Python, setup, etc. in Hexchat
# 3. Check out https://github.com/hexchat/hexchat.git and https://github.com/Arnavion/gtk-win32.git
# 4. Set the properties in the Properties section below
# 5. Paste this script in a powershell window, or run it if you know how to
#========================================================================================================================================================

#========================================================================================================================================================
# Properties begin here
#========================================================================================================================================================

# Your mozilla-build directory
$mozillaBuildDirectory = 'C:\mozilla-build'

# Location where you checked out https://github.com/Arnavion/gtk-win32.git
$patchesRootDirectory = 'C:\Stuff\Sources\gtk-win32'

# Location where you checked out https://github.com/hexchat/hexchat.git
$hexchatSourceDirectory = 'C:\Stuff\Sources\hexchat'


# Architecture: 'x86' or 'x64'
$architecture = 'x86'



# Path to any downloader. Invoked as &$wget "$url"
$wget = 'C:\Users\Arnavion\Desktop\aria2c.bat'

# Path to 7-zip executable (your own, or the one provided by mozilla-build)
$sevenZip = 'C:\Program Files\7-Zip\7z.exe'



# The directory to download the source archives to. It will be created. If an archive already exists here, it won't be downloaded again.
$archivesDownloadDirectory = 'C:\Stuff\Sources\hexchat-deps'


# Enable parallel build
$enableParallelBuild = $true

#========================================================================================================================================================
# Properties end here
#========================================================================================================================================================

#========================================================================================================================================================
# Source URLs begin here
#========================================================================================================================================================

$data = @{
	'atk'              = @('http://dl.hexchat.org/gtk-win32/src/atk-2.8.0.7z',            @('glib')                         );
	'cairo'            = @('http://dl.hexchat.org/gtk-win32/src/cairo-1.12.8.7z',         @('fontconfig', 'pixman', 'glib') );
	'enchant'          = @('http://dl.hexchat.org/gtk-win32/src/enchant-1.6.0.7z',        @('glib')                         );
	'fontconfig'       = @('http://dl.hexchat.org/gtk-win32/src/fontconfig-2.8.0.7z',     @('freetype', 'libxml2')          );
	'freetype'         = @('http://dl.hexchat.org/gtk-win32/src/freetype-2.4.11.7z',      @()                               );
	'gdk-pixbuf'       = @('http://dl.hexchat.org/gtk-win32/src/gdk-pixbuf-2.28.0.7z',    @('libpng', 'glib')               );
	'gettext-runtime'  = @('http://dl.hexchat.org/gtk-win32/src/gettext-runtime-0.18.7z', @('win-iconv')                    );
	'glib'             = @('http://dl.hexchat.org/gtk-win32/src/glib-2.36.0.7z',          @('libffi', 'gettext-runtime')    );
	'gtk'              = @('http://dl.hexchat.org/gtk-win32/src/gtk-2.24.17.7z',          @('atk', 'pango')                 );
	'harfbuzz'         = @('http://dl.hexchat.org/gtk-win32/src/harfbuzz-0.9.15.7z',      @('freetype', 'glib')             );
	'libffi'           = @('http://dl.hexchat.org/gtk-win32/src/libffi-3.0.13.7z',        @()                               );
	'libpng'           = @('http://dl.hexchat.org/gtk-win32/src/libpng-1.6.1.7z',         @('zlib')                         );
	'libxml2'          = @('http://dl.hexchat.org/gtk-win32/src/libxml2-2.9.0.7z',        @('win-iconv')                    );
	'openssl'          = @('http://dl.hexchat.org/gtk-win32/src/openssl-1.0.1e.7z',       @('zlib')                         );
	'pango'            = @('http://dl.hexchat.org/gtk-win32/src/pango-1.32.5.7z',         @('harfbuzz', 'cairo')            );
	'pixman'           = @('http://dl.hexchat.org/gtk-win32/src/pixman-0.28.2.7z',        @('libpng')                       );
	'win-iconv'        = @('http://dl.hexchat.org/gtk-win32/src/win-iconv-0.0.6.7z',      @()                               );
	'zlib'             = @('http://dl.hexchat.org/gtk-win32/src/zlib-1.2.7.7z',           @()                               );
}

#========================================================================================================================================================
# Source URLs end here
#========================================================================================================================================================

$mozillaBuildDirectory = "$mozillaBuildDirectory\hexchat"

$items = @{}
foreach ($element in $data.GetEnumerator()) {
	$name = $element.Key
	$archiveUrl = $element.Value[0]
	
	$filename = New-Object System.Uri $archiveUrl
	$filename = $filename.Segments[$filename.Segments.Length - 1]
	
	$patchDirectory = "$patchesRootDirectory\$name"
	
	$archiveFile = New-Object System.IO.FileInfo "$archivesDownloadDirectory\$filename"
	
	$result =
		New-Object PSObject |
		Add-Member NoteProperty Name $name -PassThru |
		Add-Member NoteProperty ArchiveUrl $archiveUrl -PassThru |
		Add-Member NoteProperty ArchiveFile $archiveFile -PassThru |
		Add-Member NoteProperty PatchDirectory $(New-Object System.IO.DirectoryInfo $patchDirectory) -PassThru |
		Add-Member NoteProperty BuildDirectory $(New-Object System.IO.DirectoryInfo "$mozillaBuildDirectory\$($archiveFile.BaseName)") -PassThru |
		Add-Member NoteProperty BuildArchiveFile $(New-Object System.IO.FileInfo "$mozillaBuildDirectory\$($archiveFile.BaseName)-$architecture$($archiveFile.Extension)") -PassThru |
		Add-Member NoteProperty Dependencies $element.Value[1] -PassThru
	
	$items.Add($name, $result)
}

#========================================================================================================================================================
# Build steps begin here
#========================================================================================================================================================

$items['atk'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'atk' `
		"msbuild build\win32\vc11\atk.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['cairo'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'cairo' `
		"msbuild msvc\vc11\cairo.sln /p:Platform=$platform /p:Configuration=Release_FC" `
		"release-$architecture.bat"
}

$items['enchant'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'enchant' `
		"build-$architecture.bat"
}

$items['fontconfig'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'fontconfig' `
		"$patch -p1 -i fontconfig.patch" `
		"msbuild fontconfig.sln /p:Platform=$platform /p:Configuration=Release /t:build" `
		"release-$architecture.bat"
}

$items['freetype'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'freetype' `
		"msbuild builds\win32\vc11\freetype.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['gdk-pixbuf'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'gdk-pixbuf' `
		"$patch -p1 -i gdk-pixbuf.patch" `
		"msbuild build\win32\vc11\gdk-pixbuf.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['gettext-runtime'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'gettext-runtime' `
		"$patch -p1 -i gettext-runtime.patch" `
		"build-$architecture.bat"
}

$items['glib'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'glib' `
		"msbuild build\win32\vc11\glib.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['gtk'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'gtk' `
		"$patch -p1 -i gtk-pixmap.patch" `
		"$patch -p1 -i gtk-bgimg.patch" `
		"msbuild build\win32\vc11\gtk+.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['harfbuzz'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'harfbuzz' `
		"msbuild win32\harfbuzz.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['libffi'] | Add-Member NoteProperty BuildScript {
	$currentPwd = $PWD
	Set-Location ..\..
	echo "cd $($currentPwd -replace '\\', '\\') && build-$architecture.bat" | &$mozillaBuildStartVC11
	Set-Location $currentPwd
	VSPrompt -Name 'libffi' `
		"release-$architecture.bat"
}

$items['libpng'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'libpng' `
		"msbuild projects\vc11\vstudio.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['libxml2'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'libxml2' `
		"msbuild win32\vc11\libxml2.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['openssl'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'openssl' `
		"build-$architecture.bat"
}

$items['pango'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'pango' `
		"$patch -p1 -i pango-defs.patch" `
		"$patch -p1 -i pango-nonbmp.patch" `
		"msbuild build\win32\vc11\pango_fc.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['pixman'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'pixman' `
		"msbuild build\win32\vc11\pixman.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$architecture.bat"
}

$items['win-iconv'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'win-iconv' `
		"build-$architecture.bat"
}

$items['zlib'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'zlib' `
		"build-$architecture.bat"
}

#========================================================================================================================================================
# Build steps end here
#========================================================================================================================================================

$items.GetEnumerator() | %{
	$_.Value.Dependencies = $_.Value.Dependencies | %{ $items[$_] }
}

$platform = $architecture
if ($platform -eq 'x86') {
	$platform = 'Win32'
}
$mozillaBuildStartVC11 = '.\start-msvc11.bat'
if ($architecture -eq 'x64') {
	$mozillaBuildStartVC11 = '.\start-msvc11-x64.bat'
}

$patch = "$mozillaBuildDirectory\..\msys\bin\patch.exe"

New-Item -Type Directory $archivesDownloadDirectory

New-Item -Type Directory $mozillaBuildDirectory
Set-Location $mozillaBuildDirectory
Copy-Item $patchesRootDirectory\stack.props .

$logDirectory = "$mozillaBuildDirectory\build\logs"
New-Item -Type Directory $logDirectory
Remove-Item $logDirectory\*.log

function VSPrompt([string] $Name) {
	$tempVSPromptBatchFile = "$($env:TEMP)\hexchat-build-$Name.bat"
	
	Out-File -FilePath $tempVSPromptBatchFile -InputObject "@CALL `"C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\vcvarsall.bat`" $architecture" -Encoding OEM
	foreach ($command in $args) {
		Out-File -FilePath $tempVSPromptBatchFile -InputObject $command -Encoding OEM -Append
	}
	
	$null | &$tempVSPromptBatchFile
	
	Remove-Item $tempVSPromptBatchFile
}

$items.GetEnumerator() | %{
	Start-Job -Name $_.Key -ArgumentList $_.Value, $archivesDownloadDirectory, $mozillaBuildDirectory, $wget, $sevenZip {
		param ($item, $archivesDownloadDirectory, $mozillaBuildDirectory, $wget, $sevenZip)
		
		'Beginning job to download and extract'
		
		if ($item.ArchiveFile.Exists) {
			"$($item.ArchiveFile) already exists"
		}
		else {
			"$($item.ArchiveFile) doesn't exist"
			Set-Location $archivesDownloadDirectory
			&$wget $item.ArchiveUrl
			"Downloaded $($item.ArchiveUrl)"
		}

		"Extracting $($item.ArchiveFile.Name) to $mozillaBuildDirectory"
		&$sevenZip x $item.ArchiveFile -o"$mozillaBuildDirectory" -y > $null
		"Extracted $($item.ArchiveFile.Name)"
		
		Copy-Item "$($item.PatchDirectory)\*" $item.BuildDirectory -Recurse -Force
		"Copied patch contents from $($item.PatchDirectory) to $($item.BuildDirectory)"
	} > $null
}

$downloadJobs = @()
do {
	$downloadJobs = Get-Job | %{
		$job = $_
		
		Receive-Job $job | %{
			Write-Host "$($job.Name) : $_"
		}
		
		$job
	} | ? { $_.State -ne 'Completed' }
	
	Start-Sleep 1
} while ($downloadJobs.Length -gt 0)

Get-Job | Remove-Job

$completedItems = @{}
$pendingItems = @{}

$items.GetEnumerator() | %{
	$pendingItems.Add($_.Key, $_.Value)
}

while ($completedItems.Count -ne $items.Count) {
	if ($enableParallelBuild -or $(Get-Job) -eq $null) {
		[Object[]] $nextItem =
			$pendingItems.GetEnumerator() | ?{
				$completedItems[$_.Key] -eq $null -and 
				(Get-Job -Name $_.Key 2>$null) -eq $null
			} | ?{
				$pendingItem = $_.Value
				[Object[]] $dependencies = $pendingItem.Dependencies
				if ($dependencies.Length -gt 0) {
					[Object[]] $remainingDependencies = $dependencies | ?{ $completedItems[$_.Name] -eq $null }
					return $remainingDependencies.Length -eq 0
				}
				else {
					return $true
				}
			}
		
		if ($nextItem.Length -gt 0) {
			$pendingItem = $nextItem[0].Value
			
			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($pendingItem.Name) : Started"
			Write-Host "$($pendingItem.Name) : Started"
			
			Start-Job -Name $pendingItem.Name -InitializationScript {
				function VSPrompt([string] $Name) {
					$tempVSPromptBatchFile = "$($env:TEMP)\hexchat-build-$Name.bat"
					
					Out-File -FilePath $tempVSPromptBatchFile -InputObject "@CALL `"C:\Program Files (x86)\Microsoft Visual Studio 11.0\VC\vcvarsall.bat`" $architecture" -Encoding OEM
					foreach ($command in $args) {
						Out-File -FilePath $tempVSPromptBatchFile -InputObject $command -Encoding OEM -Append
					}
					
					$null | &$tempVSPromptBatchFile
					
					Remove-Item $tempVSPromptBatchFile
				}
			} -ArgumentList $pendingItem, $mozillaBuildDirectory, $platform, $architecture, $mozillaBuildStartVC11, $sevenZip, $patch {
				param ($item, $mozillaBuildDirectory, $platform, $architecture, $mozillaBuildStartVC11, $sevenZip, $patch)
				
				Set-Location $item.BuildDirectory
				
				Invoke-Expression -Command ('$null | Invoke-Command ' + "{ $($item.BuildScript) }")
				
				&$sevenZip x $item.BuildArchiveFile -o"$mozillaBuildDirectory\build\$platform" -y
			} > $null
		}
	}
	
	Get-Job | %{
		$job = $_
		
		[string[]] $jobOutput = Receive-Job $job
		$jobOutput | %{
			Out-File -Append -Encoding OEM -FilePath "$logDirectory\$($job.Name).log" -InputObject $_
			Write-Host "$($job.Name) : $_"
		}
		
		if ($job.State -eq 'Completed') {
			$jobOutput = Receive-Job $job
			$jobOutput | %{
				Out-File -Append -Encoding OEM -FilePath "$logDirectory\$($job.Name).log" -InputObject $_
				Write-Host "$($job.Name) : $_"
			}
			
			$completedItems[$job.Name] = $items[$job.Name]
			
			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($job.Name) : Completed"
			Write-Host "$($job.Name) : Completed"
			
			Remove-Job $job
		}
	}
	
	Start-Sleep 1
}

Set-Location $hexchatSourceDirectory

VSPrompt -Name 'hexchat' "msbuild win32\hexchat.sln /p:Platform=$platform /p:Configuration=Release"
