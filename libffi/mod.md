 * Download [libffi 3.0.13](ftp://sourceware.org/pub/libffi/libffi-3.0.13.tar.gz)
 * Extract to `C:\mozilla-build\hexchat`
 * In Mozilla Build shell:
	* For x86, run `./configure CC=$(pwd)/msvcc.sh LD=link CPP='cl -nologo -EP' CFLAGS='-O2' --build=i686-pc-mingw32 && make clean && make`
	* For x64, run `./configure CC="$(pwd)/msvcc.sh -m64" LD=link CPP='cl -nologo -EP' CFLAGS='-O2' --build=x86_64-w64-mingw32 && make clean && make`
