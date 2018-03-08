GdkPixbuf-2.0.gir: GdkPixbuf_2_0_gir_list 
	@-echo Generating $@...
	$(PYTHON) $(G_IR_SCANNER)	\
	--verbose -no-libtool	\
	--namespace=GdkPixbuf	\
	--nsversion=2.0	\
		\
	--library=gdk_pixbuf-2.0	\
		\
	--add-include-path=$(G_IR_INCLUDEDIR)	\
	--include=GModule-2.0 --include=Gio-2.0	\
	--pkg-export=gdk-pixbuf-2.0	\
  	\
	--cflags-begin	\
	-DGDK_PIXBUF_COMPILATION -I.. -I../gdk-pixbuf	\
	--cflags-end	\
	--warn-all --identifier-prefix=Gdk --c-include=gdk-pixbuf/gdk-pixbuf.h	\
	--filelist=GdkPixbuf_2_0_gir_list	\
	-o $@

GdkPixbuf-2.0.typelib: GdkPixbuf-2.0.gir
	@-echo Compiling $@...
	$(G_IR_COMPILER)	\
	--includedir=. --debug --verbose	\
	GdkPixbuf-2.0.gir	\
	-o $@

