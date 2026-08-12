# -*- Makefile -*- for Enchant 2.x on Microsoft Visual C++

ENCHANT_MAJOR_VERSION=2
ENCHANT_MINOR_VERSION=8
ENCHANT_MICRO_VERSION=19
ENCHANT_VERSION=$(ENCHANT_MAJOR_VERSION).$(ENCHANT_MINOR_VERSION).$(ENCHANT_MICRO_VERSION)

!if !defined(DLL)
DLL=1
!endif
!if !defined(DEBUG)
DEBUG=0
!endif
!if !defined(MFLAGS)
MFLAGS=/MD
!endif
!if !defined(GLIBDIR)
!error GLIBDIR must point to the GLib include\glib-2.0 directory
!endif
!if !defined(CPREFIX)
!error CPREFIX must point to the final GTK prefix using forward slashes
!endif

rootdir=..
srcdir=$(rootdir)\src
libsrcdir=$(rootdir)\lib
providersdir=$(rootdir)\providers
libgnudir=$(rootdir)\libgnu
bindir=$(rootdir)\bin

!if $(DEBUG)
outdir=$(bindir)\debug
OPTIMFLAGS=/Od /D_DEBUG
!else
outdir=$(bindir)\release
OPTIMFLAGS=/O2 /DNDEBUG /D_NDEBUG
!endif

objdir=$(outdir)\obj
pdbdir=$(outdir)\pdb
otherlibdir=$(GLIBDIR)\..\..\lib

CC=cl
CXX=cl
LINK=link
COPY=copy
RM=-del

!ifdef X64
MACHINE_FLAG=X64
!else
MACHINE_FLAG=X86
!endif

INCLUDES= \
    /I"$(rootdir)" \
    /I"$(srcdir)" \
    /I"$(libsrcdir)" \
    /I"$(libgnudir)" \
    /I"$(GLIBDIR)" \
    /I"$(GLIBDIR)\glib" \
    /I"$(GLIBDIR)\gmodule" \
    /I"$(GLIBDIR)\..\..\lib\glib-2.0\include"

COMMON_DEFINES= \
    /DWIN32 \
    /D_WIN32 \
    /D_WINDOWS \
    /DUNICODE \
    /D_UNICODE \
    /D_CRT_SECURE_NO_WARNINGS \
    /DINSTALLPREFIX=\"$(CPREFIX)\"

CFLAGS= \
    /nologo \
    $(MFLAGS) \
    /W1 \
    /Z7 \
    /FS \
    /MP \
    $(OPTIMFLAGS) \
    $(COMMON_DEFINES) \
    $(INCLUDES) \
    /FI"$(srcdir)\config.h"

CXXFLAGS=$(CFLAGS) /EHsc /std:c++17

LINKFLAGS= \
    /NOLOGO \
    /INCREMENTAL:NO \
    /MACHINE:$(MACHINE_FLAG) \
    /OPT:REF \
    /OPT:ICF \
    /DEBUG \
    /MANIFEST:EMBED

LINK_DLL=$(LINK) $(LINKFLAGS) /DLL /SUBSYSTEM:WINDOWS
LINK_EXE=$(LINK) $(LINKFLAGS) /SUBSYSTEM:CONSOLE

GLIB_LIBS= \
    "$(otherlibdir)\glib-2.0.lib" \
    "$(otherlibdir)\gobject-2.0.lib" \
    "$(otherlibdir)\gmodule-2.0.lib" \
    "$(otherlibdir)\gio-2.0.lib"

all: makedirs libenchant enchant_winspell enchant enchant_lsmod aliases verify

makedirs:
	@if not exist "$(bindir)" mkdir "$(bindir)"
	@if not exist "$(outdir)" mkdir "$(outdir)"
	@if not exist "$(objdir)" mkdir "$(objdir)"
	@if not exist "$(pdbdir)" mkdir "$(pdbdir)"

################################################################################
# libenchant

LIBENCHANT_DLL=$(outdir)\libenchant.dll
LIBENCHANT_LIB=$(outdir)\libenchant.lib
LIBENCHANT_PDB=$(pdbdir)\libenchant.pdb

LIBENCHANT_DEFINES= \
    /D_ENCHANT_BUILD=1 \
    /DENABLE_RELOCATABLE=1 \
    /DENABLE_COSTLY_RELOCATABLE=1 \
    /DNO_XMALLOC=1 \
    /DPIC=1 \
    /DBUILDING_DLL=1 \
    /DDLL_EXPORT=1 \
    /DINSTALLDIR=\"$(CPREFIX)/bin\"

LIBENCHANT_OBJECTS= \
    $(objdir)\lib-api.obj \
    $(objdir)\lib-broker.obj \
    $(objdir)\lib-composite.obj \
    $(objdir)\lib-dict.obj \
    $(objdir)\lib-provider.obj \
    $(objdir)\lib-provider-dict.obj \
    $(objdir)\lib-pwl.obj \
    $(objdir)\lib-util.obj \
    $(objdir)\flock.obj \
    $(objdir)\relocatable.obj

libenchant: $(LIBENCHANT_DLL)

$(LIBENCHANT_DLL): $(LIBENCHANT_OBJECTS)
	$(LINK_DLL) $(LIBENCHANT_OBJECTS) $(GLIB_LIBS) advapi32.lib /OUT:"$@" /IMPLIB:"$(LIBENCHANT_LIB)" /PDB:"$(LIBENCHANT_PDB)"

