// test for libsigc++

// include
    #include <sigc++/sigc++.h>

int main(int argc, char * argv[])
{

    sigc::signal<void, const std::string &> m_slot;

    m_slot.emit("Check sigc++ ...");
    return 0;

}
