_sources = [
        'connection.cc',
        'signal_base.cc',
        'trackable.cc',
        'adaptors/lambda/lambda.cc',
        'functors/slot_base.cc',
]

_headers = [
    'bind.h',
    'bind_return.h',
    'connection.h',
    'limit_reference.h',
    'reference_wrapper.h',
    'retype_return.h',
    'sigc++.h',
    'signal.h',
    'signal_base.h',
    'slot.h',
    'trackable.h',
    'type_traits.h',
    'visit_each.h',
]

_headers_a = [
    'adaptors/adaptor_trait.h',
    'adaptors/adaptors.h',
    'adaptors/bind.h',
    'adaptors/bind_return.h',
    'adaptors/bound_argument.h',
    'adaptors/compose.h',
    'adaptors/deduce_result_type.h',
    'adaptors/exception_catch.h',
    'adaptors/hide.h',
    'adaptors/retype.h',
    'adaptors/retype_return.h',
    'adaptors/track_obj.h',
]

_headers_al = [
    'adaptors/lambda/base.h',
    'adaptors/lambda/select.h',
]

_headers_f = [
    'functors/functor_trait.h',
    'functors/functors.h',
    'functors/mem_fun.h',
    'functors/ptr_fun.h',
    'functors/slot.h',
    'functors/slot_base.h',
]

install_headers(_headers, subdir: _api_path)
install_headers(_headers_a, subdir: join_paths(_api_path, 'adaptors'))
install_headers(_headers_al, subdir: join_paths(_api_path, 'adaptors', 'lambda'))
install_headers(_headers_f, subdir: join_paths(_api_path, 'functors'))

# configuration header
install_headers('../MSVC_Net2013/sigc++config.h', subdir: join_paths(_libdir, 'sigc++-2.0', 'include'))

if false

        # Marshallers
        atk_marshals = gnome.genmarshal('atkmarshal',
                                        sources: 'atkmarshal.list',
                                        prefix: 'atk_marshal')
        atk_marshal_h = atk_marshals[1]

        # Enumerations for GType
        atk_enums = gnome.mkenums('atk-enum-types',
                                  sources: atk_headers,
                                  c_template: 'atk-enum-types.c.template',
                                  h_template: 'atk-enum-types.h.template',
                                  install_dir: join_paths(atk_includedir, atk_api_path),
                                  install_header: true)
        atk_enum_h = atk_enums[1]

        atk_cflags = [
          '-DG_LOG_DOMAIN="Atk"',
          '-DG_LOG_USE_STRUCTURED=1',
          '-DGLIB_DISABLE_DEPRECATION_WARNINGS',
          '-DATK_DISABLE_DEPRECATION_WARNINGS',
          '-DATK_COMPILATION',
          '-DATK_LOCALEDIR="@0@"'.format(join_paths(atk_datadir, 'locale')),
        ]

        atk_inc = include_directories('.')
endif

_inc = include_directories('.')
_cflags = [
    '-DSIGC_BUILD',
    '-D_WINDLL',
    '-DCONSOLE',
    '-D_MBCS',
]
win = import('windows')
libsigc = shared_library('sigc-@0@'.format(_api_version),
                        _sources,
                        win.compile_resources('sigc.rc'),
#                        soversion: atk_soversion,
                        version: _libversion,
                        install: true,
#                        dependencies: gobject_dep,
                        include_directories: [ root_inc, _inc, ],
                        cpp_args: common_cflags + _cflags,
                        link_args: common_ldflags)

libsigc_dep = declare_dependency(link_with: libsigc,
                                include_directories: _inc,
#                                 dependencies: gobject_dep,
#                                sources: atk_enum_h
                                )

if false
        libatk_dep = declare_dependency(link_with: libatk,
                                        include_directories: atk_inc,
                                        dependencies: gobject_dep,
                                        sources: atk_enum_h)

        if not meson.is_cross_build()
          gnome.generate_gir(libatk,
                             sources: atk_sources + atk_headers + [ atk_enum_h ],
                             namespace: 'Atk',
                             nsversion: atk_api_version,
                             identifier_prefix: 'Atk',
                             symbol_prefix: 'atk',
                             export_packages: 'atk',
                             includes: [ 'GObject-2.0' ],
                             install: true,
                             extra_args: [
                               '--quiet',
                               '--c-include=atk/atk.h',
                               '-DATK_COMPILATION',
                             ])
        endif
endif
