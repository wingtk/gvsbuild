/* atk/atkmmconfig.h.  Generated from atkmmconfig.h.in by configure.  */
/* atkmm library configuration header */

#ifndef ATKMMCONFIG_H_INCLUDED
#define ATKMMCONFIG_H_INCLUDED

#include <glibmmconfig.h>

/* Major version number of atkmm. */
#define ATKMM_MAJOR_VERSION 2

/* Minor version number of atkmm. */
#define ATKMM_MINOR_VERSION 24

/* Micro version number of atkmm. */
#define ATKMM_MICRO_VERSION 2

/* Define when building atkmm as a static library. */
/* #undef ATKMM_STATIC_LIB */

/* Enable DLL-specific stuff only when not building a static library */
#if !defined(ATKMM_STATIC_LIB) && defined(__MINGW32__) && !defined(__CYGWIN__)
# define ATKMM_DLL 1
#endif

/* Do not dllexport as it is handled by gendef on MSVC */
#if defined(ATKMM_DLL) && !defined(ATKMM_BUILD)
# define ATKMM_API __declspec(dllimport)
#else
# define ATKMM_API
#endif

#endif /* !ATKMMCONFIG_H_INCLUDED */
