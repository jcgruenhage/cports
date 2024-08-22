pkgname = "usbutils"
pkgver = "017"
pkgrel = 2
build_style = "gnu_configure"
hostmakedepends = ["automake", "libtool", "pkgconf"]
makedepends = ["udev-devel", "libusb-devel", "linux-headers"]
depends = ["hwdata-usb"]
pkgdesc = "Linux USB utilities"
maintainer = "q66 <q66@chimera-linux.org>"
license = "GPL-2.0-only"
url = "http://linux-usb.sourceforge.net"
source = f"$(KERNEL_SITE)/utils/usb/usbutils/usbutils-{pkgver}.tar.xz"
sha256 = "a6a25ffdcf9103e38d7a44732aca17073f4e602b92e4ae55625231a82702e05b"
hardening = ["vis", "cfi"]


def post_install(self):
    self.uninstall("usr/bin/lsusb.py")


@subpackage("usbutils-devel")
def _(self):
    self.depends = [self.parent]
    return self.default_devel()
