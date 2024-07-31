#!/usr/bash

prefix="$1"
gtk_dir="$2"
build_type="$3"
enable_gpl="$4"

declare -a configure_cmd
declare -i idx=0

configure_cmd[idx++]="./configure"
configure_cmd[idx++]="--toolchain=msvc"
configure_cmd[idx++]="--prefix=\"$prefix\""
configure_cmd[idx++]="--enable-shared"
configure_cmd[idx++]="--disable-everything"
configure_cmd[idx++]="--enable-swscale"
configure_cmd[idx++]="--enable-avcodec"
configure_cmd[idx++]="--enable-hwaccel=h264_dxva2"
configure_cmd[idx++]="--enable-hwaccel=hevc_dxva2"
configure_cmd[idx++]="--enable-dxva2"
configure_cmd[idx++]="--enable-decoder=h264"
configure_cmd[idx++]="--enable-decoder=hevc"
configure_cmd[idx++]="--enable-decoder=libdav1d"
configure_cmd[idx++]="--enable-decoder=mpeg1video"
configure_cmd[idx++]="--enable-encoder=mpeg1video"
configure_cmd[idx++]="--enable-hwaccel=h264_d3d11va"
configure_cmd[idx++]="--enable-hwaccel=h264_d3d11va2"
configure_cmd[idx++]="--enable-hwaccel=hevc_d3d11va"
configure_cmd[idx++]="--enable-hwaccel=hevc_d3d11va2"
configure_cmd[idx++]="--enable-libdav1d"
configure_cmd[idx++]="--enable-d3d11va"
configure_cmd[idx++]="--enable-nvdec"
configure_cmd[idx++]="--enable-hwaccel=h264_nvdec"
configure_cmd[idx++]="--enable-hwaccel=hevc_nvdec"
configure_cmd[idx++]="--disable-programs"
configure_cmd[idx++]="--disable-avformat"
configure_cmd[idx++]="--disable-avfilter"
configure_cmd[idx++]="--disable-avdevice"
configure_cmd[idx++]="--disable-swresample"
configure_cmd[idx++]="--disable-postproc"

if [ "$build_type" = "debug" ]; then
    configure_cmd[idx++]="--enable-debug"
    # FIXME: the -Od and -Zi instructions are overriden in the compilation command
    configure_cmd[idx++]="--extra-cflags=-MDd -Od -Zi"
else
    configure_cmd[idx++]="--extra-cflags=-MD"
fi

if [ "$build_type" = "debug-optimized" ]; then
    configure_cmd[idx++]="--extra-ldflags=-DEBUG:FULL"
    configure_cmd[idx++]="--extra-cflags=-Zi"
fi

if [ "$enable_gpl" = "enable_gpl" ]; then
    configure_cmd[idx++]="--enable-libx264"
    configure_cmd[idx++]="--enable-gpl"
    configure_cmd[idx++]="--enable-encoder=libx264"
fi

export PKG_CONFIG_PATH=$gtk_dir/lib/pkgconfig:$PKG_CONFIG_PATH

"${configure_cmd[@]}"

make
make install
