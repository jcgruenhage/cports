pkgname = "zizmor"
pkgver = "1.26.1"
pkgrel = 0
build_style = "cargo"
prepare_after_patch = True
make_check_args = [
    "--",
    # asserted output assumes a git checkout, run from extracted tarball fails
    "--skip=issue_1745",
]
hostmakedepends = ["cargo-auditable"]
makedepends = ["rust-std"]
pkgdesc = "Static analysis for GitHub Actions"
license = "MIT"
url = "https://docs.zizmor.sh"
source = (
    f"https://github.com/zizmorcore/zizmor/archive/refs/tags/v{pkgver}.tar.gz"
)
sha256 = "ec5540b3bd6d347df61dcd24ecd2eaffd3181808f4dafc59a9c889e26b075eb8"
# Generates completions using host binaries
options = ["!cross"]


def post_build(self):
    for shell in ["bash", "fish", "zsh", "nushell"]:
        with open(self.cwd / f"zizmor.{shell}", "w") as f:
            self.do(
                f"./target/{self.profile().triplet}/release/zizmor",
                "--completions",
                shell,
                stdout=f,
            )


def install(self):
    self.install_bin(f"./target/{self.profile().triplet}/release/zizmor")
    for shell in ["bash", "fish", "zsh", "nushell"]:
        self.install_completion(f"zizmor.{shell}", shell)
    self.install_license("LICENSE")
