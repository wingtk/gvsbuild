<#

.SYNOPSIS
This is a build script to build GTK+ and openssl.


.DESCRIPTION
1. Install mozilla-build, cmake, nasm, perl, msgfmt as per http://gtk.hexchat.org/
2. Clone https://github.com/hexchat/gtk-win32.git
3. Run this script. Set the parameters, if needed.


.PARAMETER Configuration
The configuration to be built. One of the following:
x86       - 32-bit build.
x86_amd64 - 64-bit build using the 32-bit cross-compiler. Use this if you have VS Express.
x64       - 64-bit build using the native 64-bit compiler. Not available in VS Express.


.PARAMETER DisableParallelBuild
Setting this to $true forces the items to be built one after the other.


.PARAMETER MozillaBuildDirectory
The directory where you installed Mozilla Build.


.PARAMETER ArchivesDownloadDirectory
The directory to download the source archives to. It will be created. If a source archive already exists here, it won't be downloaded again.


.PARAMETER PatchesRootDirectory
The directory where you checked out https://github.com/hexchat/gtk-win32.git


.PARAMETER VSInstallPath
The directory where you installed Visual Studio.


.PARAMETER Wget
The path to any downloader. It is invoked as &$Wget "$url" and should output a file in the current directory.


.PARAMETER Patch
The path to a patch.exe binary.


.PARAMETER SevenZip
The path to a 7-zip executable. Do not use the one provided by Mozilla Build as it's too old and will not work.


.PARAMETER OnlyBuild
A subset of the items you want built.


.EXAMPLE
build.ps1
Default paths. x86 build.


.EXAMPLE
build.ps1 -Configuration x86_amd64
Default paths. x64 build using the x64 cross compiler.


.EXAMPLE
build.ps1 -Configuration x64
Default paths. x64 build using the x64 native compiler.


.EXAMPLE
build.ps1 -DisableParallelBuild
Default paths. Items are built one at a time. x86 build.


.EXAMPLE
build.ps1 -MozillaBuildDirectory D:\mozilla-build -ArchivesDownloadDirectory C:\hexchat-deps -SevenZip C:\Downloads\7-Zip\7za.exe
Custom paths. x86 build.


.EXAMPLE
build.ps1 -OnlyBuild openssl
Only builds openssl and its dependencies (zlib).


.LINK
http://gtk.hexchat.org/

#>

#========================================================================================================================================================
# Parameters begin here
#========================================================================================================================================================

param (
	[string][ValidateSet('x86', 'x86_amd64', 'x64')]
	$Configuration = 'x86',

	[switch]
	$DisableParallelBuild = $false,

	[string]
	$MozillaBuildDirectory = 'C:\mozilla-build',

	[string]
	$ArchivesDownloadDirectory = 'C:\mozilla-build\hexchat\src',

	[string]
	$PatchesRootDirectory = 'C:\mozilla-build\hexchat\github\gtk-win32',

	[string]
	$VSInstallPath = 'C:\Program Files (x86)\Microsoft Visual Studio 12.0',

	[string]
	$Wget = "$MozillaBuildDirectory\wget\wget.exe",

	[string]
	$Patch = "$MozillaBuildDirectory\msys\bin\patch.exe",

	[string]
	$SevenZip = 'C:\Program Files\7-Zip\7z.exe',

	[string[]]
	$OnlyBuild = @()
)

#========================================================================================================================================================
# Parameters end here
#========================================================================================================================================================

#========================================================================================================================================================
# Source URLs begin here
#========================================================================================================================================================

