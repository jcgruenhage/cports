pkgname = "gnome-shell-extensions"
pkgver = "45.1"
pkgrel = 0
build_style = "meson"
hostmakedepends = ["meson", "pkgconf", "gettext", "glib-devel"]
depends = [f"gnome-shell~{pkgver[:-2]}", "nautilus", "gnome-menus"]
pkgdesc = "Optional extensions for GNOME shell"
maintainer = "q66 <q66@chimera-linux.org>"
license = "GPL-2.0-or-later"
url = "https://wiki.gnome.org/Projects/GnomeShell/Extensions"
source = f"$(GNOME_SITE)/{pkgname}/{pkgver[:-2]}/{pkgname}-{pkgver}.tar.xz"
sha256 = "242e15a0c06e820c3fd8dd6aeac1a8ef865ce58882e5975af1d65934bb4d4261"
