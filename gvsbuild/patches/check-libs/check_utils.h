// Common declare for the library test
//

// include
    #include <stdio.h>

// declare
    extern void check_lib_symbol(void *s, char *name);

// macro
    // check one single symbol
    #define CHECK_SYMBOL(symb)  check_lib_symbol((void *)symb, #symb)

    // main function with one check
    #define CHECK_ONE(symb)                         \
        int main(int argc, const char *argv[]) {    \
            CHECK_SYMBOL(symb);                     \
            return(0);                              \
        }
