#ifndef ENCHANT_GNULIB_COMPAT_H
#define ENCHANT_GNULIB_COMPAT_H

#include <string.h>

#ifndef memeq
#define memeq(a, b, n) (memcmp((a), (b), (n)) == 0)
#endif

#ifndef streq
#define streq(a, b) (strcmp((a), (b)) == 0)
#endif

#endif
