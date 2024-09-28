pkgname = "opentally"
pkgver = "0.0.20230611"
_commit = "4cf9053681528d9e3804dfeed38d9093455687f5"
pkgrel = 0
build_style = "cargo"
# We patch out a dependency
prepare_after_patch = True
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
pkgdesc = "Election counting tool for various preferential voting systems"
maintainer = "Jan Christian Grünhage <jan.christian@gruenhage.xyz>"
license = "AGPL-3.0-only"
url = "https://yingtongli.me/opentally"
source = f"https://yingtongli.me/git/OpenTally/archive/{_commit}.tar.gz"
sha256 = "4a07634a61d463808eeafc0b4a68bad8112efb981dcb2981b20053e3c1cab272"
# Checks depend on debug formatting of rug, which we patch out and replace with the pure rust num-bigint
options = ["!check"]


def post_install(self):
    self.install_license("COPYING")
