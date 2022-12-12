project(
  'libxml2',
  'c',
  version: '2.10.3',
  meson_version: '>=0.54.0',
  license: 'MIT',
)

add_project_arguments('-D_GNU_SOURCE', language: 'c')

cdata = configuration_data()

cdata.set('PACKAGE', meson.project_name())
cdata.set('PACKAGE_NAME', meson.project_name())
cdata.set('PACKAGE_TARNAME', meson.project_name())
cdata.set('PACKAGE_STRING', '@0@ @1@'.format(meson.project_name(), meson.project_version()))
cdata.set('PACKAGE_URL', 'https://gitlab.gnome.org/GNOME/libxml2')
cdata.set('PACKAGE_BUGREPORT', 'xml@gnome.org')
cdata.set('PACKAGE_VERSION', meson.project_version())
cdata.set('VERSION', meson.project_version())

cc = meson.get_compiler('c')

cdata.set('SUPPORT_IP6', cc.has_header_symbol('sys/socket.h', 'AF_INET6'))
cdata.set('XML_SOCKLEN_T', 'socklen_t')
cdata.set('SEND_ARG2_CAST', '')
cdata.set('GETHOSTBYNAME_ARG_CAST', '')

if cc.has_function_attribute('destructor')
  cdata.set('ATTRIBUTE_DESTRUCTOR', '__attribute__((destructor))')
endif

checked_headers = [
  'arpa/inet.h',
  'dl.h',
  'dlfcn.h',
  'fcntl.h',
  'float.h',
  'inttypes.h',
  'netdb.h',
  'netinet/in.h',
  'poll.h',
  'pthread.h',
  'stdint.h',
  'sys/mman.h',
  'sys/select.h',
  'sys/socket.h',
  'sys/stat.h',
  'sys/time.h',
  'sys/timeb.h',
  'unistd.h',
  'zlib.h',
]

foreach h : checked_headers
  cdata.set('HAVE_@0@'.format(h.underscorify().to_upper()), cc.has_header(h))
endforeach

checked_funcs = [
  'ftime',
  'gettimeofday',
  'isascii',
  'mmap',
  'munmap',
  'putenv',
  'rand_r',
  'stat',
  'va_copy',
  '__va_copy',
]

foreach f : checked_funcs
  cdata.set('HAVE_@0@'.format(f.underscorify().to_upper()), cc.has_function(f))
endforeach

if meson.version().version_compare('>= 0.62')
  dl_lib = dependency('dl', required: false)
else
  dl_lib = cc.find_library('dl', required: false)
endif
cdata.set('HAVE_DLOPEN', cc.has_function('dlopen', dependencies: dl_lib))

math_lib = cc.find_library('m', required: false)

if meson.version().version_compare('>= 0.60')
  iconv_lib = dependency('iconv', required: false)
else
  iconv_lib = dependency('', required: false)
endif

thread_dep = dependency('threads', required: false)

lzma_dep = dependency('liblzma', required: false)
cdata.set('HAVE_LIBLZMA', lzma_dep.found())

zlib_dep = dependency('zlib', required: false)
cdata.set('HAVE_LIBZ', zlib_dep.found())

readline_lib = cc.find_library('readline', required: false)
cdata.set('HAVE_LIBREADLINE', readline_lib.found())

history_lib = cc.find_library('history', required: false)
cdata.set('HAVE_LIBHISTORY', history_lib.found())

deps = [math_lib, iconv_lib, dl_lib, lzma_dep, thread_dep, zlib_dep, readline_lib, history_lib]

if target_machine.system() == 'windows'
  deps += cc.find_library('ws2_32')
endif

configure_file(
  input: 'config.h.cmake.in',
  output: 'config.h',
  format: 'cmake@',
  configuration: cdata,
)

withcdata = configuration_data()
withcdata.set10('HAVE_LIBLZMA', lzma_dep.found())
version = meson.project_version()
version_array = version.split('.')
major = version_array[0].to_int()
minor = version_array[1].to_int()
micro = version_array[2].to_int()
version_number = major * 10000 + minor * 100 + micro
withcdata.set('VERSION', version)
withcdata.set('LIBXML_VERSION_NUMBER', version_number)
withcdata.set('LIBXML_VERSION_STRING', '@0@'.format(version_number))
withcdata.set('LIBXML_VERSION_EXTRA', '')

need_trio = false
foreach f : ['printf', 'sprintf', 'fprintf', 'snprintf', 'vfprintf', 'vsprintf', 'vsnprintf', 'sscanf']
  if not cc.has_function(f, prefix: '#include <stdio.h>')
    need_trio = true
    break
  endif
endforeach
withcdata.set10('WITH_TRIO', need_trio)

