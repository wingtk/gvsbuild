 * In `build\Makefile.win32.features`, replace:
	* `CAIRO_HAS_FT_FONT=0` with
`CAIRO_HAS_FT_FONT=1`
	* `CAIRO_HAS_FC_FONT=0` with
`CAIRO_HAS_FC_FONT=1`
	* `CAIRO_HAS_GOBJECT_FUNCTIONS=0` with
`CAIRO_HAS_GOBJECT_FUNCTIONS=1`

* In `build\Makefile.win32.common`, handle:
	* The right paths for pixman, png and zlib
	* Add fontconfig, freetype and gobject

* Add `util\cairo-gobject\Makefile.win32` to build the cairo-gobject.dll
