 * For each project, delete
	* `^\s*<Optimization.*\r\n`
	* `^\s*<PlatformToolset>.*\r\n`
 * Add to `lmdb` directory
 * In `build.py`, replace:
  * `self.exec_msbuild(r'libraries\liblmdb\lmdb.sln')` with
    `self.exec_msbuild(r'libraries\liblmdb\win32\vc%(vs_ver)s\lmdb.sln')`
  * `self.install(r'.\libraries\liblmdb\%(platform)s\%(configuration)s\lmdb.lib lib')` with
    `self.install(r'.\libraries\liblmdb\win32\vc%(vs_ver)s\%(platform)s\%(configuration)s\lmdb.lib lib')`
  * `help="Visual Studio version 10,12, etc. Default is 12.")` with
    `help="Visual Studio version 10,12,14, etc. Default is 12.")`