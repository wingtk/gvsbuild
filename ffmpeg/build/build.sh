./configure \
    --toolchain=msvc \
    --prefix="$1" \
    --enable-shared \
    --disable-everything \
    --enable-swscale \
    --enable-avcodec \
    --enable-decoder=h264 \
    --disable-programs \
    --disable-avformat \
    --disable-avfilter \
    --disable-avdevice \
    --disable-swresample \

make
make install
