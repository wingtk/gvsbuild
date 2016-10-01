 * In `config.h`, replace:
  * `#define snprintf _snprintf` with
  ```
    #if _MSC_VER < 1900
    #define snprintf _snprintf
    #endif
  ```
 * In `fontconfig.vcxproj`, replace:
  * `freetype_d.lib` with `freetype.lib`
  * `iconvd.lib` with `iconv.lib`
