#ifndef ENCHANT_MSVC_CONFIG_H
#define ENCHANT_MSVC_CONFIG_H

#include <BaseTsd.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <sys/types.h>

#if !defined(_SSIZE_T_DEFINED) && !defined(SSIZE_T_DEFINED)
typedef SSIZE_T ssize_t;
#define _SSIZE_T_DEFINED
#define SSIZE_T_DEFINED
#endif

#define _GL_CONFIG_H_INCLUDED 1

#define PACKAGE "enchant"
#define PACKAGE_NAME "Enchant"
#define PACKAGE_TARNAME "enchant"
#define PACKAGE_VERSION "2.8.19"
#define VERSION "2.8.19"
#define ENCHANT_MAJOR_VERSION "2"
#define ENCHANT_VERSION_STRING "2.8.19"

#define ENABLE_RELOCATABLE 1
#define ENABLE_COSTLY_RELOCATABLE 1
#define NO_XMALLOC 1
#define HAVE_VISIBILITY 0
#define DEPENDS_ON_LIBCHARSET 0
#define DEPENDS_ON_LIBICONV 0
#define DEPENDS_ON_LIBINTL 0
#define HAVE_ICONV 0
#define ENABLE_NLS 0
#define HAVE_FLOCK 0
#define HAVE_SYS_FILE_H 0
#define GNULIB_FLOCK 1
#define GNULIB_MSVC_NOTHROW 0
#define HAVE_C_BOOL 1
#define HAVE_STDBOOL_H 1
#define STDC_HEADERS 1

#define _GL_INLINE static __inline
#define _GL_EXTERN_INLINE static __inline
#define _GL_INLINE_HEADER_BEGIN
#define _GL_INLINE_HEADER_END
#define _GL_ATTRIBUTE_MALLOC
#define _GL_ATTRIBUTE_DEALLOC_FREE
#define _GL_ATTRIBUTE_NONSTRING
#define _GL_ATTRIBUTE_PURE
#define _GL_ATTRIBUTE_CONST
#define _GL_ATTRIBUTE_UNUSED
#define _GL_UNUSED

#if defined(_MSC_VER)
#pragma warning(disable: 4996)
#ifndef strdup
#define strdup _strdup
#endif
#endif

#endif
