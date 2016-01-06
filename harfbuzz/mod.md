 * Download [HarfBuzz 1.1.2](https://github.com/wingtk/harfbuzz/releases/download/1.1.2.msvc/harfbuzz-1.1.2.tar.bz2)
 * In `build\win32\config-msvc.mak`, remove: the -vs$(VSVER) suffix from 
    * HARFBUZZ_DLL_FILENAME
    * HARFBUZZ_ICU_DLL_FILENAME
    * HARFBUZZ_GOBJECT_DLL_FILENAME