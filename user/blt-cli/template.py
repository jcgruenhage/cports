pkgname = "blt-cli"
pkgver = "0.1.0"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
pkgdesc = "CLI for transferring paper ballots into a blt file"
maintainer = "Jan Christian Grünhage <jan.christian@gruenhage.xyz>"
license = "AGPL-3.0-only"
url = "https://git.jcg.re/jcgruenhage/blt-cli"
source = f"{url}/archive/v{pkgver}.tar.gz"
sha256 = "18350d6f647f88a64774ecb065d794685751c07fac8574a014524964cab59d22"


def post_build(self):
    self.do(
        f"target/{self.profile().triplet}/release/blt-cli",
        env={"BLT_CLI_GENERATE": "generated"},
    )


def post_install(self):
    self.install_license("LICENSE.md")
    self.install_man("generated/man/*.1", glob=True)
    with self.pushd("generated/completions"):
        self.install_completion("blt-cli.bash", "bash")
        self.install_completion("blt-cli.fish", "fish")
        self.install_completion("_blt-cli", "zsh")
        self.install_completion("blt-cli.nu", "nushell")
