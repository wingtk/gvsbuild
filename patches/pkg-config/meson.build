project('pkg-config', 'c',
        version: '0.29.2',
        default_options: [
          'buildtype=debugoptimized',
          'warning_level=2',
        ],
        meson_version : '>= 0.47.0',
        license: 'LGPLv2.1+')

# extarnal libs
cc = meson.get_compiler('c')
winsock2 = cc.find_library('ws2_32')

sources = [
  'main.c',
  'parse.c',
  'pkg.c',
  'rpmvercmp.c',
]

cflags = [
  '-W3',
  '-Zi',
  '-FImsvc_recommended_pragmas.h',
  '-DHAVE_CONFIG_H',
]
pkg_def = [
  '-DPKG_CONFIG_SYSTEM_INCLUDE_PATH=""',
  '-DPKG_CONFIG_SYSTEM_LIBRARY_PATH=""',
]
add_project_arguments(pkg_def, language: 'c', )

# The glib part we need
subdir('glib-lite')

# final executable
exe = executable('pkg-config',
  sources,
  install: true,
  dependencies: [
    glib_dep,
    winsock2,
  ],
  c_args: cflags,
  link_args: [
    '/OPT:REF,NOICF',
  ],
)
