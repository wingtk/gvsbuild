 * Download [OpenSSL 1.0.1k](http://www.openssl.org/source/openssl-1.0.1k.tar.gz)
 * Download the latest [NSS certificate list](http://hg.mozilla.org/mozilla-central/raw-file/default/security/nss/lib/ckfw/builtins/certdata.txt)
 * Download the latest [mk-ca-bundle.pl](https://raw.githubusercontent.com/bagder/curl/master/lib/mk-ca-bundle.pl) and make the following changes:
	* Remove `use LWP::UserAgent`
 * Extract to `C:\mozilla-build\hexchat`
 * Open VS x86 command prompt
 * Build with `build-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
