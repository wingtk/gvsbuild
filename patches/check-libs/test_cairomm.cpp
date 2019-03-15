// test for cairomm

// include
    #include <cairommconfig.h>
    #include <cairomm/cairomm.h>

// code
int main(int argc, char * argv[])
{

    auto surface = Cairo::ImageSurface::create(Cairo::FORMAT_ARGB32, 256, 256);
    return 0;

}

