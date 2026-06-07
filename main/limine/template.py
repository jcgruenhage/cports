pkgname = "limine"
pkgver = "12.3.3"
pkgrel = 1
# these targets implemented
archs = ["aarch64", "loongarch64", "riscv64", "x86_64"]
build_style = "gnu_configure"
configure_args = ["--enable-all"]
hostmakedepends = ["automake", "mtools", "nasm"]
depends = ["base-kernel", "efibootmgr"]
pkgdesc = "Multiprotocol EFI bootloader"
license = "BSD-2-Clause AND 0BSD"
url = "https://limine-bootloader.org"
source = f"https://github.com/Limine-Bootloader/Limine/releases/download/v{pkgver}/limine-{pkgver}.tar.gz"
sha256 = "f1a529da5cd50a5ca37ba5873133a7b8e72584b127d7331fe94e554e5e6012f7"
# no test suite
options = ["!check"]


def post_install(self):
    self.uninstall(f"usr/share/doc/{pkgname}/COPYING")
    self.install_license("COPYING")
    # config generator
    self.install_bin(self.files_path / "gen-limine.sh", name="gen-limine")
    # installer
    self.install_bin(
        self.files_path / "install-limine.sh", name="install-limine"
    )
    # conf file
    self.install_file(self.files_path / "limine", "usr/lib/limine")
    # kernel hook
    self.install_file(
        self.files_path / "99-gen-limine.sh", "usr/lib/kernel.d", mode=0o755
    )