$items = @{
	'atk'              = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/atk-2.9.3.7z';            'Dependencies' = @('glib')                         };
	'cairo'            = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/cairo-1.12.14.7z';        'Dependencies' = @('fontconfig', 'glib', 'pixman') };
	'enchant'          = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/enchant-1.6.0.7z';        'Dependencies' = @('glib')                         };
	'fontconfig'       = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/fontconfig-2.8.0.7z';     'Dependencies' = @('freetype', 'libxml2')          };
	'freetype'         = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/freetype-2.5.0.1.7z';     'Dependencies' = @()                               };
	'gdk-pixbuf'       = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gdk-pixbuf-2.28.1.7z';    'Dependencies' = @('glib', 'libpng')               };
	'gettext-runtime'  = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gettext-runtime-0.18.7z'; 'Dependencies' = @('win-iconv')                    };
	'glib'             = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/glib-2.36.2.7z';          'Dependencies' = @('gettext-runtime', 'libffi')    };
	'gtk'              = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/gtk-2.24.19.7z';          'Dependencies' = @('atk', 'gdk-pixbuf', 'pango')   };
	'harfbuzz'         = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/harfbuzz-0.9.18.7z';      'Dependencies' = @('freetype', 'glib')             };
	'libffi'           = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libffi-3.0.13.7z';        'Dependencies' = @()                               };
	'libpng'           = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libpng-1.6.2.7z';         'Dependencies' = @('zlib')                         };
	'libxml2'          = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/libxml2-2.9.1.7z';        'Dependencies' = @('win-iconv')                    };
	'openssl'          = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/openssl-1.0.1e.7z';       'Dependencies' = @('zlib')                         };
	'pango'            = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/pango-1.32.5.7z';         'Dependencies' = @('cairo', 'harfbuzz')            };
	'pixman'           = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/pixman-0.30.0.7z';        'Dependencies' = @('libpng')                       };
	'win-iconv'        = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/win-iconv-0.0.6.7z';      'Dependencies' = @()                               };
	'zlib'             = @{ 'ArchiveUrl' = 'http://dl.hexchat.net/gtk-win32/src/zlib-1.2.8.7z';           'Dependencies' = @()                               };
}

#========================================================================================================================================================
# Source URLs end here
#========================================================================================================================================================

#========================================================================================================================================================
# Build steps begin here
#========================================================================================================================================================

$items['atk']['BuildScript'] = {
	VSPrompt -Name 'atk' `
		"msbuild build\win32\vc12\atk.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['cairo']['BuildScript'] = {
	VSPrompt -Name 'cairo' `
		"msbuild msvc\vc12\cairo.sln /p:Platform=$platform /p:Configuration=Release_FC /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['enchant']['BuildScript'] = {
	VSPrompt -Name 'enchant' `
		"build-$filenameArch.bat"
}

$items['fontconfig']['BuildScript'] = {
	VSPrompt -Name 'fontconfig' `
		"$Patch -p1 -i fontconfig.patch" `
		"msbuild fontconfig.sln /p:Platform=$platform /p:Configuration=Release /t:build /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['freetype']['BuildScript'] = {
	VSPrompt -Name 'freetype' `
		"msbuild builds\win32\vc12\freetype.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['gdk-pixbuf']['BuildScript'] = {
	VSPrompt -Name 'gdk-pixbuf' `
		"$Patch -p1 -i gdk-pixbuf.patch" `
		"msbuild build\win32\vc12\gdk-pixbuf.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['gettext-runtime']['BuildScript'] = {
	VSPrompt -Name 'gettext-runtime' `
		"$Patch -p1 -i gettext-runtime.patch" `
		"build-$filenameArch.bat"
}

$items['glib']['BuildScript'] = {
	VSPrompt -Name 'glib' `
		"msbuild build\win32\vc12\glib.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['gtk']['BuildScript'] = {
	VSPrompt -Name 'gtk' `
		"$Patch -p1 -i gtk-revert-scrolldc-commit.patch" `
		"$Patch -p1 -i gtk-pixmap.patch" `
		"$Patch -p1 -i gtk-bgimg.patch" `
		"$Patch -p1 -i gtk-statusicon.patch" `
		"msbuild build\win32\vc12\gtk+.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['harfbuzz']['BuildScript'] = {
	VSPrompt -Name 'harfbuzz' `
		"msbuild win32\harfbuzz.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['libffi']['BuildScript'] = {
	$currentPwd = $PWD
	Set-Location ..\..
	echo "cd $($currentPwd -replace '\\', '\\') && build-$filenameArch.bat" | &$mozillaBuildStartVC
	Set-Location $currentPwd
	VSPrompt -Name 'libffi' `
		"release-$filenameArch.bat"
}

