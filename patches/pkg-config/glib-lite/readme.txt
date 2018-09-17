Glib for building pkg-config for windows.

In this directory is present a 'lite' version of Glib, from
the official Glib 2.58.0 release, to be used to build a
stand alone pkg-config package from the freedesktop.org
tarballs.

The pkg-config depends on glib and this, for the old version, is
not a big problem because, at the time, glib doesn't depends on
pkg-config so building gettext & glib gives you also pkg-config.

Now, with Glib version 2.58, the build system is based on meson and
depends heavily on pkg-config for the dependency so pkg-config is
needed before Glib and we have the classical chicken & egg problem.

Only the c source of function used by pkg-config are presents and
are exactly the same of the official 2.58.0 tarball except for the
ggettext.c source: even if built without NLS support in some modules
the g_dgettext(...) and g_dngettext(...) functions are used so I put
the two at the beginning of the module if ENABLE_NLS is not defined.

The other modification is the comment on glib.h of the includes not
used by pkg-config and the glib part copied.

No other patches or code moved around.

The sources create a static lib that is linked directly to the
pkg-config, resulting in a 500k executable.

In pkg-config the only modification is the initialization of the
library at startup (normally, with the glib dinamically linked, the
task is made by the DllMain function in the glib-xxx.dll): without
this init the program crash and is not usable.

The config.h & glibconfig.h are taken from the windows build and
changed to try to limit the size and the modules used (for example
the international part, libintl & gettext, is disabled).
