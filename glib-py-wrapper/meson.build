
project('glib-py-warpper', 'c')
glib = dependency('glib-2.0')

executable('glib-genmarshal', 'glib-py-wrapper.c', dependencies : glib, install : true)
executable('glib-mkenums', 'glib-py-wrapper.c', dependencies : glib, install : true)

install_data('glib-genmarshal.config', install_dir : get_option('bindir'))
install_data('glib-mkenums.config', install_dir : get_option('bindir'))