$(objdir)\lib-api.obj: $(libsrcdir)\api.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\lib-broker.obj: $(libsrcdir)\broker.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\lib-composite.obj: $(libsrcdir)\composite.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\lib-dict.obj: $(libsrcdir)\dict.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\lib-provider.obj: $(libsrcdir)\provider.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\lib-provider-dict.obj: $(libsrcdir)\provider-dict.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\lib-pwl.obj: $(libsrcdir)\pwl.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\lib-util.obj: $(libsrcdir)\util.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\flock.obj: $(libgnudir)\flock.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

$(objdir)\relocatable.obj: $(libgnudir)\relocatable.c
	$(CC) $(CFLAGS) $(LIBENCHANT_DEFINES) /c "$**" /Fo"$@"

################################################################################
# Windows Spell Checking API provider

WINSPELL_DLL=$(outdir)\enchant_winspell.dll
WINSPELL_PDB=$(pdbdir)\enchant_winspell.pdb
WINSPELL_LIB=$(outdir)\enchant_winspell.lib

WINSPELL_DEFINES= \
    /D_ENCHANT_BUILD=1 \
    /D_WIN32_WINNT=_WIN32_WINNT_WIN8 \
    /DNTDDI_VERSION=NTDDI_WIN8

WINSPELL_OBJECTS= \
    $(objdir)\enchant-winspell.obj \
    $(objdir)\bcp47.obj

enchant_winspell: $(WINSPELL_DLL)

$(WINSPELL_DLL): $(LIBENCHANT_DLL) $(WINSPELL_OBJECTS)
	$(LINK_DLL) $(WINSPELL_OBJECTS) "$(LIBENCHANT_LIB)" $(GLIB_LIBS) ole32.lib oleaut32.lib uuid.lib /EXPORT:init_enchant_provider /OUT:"$@" /IMPLIB:"$(WINSPELL_LIB)" /PDB:"$(WINSPELL_PDB)"

$(objdir)\enchant-winspell.obj: $(providersdir)\enchant_winspell.cpp
	$(CXX) $(CXXFLAGS) $(WINSPELL_DEFINES) /c "$**" /Fo"$@"

$(objdir)\bcp47.obj: $(libgnudir)\bcp47.c
	$(CC) $(CFLAGS) $(WINSPELL_DEFINES) /FI"$(srcdir)\gnulib-compat.h" /c "$**" /Fo"$@"

################################################################################
# Command-line programs

ENCHANT_EXE=$(outdir)\enchant-2.exe
ENCHANT_PDB=$(pdbdir)\enchant-2.pdb
ENCHANT_OBJECTS= \
    $(objdir)\cli-enchant.obj \
    $(objdir)\cli-util.obj

enchant: $(ENCHANT_EXE)

$(ENCHANT_EXE): $(LIBENCHANT_DLL) $(ENCHANT_OBJECTS)
	$(LINK_EXE) $(ENCHANT_OBJECTS) "$(LIBENCHANT_LIB)" $(GLIB_LIBS) /OUT:"$@" /PDB:"$(ENCHANT_PDB)"

$(objdir)\cli-enchant.obj: $(srcdir)\enchant.c
	$(CC) $(CFLAGS) /D_CONSOLE /c "$**" /Fo"$@"

$(objdir)\cli-util.obj: $(srcdir)\util.c
	$(CC) $(CFLAGS) /D_CONSOLE /c "$**" /Fo"$@"

ENCHANT_LSMOD_EXE=$(outdir)\enchant-lsmod-2.exe
ENCHANT_LSMOD_PDB=$(pdbdir)\enchant-lsmod-2.pdb
ENCHANT_LSMOD_OBJECTS= \
    $(objdir)\cli-enchant-lsmod.obj \
    $(objdir)\cli-util.obj

enchant_lsmod: $(ENCHANT_LSMOD_EXE)

$(ENCHANT_LSMOD_EXE): $(LIBENCHANT_DLL) $(ENCHANT_LSMOD_OBJECTS)
	$(LINK_EXE) $(ENCHANT_LSMOD_OBJECTS) "$(LIBENCHANT_LIB)" $(GLIB_LIBS) /OUT:"$@" /PDB:"$(ENCHANT_LSMOD_PDB)"

$(objdir)\cli-enchant-lsmod.obj: $(srcdir)\enchant-lsmod.c
	$(CC) $(CFLAGS) /D_CONSOLE /c "$**" /Fo"$@"

aliases: $(ENCHANT_EXE) $(ENCHANT_LSMOD_EXE)
	$(COPY) /Y "$(ENCHANT_EXE)" "$(outdir)\enchant.exe" >NUL
	$(COPY) /Y "$(ENCHANT_LSMOD_EXE)" "$(outdir)\enchant-lsmod.exe" >NUL

verify: $(LIBENCHANT_DLL) $(WINSPELL_DLL)
	@dumpbin /nologo /exports "$(LIBENCHANT_DLL)" | findstr /C:"enchant_broker_init" >NUL
	@dumpbin /nologo /exports "$(WINSPELL_DLL)" | findstr /C:"init_enchant_provider" >NUL

clean:
	$(RM) "$(objdir)\*.obj"
	$(RM) "$(outdir)\*.dll"
	$(RM) "$(outdir)\*.exe"
	$(RM) "$(outdir)\*.lib"
	$(RM) "$(outdir)\*.exp"
	$(RM) "$(pdbdir)\*.pdb"
