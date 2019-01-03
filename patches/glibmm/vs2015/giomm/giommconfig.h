/* gio/giommconfig.h.  Generated from giommconfig.h.in by configure.  */
#ifndef _GIOMM_CONFIG_H
#define _GIOMM_CONFIG_H

#include <glibmmconfig.h>

/* Define to omit deprecated API from the library. */
/* #undef GIOMM_DISABLE_DEPRECATED */

/* Major version number of giomm. */
#define GIOMM_MAJOR_VERSION 2

/* Micro version number of giomm. */
#define GIOMM_MICRO_VERSION 1

/* Minor version number of giomm. */
#define GIOMM_MINOR_VERSION 54

/* Define if giomm is built as a static library */
/* #undef GIOMM_STATIC_LIB */

// Enable DLL-specific stuff only when not building a static library
#if !defined(__CYGWIN__) && defined(__MINGW32__) && !defined(GIOMM_STATIC_LIB)
# define GIOMM_DLL 1
#endif

#ifdef GIOMM_DLL
# if defined(GIOMM_BUILD) && defined(_WINDLL)
   /* Do not dllexport as it is handled by gendef on MSVC */
#  define GIOMM_API
# elif !defined(GIOMM_BUILD)
#  define GIOMM_API __declspec(dllimport)
# else
   /* Build a static library */
#  define GIOMM_API
# endif /* GIOMM_BUILD - _WINDLL */
#else
# define GIOMM_API
#endif /* GIOMM_DLL */

#endif /* _GIOMM_CONFIG_H */
