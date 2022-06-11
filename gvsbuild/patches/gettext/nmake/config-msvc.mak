# NMake Makefile portion for enabling features for Windows builds

# You may change these lines to customize the .lib files that will be linked to

# Please do not change anything beneath this line unless maintaining the NMake Makefiles
# Bare minimum features and sources built into libiconv on Windows
GETTEXT_VERSION_MAJOR=0
GETTEXT_VERSION_MINOR=21
GETTEXT_VERSION_MICRO=0
GETTEXT_VERSION=$(GETTEXT_VERSION_MAJOR).$(GETTEXT_VERSION_MINOR).$(GETTEXT_VERSION_MICRO)

# For Windows 7 or later
GETTEXT_BASE_DEFINES =	\
	/DENABLE_RELOCATABLE=1	\
	/DHAVE_CONFIG_H	\
	/D_CRT_SECURE_NO_WARNINGS	\
	/D_CRT_NONSTDC_NO_WARNINGS	\
	/D_WIN32_WINNT=0x0601	\
	/wd4273	\
	$(CFLAGS)

GETTEXT_RUNTIME_BASE_DEFINES =	\
	$(GETTEXT_BASE_DEFINES)	\
	/DBUILDING_DLL	\
	/DIN_LIBRARY	\
	/DNO_XMALLOC	\
	/DPIC

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
	/DDEPENDS_ON_LIBICONV=1	\
	/Dset_relocation_prefix=libintl_set_relocation_prefix	\
	/Drelocate=libintl_relocate	\
	/Drelocate2=libintl_relocate2

GETTEXT_RUNTIME_GNULIB_CFLAGS =	\
	$(GETTEXT_BASE_DEFINES)	\
	$(GETTEXT_BASE_PATH_DEFINES)	\
	/DDEPENDS_ON_LIBICONV=1	\
	/DDEPENDS_ON_LIBINTL=1	\
	/DEXEEXT=\".exe\"

GETTEXT_RUNTIME_DEP_LIBS = iconv.lib advapi32.lib

TEXTSTYLE_DEP_LIBS = ws2_32.lib $(GETTEXT_RUNTIME_DEP_LIBS)
GETTEXTLIB_DEP_LIBS = bcrypt.lib $(GETTEXT_RUNTIME_DEP_LIBS)

FORCED_INCLUDED_HEADERS =	\
	/FIarg-nonnull.h	\
	/FIc++defs.h	\
	/FIwarn-on-use.h	\
	/FI_Noreturn.h

BASE_GETTEXT_RUNTIME_INCLUDES =	\
	/I..\gettext-runtime\gnulib-lib	\
	$(FORCED_INCLUDED_HEADERS)

GETTEXT_RUNTIME_INCLUDES =	\
	/I..\msvc\gettext-runtime\intl	\
	/I..\gettext-runtime\intl	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-runtime	\
	$(BASE_GETTEXT_RUNTIME_INCLUDES)

GETTEXT_RUNTIME_GNULIB_INCLUDES =	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-runtime\gnulib-lib	\
	/I..\msvc\gettext-runtime\gnulib-lib	\
	/I..\gettext-runtime\gnulib-lib	\
	$(GETTEXT_RUNTIME_INCLUDES)

ASPRINTF_INCLUDES =	\
	/I..\msvc\gettext-runtime\libasprintf	\
	/I..\gettext-runtime\libasprintf	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-runtime	\
	$(BASE_GETTEXT_RUNTIME_INCLUDES)

ASPRINTF_DEFINES =	\
	/DIN_LIBASPRINTF=1	\
	$(GETTEXT_BASE_DEFINES)

GETTEXT_RC_FLAGS =	\
	/dPACKAGE_VERSION_MAJOR=$(GETTEXT_VERSION_MAJOR)	\
	/dPACKAGE_VERSION_MINOR=$(GETTEXT_VERSION_MINOR)	\
	/dPACKAGE_VERSION_SUBMINOR=$(GETTEXT_VERSION_MICRO)	\
	/dPACKAGE_VERSION_STRING=\"$(GETTEXT_VERSION)\"

BASE_LIBTEXTSTYLE_INCLUDES =	\
	/I..\libtextstyle\lib	\
	$(FORCED_INCLUDED_HEADERS)

