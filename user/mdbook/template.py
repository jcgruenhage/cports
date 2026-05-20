pkgname = "mdbook"
pkgver = "0.5.4"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
pkgdesc = "Utility to create online books from markdown files"
license = "MPL-2.0"
url = "https://rust-lang.github.io/mdBook"
source = (
    f"https://github.com/rust-lang/mdBook/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "107614330c35c77d53b6f6ce7826c50eed087650efe5646a4d0a16ca6bf5544b"
# Generates completions using host binary
options = ["!cross"]


def post_build(self):
    for shell in ["bash", "fish", "zsh"]:
        with open(self.cwd / f"mdbook.{shell}", "w") as outf:
            self.do(
                f"target/{self.profile().triplet}/release/mdbook",
                "completions",
                shell,
                stdout=outf,
            )


def post_install(self):
    for shell in ["bash", "fish", "zsh"]:
        self.install_completion(f"mdbook.{shell}", shell)
