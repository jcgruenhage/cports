pkgname = "rsop"
pkgver = "0.11.0"
pkgrel = 0
build_wrksrc = "rsop"
build_style = "cargo"
make_build_env = {"CLAP_ARTIFACTS": "clap_artifacts"}
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
pkgdesc = "Stateless OpenPGP CLI tool backed by rpgp"
license = "MIT OR Apache-2.0"
url = "https://codeberg.org/heiko/rsop"
source = f"{url}/archive/rsop/v{pkgver}.tar.gz"
sha256 = "d3fe9a5a8b160cdce3b1f57e158389a16c56fa2347ee2b6ba8dc19de81e4158b"


def post_install(self):
    self.install_completion("clap_artifacts/_rsop", "zsh")
    self.install_completion("clap_artifacts/rsop.bash", "bash")
    self.install_completion("clap_artifacts/rsop.fish", "fish")
    self.install_man("clap_artifacts/*.1", glob=True)
    self.install_license("../LICENSES/MIT.txt")