LIBTEXTSTYLE_INCLUDES =	\
	/I..\libtextstyle\lib\libcroco	\
	/I..\msvc\libtextstyle\lib\glib	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\libtextstyle\lib	\
	/I..\msvc\libtextstyle\lib	\
	/I..\libtextstyle\lib	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\libtextstyle	\
	/I..\msvc\libtextstyle	\
	$(BASE_LIBTEXTSTYLE_INCLUDES)

LIBTEXTSTYLE_DEFINES =	\
	/DIN_LIBTEXTSTYLE=1	\
	/DDEPENDS_ON_LIBICONV=1	\
	/DLIBXML_STATIC=1	\
	$(GETTEXT_BASE_DEFINES)

BASE_GETTEXT_TOOLS_INCLUDES =	\
	/I..\gettext-tools\gnulib-lib	\
	$(FORCED_INCLUDED_HEADERS)

GETTEXT_TOOLS_INCLUDES =	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools\gnulib-lib	\
	/I..\msvc\gettext-tools\gnulib-lib	\
	/I..\gettext-tools\gnulib-lib	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools	\
	/I..\msvc\gettext-runtime\intl	\
	$(BASE_GETTEXT_TOOLS_INCLUDES)

GETTEXT_TOOLS_GNULIB_CFLAGS =	\
	$(GETTEXT_RUNTIME_GNULIB_CFLAGS)	\
	/DLIBXML_STATIC=1

LIBGREP_INCLUDES =	\
	/I..\msvc\gettext-tools\libgrep	\
	/I..\gettext-tools\libgrep	\
	$(GETTEXT_TOOLS_INCLUDES)

LIBGREP_CFLAGS =	\
	$(GETTEXT_RUNTIME_GNULIB_CFLAGS)	\
	/DIN_GETTEXT_TOOLS_LIBGREP=1

GETTEXTPO_GNULIB_INCLUDES =	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools\libgettextpo	\
	/I..\msvc\gettext-tools\libgettextpo	\
	/I..\gettext-tools\libgettextpo	\
	/I..\gettext-tools\src	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools\gnulib-lib	\
	/I..\msvc\gettext-tools\gnulib-lib	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools	\
	/I..\msvc\gettext-runtime\intl	\
	/I..\gettext-runtime\intl	\
	$(BASE_GETTEXT_TOOLS_INCLUDES)

LIBGETTEXTPO_DEFINES =	\
	/DIN_LIBGETTEXTPO=1	\
	/DOMIT_SETLOCALE_LOCK=1	\
	$(GETTEXT_RUNTIME_GNULIB_CFLAGS)

LIBGETTEXTSRC_INCLUDES =	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools\src	\
	/I..\msvc\gettext-tools\src	\
	/I..\gettext-tools\src	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools\gnulib-lib	\
	/I..\msvc\gettext-tools\gnulib-lib	\
	/I..\gettext-tools\gnulib-lib	\
	/I..\msvc\vs$(PDBVER)\$(PLAT)\gettext-tools	\
	/I..\msvc\libtextstyle\lib	\
	/I..\msvc\gettext-runtime\intl	\
	/I..\gettext-runtime\intl	\
	$(BASE_GETTEXT_TOOLS_INCLUDES)

LIBGETTEXTSRC_CFLAGS =	\
	$(GETTEXT_TOOLS_GNULIB_CFLAGS)	\
	/DBISON_LOCALEDIR=\"c:/vs$(VSVER).0/$(PLAT)/share/locale\"	\
	/DUSE_JAVA=0	\
	/DGETTEXTJAR=\"c:/vs$(VSVER).0/$(PLAT)/share/gettext/gettext.jar\"	\
	/DGETTEXTDATADIR=\"c:/vs$(VSVER).0/$(PLAT)/share/gettext\"	\
	/DPROJECTSDIR=\"c:/vs$(VSVER).0/$(PLAT)/share/gettext/projects\"

# We build the libintl DLL/LIB at least
INTL_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\intl.lib
ASPRINTF_LIB = vs$(VSVER)\$(CFG)\$(PLAT)\asprintf.lib
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
