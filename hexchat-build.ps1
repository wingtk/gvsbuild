#========================================================================================================================================================
# Instructions:-
# 1. Install mozilla-build, cmake, nasm, perl, msgfmt as per http://gtk.hexchat.org/
# 2. Install gendef, Python and ISS as per http://docs.hexchat.org/en/latest/building.html if you want to build Perl, Python, setup, etc. in Hexchat
# 3. Check out https://github.com/hexchat/hexchat.git and https://github.com/hexchat/gtk-win32.git
# 4. Set the properties in the Properties section below
# 5. Paste this script in a powershell window, or run it if you know how to
#
# Examples:-
# 
# Default paths. x86 build.
# C:\mozilla-build\hexchat\github\gtk-win32\hexchat-build.ps1
# 
# Default paths. x64 build using the x64 cross compiler.
# C:\mozilla-build\hexchat\github\gtk-win32\hexchat-build.ps1 -Configuration x86_amd64
# 
# Default paths. x64 build using the x64 native compiler.
# C:\mozilla-build\hexchat\github\gtk-win32\hexchat-build.ps1 -Configuration x64
# 
# Default paths. Items are built one at a time. x86 build.
# C:\mozilla-build\hexchat\github\gtk-win32\hexchat-build.ps1 -DisableParallelBuild
# 
# Custom paths. x86 build.
# C:\mozilla-build\hexchat\github\gtk-win32\hexchat-build.ps1 -MozillaBuildDirectory D:\mozilla-build -ArchivesDownloadDirectory C:\hexchat-deps -SevenZip C:\Downloads\7-Zip\7za.exe
#========================================================================================================================================================

#========================================================================================================================================================
# Properties begin here
#========================================================================================================================================================

param (
	# Configuration: 'x86' (native 32 bit), 'x86_amd64' (cross-compiled 64 bit) or 'x64' (native 64 bit). 'x64' is not available in Visual Studio Express.
	[string][ValidateSet('x86', 'x86_amd64', 'x64')]
	$Configuration = 'x86',

	# Disable building in parallel or not
	[switch]
	$DisableParallelBuild = $false,

	# Your mozilla-build directory
	[string]
	$MozillaBuildDirectory = 'C:\mozilla-build',

	# The directory to download the source archives to. It will be created. If an archive already exists here, it won't be downloaded again.
	[string]
	$ArchivesDownloadDirectory = 'C:\mozilla-build\hexchat\src',

	# Location where you checked out https://github.com/hexchat/gtk-win32.git
	[string]
	$PatchesRootDirectory = 'C:\mozilla-build\hexchat\github\gtk-win32',

	# Location where you checked out https://github.com/hexchat/hexchat.git
	[string]
	$HexchatSourceDirectory = 'C:\mozilla-build\hexchat\github\hexchat',

	# Visual Studio install path
	[string]
	$VSInstallPath = 'C:\Program Files (x86)\Microsoft Visual Studio 11.0',

	# Path to any downloader. Invoked as &$Wget "$url"
	[string]
	$Wget = "$MozillaBuildDirectory\wget\wget.exe",

	# Path to 7-zip executable (do not use the one provided by mozilla-build, it's too old)
	[string]
	$SevenZip = 'C:\Program Files\7-Zip\7z.exe'
)

#========================================================================================================================================================
# Properties end here
#========================================================================================================================================================

#========================================================================================================================================================
# Source URLs begin here
#========================================================================================================================================================

