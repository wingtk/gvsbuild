GETTEXT_LIB_BASE_SRCS =	\
	access.c	\
	acl-errno-valid.c	\
	acl-internal.c	\
	addext.c	\
	allocator.c	\
	asprintf.c	\
	areadlink.c	\
	argmatch.c	\
	asnprintf.c	\
	asyncsafe-spin.c	\
	backupfile.c	\
	basename-lgpl.c	\
	binary-io.c	\
	bitrotate.c	\
	btoc32.c	\
	c-ctype.c	\
	c-strcasecmp.c	\
	c-strcasestr.c	\
	c-strncasecmp.c	\
	c-strstr.c	\
	c32isalnum.c	\
	c32isalpha.c	\
	c32isblank.c	\
	c32iscntrl.c	\
	c32isdigit.c	\
	c32isgraph.c	\
	c32islower.c	\
	c32isprint.c	\
	c32ispunct.c	\
	c32isspace.c	\
	c32isupper.c	\
	c32isxdigit.c	\
	c32tolower.c	\
	c32width.c	\
	c32_apply_type_test.c	\
	c32_get_type_test.c	\
	calloc.c	\
	canonicalize-lgpl.c	\
	canonicalize.c	\
	careadlinkat.c	\
	chdir-long.c	\
	classpath.c	\
	clean-temp-simple.c	\
	clean-temp.c	\
	cloexec.c	\
	close.c	\
	closedir.c	\
	closeout.c	\
	concat-filename.c	\
	copy-file-range.c	\
	copy-file.c	\
	csharpcomp.c	\
	csharpexec.c	\
	dirfd.c	\
	dirname-lgpl.c	\
	dup-safer-flag.c	\
	dup-safer.c	\
	dup.c	\
	dup2.c	\
	error-progname.c	\
	error.c	\
	execute.c	\
	exitfail.c	\
	fatal-signal.c	\
	fchdir.c	\
	fcntl.c	\
	fd-hook.c	\
	fd-safer-flag.c	\
	fd-safer.c	\
	fdopen.c	\
	fdopendir.c	\
	file-set.c	\
	filenamecat-lgpl.c	\
	findprog-in.c	\
	findprog.c	\
	fnmatch.c	\
	fopen.c	\
	free.c	\
	fstat.c	\
	fstatat.c	\
	fstrcmp.c	\
	ftell.c	\
	ftello.c	\
	full-write.c	\
	fwriteerror.c	\
	gai_strerror.c	\
	gcd.c	\
	get-permissions.c	\
	getcwd-lgpl.c	\
	getcwd.c	\
	getdelim.c	\
	getdtablesize.c	\
	getline.c	\
	getopt.c	\
	getopt1.c	\
	getprogname.c	\
	getrandom.c	\
	gettime.c	\
	gettimeofday.c	\
	gl_linkedhash_list.c	\
	gl_linked_list.c	\
	gl_list.c	\
	gl_xlist.c	\
	hard-locale.c	\
	hash-pjw.c	\
	hash-triple-simple.c	\
	hash.c	\
	ialloc.c	\
	inet_ntop.c	\
	isinf.c	\
	isnand.c	\
	isnanf.c	\
	isnanl.c	\
	iswctype.c	\
	javacomp.c	\
	javaexec.c	\
	javaversion.c	\
	localcharset.c	\
	localename-table.c	\
	localename.c	\
	localtime.c	\
	lseek.c	\
	malloc.c	\
	malloca.c	\
	math.c	\
	mbchar.c	\
	mbrtoc32.c	\
	mbrtowc.c	\
	mbsinit.c	\
	mbslen.c	\
	mbsrtoc32s.c	\
	mbsrtoc32s-state.c	\
	mbsstr.c	\
	mbswidth.c	\
	mbszero.c	\
	mbuiter.c	\
	mbuiterf.c	\
	mem-hash-map.c	\
	memmem.c	\
	mempcpy.c	\
	memrchr.c	\
	memset_explicit.c	\
	mkdir.c	\
	mkdtemp.c	\
	msvc-inval.c	\
	msvc-nothrow.c	\
	obstack.c	\
	omp-init.c	\
	open.c	\
	openat-die.c	\
	openat-proc.c	\
	openat.c	\
	opendir.c	\
	pipe-filter-aux.c	\
	pipe-filter-ii.c	\
	pipe-safer.c	\
	pipe.c	\
	pipe2-safer.c	\
	pipe2.c	\
	printf-args.c	\
	printf-parse.c	\
	progname.c	\
	progreloc.c	\
	propername.c	\
	qcopy-acl.c	\
	quotearg.c	\
	raise.c	\
	rawmemchr.c	\
	read-file.c	\
	read.c	\
	readdir.c	\
	readlink.c	\
	realloc.c	\
	reallocarray.c	\
	relocatable.c	\
	rewinddir.c	\
	rmdir.c	\
	safe-read.c	\
	safe-write.c	\
	same-inode.c	\
	save-cwd.c	\
	secure_getenv.c	\
	set-permissions.c	\
	setenv.c	\
	setlocale.c	\
	setlocale_null.c	\
	sh-quote.c	\
	sig-handler.c	\
	sigaction.c	\
	sigprocmask.c	\
	snprintf.c	\
	sockets.c	\
	spawn-pipe.c	\
	spawn.c	\
	spawnattr_destroy.c	\
	spawnattr_init.c	\
	spawnattr_setflags.c	\
	spawnattr_setpgroup.c	\
	spawnattr_setsigmask.c	\
	spawni.c	\
	spawnp.c	\
	spawn_faction_addchdir.c	\
	spawn_faction_addclose.c	\
	spawn_faction_adddup2.c	\
	spawn_faction_addopen.c	\
	spawn_faction_destroy.c	\
	spawn_faction_init.c	\
	stat-time.c	\
	stat.c	\
	stat-w32.c	\
	stdio-write.c	\
	stpcpy.c	\
	stpncpy.c	\
	strchrnul.c	\
	strdup.c	\
	strerror-override.c	\
	strerror.c	\
	striconv.c	\
	striconveh.c	\
	striconveha.c	\
	string-desc-contains.c	\
	string-desc.c	\
	stripslash.c	\
	strnlen1.c	\
	strstr.c	\
	strtol.c	\
	strtoul.c	\
	supersede.c	\
	sys_socket.c	\
	tempname.c	\
	timespec.c	\
	tmpdir.c	\
	trim.c	\
	unistd.c	\
	unlink.c	\
	unsetenv.c	\
	utime.c	\
	utimens.c	\
	vasnprintf.c	\
	vasprintf.c	\
	vsnprintf.c	\
	wait-process.c	\
	waitpid.c	\
	wctype-h.c	\
	wctype.c	\
	wcwidth.c	\
	windows-mutex.c	\
	windows-once.c	\
	windows-recmutex.c	\
	windows-rwlock.c	\
	windows-spawn.c	\
	windows-spin.c	\
	windows-tls.c	\
	wmempcpy.c	\
	write.c	\
	xalloc-die.c	\
	xasprintf.c	\
	xconcat-filename.c	\
	xerror.c	\
	xmalloc.c	\
	xmalloca.c	\
	xmemdup0.c	\
	xreadlink.c	\
	xsetenv.c	\
	xsize.c	\
	xstriconv.c	\
	xstriconveh.c	\
	xvasprintf.c

