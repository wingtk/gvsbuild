#ifndef ENCHANT_CONFIGMAKE_H
#define ENCHANT_CONFIGMAKE_H

#ifndef INSTALLPREFIX
#error INSTALLPREFIX must be supplied by the build system
#endif

#define PKGDATADIR INSTALLPREFIX "/share/enchant-2"
#define PKGLIBDIR INSTALLPREFIX "/lib/enchant-2"
#define SYSCONFDIR INSTALLPREFIX "/etc"

#endif
