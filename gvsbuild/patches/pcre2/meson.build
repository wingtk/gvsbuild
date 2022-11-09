project('pcre2', 'c',
  license: 'BSD-3',
  meson_version: '>=0.49.0',
  version: '10.40',
)

c_compiler = meson.get_compiler('c')

pcre2_h = configure_file(input : 'src/pcre2.h.generic',
  output : 'pcre2.h',
  copy: true)

chartables = configure_file(input : 'src/pcre2_chartables.c.dist',
  output : 'pcre2_chartables.c',
  copy: true)


config_h = configure_file(input : 'src/config.h.generic',
  output : 'config.h',
  copy: true)

sources = [
  'src/pcre2_auto_possess.c',
  chartables,
  config_h, pcre2_h,
  'src/pcre2_compile.c',
  'src/pcre2_config.c',
  'src/pcre2_context.c',
  'src/pcre2_convert.c',
  'src/pcre2_dfa_match.c',
  'src/pcre2_error.c',
  'src/pcre2_extuni.c',
  'src/pcre2_find_bracket.c',
  'src/pcre2_jit_compile.c',
  'src/pcre2_maketables.c',
  'src/pcre2_match.c',
  'src/pcre2_match_data.c',
  'src/pcre2_newline.c',
  'src/pcre2_ord2utf.c',
  'src/pcre2_pattern_info.c',
  'src/pcre2_script_run.c',
  'src/pcre2_serialize.c',
  'src/pcre2_string_utils.c',
  'src/pcre2_study.c',
  'src/pcre2_substitute.c',
  'src/pcre2_substring.c',
  'src/pcre2_tables.c',
  'src/pcre2_ucd.c',
  'src/pcre2_valid_utf.c',
  'src/pcre2_xclass.c'
]

includes = [include_directories('.'), include_directories('src')]

check_headers = [
  'inttypes.h',
  'bzlib.h',
  'sys/stat.h',
  'sys/types.h',
  'sys/wait.h',
  'inttypes.h',
  'dirent.h',
  'dlfcn.h',
  'limits.h',
  'stdint.h',
  'stdlib.h',
  'string.h',
  'windows.h',
  'unistd.h'
]

config_h_defs = []
foreach h : check_headers
  if c_compiler.has_header(h)
    config_h_defs += ['-DHAVE_' + h.underscorify().to_upper()]
  endif
endforeach


check_funs = [
  ['HAVE_STRERROR', 'strerror'],
]

foreach f : check_funs
  if c_compiler.has_function(f.get(1))
    config_h_defs += ['-D' + f.get(0)]
  endif
endforeach


config_h_defs += ['-DHAVE_MEMMOVE', '-DSTDC_HEADERS', '-DSUPPORT_PCRE2_8', '-DSUPPORT_UNICODE']

if get_option('default_library') == 'static'
  static_defs = ['-DPCRE2_STATIC']
  config_h_defs += static_defs
else
  static_defs = []
endif

pcre2_8_lib = library('pcre2-8', sources,
  include_directories: includes,
  c_args: config_h_defs + ['-DHAVE_CONFIG_H', '-DPCRE2_CODE_UNIT_WIDTH=8'],
  install: true)

pcre2_posix_lib = library('pcre2-posix', ['src/pcre2posix.c', 'src/pcre2posix.h'],
  include_directories: includes,
  link_with: pcre2_8_lib,
  c_args: config_h_defs + ['-DHAVE_CONFIG_H', '-DPCRE2_CODE_UNIT_WIDTH=8'],
  install: true)

pcre2_16_lib = library('pcre2-16', sources,
  include_directories: includes,
  c_args: config_h_defs + ['-DHAVE_CONFIG_H', '-DPCRE2_CODE_UNIT_WIDTH=16'],
  install: true)

pcre2_32_lib = library('pcre2-32', sources,
  include_directories: includes,
  c_args: config_h_defs + ['-DHAVE_CONFIG_H', '-DPCRE2_CODE_UNIT_WIDTH=32'],
  install: true)

libpcre2_8 = declare_dependency(link_with: pcre2_8_lib,
  include_directories: includes,
  compile_args: static_defs)
libpcre2_posix = declare_dependency(link_with: pcre2_posix_lib,
  include_directories: includes,
  compile_args: static_defs)
libpcre2_16 = declare_dependency(link_with: pcre2_16_lib,
  include_directories: includes,
  compile_args: static_defs)
libpcre2_32 = declare_dependency(link_with: pcre2_32_lib,
  include_directories: includes,
  compile_args: static_defs)

if get_option('grep')
  pcre2grep = executable('pcre2grep', ['src/pcre2grep.c'],
    include_directories: includes,
    link_with: [pcre2_8_lib],
    c_args: config_h_defs + ['-DHAVE_CONFIG_H'],
    install: true)
endif

install_headers([pcre2_h, 'src/pcre2posix.h'])

########### pkg-config #############

pkg = import('pkgconfig')

pkg.generate(pcre2_8_lib,
             name : 'libpcre2-8',
             description: 'PCRE2 - Perl compatible regular expressions C library (2nd API) with 8 bit character support',
             version: meson.project_version())

pkg.generate(pcre2_16_lib,
             name : 'libpcre2-16',
             description: 'PCRE2 - Perl compatible regular expressions C library (2nd API) with 16 bit character support',
             version: meson.project_version())

pkg.generate(pcre2_32_lib,
             name : 'libpcre2-32',
             description: 'PCRE2 - Perl compatible regular expressions C library (2nd API) with 32 bit character support',
             version: meson.project_version())


#### tests

if get_option('test') and not meson.is_cross_build() # wine wrappers are not bat-friendly, this would need better testing
  link_args = []
  if c_compiler.get_argument_syntax() == 'msvc'
    link_args += '/STACK:2500000'
  endif

  pcre2test = executable('pcre2test', ['src/pcre2test.c'],
    include_directories: includes,
    link_with: [pcre2_8_lib, pcre2_posix_lib, pcre2_16_lib, pcre2_32_lib],
    c_args: config_h_defs + ['-DHAVE_CONFIG_H'],
    link_args: link_args)

  if c_compiler.get_argument_syntax() == 'msvc'
    runtest = find_program('RunTest.bat')
    rungreptest = find_program('RunGrepTest.bat')
  else
    runtest = find_program('RunTest')
    rungreptest = find_program('RunGrepTest')
  endif

  test('RunTest', runtest,
    should_fail: host_machine.system() == 'windows' and c_compiler.get_argument_syntax() != 'msvc',
    env : ['srcdir=@0@'.format(meson.current_source_dir())],
    workdir: meson.current_build_dir())

  test('RunGrepTest', rungreptest,
    should_fail: host_machine.system() == 'windows',
    env : ['srcdir=@0@'.format(meson.current_source_dir())],
    workdir: meson.current_build_dir())
endif
