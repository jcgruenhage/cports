pkgname = "rpiboot"
pkgver = "0_git20260605"
pkgrel = 0
_gitrev = "87d6e03272b0ae155d85a125bfdec03e3d4a1095"
build_style = "makefile"
hostmakedepends = ["pkgconf"]
makedepends = ["libusb-devel"]
pkgdesc = "Raspberry Pi USB device provisioning tool"
license = "Apache-2.0"
url = "https://github.com/raspberrypi/usbboot"
source = f"{url}/archive/{_gitrev}.tar.gz"
sha256 = "a8df35af583d3b1b550d63397e7b4872481b6e93b70638a186f2d349b52edbc8"
hardening = ["vis", "cfi"]
# no test suite
options = ["!check"]


def init_configure(self):
    self.make_build_args += [
        "CC_FOR_BUILD=" + self.get_tool("CC", target="host"),
    ]


def post_install(self):
    # bootcode.bin/start.elf/bootcode4.bin are compiled into the rpiboot
    # binary itself (via msd/*.h); the installed copies are unused
    self.uninstall("usr/share/rpiboot/msd")
    self.install_license("LICENSE")
