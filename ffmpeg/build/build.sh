prefix="$1"
gtk_dir="$2"
export PKG_CONFIG_PATH=$gtk_dir/lib/pkgconfig:$PKG_CONFIG_PATH

./configure \
    --toolchain=msvc \
    --prefix="$prefix" \
    --enable-shared \
    --disable-everything \
    --enable-swscale \
    --enable-avcodec \
    --enable-decoder=h264 \
    --enable-libx264 \
    --enable-gpl \
    --enable-encoder="libx264" \
    --disable-programs \
    --disable-avformat \
    --disable-avfilter \
    --disable-avdevice \
    --disable-swresample \

make
make install
