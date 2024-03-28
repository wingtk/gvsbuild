# NMake Makefile portion for enabling features for Windows builds

# You may change these lines to customize the .lib files that will be linked to

# Please do not change anything beneath this line unless maintaining the NMake Makefiles
# Bare minimum features and sources built into libiconv on Windows
GETTEXT_VERSION_MAJOR=0
GETTEXT_VERSION_MINOR=22
GETTEXT_VERSION_MICRO=3
GETTEXT_VERSION=$(GETTEXT_VERSION_MAJOR).$(GETTEXT_VERSION_MINOR).$(GETTEXT_VERSION_MICRO)

!ifndef ICON_DIR
ICONV_DIR=$(PREFIX)
!endif
!ifndef ICONV_INCLUDEDIR
ICONV_INCLUDEDIR=$(ICONV_DIR)\include
!endif
!ifndef ICONV_LIBDIR
ICONV_LIBDIR=$(ICONV_DIR)\lib
!endif
!ifndef ICONV_BINDIR
ICONV_BINDIR=$(ICONV_DIR)\bin
!endif

# For Windows 7 or later
GETTEXT_BASE_DEFINES =	\
	/DENABLE_RELOCATABLE=1	\
	/DPIC	\
	/DHAVE_CONFIG_H	\
	/D_CRT_SECURE_NO_WARNINGS	\
	/D_CRT_NONSTDC_NO_WARNINGS	\
	/D_WIN32_WINNT=0x0601	\
	/wd4273	\
	$(CFLAGS)

GETTEXT_RUNTIME_BASE_DEFINES =	\
	$(GETTEXT_BASE_DEFINES)	\
	/DBUILDING_DLL	\
	/DDLL_EXPORT	\
	/DIN_LIBRARY	\
	/DNO_XMALLOC

GETTEXT_BASE_PATH_DEFINES =	\
	/DINSTALLDIR=\"c:/vs$(VSVER).0/$(PLAT)\"	\
	/DLIBDIR=\"c:/vs$(VSVER).0/$(PLAT)/lib\"	\
	/DLOCALEDIR=\"c:/vs$(VSVER).0/$(PLAT)/share/locale\"	\
	/DLOCALE_ALIAS_PATH=\"c:/vs$(VSVER).0/$(PLAT)/share/locale\"

EXTRA_INSTALL_PATHS_DEFINES =	\
	/DLIBPATHVAR=\"PATH\"	\
	/DLIBDIRS=\"c:/vs$(VSVER).0/$(PLAT)/bin\",	\
	/DINSTALLDIR=\"c:/vs$(VSVER).0/$(PLAT)/bin\"

GETTEXT_RUNTIME_CFLAGS =	\
	$(GETTEXT_RUNTIME_BASE_DEFINES)	\
	$(GETTEXT_BASE_PATH_DEFINES)	\
	/DBUILDING_LIBINTL	\
	/DIN_LIBINTL	\
	/DWOE32DLL		\
	/DDEPENDS_ON_LIBICONV=1	\
	/Dset_relocation_prefix=libintl_set_relocation_prefix

GETTEXT_RUNTIME_GNULIB_CFLAGS =	\
	$(GETTEXT_BASE_DEFINES)	\
	$(GETTEXT_BASE_PATH_DEFINES)	\
	/DDLL_EXPORT	\
	/DDEPENDS_ON_LIBICONV=1	\
	/DDEPENDS_ON_LIBINTL=1	\
	/DEXEEXT=\".exe\"

GETTEXT_RUNTIME_DEP_LIBS = iconv.lib advapi32.lib

TEXTSTYLE_DEP_LIBS = ws2_32.lib $(GETTEXT_RUNTIME_DEP_LIBS)
GETTEXTLIB_DEP_LIBS = bcrypt.lib $(TEXTSTYLE_DEP_LIBS)

FORCED_INCLUDED_HEADERS =	\
	/FIarg-nonnull.h	\
	/FIc++defs.h	\
	/FIwarn-on-use.h	\
	/FI_Noreturn.h

BASE_INCLUDE_FLAGS =	\
	/I$(ICONV_INCLUDEDIR)	\
	/I$(PREFIX)\include	\
	$(FORCED_INCLUDED_HEADERS)

# Look for iconv.lib in ICONV_LIBDIR too
LDFLAGS = $(LDFLAGS) /libpath:$(ICONV_LIBDIR) /libpath:$(PREFIX)\lib

LIBINTL_INCLUDES = \
	/I..\gettext-runtime\intl	\
	/I..\msvc\gettext-runtime\intl	\
	/I..\gettext-runtime\intl\gnulib-lib	\
	/I..\msvc\gettext-runtime\intl\gnulib-lib	\
	$(BASE_INCLUDE_FLAGS)

GETTEXT_RUNTIME_GNULIB_INCLUDES =	\
	/I..\msvc\gettext-runtime\gnulib-lib	\
	/I..\gettext-runtime\gnulib-lib	\
	/I..\msvc\gettext-runtime	\
	/I..\gettext-runtime\intl	\
	/I..\msvc\gettext-runtime\intl	\
	$(BASE_INCLUDE_FLAGS)

ASPRINTF_INCLUDES =	\
	/I..\msvc\gettext-runtime\libasprintf	\
	/I..\gettext-runtime\libasprintf	\
	/I..\gettext-runtime\libasprintf\gnulib-lib	\
	/I..\msvc\gettext-runtime\libasprintf\gnulib-lib	\
	$(BASE_INCLUDE_FLAGS)

ASPRINTF_DEFINES =	\
	/DIN_LIBASPRINTF=1	\
	$(GETTEXT_BASE_DEFINES)

