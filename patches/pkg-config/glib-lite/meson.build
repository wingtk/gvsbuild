#
# glib-lite, for use with pkg-config 0.29.2
#

lib_sources = [
  'garray.c',
  'gatomic.c',
  'gbitlock.c',
  'gbytes.c',
  'gcharset.c',
  'gconvert.c',
  'gdir.c',
  'genviron.c',
  'gerror.c',
  'gfileutils.c',
  'ggettext.c',
  'ghash.c',
  'giochannel.c',
  'giowin32.c',
  'glib-init.c',
  'glist.c',
  'gmain.c',
  'gmem.c',
  'gmessages.c',
  'goption.c',
  'gpattern.c',
  'gpoll.c',
  'gprintf.c',
  'gqsort.c',
  'gquark.c',
  'gqueue.c',
  'grand.c',
  'grefcount.c',
  'gshell.c',
  'gslice.c',
  'gslist.c',
  'gspawn-win32.c',
  'gstdio.c',
  'gstrfuncs.c',
  'gstring.c',
  'gtestutils.c',
  'gthread.c',
  'gthread-win32.c',
  'gtimer.c',
  'gtranslit.c',
  'gtrashstack.c',
  'gunidecomp.c',
  'guniprop.c',
  'gutf8.c',
  'gutils.c',
  'gvariant-core.c',
  'gvariant-serialiser.c',
  'gvariant.c',
  'gvarianttype.c',
  'gvarianttypeinfo.c',
  'gwakeup.c',
  'gwin32.c',
  'localcharset.c',

  'gnulib/asnprintf.c',
  'gnulib/printf.c',
  'gnulib/printf-args.c',
  'gnulib/printf-parse.c',
  'gnulib/vasnprintf.c',

]

cflags = [
  '-W3',
  '-Zi',
  '-FImsvc_recommended_pragmas.h',
  '-DHAVE_CONFIG_H',
  '-DGLIB_COMPILATION',
  '/Gy',
]

lib_include = include_directories([
  '.',
  'glib',
  'glib/gnulib',
  'glib/libcharset',
])

glib = static_library('glib-lite',
  lib_sources,
  c_args: cflags,
  include_directories: lib_include,
)
glib_dep = declare_dependency(link_with: [ glib, ], include_directories: lib_include)
