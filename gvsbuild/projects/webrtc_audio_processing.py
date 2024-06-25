from gvsbuild.utils.base_builders import Meson
from gvsbuild.utils.base_expanders import Tarball
from gvsbuild.utils.base_project import Project, project_add


@project_add
class WebrtcAudioProcessing(Tarball, Meson):
    def __init__(self):
        Project.__init__(
            self,
            "webrtc-audio-processing",
            repository="https://gitlab.freedesktop.org/pulseaudio/webrtc-audio-processing/",
            version="1.3",
            archive_url="https://freedesktop.org/software/pulseaudio/webrtc-audio-processing/webrtc-audio-processing-{version}.tar.gz",
            hash="95552fc17faa0202133707bbb3727e8c2cf64d4266fe31bfdb2298d769c1db75",
            dependencies=["meson", "ninja"],
        )

    def build(self):
        Meson.build(self)
        self.install(r".\COPYING share\doc\webrtc-audio-processing")
        self.install(
            r".\webrtc\LICENSE .\webrtc\PATENTS share\doc\webrtc-audio-processing\webrtc"
        )