$data = @{
	'atk'              = @('http://dl.hexchat.org/gtk-win32/src/atk-2.8.0.7z',            @('glib')                         );
	'cairo'            = @('http://dl.hexchat.org/gtk-win32/src/cairo-1.12.8.7z',         @('fontconfig', 'glib', 'pixman') );
	'enchant'          = @('http://dl.hexchat.org/gtk-win32/src/enchant-1.6.0.7z',        @('glib')                         );
	'fontconfig'       = @('http://dl.hexchat.org/gtk-win32/src/fontconfig-2.8.0.7z',     @('freetype', 'libxml2')          );
	'freetype'         = @('http://dl.hexchat.org/gtk-win32/src/freetype-2.4.11.7z',      @()                               );
	'gdk-pixbuf'       = @('http://dl.hexchat.org/gtk-win32/src/gdk-pixbuf-2.28.0.7z',    @('glib', 'libpng')               );
	'gettext-runtime'  = @('http://dl.hexchat.org/gtk-win32/src/gettext-runtime-0.18.7z', @('win-iconv')                    );
	'glib'             = @('http://dl.hexchat.org/gtk-win32/src/glib-2.36.0.7z',          @('gettext-runtime', 'libffi')    );
	'gtk'              = @('http://dl.hexchat.org/gtk-win32/src/gtk-2.24.17.7z',          @('atk', 'pango')                 );
	'harfbuzz'         = @('http://dl.hexchat.org/gtk-win32/src/harfbuzz-0.9.15.7z',      @('freetype', 'glib')             );
	'libffi'           = @('http://dl.hexchat.org/gtk-win32/src/libffi-3.0.13.7z',        @()                               );
	'libpng'           = @('http://dl.hexchat.org/gtk-win32/src/libpng-1.6.1.7z',         @('zlib')                         );
	'libxml2'          = @('http://dl.hexchat.org/gtk-win32/src/libxml2-2.9.0.7z',        @('win-iconv')                    );
	'openssl'          = @('http://dl.hexchat.org/gtk-win32/src/openssl-1.0.1e.7z',       @('zlib')                         );
	'pango'            = @('http://dl.hexchat.org/gtk-win32/src/pango-1.32.5.7z',         @('cairo', 'harfbuzz')            );
	'pixman'           = @('http://dl.hexchat.org/gtk-win32/src/pixman-0.28.2.7z',        @('libpng')                       );
	'win-iconv'        = @('http://dl.hexchat.org/gtk-win32/src/win-iconv-0.0.6.7z',      @()                               );
	'zlib'             = @('http://dl.hexchat.org/gtk-win32/src/zlib-1.2.7.7z',           @()                               );
}

#========================================================================================================================================================
# Source URLs end here
#========================================================================================================================================================

switch ($Configuration) {
	'x86' {
		$platform = 'Win32'
		$filenameArch = 'x86'
		$mozillaBuildStartVC11 = "$MozillaBuildDirectory\start-msvc11.bat"
	}

	'x86_amd64' {
		$platform = 'x64'
		$filenameArch = 'x64'
		$mozillaBuildStartVC11 = "$MozillaBuildDirectory\start-msvc11-x86_amd64.bat"
	}

	'x64' {
		$platform = 'x64'
		$filenameArch = 'x64'
		$mozillaBuildStartVC11 = "$MozillaBuildDirectory\start-msvc11-x64.bat"
	}
}

$workingDirectory = "$MozillaBuildDirectory\hexchat\build\$platform"

$items = @{}
foreach ($element in $data.GetEnumerator()) {
	$name = $element.Key
	$archiveUrl = $element.Value[0]

	$filename = New-Object System.Uri $archiveUrl
	$filename = $filename.Segments[$filename.Segments.Length - 1]

	$patchDirectory = "$PatchesRootDirectory\$name"

	$archiveFile = New-Object System.IO.FileInfo "$ArchivesDownloadDirectory\$filename"

	$result =
		New-Object PSObject |
		Add-Member NoteProperty Name $name -PassThru |
		Add-Member NoteProperty ArchiveUrl $archiveUrl -PassThru |
		Add-Member NoteProperty ArchiveFile $archiveFile -PassThru |
		Add-Member NoteProperty PatchDirectory $(New-Object System.IO.DirectoryInfo $patchDirectory) -PassThru |
		Add-Member NoteProperty BuildDirectory $(New-Object System.IO.DirectoryInfo "$workingDirectory\$($archiveFile.BaseName)") -PassThru |
		Add-Member NoteProperty BuildArchiveFile $(New-Object System.IO.FileInfo "$workingDirectory\$($archiveFile.BaseName)-$filenameArch$($archiveFile.Extension)") -PassThru |
		Add-Member NoteProperty Dependencies $element.Value[1] -PassThru

	$items.Add($name, $result)
}

#========================================================================================================================================================
# Build steps begin here
#========================================================================================================================================================

$items['atk'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'atk' `
		"msbuild build\win32\vc11\atk.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['cairo'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'cairo' `
		"msbuild msvc\vc11\cairo.sln /p:Platform=$platform /p:Configuration=Release_FC" `
		"release-$filenameArch.bat"
}

$items['enchant'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'enchant' `
		"build-$filenameArch.bat"
}