$items['libpng']['BuildScript'] = {
	VSPrompt -Name 'libpng' `
		"msbuild projects\vc12\vstudio.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['libxml2']['BuildScript'] = {
	VSPrompt -Name 'libxml2' `
		"msbuild win32\vc12\libxml2.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['openssl']['BuildScript'] = {
	VSPrompt -Name 'openssl' `
		"build-$filenameArch.bat"
}

$items['pango']['BuildScript'] = {
	# Add BOM to .\pango\pango-language-sample-table.h because cl.exe throws C2001 otherwise
	$languageSampleTableFileContents = Get-Content .\pango\pango-language-sample-table.h -Encoding UTF8
	Out-File .\pango\pango-language-sample-table.h -InputObject $languageSampleTableFileContents -Encoding UTF8

	VSPrompt -Name 'pango' `
		"$Patch -p1 -i pango-defs.patch" `
		"$Patch -p1 -i pango-nonbmp.patch" `
		"$Patch -p1 -i pango-synthesize-all-fonts.patch" `
		"msbuild build\win32\vc12\pango_fc.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['pixman']['BuildScript'] = {
	VSPrompt -Name 'pixman' `
		"$Patch -p1 -i pixman.patch" `
		"msbuild build\win32\vc12\pixman.sln /p:Platform=$platform /p:Configuration=Release /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
}

$items['win-iconv']['BuildScript'] = {
	VSPrompt -Name 'win-iconv' `
		"build-$filenameArch.bat"
}

