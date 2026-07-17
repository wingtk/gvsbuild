#include <sys/types.h>

#ifndef SSIZE_T_DEFINED
#ifdef ssize_t
#undef ssize_t
#endif
#ifdef _WIN64
typedef __int64          ssize_t;
#else
typedef int         ssize_t;
#endif
#define SSIZE_T_DEFINED
#endif

#define PACKAGE "enchant"
#define PACKAGE_VERSION "2.8.19"
#define ENCHANT_MAJOR_VERSION "2"
#define ENCHANT_VERSION_STRING "2.8.19"

#if defined(_MSC_VER)
#pragma warning(disable: 4996) /* The POSIX name for this item is deprecated. Instead, use the ISO C++ conformant name. */
#endif
