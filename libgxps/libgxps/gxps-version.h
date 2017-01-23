/*
 * Copyright (C) 2011  Carlos Garcia Campos <carlosgc@gnome.org>
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 */

/**
 * SECTION:gxps-version
 * @Short_description: Variables and functions to check the GXPS version
 * @Title: Version Information
 *
 * GXPS provides version information, primarily useful in configure checks
 * for builds that have a configure script. Applications will not typically
 * use the features described here.
 */

#if !defined (__GXPS_H_INSIDE__) && !defined (GXPS_COMPILATION)
#error "Only <libgxps/gxps.h> can be included directly."
#endif

#ifndef __GXPS_VERSION_H__
#define __GXPS_VERSION_H__

/**
 * GXPS_MAJOR_VERSION:
 *
 * The major version number of the GXPS header files (e.g. in GXPS version
 * 0.1.2 this is 0.)
 */
#define GXPS_MAJOR_VERSION (0)

/**
 * GXPS_MINOR_VERSION:
 *
 * The major version number of the GXPS header files (e.g. in GXPS version
 * 0.1.2 this is 1.)
 */
#define GXPS_MINOR_VERSION (2)

/**
 * GXPS_MICRO_VERSION:
 *
 * The micro version number of the GXPS header files (e.g. in GXPS version
 * 0.1.2 this is 2.)
 */
#define GXPS_MICRO_VERSION (4)

/**
 * GXPS_VERSION_STRING:
 *
 * The version number of the GXPS library as a string
 *
 * Since: 0.2.1
 */
#define GXPS_VERSION_STRING "0.2.4"

/**
 * GXPS_CHECK_VERSION:
 * @major: major version (e.g. 0 for version 0.1.2)
 * @minor: minor version (e.g. 1 for version 0.1.2)
 * @micro: micro version (e.g. 2 for version 0.1.2)
 *
 * Checks the version fo the GXPS library
 *
 * Returns: %TRUE if the version of the GXPS header files is the same
 *      as or newer than the passed-in version
 */
#define GXPS_CHECK_VERSION(major,minor,micro)                               \
        (GXPS_MAJOR_VERSION > (major) ||                                    \
         (GXPS_MAJOR_VERSION == (major) && GXPS_MINOR_VERSION > (minor)) || \
         (GXPS_MAJOR_VERSION == (major) && GXPS_MINOR_VERSION == (minor) && GXPS_MICRO_VERSION >= (micro)))

#ifndef _GXPS_EXTERN
#define _GXPS_EXTERN extern
#endif

/* We prefix variable declarations so they can
 * properly get exported in Windows DLLs.
 */
#ifndef GXPS_VAR
#  ifdef G_PLATFORM_WIN32
#    ifdef GXPS_COMPILATION
#      ifdef DLL_EXPORT
#        define GXPS_VAR __declspec(dllexport)
#      else /* !DLL_EXPORT */
#        define GXPS_VAR extern
#      endif /* !DLL_EXPORT */
#    else /* !GXPS_COMPILATION */
#      define GXPS_VAR extern __declspec(dllimport)
#    endif /* !GXPS_COMPILATION */
#  else /* !G_PLATFORM_WIN32 */
#    define GXPS_VAR _GXPS_EXTERN
#  endif /* !G_PLATFORM_WIN32 */
#endif /* GXPS_VAR */

#define GXPS_AVAILABLE_IN_ALL                   _GXPS_EXTERN

#endif /* __GXPS_VERSION_H__ */
