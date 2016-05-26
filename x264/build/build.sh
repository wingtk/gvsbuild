CC=cl ./configure --enable-static --enable-shared --prefix="$1" --extra-cflags="-DNO_PREFIX"
make install