!if "$(PLAT)" == "Win32"
GETTEXT_LIB_BASE_SRCS = $(GETTEXT_LIB_BASE_SRCS) getaddrinfo.c
!endif

LIBGREP_SOURCES =	\
	iswctype.c	\
	kwset.c	\
	localeconv.c	\
	m-fgrep.c	\
	m-regex.c	\
	mbrlen.c	\
	mbszero.c	\
	nl_langinfo.c	\
	regex.c	\
	unistd.c	\
	wcrtomb.c	\
	wctype.c	\
	wctype-h.c

LIBGETTEXTPO_GNULIB_SRCS =	\
	asnprintf.c	\
	asprintf.c	\
	basename-lgpl.c	\
	c-ctype.c	\
	c-strcasecmp.c	\
	c-strncasecmp.c	\
	c-strstr.c	\
	calloc.c	\
	cloexec.c	\
	close.c	\
	concat-filename.c	\
	c32iscntrl.c	\
	c32width.c	\
	dup2.c	\
	error-progname.c	\
	error.c	\
	exitfail.c	\
	fcntl.c	\
	fd-hook.c	\
	fdopen.c	\
	fopen.c	\
	free.c	\
	fstat.c	\
	fstrcmp.c	\
	fsync.c	\
	full-write.c	\
	fwriteerror.c	\
	gcd.c	\
	getdelim.c	\
	getdtablesize.c	\
	getline.c	\
	getprogname.c	\
	gl_linked_list.c	\
	gl_list.c	\
	gl_xlist.c	\
	hard-locale.c	\
	ialloc.c	\
	localcharset.c	\
	malloc.c	\
	malloca.c	\
	markup.c	\
	mbrtoc32.c	\
	mbrtowc.c	\
	mbsinit.c	\
	mbswidth.c	\
	mbszero.c	\
	memmem.c	\
	mem-hash-map.c	\
	memrchr.c	\
	msvc-inval.c	\
	msvc-nothrow.c	\
	obstack.c	\
	open.c	\
	printf-args.c	\
	printf-parse.c	\
	raise.c	\
	rawmemchr.c	\
	realloc.c	\
	reallocarray.c	\
	relocatable.c	\
	safe-write.c	\
	setlocale_null.c	\
	sigprocmask.c	\
	stat-time.c	\
	stat-w32.c	\
	stat.c	\
	stdio-write.c	\
	stpcpy.c	\
	stpncpy.c	\
	strchrnul.c	\
	strerror-override.c	\
	strerror.c	\
	striconv.c	\
	striconveh.c	\
	striconveha.c	\
	string-desc-contains.c	\
	string-desc.c	\
	strstr.c	\
	unistd.c	\
	vasnprintf.c	\
	vasprintf.c	\
	wctype-h.c	\
	wcwidth.c	\
	windows-mutex.c	\
	windows-once.c	\
	windows-recmutex.c	\
	windows-rwlock.c	\
	windows-tls.c	\
	write.c	\
	xalloc-die.c	\
	xasprintf.c	\
	xconcat-filename.c	\
	xerror.c	\
	xmalloc.c	\
	xmalloca.c	\
	xsize.c	\
	xstriconv.c	\
	xvasprintf.c

