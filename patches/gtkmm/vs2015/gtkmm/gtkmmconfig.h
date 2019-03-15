/* gtk/gtkmmconfig.h.  Generated from gtkmmconfig.h.in by configure.  */
#ifndef _GTKMM_CONFIG_H
#define _GTKMM_CONFIG_H

#include <gdkmmconfig.h>

/* Defined when the --enable-api-atkmm configure argument was given */
#define GTKMM_ATKMM_ENABLED 1

/* Define to omit deprecated API from gtkmm. */
/* #undef GTKMM_DISABLE_DEPRECATED */

/* Major version number of gtkmm. */
#define GTKMM_MAJOR_VERSION 3

/* Micro version number of gtkmm. */
#define GTKMM_MICRO_VERSION 2

/* Minor version number of gtkmm. */
#define GTKMM_MINOR_VERSION 22

/* Define when building gtkmm as a static library. */
/* #undef GTKMM_STATIC_LIB */

/* Enable DLL-specific stuff only when not building a static library. */
#if (!defined(GTKMM_STATIC_LIB) && !defined(__CYGWIN__) && defined(_WIN32))
# define GTKMM_DLL 1
#endif

#ifdef GTKMM_DLL
# if defined(GTKMM_BUILD) && defined(_WINDLL)
   /* Do not dllexport as it is handled by gendef on MSVC. */
#  define GTKMM_API
# elif !defined(GTKMM_BUILD)
#  define GTKMM_API __declspec(dllimport)
# else
   /* Build a static library. */
#  define GTKMM_API
# endif /* GTKMM_BUILD - _WINDLL */
#else
# define GTKMM_API
#endif /* GTKMM_DLL */

#endif /* !_GTKMM_CONFIG_H */