$items['fontconfig'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'fontconfig' `
		"$patch -p1 -i fontconfig.patch" `
		"msbuild fontconfig.sln /p:Platform=$platform /p:Configuration=Release /t:build" `
		"release-$filenameArch.bat"
}

$items['freetype'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'freetype' `
		"msbuild builds\win32\vc11\freetype.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['gdk-pixbuf'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'gdk-pixbuf' `
		"$patch -p1 -i gdk-pixbuf.patch" `
		"msbuild build\win32\vc11\gdk-pixbuf.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['gettext-runtime'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'gettext-runtime' `
		"$patch -p1 -i gettext-runtime.patch" `
		"build-$filenameArch.bat"
}

$items['glib'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'glib' `
		"msbuild build\win32\vc11\glib.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['gtk'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'gtk' `
		"$patch -p1 -i gtk-pixmap.patch" `
		"$patch -p1 -i gtk-bgimg.patch" `
		"$patch -p1 -i gtk-statusicon.patch" `
		"msbuild build\win32\vc11\gtk+.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['harfbuzz'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'harfbuzz' `
		"msbuild win32\harfbuzz.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['libffi'] | Add-Member NoteProperty BuildScript {
	$currentPwd = $PWD
	Set-Location ..\..
	echo "cd $($currentPwd -replace '\\', '\\') && build-$filenameArch.bat" | &$mozillaBuildStartVC11
	Set-Location $currentPwd
	VSPrompt -Name 'libffi' `
		"release-$filenameArch.bat"
}

$items['libpng'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'libpng' `
		"msbuild projects\vc11\vstudio.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['libxml2'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'libxml2' `
		"msbuild win32\vc11\libxml2.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['openssl'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'openssl' `
		"build-$filenameArch.bat"
}

$items['pango'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'pango' `
		"$patch -p1 -i pango-defs.patch" `
		"$patch -p1 -i pango-nonbmp.patch" `
		"msbuild build\win32\vc11\pango_fc.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['pixman'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'pixman' `
		"msbuild build\win32\vc11\pixman.sln /p:Platform=$platform /p:Configuration=Release" `
		"release-$filenameArch.bat"
}

$items['win-iconv'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'win-iconv' `
		"build-$filenameArch.bat"
}

$items['zlib'] | Add-Member NoteProperty BuildScript {
	VSPrompt -Name 'zlib' `
		"build-$filenameArch.bat"
}

#========================================================================================================================================================
# Build steps end here
#========================================================================================================================================================

# Verify VS exists at the indicated location, and that it supports the required target
switch ($Configuration) {
	'x86' {
		$vcvarsBat = "$VSInstallPath\VC\bin\vcvars32.bat"
	}

	'x86_amd64' {
		$vcvarsBat = "$VSInstallPath\VC\bin\x86_amd64\vcvarsx86_amd64.bat"
	}

	'x64' {
		$vcvarsBat = "$VSInstallPath\VC\bin\amd64\vcvars64.bat"
	}
}

if (-not $(Test-Path $vcvarsBat)) {
	throw "`"$vcvarsBat`" could not be found. Please check you have Visual Studio installed at `"$VSInstallPath`" and that it supports the configuration `"$Configuration`"."
}


# Connect the items to their dependencies
$items.GetEnumerator() | %{
	$_.Value.Dependencies = $_.Value.Dependencies | %{ $items[$_] }
}


$patch = "$MozillaBuildDirectory\msys\bin\patch.exe"


# For x86_amd64 configuration, ensure start-msvc11-x86_amd64.bat exists in mozilla-build, otherwise patch mozilla-build
if ($Configuration -eq 'x86_amd64' -and -not $(Test-Path "$MozillaBuild\start-msvc11-x86_amd64.bat")) {
	Set-Location $MozillaBuildDirectory
	&$patch -p0 -i $PatchesRootDirectory\mozilla-build.patch -o start-msvc11-x86_amd64.bat
}


New-Item -Type Directory $ArchivesDownloadDirectory


New-Item -Type Directory $workingDirectory
Set-Location $workingDirectory
Copy-Item $PatchesRootDirectory\stack.props .


$logDirectory = "$workingDirectory\logs"
New-Item -Type Directory $logDirectory
Remove-Item $logDirectory\*.log


# Runs all unnamed arguments as commands in a VS prompt
function VSPrompt([string] $Name) {
	$tempVSPromptBatchFile = "$($env:TEMP)\hexchat-build-$Name.bat"

	Out-File -FilePath $tempVSPromptBatchFile -InputObject "@CALL `"$VSInstallPath\VC\vcvarsall.bat`" $Configuration" -Encoding OEM
	foreach ($command in $args) {
		Out-File -FilePath $tempVSPromptBatchFile -InputObject $command -Encoding OEM -Append
	}

	$null | &$tempVSPromptBatchFile

	Remove-Item $tempVSPromptBatchFile
}