FORMAT_SOURCES =	\
	..\gettext-tools\woe32dll\c++format.cc	\
	format-c.c	\
	format-c++-brace.c	\
	format-python.c	\
	format-python-brace.c	\
	format-java.c	\
	format-java-printf.c	\
	format-csharp.c	\
	format-javascript.c	\
	format-scheme.c	\
	format-lisp.c	\
	format-elisp.c	\
	format-librep.c	\
	format-ruby.c	\
	format-sh.c	\
	format-awk.c	\
	format-lua.c	\
	format-pascal.c	\
	format-smalltalk.c	\
	format-qt.c	\
	format-qt-plural.c	\
	format-kde.c	\
	format-kde-kuit.c	\
	format-boost.c	\
	format-tcl.c	\
	format-perl.c	\
	format-perl-brace.c	\
	format-php.c	\
	format-gcc-internal.c	\
	format-gfc-internal.c

COMMON_SRCS =	\
	message.c	\
	pos.c	\
	po-error.c	\
	po-xerror.c	\
	read-catalog-abstract.c	\
	po-lex.c	\
	po-gram-gen.c	\
	po-charset.c	\
	read-po.c	\
	read-properties.c	\
	read-stringtable.c	\
	open-catalog.c	\
	dir-list.c	\
	str-list.c
  
LIBGETTEXTSRC_SRCS =	\
	$(COMMON_SRCS)	\
	read-catalog.c	\
	write-catalog.c	\
	write-properties.c	\
	write-stringtable.c	\
	write-po.c	\
	msgl-ascii.c	\
	msgl-ofn.c	\
	msgl-iconv.c	\
	msgl-equal.c	\
	msgl-cat.c	\
	msgl-header.c	\
	msgl-english.c	\
	msgl-check.c	\
	file-list.c	\
	msgl-charset.c	\
	po-time.c	\
	plural-exp.c	\
	plural-eval.c	\
	plural-table.c	\
	sentence.c	\
	$(FORMAT_SOURCES)	\
	read-desktop.c \
	locating-rule.c	\
	its.c \
	search-path.c

