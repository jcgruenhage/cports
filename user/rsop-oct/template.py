pkgname = "rsop-oct"
pkgver = "0.1.9"
pkgrel = 0
build_wrksrc = "rsop-oct"
build_style = "cargo"
hostmakedepends = ["cargo-auditable", "pkgconf"]
makedepends = ["rust-std", "dbus-devel", "pcsc-lite-devel"]
pkgdesc = "Stateless OpenPGP CLI tool backed by rpgp and OpenPGP smartcards"
license = "MIT OR Apache-2.0"
url = "https://codeberg.org/heiko/rsop"
source = f"{url}/archive/rsop-oct/v{pkgver}.tar.gz"
sha256 = "28681404d75b3ca59810074d9b7091202ac268c5e2d08fadf54c2d5f99c6280c"


def post_install(self):
    self.install_license("../LICENSES/MIT.txt")
