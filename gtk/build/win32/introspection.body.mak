Gdk-2.0.gir: Gdk_2_0_gir_list
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=Gdk	\
	--nsversion=2.0	\
		\
	--library=gdk-win32-2.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
	--include=Gio-2.0 --include=GdkPixbuf-2.0 --include=Pango-1.0 --include=cairo-1.0	\
	--pkg-export=gdk-2.0	\
	--cflags-begin	\
	-DGDK_COMPILATION -I../.. -I../../gdk -I.../../gdk/win32	\
	--cflags-end	\
	--c-include=gdk/gdk.h	\
	--filelist=Gdk_2_0_gir_list	\
	-o $@

Gdk-2.0.typelib: Gdk-2.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	Gdk-2.0.gir	\
	-o $@

Gtk-2.0.gir: Gtk_2_0_gir_list
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=Gtk	\
	--nsversion=2.0	\
		\
	--library=gtk-win32-2.0 --library=gdk-win32-2.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
	--include=Atk-1.0	\
	--pkg-export=gtk+-2.0	\
	--cflags-begin	\
	-DGTK_VERSION="2.24.31" -DGTK_BINARY_VERSION="2.10.0" -DGTK_COMPILATION -DGTK_DISABLE_DEPRECATED -DGTK_FILE_SYSTEM_ENABLE_UNSUPPORTED -DGTK_PRINT_BACKEND_ENABLE_UNSUPPORTED -DGTK_LIBDIR=\"/dummy/lib\" -DGTK_DATADIR=\"/dummy/share\" -DGTK_DATA_PREFIX=\"/dummy\" -DGTK_SYSCONFDIR=\"/dummy/etc\" -DGTK_HOST=\"$(AT_PLAT)-pc-vs$(VSVER)\" -DGTK_PRINT_BACKENDS=\"file\" -DINCLUDE_IM_am_et -DINCLUDE_IM_cedilla -DINCLUDE_IM_cyrillic_translit -DINCLUDE_IM_ime -DINCLUDE_IM_inuktitu -DINCLUDE_IM_ipa -DINCLUDE_IM_multipress -DINCLUDE_IM_thai -DINCLUDE_IM_ti_er -DINCLUDE_IM_ti_et -DINCLUDE_IM_viqr -UGDK_DISABLE_DEPRECATED -UGTK_DISABLE_DEPRECATED -DGTK_TEXT_USE_INTERNAL_UNSUPPORTED_API -I../.. -I../../gtk -I../../gdk	\
	--cflags-end	\
	--warn-all --add-include-path=. --include-uninstalled=./Gdk-2.0.gir	\
	--filelist=Gtk_2_0_gir_list	\
	-o $@

Gtk-2.0.typelib: Gtk-2.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	Gtk-2.0.gir	\
	-o $@