LIBGETTEXTPO_AUX_SRCS =	\
	str-list.c \
	dir-list.c \
	message.c \
	pos.c \
	msgl-ascii.c \
	po-error.c \
	po-xerror.c \
	write-catalog.c \
	write-po.c \
	open-catalog.c \
	po-charset.c \
	po-lex.c \
	po-gram-gen.c \
	read-po.c \
	read-catalog-abstract.c \
	read-catalog.c \
	plural-table.c \
	format-c.c \
	format-c++-brace.c \
	format-python.c \
	format-python-brace.c \
	format-java.c \
	format-java-printf.c \
	format-csharp.c \
	format-javascript.c \
	format-scheme.c \
	format-lisp.c \
	format-elisp.c \
	format-librep.c \
	format-ruby.c \
	format-sh.c \
	format-awk.c \
	format-lua.c \
	format-pascal.c \
	format-smalltalk.c \
	format-qt.c \
	format-qt-plural.c \
	format-kde.c \
	format-kde-kuit.c \
	format-boost.c \
	format-tcl.c \
	format-perl.c \
	format-perl-brace.c \
	format-php.c \
	format-gcc-internal.c \
	format-gfc-internal.c \
	format.c \
	plural-exp.c \
	plural-eval.c \
	msgl-check.c \
	sentence.c

MSGATTRIB_SOURCES = msgattrib.c
MSGCAT_SOURCES = msgcat.c

MSGCMP_SOURCES =	\
	msgcmp.c	\
	msgl-fsearch.c

MSGCOMM_SOURCES = msgcomm.c
MSGCONV_SOURCES = msgconv.c
MSGEN_SOURCES = msgen.c
MSGEXEC_SOURCES = msgexec.c

MSGFILTER_SOURCES =	\
	msgfilter.c	\
	filter-sr-latin.c	\
	filter-quote.c
	
MSGFMT_SOURCES =	\
	msgfmt.c	\
	write-mo.c	\
	write-csharp.c	\
	write-desktop.c	\
	write-java.c	\
	write-qt.c	\
	write-resources.c	\
	write-tcl.c	\
	write-xml.c	\
	..\gettext-runtime\intl\hash-string.c

MSGGREP_SOURCES = msggrep.c

MSGMERGE_SOURCES =	\
	msgmerge.c	\
	msgl-fsearch.c	\
	lang-table.c	\
	plural-count.c

MSGUNFMT_SOURCES =	\
	msgunfmt.c	\
	read-csharp.c	\
	read-java.c	\
	read-mo.c	\
	read-resources.c	\
	read-tcl.c	\
	..\gettext-runtime\intl\hash-string.c

MSGUNIQ_SOURCES = msguniq.c

RECODE_SR_LATIN_SOURCES =	\
	filter-sr-latin.c	\
	recode-sr-latin.c

XGETTEXT_SOURCES =	\
	..\gettext-tools\woe32dll\c++xgettext.cc	\
	xg-arglist-callshape.c	\
	xg-arglist-context.c	\
	xg-arglist-parser.c	\
	xg-encoding.c	\
	xg-pos.c	\
	xg-message.c	\
	xg-mixed-string.c	\
	x-awk.c	\
	x-c.c	\
	x-csharp.c	\
	x-desktop.c	\
	x-elisp.c	\
	x-java.c	\
	x-javascript.c	\
	x-librep.c	\
	x-lisp.c	\
	x-lua.c	\
	x-perl.c	\
	x-php.c	\
	x-po.c	\
	x-python.c	\
	x-rst.c	\
	x-ruby.c	\
	x-scheme.c	\
	x-sh.c	\
	x-smalltalk.c	\
	x-tcl.c	\
	x-vala.c	\
	x-ycp.c

MSGINIT_SOURCES =	\
	msginit.c	\
	lang-table.c	\
	plural-count.c	\
	..\gettext-runtime\intl\localealias.c

GETTEXT_TOOLS_TOOLS =	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgattrib.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgcat.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgcmp.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgcomm.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgconv.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgen.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgexec.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgfilter.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgfmt.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msggrep.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msginit.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgmerge.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msgunfmt.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\msguniq.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\recode-sr-latin.exe	\
	vs$(VSVER)\$(CFG)\$(PLAT)\xgettext.exe
