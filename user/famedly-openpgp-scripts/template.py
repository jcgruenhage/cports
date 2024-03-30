pkgname = "famedly-openpgp-scripts"
pkgver = "20240702"
pkgrel = 0
_commit = "2d4d9645ef19732dbc175c7a707434e3cbe54b88"
depends = [
    "bash",
    "chimerautils",
    "jq",
    "openpgp-ca",
    "openpgp-card-tools",
    "rusty-diceware",
    "sequoia-sq",
]
pkgdesc = "Famedly OpenPGP scripts"
maintainer = "Jan Christian Grünhage <jan.christian@gruenhage.xyz>"
license = "AGPL-3.0-or-later"
url = "https://github.com/famedly/openpgp-scripts"
source = f"{url}/archive/{_commit}.tar.gz"
sha256 = "05c60d53c1e3c1d22836cce9253a0b2575ec2c2e5c4625db20c3f9941606585d"


def do_install(self):
    for bin in [
        "fos-export",
        "fos-mount",
        "fos-new",
        "fos-partitions",
        "fos-sync",
        "fos-working-directory",
    ]:
        self.install_bin(bin)

    self.install_license("LICENSE")