withcdata.set10('WITH_THREADS', thread_dep.found())
withcdata.set10('WITH_THREAD_ALLOC', false)
withcdata.set10('WITH_TREE', true)
withcdata.set10('WITH_OUTPUT', true)
withcdata.set10('WITH_PUSH', true)
withcdata.set10('WITH_READER', true)
withcdata.set10('WITH_PATTERN', true)
withcdata.set10('WITH_WRITER', true)
withcdata.set10('WITH_SAX1', true)
withcdata.set10('WITH_FTP', true)
withcdata.set10('WITH_HTTP', true)
withcdata.set10('WITH_VALID', true)
withcdata.set10('WITH_HTML', true)
withcdata.set10('WITH_LEGACY', true)
withcdata.set10('WITH_C14N', true)
withcdata.set10('WITH_CATALOG', true)
withcdata.set10('WITH_DOCB', true)
withcdata.set10('WITH_XPATH', true)
withcdata.set10('WITH_XPTR', true)
withcdata.set10('WITH_XPTR_LOCS', false)
withcdata.set10('WITH_XINCLUDE', true)
withcdata.set10('WITH_ICONV', iconv_lib.found())
withcdata.set10('WITH_ICU', false)
withcdata.set10('WITH_ISO8859X', true)
withcdata.set10('WITH_DEBUG', true)
withcdata.set10('WITH_MEM_DEBUG', false)
withcdata.set10('WITH_RUN_DEBUG', false)
withcdata.set10('WITH_REGEXPS', true)
withcdata.set10('WITH_SCHEMAS', true)
withcdata.set10('WITH_SCHEMATRON', true)
withcdata.set10('WITH_MODULES', dl_lib.found())

system = target_machine.system()
if system == 'cygwin'
  module_ext = '.cygdll'
elif system == 'darwin'
  module_ext = '.bundle'
elif system == 'windows'
  module_ext = '.dll'
else
  module_ext = '.so'
endif

withcdata.set('MODULE_EXTENSION', module_ext)

withcdata.set10('WITH_ZLIB', zlib_dep.found())
withcdata.set10('WITH_LZMA', lzma_dep.found())

subdir('include/libxml')

sources = files(
  'HTMLparser.c',
  'HTMLtree.c',
  'SAX.c',
  'SAX2.c',
  'buf.c',
  'c14n.c',
  'catalog.c',
  'chvalid.c',
  'debugXML.c',
  'dict.c',
  'encoding.c',
  'entities.c',
  'error.c',
  'globals.c',
  'hash.c',
  'legacy.c',
  'list.c',
  'nanoftp.c',
  'nanohttp.c',
  'parser.c',
  'parserInternals.c',
  'pattern.c',
  'relaxng.c',
  'schematron.c',
  'threads.c',
  'tree.c',
  'uri.c',
  'valid.c',
  'xinclude.c',
  'xlink.c',
  'xmlIO.c',
  'xmlmemory.c',
  'xmlmodule.c',
  'xmlreader.c',
  'xmlregexp.c',
  'xmlsave.c',
  'xmlschemas.c',
  'xmlschemastypes.c',
  'xmlstring.c',
  'xmlunicode.c',
  'xmlwriter.c',
  'xpath.c',
  'xpointer.c',
  'xzlib.c',
)

if need_trio
  sources += files('trio.c', 'trionan.c', 'triostr.c')
endif

cargs = thread_dep.found() ? ['-D_REENTRANT'] : []
cargs += get_option('default_library') == 'static' ? '-DLIBXML_STATIC' : []

incdir = include_directories('include')
xml2lib = library(
  'libxml2',
  sources,
  c_args: cargs,
  include_directories: incdir,
  dependencies: deps,
  install: true,
)

libxml2_dep = declare_dependency(
  link_with: xml2lib,
  include_directories: incdir,
  dependencies: deps,
  variables: {'modules': withcdata.get('WITH_MODULES').to_string()},
  compile_args: get_option('default_library') == 'static' ? '-DLIBXML_STATIC' : [],
)

pkg = import('pkgconfig')
pkg.generate(
  xml2lib,
  name: 'libXML',
  description: 'libXML library version2.',
  filebase: 'libxml-2.0',
  subdirs: 'libxml2',
  variables: ['modules=@0@'.format(withcdata.get('WITH_MODULES'))],
  extra_cflags: get_option('default_library') == 'static' ? '-DLIBXML_STATIC' : [],
)

executable('xmllint', 'xmllint.c', dependencies: libxml2_dep, install: true)

dictexe = executable('testdict', 'testdict.c', dependencies: libxml2_dep)

test('dict', dictexe)
