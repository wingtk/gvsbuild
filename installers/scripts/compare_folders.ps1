$gvsbuild = Get-ChildItem -Recurse -name -path C:\gtk-build\gtk\x64\release
$gtk = Get-ChildItem -Recurse -name -path C:\gtk
Compare-Object -ReferenceObject $gvsbuild -DifferenceObject $gtk