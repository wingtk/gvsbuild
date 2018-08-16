Gdk-3.0.gir: Gdk_3_0_gir_list
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=Gdk	\
	--nsversion=3.0	\
		\
	--library=gdk-3.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
	--include=Gio-2.0 --include=GdkPixbuf-2.0 --include=Pango-1.0 --include=cairo-1.0	\
	--pkg-export=gdk-3.0	\
	--cflags-begin	\
	-DG_LOG_USE_STRUCTURED=1 -DGDK_COMPILATION -I../.. -I../../gdk -I.../../gdk/win32	\
	--cflags-end	\
	--c-include=gdk/gdk.h	\
	--filelist=Gdk_3_0_gir_list	\
	-o $@

Gdk-3.0.typelib: Gdk-3.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	Gdk-3.0.gir	\
	-o $@

GdkWin32-3.0.gir: GdkWin32_3_0_gir_list
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=GdkWin32	\
	--nsversion=3.0	\
		\
	--library=gdk-3.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
		\
		\
	--cflags-begin	\
	-DG_LOG_USE_STRUCTURED=1 -DGDK_COMPILATION -I../.. -I../../gdk -I.../../gdk/win32	\
	--cflags-end	\
	--identifier-prefix=Gdk --c-include=gdk/gdkwin32.h --include-uninstalled=./Gdk-3.0.gir	\
	--filelist=GdkWin32_3_0_gir_list	\
	-o $@

GdkWin32-3.0.typelib: GdkWin32-3.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	GdkWin32-3.0.gir	\
	-o $@

Gtk-3.0.gir: Gtk_3_0_gir_list
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=Gtk	\
	--nsversion=3.0	\
		\
	--library=gtk-3.0 --library=gdk-3.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
	--include=Atk-1.0	\
	--pkg-export=gtk+-3.0	\
	--cflags-begin	\
	-DG_LOG_USE_STRUCTURED=1 -DGTK_VERSION="3.22.26" -DGTK_BINARY_VERSION="3.0.0" -DGTK_COMPILATION -DGTK_PRINT_BACKEND_ENABLE_UNSUPPORTED -DGTK_LIBDIR=\"/dummy/lib\" -DGTK_DATADIR=\"/dummy/share\" -DGTK_DATA_PREFIX=\"/dummy\" -DGTK_SYSCONFDIR=\"/dummy/etc\" -DGTK_HOST=\"$(AT_PLAT)-pc-vs$(VSVER)\" -DGTK_PRINT_BACKENDS=\"file\" -DINCLUDE_IM_am_et -DINCLUDE_IM_cedilla -DINCLUDE_IM_cyrillic_translit -DINCLUDE_IM_ime -DINCLUDE_IM_inuktitu -DINCLUDE_IM_ipa -DINCLUDE_IM_multipress -DINCLUDE_IM_thai -DINCLUDE_IM_ti_er -DINCLUDE_IM_ti_et -DINCLUDE_IM_viqr -DGTK_TEXT_USE_INTERNAL_UNSUPPORTED_API -I../.. -I../../gtk -I../../gdk	\
	--cflags-end	\
	--warn-all --add-include-path=. --include-uninstalled=./Gdk-3.0.gir	\
	--filelist=Gtk_3_0_gir_list	\
	-o $@

Gtk-3.0.typelib: Gtk-3.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	Gtk-3.0.gir	\
	-o $@

