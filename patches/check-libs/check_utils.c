// Utility for testing libs, actually very much simple

// include
    #include "check_utils.h"

// code
void check_lib_symbol(void *s, char *name)
{
    printf("Symbol '%s' loaded at %p\n", name, s);
}
