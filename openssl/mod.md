 * Download [OpenSSL 1.0.1j](http://www.openssl.org/source/openssl-1.0.1j.tar.gz)
 * Download the latest [NSS certificate list](http://hg.mozilla.org/mozilla-central/raw-file/default/security/nss/lib/ckfw/builtins/certdata.txt)
 * Download the latest [mk-ca-bundle.pl](https://raw.githubusercontent.com/bagder/curl/master/lib/mk-ca-bundle.pl) and make the following changes:
	* Remove `use LWP::UserAgent`
	* Remove the calls to `oldsha1` and `sha1` and any code that uses the output of those functions
	* Replace `my $crt = $ARGV[0] || 'ca-bundle.crt';` with `my $crt = $ARGV[0] || 'cert.pem';`
 * Extract to `C:\mozilla-build\hexchat`
 * Open VS x86 command prompt
 * Build with `build-x86.bat`
 * Extract package to `C:\mozilla-build\hexchat\build\Win32`
