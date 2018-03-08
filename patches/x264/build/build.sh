prefix=$1
build_type=$2

extra_flags=""
extra_cflags="-DNO_PREFIX"

if [ "$build_type" = "debug" ]; then
    extra_flags="--enable-debug $extra_flags"
    extra_cflags="-MDd -Od -Zi $extra_cflags"
fi

CC=cl ./configure --enable-shared --prefix="$prefix" $extra_flags --extra-cflags="$extra_cflags"
make install