GETTEXT_RC_FLAGS =	\
	/dPACKAGE_VERSION_MAJOR=$(GETTEXT_VERSION_MAJOR)	\
	/dPACKAGE_VERSION_MINOR=$(GETTEXT_VERSION_MINOR)	\
	/dPACKAGE_VERSION_SUBMINOR=$(GETTEXT_VERSION_MICRO)	\
	/dPACKAGE_VERSION_STRING=\"$(GETTEXT_VERSION)\"

LIBTEXTSTYLE_INCLUDES =	\
	/I..\msvc\libtextstyle\lib	\
	/I..\libtextstyle\lib	\
	/I..\msvc\libtextstyle	\
	/I..\libtextstyle	\
	/I..\msvc\libtextstyle\lib\glib	\
	/I..\libtextstyle\lib\libcroco	\
	$(BASE_INCLUDE_FLAGS)

LIBTEXTSTYLE_DEFINES =	\
	/DIN_LIBTEXTSTYLE=1	\
	/DDEPENDS_ON_LIBICONV=1	\
	$(GETTEXT_BASE_DEFINES)

GETTEXT_TOOLS_INCLUDES =	\
	/I..\msvc\gettext-tools\gnulib-lib	\
	/I..\gettext-tools\gnulib-lib	\
	/I..\msvc\gettext-tools	\
	/I..\gettext-tools	\
	/I..\msvc\gettext-runtime\intl	\
	/I..\gettext-runtime\intl	\
	$(BASE_INCLUDE_FLAGS)

GETTEXT_TOOLS_GNULIB_CFLAGS =	\
	$(GETTEXT_RUNTIME_GNULIB_CFLAGS)

LIBGREP_INCLUDES =	\
	/I..\msvc\gettext-tools\libgrep	\
	/I..\gettext-tools\libgrep	\
	$(GETTEXT_TOOLS_INCLUDES)

LIBGREP_CFLAGS =	\
	$(GETTEXT_RUNTIME_GNULIB_CFLAGS)	\
	/DIN_GETTEXT_TOOLS_LIBGREP=1

GETTEXTPO_GNULIB_INCLUDES =	\
	/I..\msvc\gettext-tools\libgettextpo	\
	/I..\gettext-tools\libgettextpo	\
	/I..\msvc\gettext-tools	\
	/I..\gettext-tools	\
	/I..\msvc\gettext-tools\src	\
	/I..\gettext-tools\src	\
	/I..\msvc\gettext-runtime\intl	\
	/I..\gettext-runtime\intl	\
	$(BASE_INCLUDE_FLAGS)

LIBGETTEXTPO_DEFINES =	\
	/DIN_LIBGETTEXTPO=1	\
	/DOMIT_SETLOCALE_LOCK=1	\
	$(GETTEXT_RUNTIME_GNULIB_CFLAGS)

LIBGETTEXTSRC_INCLUDES =	\
	/I..\msvc\gettext-tools\src	\
	/I..\gettext-tools\src	\
	/I..\msvc\gettext-tools	\
	/I..\gettext-tools	\
	/I..\gettext-tools\libgrep	\
	/I..\msvc\gettext-tools\gnulib-lib	\
	/I..\gettext-tools\gnulib-lib	\
	/I..\msvc\gettext-runtime\intl	\
	/I..\gettext-runtime\intl	\
	$(BASE_INCLUDE_FLAGS)

LIBGETTEXTSRC_CFLAGS =	\
	$(GETTEXT_TOOLS_GNULIB_CFLAGS)	\
	/DBISON_LOCALEDIR=\"c:/vs$(VSVER).0/$(PLAT)/share/locale\"	\
	/DUSE_JAVA=0	\
	/DGETTEXTJAR=\"c:/vs$(VSVER).0/$(PLAT)/share/gettext/gettext.jar\"	\
	/DGETTEXTDATADIR=\"c:/vs$(VSVER).0/$(PLAT)/share/gettext\"	\
	/DPROJECTSDIR=\"c:/vs$(VSVER).0/$(PLAT)/share/gettext/projects\"

# We build the libintl DLL/LIB at least
INTL_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\intl.lib
INTL_GNULIB_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\intl-gnulib.lib
ASPRINTF_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\asprintf.lib
ASPRINTF_GNULIB_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\asprintf-gnulib.lib
GETTEXTLIB_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\gettextlib-$(GETTEXT_VERSION).lib
GETTEXTPO_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\gettextpo.lib
GETTEXTSRC_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\gettextsrc-$(GETTEXT_VERSION).lib
GRT_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\grt.lib
INTL_CS_DLL = vs$(VSVER)\$(CFG)\$(PLAT)\GNU.Gettext.dll
LIBGREP_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\grep.lib
LIBTEXTSTYLE_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\textstyle.lib

!ifdef USE_LIBTOOL_DLL_SCHEME
INTL_DLL_SUFFIX = -8
OTHER_DLL_SUFFIX = -0
!else
INTL_DLL_SUFFIX =
OTHER_DLL_SUFFIX =
!endif

LIBINTL_DLL = intl$(INTL_DLL_SUFFIX).dll
LIBASPRINTF_DLL = asprintf$(OTHER_DLL_SUFFIX).dll
LIBTEXTSTYLE_DLL = textstyle$(OTHER_DLL_SUFFIX).dll
LIBGETTEXTPO_DLL = gettextpo$(OTHER_DLL_SUFFIX).dll
GETTEXT_RUNTIME_LIBS =	\
	$(ASPRINTF_LIB)	\
	$(INTL_LIB)	\
	$(INTL_CS_DLL)
