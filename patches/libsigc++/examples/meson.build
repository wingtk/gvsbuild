examples_sources = [
    'hello_world',
    'member_method',
]

foreach t: examples_sources
  c_example = executable(t,
                         sources: t + '.cc',
                         dependencies: libsigc_dep,
                         include_directories: root_inc,
                         link_args: common_ldflags,
                         cpp_args: common_cflags + [
                                '-DG_DISABLE_DEPRECATED',
                         ])
endforeach
