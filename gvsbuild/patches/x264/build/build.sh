#!/bin/bash

prefix="$1"
build_type="$2"

declare -a configure_cmd
declare -i idx=0

configure_cmd[idx++]="./configure"
configure_cmd[idx++]="--prefix=\"$prefix\""
configure_cmd[idx++]="--enable-shared"
configure_cmd[idx++]="--extra-cflags=-DNO_PREFIX"

if [ "$build_type" = "debug" ]; then
    configure_cmd[idx++]="--enable-debug"
    configure_cmd[idx++]="--extra-cflags=-MDd -Od -Zi"
fi

if [ "$build_type" = "debug-optimized" ]; then
    configure_cmd[idx++]="--extra-ldflags=-DEBUG:FULL"
fi

CC=cl "${configure_cmd[@]}"

make
make install
