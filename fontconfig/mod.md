 * In `config.h`, replace:
  * `#define snprintf _snprintf` with
`
#if _MSC_VER < 1900
#define snprintf _snprintf
#endif
`