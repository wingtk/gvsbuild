SOURCES = \
	buffer.c \
	callable.c \
	core.c \
	gi.c \
	marshal.c \
	object.c \
	record.c

DLL = corelgilua51.dll
VERSION_FILE = version.lua

VERSION = 0.9.2

LUA_CFLAGS = /I$(PREFIX)\include\luajit-2.1
GLIB_CFLAGS = /I$(PREFIX)\include\glib-2.0 /I$(PREFIX)\lib\glib-2.0\include
GIR_CFLAGS = /I$(PREFIX)\include\gobject-introspection-1.0

LUA_LIBS = lua51.lib
GLIB_LIBS = gmodule-2.0.lib gobject-2.0.lib glib-2.0.lib
GIR_LIBS = girepository-1.0.lib
FFI_LIBS = ffi.lib

$(VERSION_FILE):
	echo return '$(VERSION)' > $@

$(DLL): $(SOURCES)
	cl /nologo /c /O2 /MD $(SOURCES) /I$(PREFIX)/include $(LUA_CFLAGS) $(GLIB_CFLAGS) $(GIR_CFLAGS)
	link /nologo /DLL /OUT:$(DLL) .\*.obj /libpath:$(PREFIX)\lib $(LUA_LIBS) $(GLIB_LIBS) $(GIR_LIBS) $(FFI_LIBS)

install: $(DLL) $(VERSION_FILE)
	mkdir $(DESTDIR)\lib\lua\lgi
	copy $(DLL) $(DESTDIR)\lib\lua\lgi

	mkdir $(DESTDIR)\share\lua\lgi\override
	copy ..\lgi.lua $(DESTDIR)\share\lua
	copy .\*.lua $(DESTDIR)\share\lua\lgi
	copy .\override\*.lua $(DESTDIR)\share\lua\lgi\override

	mkdir $(DESTDIR)\share\docs\lgi
	copy ..\LICENSE $(DESTDIR)\share\docs\lgi