$items['zlib']['BuildScript'] = {
	VSPrompt -Name 'zlib' `
		"msbuild contrib\vstudio\vc12\zlibvc.sln /p:Platform=$platform /p:Configuration=ReleaseWithoutAsm /maxcpucount /nodeReuse:True" `
		"release-$filenameArch.bat"
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


switch ($Configuration) {
	'x86' {
		$platform = 'Win32'
		$filenameArch = 'x86'
		$mozillaBuildStartVC = "$MozillaBuildDirectory\start-msvc12.bat"
	}

	'x86_amd64' {
		$platform = 'x64'
		$filenameArch = 'x64'
		$mozillaBuildStartVC = "$MozillaBuildDirectory\start-msvc12-x86_amd64.bat"
	}

	'x64' {
		$platform = 'x64'
		$filenameArch = 'x64'
		$mozillaBuildStartVC = "$MozillaBuildDirectory\start-msvc12-x64.bat"
	}
}

$workingDirectory = "$MozillaBuildDirectory\hexchat\build\$platform"


# Set up additional properties on the items
foreach ($element in $items.GetEnumerator()) {
	$name = $element.Key
	$item = $element.Value

	$archiveUrl = $item['ArchiveUrl']

	$filename = New-Object System.Uri $archiveUrl
	$filename = $filename.Segments[$filename.Segments.Length - 1]

	$patchDirectory = "$PatchesRootDirectory\$name"

	$archiveFile = New-Object System.IO.FileInfo "$ArchivesDownloadDirectory\$filename"

	$item = $items[$name]

	$item['Name'] = $name
	$item['ArchiveFile'] = $archiveFile
	$item['PatchDirectory'] = $(New-Object System.IO.DirectoryInfo $patchDirectory)
	$item['BuildDirectory'] = $(New-Object System.IO.DirectoryInfo "$workingDirectory\$($archiveFile.BaseName)")
	$item['BuildArchiveFile'] = $(New-Object System.IO.FileInfo "$workingDirectory\$($archiveFile.BaseName)-$filenameArch$($archiveFile.Extension)")
	$item['Dependencies'] = @($item['Dependencies'] | %{ $items[$_] })
}


# If OnlyBuild is not an empty array, only keep the items that are specified
if ($OnlyBuild.Length -gt 0) {
	$newItems = @{}

	$queue = New-Object System.Collections.Generic.Queue[string] (, $OnlyBuild)

	while ($queue.Length -gt 0) {
		$itemName = $queue.Dequeue()
		$item = $items[$itemName]

		$newItems[$itemName] = $item

		@($item['Dependencies']) | %{ $queue.Enqueue($_.Name) }
	}

	$items = $newItems
}


if (-not $(Test-Path "$MozillaBuild\start-msvc12.bat")) {
	Copy-Item $PatchesRootDirectory\mozilla-build\start-msvc12.bat $MozillaBuildDirectory
}
if (-not $(Test-Path "$MozillaBuild\start-msvc12-x64.bat")) {
	Copy-Item $PatchesRootDirectory\mozilla-build\start-msvc12-x64.bat $MozillaBuildDirectory
}
if (-not $(Test-Path "$MozillaBuild\start-msvc12-x86_amd64.bat")) {
	Copy-Item $PatchesRootDirectory\mozilla-build\start-msvc12-x86_amd64.bat $MozillaBuildDirectory
}

Set-Location $MozillaBuildDirectory
&$Patch -p1 -i $PatchesRootDirectory\mozilla-build\mozilla-build-vs2013.patch > $null


New-Item -Type Directory $ArchivesDownloadDirectory


New-Item -Type Directory $workingDirectory
Set-Location $workingDirectory
Copy-Item $PatchesRootDirectory\stack.props .


$logDirectory = "$workingDirectory\logs"
New-Item -Type Directory $logDirectory
Remove-Item $logDirectory\*.log


# For each item, start a job to download the source archives, extract them to mozilla-build, and copy over the stuff from gtk-win32
$items.GetEnumerator() | %{
	Start-Job -Name $_.Key -ArgumentList $_.Value, $ArchivesDownloadDirectory, $workingDirectory, $Wget, $SevenZip {
		param ($item, $ArchivesDownloadDirectory, $workingDirectory, $Wget, $SevenZip)

		'Beginning job to download and extract'

		if ($item['ArchiveFile'].Exists) {
			"$($item['ArchiveFile']) already exists"
		}
		else {
			"$($item['ArchiveFile']) doesn't exist"
			Set-Location $ArchivesDownloadDirectory
			&$Wget $item['ArchiveUrl'] > $null 2>&1
			"Downloaded $($item['ArchiveUrl'])"
		}

		"Extracting $($item['ArchiveFile'].Name) to $workingDirectory"
		&$SevenZip x $item['ArchiveFile'] -o"$workingDirectory" -y > $null
		"Extracted $($item['ArchiveFile'].Name)"

		Copy-Item "$($item['PatchDirectory'])\*" $item['BuildDirectory'] -Recurse -Force
		"Copied patch contents from $($item['PatchDirectory']) to $($item['BuildDirectory'])"
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
			} | %{ $_.Value } | ?{
				[Object[]] $dependencies = @($_['Dependencies'])
				if ($dependencies.Length -gt 0) {
					[Object[]] $remainingDependencies = $dependencies | ?{ $completedItems[$_['Name']] -eq $null }
					return $remainingDependencies.Length -eq 0
				}
				else {
					return $true
				}
			}

		# If such an item exists...
		if ($nextItem.Length -gt 0) {
			$pendingItem = $nextItem[0]

			Out-File -Append -Encoding OEM -FilePath "$logDirectory\build.log" -InputObject "$($pendingItem['Name']) : Started"
			Write-Host "$($pendingItem['Name']) : Started"

			# Start a job to build it
			Start-Job -Name $pendingItem['Name'] -InitializationScript {
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
			} -ArgumentList $pendingItem {
				param ($item)

				$mozillaBuildStartVC = $using:mozillaBuildStartVC
				$Configuration = $using:Configuration
				$filenameArch = $using:filenameArch
				$Patch = $using:Patch
				$platform = $using:platform
				$VSInstallPath = $using:VSInstallPath
				$workingDirectory = $using:workingDirectory
				$SevenZip = $using:SevenZip

				Set-Location $item['BuildDirectory']

				Invoke-Expression -Command ('$null | Invoke-Command ' + "{ $($item['BuildScript']) }")

				&$SevenZip x $item['BuildArchiveFile'] -o"$workingDirectory\..\..\gtk\$platform" -y
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
