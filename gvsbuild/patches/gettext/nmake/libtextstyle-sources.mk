LIBTEXTSTYLE_BASE_SRCS =	\
	..\libtextstyle\lib\asnprintf.c	\
	..\libtextstyle\lib\asprintf.c	\
	..\libtextstyle\lib\basename-lgpl.c	\
	..\libtextstyle\lib\binary-io.c	\
	..\libtextstyle\lib\c-ctype.c	\
	..\libtextstyle\lib\c-strcasecmp.c	\
	..\libtextstyle\lib\c-strncasecmp.c	\
	..\libtextstyle\lib\cloexec.c	\
	..\libtextstyle\lib\close.c	\
	..\libtextstyle\lib\color.c	\
	..\libtextstyle\lib\concat-filename.c	\
	..\libtextstyle\lib\dup2.c	\
	..\libtextstyle\lib\error.c	\
	..\libtextstyle\lib\exitfail.c	\
	..\libtextstyle\lib\fatal-signal.c	\
	..\libtextstyle\lib\fcntl.c	\
	..\libtextstyle\lib\fd-hook.c	\
	..\libtextstyle\lib\fd-ostream.c	\
	..\libtextstyle\lib\file-ostream.c	\
	..\libtextstyle\lib\frexpl.c	\
	..\libtextstyle\lib\fstat.c	\
	..\libtextstyle\lib\fsync.c	\
	..\libtextstyle\lib\full-write.c	\
	..\libtextstyle\lib\getdtablesize.c	\
	..\libtextstyle\lib\gethostname.c	\
	..\libtextstyle\lib\getprogname.c	\
	..\libtextstyle\lib\gettimeofday.c	\
	..\libtextstyle\lib\get_ppid_of.c	\
	..\libtextstyle\lib\get_progname_of.c	\
	..\libtextstyle\lib\gl_array_list.c	\
	..\libtextstyle\lib\gl_list.c	\
	..\libtextstyle\lib\gl_xlist.c	\
	..\libtextstyle\lib\html-ostream.c	\
	..\libtextstyle\lib\html-styled-ostream.c	\
	..\libtextstyle\lib\iconv-ostream.c	\
	..\libtextstyle\lib\isatty.c	\
	..\libtextstyle\lib\isinf.c	\
	..\libtextstyle\lib\isnand.c	\
	..\libtextstyle\lib\isnanf.c	\
	..\libtextstyle\lib\isnanl.c	\
	..\libtextstyle\lib\malloc.c	\
	..\libtextstyle\lib\malloca.c	\
	..\libtextstyle\lib\math.c	\
	..\libtextstyle\lib\mem-hash-map.c	\
	..\libtextstyle\lib\memory-ostream.c	\
	..\libtextstyle\lib\misc.c	\
	..\libtextstyle\lib\msvc-inval.c	\
	..\libtextstyle\lib\msvc-nothrow.c	\
	..\libtextstyle\lib\noop-styled-ostream.c	\
	..\libtextstyle\lib\obstack.c	\
	..\libtextstyle\lib\open.c	\
	..\libtextstyle\lib\ostream.c	\
	..\libtextstyle\lib\printf-args.c	\
	..\libtextstyle\lib\printf-frexp.c	\
	..\libtextstyle\lib\printf-frexpl.c	\
	..\libtextstyle\lib\printf-parse.c	\
	..\libtextstyle\lib\raise.c	\
	..\libtextstyle\lib\read.c	\
	..\libtextstyle\lib\safe-read.c	\
	..\libtextstyle\lib\safe-write.c	\
	..\libtextstyle\lib\sig-handler.c	\
	..\libtextstyle\lib\sigaction.c	\
	..\libtextstyle\lib\sigprocmask.c	\
	..\libtextstyle\lib\snprintf.c	\
	..\libtextstyle\lib\sockets.c	\
	..\libtextstyle\lib\stat-time.c	\
	..\libtextstyle\lib\stat-w32.c	\
	..\libtextstyle\lib\stat.c	\
	..\libtextstyle\lib\stpcpy.c	\
	..\libtextstyle\lib\strerror-override.c	\
	..\libtextstyle\lib\strerror.c	\
	..\libtextstyle\lib\styled-ostream.c	\
	..\libtextstyle\lib\sys_socket.c	\
	..\libtextstyle\lib\term-ostream.c	\
	..\libtextstyle\lib\term-style-control.c	\
	..\libtextstyle\lib\term-styled-ostream.c	\
	..\libtextstyle\lib\tparm.c	\
	..\libtextstyle\lib\tputs.c	\
	..\libtextstyle\lib\unistd.c	\
	..\libtextstyle\lib\vasnprintf.c	\
	..\libtextstyle\lib\vasprintf.c	\
	..\libtextstyle\lib\version.c	\
	..\libtextstyle\lib\vsnprintf.c	\
	..\libtextstyle\lib\windows-mutex.c	\
	..\libtextstyle\lib\windows-once.c	\
	..\libtextstyle\lib\windows-recmutex.c	\
	..\libtextstyle\lib\windows-rwlock.c	\
	..\libtextstyle\lib\write.c	\
	..\libtextstyle\lib\xasprintf.c	\
	..\libtextstyle\lib\xconcat-filename.c	\
	..\libtextstyle\lib\xgethostname.c	\
	..\libtextstyle\lib\xmalloc.c	\
	..\libtextstyle\lib\xsize.c	\
	..\libtextstyle\lib\xstrdup.c	\
	..\libtextstyle\lib\xvasprintf.c

!if $(PDBVER) < 14
LIBTEXTSTYLE_BASE_SRCS = $(LIBTEXTSTYLE_BASE_SRCS) ..\libtextstyle\lib\frexp.c
!endif

!if $(PDBVER) < 12
LIBTEXTSTYLE_BASE_SRCS =	\
	$(LIBTEXTSTYLE_BASE_SRCS)	\
	..\libtextstyle\lib\signbitd.c	\
	..\libtextstyle\lib\signbitf.c	\
	..\libtextstyle\lib\signbitl.c
!endif
