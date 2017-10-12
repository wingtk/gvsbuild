prefix="$1"
gtk_dir="$2"
build_type="$3"

extra_cflags=""
extra_flags=""

if [ "$build_type" = "debug" ]; then
    extra_flags="--enable-debug $extra_flags"
    # FIXME: the -Od and -Zi instructions are overriden in the compilation command
    extra_cflags="-Od -Zi -MDd $extra_cflags"
fi

export PKG_CONFIG_PATH=$gtk_dir/lib/pkgconfig:$PKG_CONFIG_PATH

./configure \
    --toolchain=msvc \
    --prefix="$prefix" \
    --enable-shared \
    --disable-everything \
    --enable-swscale \
    --enable-avcodec \
    --enable-decoder=h264 \
    --enable-decoder=mpeg1video \
    --enable-encoder=mpeg1video \
    --enable-libx264 \
    --enable-gpl \
    --enable-encoder="libx264" \
    --disable-programs \
    --disable-avformat \
    --disable-avfilter \
    --disable-avdevice \
    --disable-swresample \
    --extra-cflags="$extra_cflags" \
    $extra_flags

make
make install
