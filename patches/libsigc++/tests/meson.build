tests = [
##    'benchmark',
    'test_accumulated',
    'test_accum_iter',
    'test_bind',
    'test_bind_as_slot',
    'test_bind_ref',
    'test_bind_refptr',
    'test_bind_return',
    'test_compose',
    'test_copy_invalid_slot',
    'test_cpp11_lambda',
    'test_custom',
    'test_deduce_result_type',
    'test_disconnect',
    'test_disconnect_during_emit',
    'test_exception_catch',
    'test_functor_trait',
    'test_hide',
    'test_limit_reference',
    'test_mem_fun',
    'test_ptr_fun',
    'test_retype',
    'test_retype_return',
    'test_signal',
    'test_signal_move',
    'test_size',
    'test_slot',
    'test_slot_disconnect',
    'test_slot_move',
    'test_trackable',
    'test_trackable_move',
    'test_track_obj',
    'test_visit_each',
]

cenv = environment()
# To let the test use the new dll we build ...
cenv.prepend('PATH', join_paths(meson.build_root(), 'sigc++'))

foreach t: tests
  bin = executable(t,
                   sources: [ t + '.cc',
                              'testutilities.cc',
                            ],
                   dependencies: libsigc_dep,
                   include_directories: root_inc,
                   link_args: common_ldflags,
                   cpp_args: common_cflags + [
                     '-DG_DISABLE_DEPRECATED',
                   ])
  test(t, bin, env: cenv)
endforeach
