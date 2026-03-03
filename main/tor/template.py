pkgname = "tor"
pkgver = "0.4.9.8"
pkgrel = 0
build_style = "gnu_configure"
configure_args = [
    "--enable-pic",
]
hostmakedepends = [
    "autoconf",
    "automake",
    "libtool",
    "pkgconf",
]

makedepends = [
    "libevent-devel",
    "openssl3-devel",
    "zlib-ng-compat-devel",
    "xz-devel",
]

depends = [
    "libevent",
    "openssl3",
    "zlib-ng-compat",
]
options = ["!check"]
pkgdesc = "Anonymizing overlay network"
license = "BSD-3-Clause"
url = "https://www.torproject.org"
source = f"https://dist.torproject.org/tor-{pkgver}.tar.gz"
sha256 = "ac1f394e2dd2ab0877d27d928fd0d9e86662fe3ca6afdffb9fd9b6f0f96d05de"


def install(self):
    self.make.invoke(["install"], env={"DESTDIR": str(self.chroot_destdir)})
    self.install_license("LICENSE")
