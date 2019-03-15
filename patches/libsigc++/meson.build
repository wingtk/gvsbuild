project('libsigc++', 'cpp',
        version: '2.10.0',
        license: 'LGPLv2.1+',
        default_options: [
          'buildtype=debugoptimized',
          'warning_level=1',
          'cpp_std=c++11',
        ],
        meson_version : '>= 0.40.1')

version = meson.project_version().split('.')
_major_version = version[0].to_int()
_minor_version = version[1].to_int()
_micro_version = version[2].to_int()

_api_version = '2.0'
_api_path = 'sigc++-@0@/sigc++'.format(_api_version)

_prefix = get_option('prefix')
_libdir = join_paths(_prefix, get_option('libdir'))
_sysconfdir = join_paths(_prefix, get_option('sysconfdir'))
_includedir = join_paths(_prefix, get_option('includedir'))
_datadir = join_paths(_prefix, get_option('datadir'))
_libexecdir = join_paths(_prefix, get_option('libexecdir'))

_conf = configuration_data()

_conf.set_quoted('VERSION', meson.project_version())

# Maintain version scheme with libtool
_libversion = '2.0'

# Compiler and linker flags
common_cflags = []
common_ldflags = [ '/MACHINE:X86', ]

test_cflags = []

if false
        # Symbol visibility
        if get_option('default_library') != 'static'
          if host_system == 'windows'
            atk_conf.set('DLL_EXPORT', true)
            atk_conf.set('_ATK_EXTERN', '__declspec(dllexport) extern')
            if cc.get_id() != 'msvc'
              test_cflags += ['-fvisibility=hidden']
            endif
          else
            atk_conf.set('_ATK_EXTERN', '__attribute__((visibility("default"))) extern')
            test_cflags += ['-fvisibility=hidden']
          endif
        endif

        # Check all compiler flags
        foreach cflag: test_cflags
          if cc.has_argument(cflag)
            common_cflags += [ cflag ]
          endif
        endforeach

        # Linker flags
        if host_machine.system() == 'linux'
          foreach ldflag: [ '-Wl,-Bsymbolic', '-Wl,-z,relro', '-Wl,-z,now', ]
            if cc.has_argument(ldflag)
              common_ldflags += [ ldflag ]
            endif
          endforeach
        endif

        # Maintain compatibility with autotools on macOS
        if host_machine.system() == 'darwin'
          common_ldflags += [ '-compatibility_version=1', '-current_version=1.0', ]
        endif

        # Functions
        checked_funcs = [
          'bind_textdomain_codeset',
        ]

        foreach f: checked_funcs
          if cc.has_function(f)
            atk_conf.set('HAVE_' + f.underscorify().to_upper(), 1)
          endif
        endforeach

        # Dependencies
        gobject_req_version = '>= 2.31.2'

        gobject_dep = dependency('gobject-2.0', version: gobject_req_version)
endif

# Compat variables for pkgconfig
pkgconf = configuration_data()
pkgconf.set('prefix', _prefix)
pkgconf.set('exec_prefix', _prefix)
pkgconf.set('libdir', _libdir)
pkgconf.set('includedir', _includedir)
pkgconf.set('PACKAGE_VERSION', meson.project_version())
pkgconf.set('SIGCXX_MAJOR_VERSION', _major_version)
pkgconf.set('SIGCXX_MINOR_VERSION', _minor_version)
pkgconf.set('SIGCXX_MICRO_VERSION', _micro_version)
pkgconf.set('SIGCXX_API_VERSION', _api_version)
pkgconf.set('srcdir', '.')

configure_file(input: 'sigc++.pc.in',
         output: 'sigc++-2.0.pc',
         configuration: pkgconf,
         install: true,
         install_dir: join_paths(_libdir, 'pkgconfig'))

root_inc = include_directories('.')

subdir('sigc++')
subdir('tests')
subdir('examples')

##? if get_option('enable_docs')
##?   subdir('docs')
##? endif