# For each item, start a job to download the source archives, extract them to mozilla-build, and copy over the stuff from gtk-win32
$items.GetEnumerator() | %{
	Start-Job -Name $_.Key -ArgumentList $_.Value, $ArchivesDownloadDirectory, $workingDirectory, $Wget, $SevenZip {
		param ($item, $ArchivesDownloadDirectory, $workingDirectory, $Wget, $SevenZip)

		'Beginning job to download and extract'

		if ($item.ArchiveFile.Exists) {
			"$($item.ArchiveFile) already exists"
		}
		else {
			"$($item.ArchiveFile) doesn't exist"
			Set-Location $ArchivesDownloadDirectory
			&$Wget $item.ArchiveUrl > $null 2>&1
			"Downloaded $($item.ArchiveUrl)"
		}

		"Extracting $($item.ArchiveFile.Name) to $workingDirectory"
		&$SevenZip x $item.ArchiveFile -o"$workingDirectory" -y > $null
		"Extracted $($item.ArchiveFile.Name)"

		Copy-Item "$($item.PatchDirectory)\*" $item.BuildDirectory -Recurse -Force
		"Copied patch contents from $($item.PatchDirectory) to $($item.BuildDirectory)"
	} > $null
}

# While the jobs are running...
$downloadJobs = @()
do {
	# Log their output
	$downloadJobs = Get-Job | %{
		$job = $_

		[string[]] $jobOutput = Receive-Job $job
		$jobOutput | %{
			Write-Host "$($job.Name) : $_"
		}

		$job
	} | ? { $_.State -ne 'Completed' }

	# Sleep a bit and then try again
	Start-Sleep 1
} while ($downloadJobs.Length -gt 0)

# All the jobs have been completed. Delete them all.
Get-Job | Remove-Job


# Map of items that have finished building (name -> item)
$completedItems = @{}


# Until all items have been built
while ($completedItems.Count -ne $items.Count) {

	# If another job can be started (either parallel build is enabled, or it's disabled and there is no running build job)...
	if (-not $DisableParallelBuild -or $(Get-Job) -eq $null) {

		# Find an item which hasn't already been built, isn't being built currently, and whose dependencies have all been built
		[Object[]] $nextItem =
			$items.GetEnumerator() | ?{
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

		# If such an item exists...
		if ($nextItem.Length -gt 0) {
			$pendingItem = $nextItem[0].Value

			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($pendingItem.Name) : Started"
			Write-Host "$($pendingItem.Name) : Started"

			# Start a job to build it
			Start-Job -Name $pendingItem.Name -InitializationScript {
				function VSPrompt([string] $Name) {
					$tempVSPromptBatchFile = "$($env:TEMP)\hexchat-build-$Name.bat"

					Out-File -FilePath $tempVSPromptBatchFile -InputObject "@CALL `"$VSInstallPath\VC\vcvarsall.bat`" $Configuration" -Encoding OEM
					foreach ($command in $args) {
						Out-File -FilePath $tempVSPromptBatchFile -InputObject $command -Encoding OEM -Append
					}

					$null | &$tempVSPromptBatchFile

					Remove-Item $tempVSPromptBatchFile
				}
			} -ArgumentList $pendingItem, $Configuration, $filenameArch, $mozillaBuildStartVC11, $patch, $platform, $VSInstallPath, $workingDirectory, $SevenZip {
				param ($item, $Configuration, $filenameArch, $mozillaBuildStartVC11, $patch, $platform, $VSInstallPath, $workingDirectory, $SevenZip)

				Set-Location $item.BuildDirectory

				Invoke-Expression -Command ('$null | Invoke-Command ' + "{ $($item.BuildScript) }")

				&$SevenZip x $item.BuildArchiveFile -o"$workingDirectory\..\gtk\$platform" -y
			} > $null
		}
	}

	# For each job...
	Get-Job | %{
		$job = $_

		# Log all its output
		[string[]] $jobOutput = Receive-Job $job
		$jobOutput | %{
			Out-File -Append -Encoding OEM -FilePath "$logDirectory\$($job.Name).log" -InputObject $_
			Write-Host "$($job.Name) : $_"
		}

		# If the job has been completed...
		if ($job.State -eq 'Completed') {

			# Make sure all its output has been logged
			$jobOutput = Receive-Job $job
			$jobOutput | %{
				Out-File -Append -Encoding OEM -FilePath "$logDirectory\$($job.Name).log" -InputObject $_
				Write-Host "$($job.Name) : $_"
			}

			# Add the item to the completed items map
			$completedItems[$job.Name] = $items[$job.Name]

			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($job.Name) : Completed"
			Write-Host "$($job.Name) : Completed"

			# Delete the job
			Remove-Job $job
		}
	}

	# Sleep a bit and then try again
	Start-Sleep 1
}


# Everything has been built. Now build hexchat.

Set-Location $HexchatSourceDirectory

VSPrompt -Name 'hexchat' "msbuild win32\hexchat.sln /p:Platform=$platform /p:Configuration=Release"
