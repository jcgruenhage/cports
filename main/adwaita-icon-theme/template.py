pkgname = "adwaita-icon-theme"
pkgver = "47.0"
pkgrel = 0
build_style = "meson"
hostmakedepends = ["meson", "pkgconf"]
depends = ["hicolor-icon-theme"]
pkgdesc = "Icon theme for GTK+"
maintainer = "q66 <q66@chimera-linux.org>"
license = "LGPL-3.0-or-later OR CC-BY-SA-3.0"
url = "https://gitlab.gnome.org/GNOME/adwaita-icon-theme"
source = f"$(GNOME_SITE)/adwaita-icon-theme/{pkgver[:-2]}/adwaita-icon-theme-{pkgver}.tar.xz"
sha256 = "ad088a22958cb8469e41d9f1bba0efb27e586a2102213cd89cc26db2e002bdfe"
