#!/bin/sh
# install the Limine bootloader
#
# usage: install-limine [DISK]
#
# On EFI systems it deploys the payload to the ESP and registers a firmware boot
# entry. On x86 BIOS systems, pass the whole target disk to deploy the BIOS
# stage to it.

LIMINE_CFG=/etc/default/limine
# overridable defaults
LIMINE_ESP_PATH=
LIMINE_LABEL="Limine"
# if set, install to the removable EFI/BOOT path and register no firmware entry
LIMINE_REMOVABLE=

[ -r "$LIMINE_CFG" ] && . "$LIMINE_CFG"

DISK=$1

# the EFI payload that matches this machine
case "$(uname -m)" in
    x86_64) EFI_NAME="BOOTX64.EFI" ;;
    aarch64) EFI_NAME="BOOTAA64.EFI" ;;
    riscv64) EFI_NAME="BOOTRISCV64.EFI" ;;
    loongarch64) EFI_NAME="BOOTLOONGARCH64.EFI" ;;
    i?86) EFI_NAME="BOOTIA32.EFI" ;;
    *) EFI_NAME= ;;
esac

# register a firmware boot entry for the deployed payload; returns nonzero if it
# could not be done (caller then falls back to the removable path)
register_nvram() {
    if [ ! -d /sys/firmware/efi ]; then
        echo "Not booted via EFI; cannot register a firmware entry." >&2
        return 1
    fi
    if ! command -v efibootmgr >/dev/null 2>&1; then
        echo "efibootmgr not found; cannot register a firmware entry." >&2
        return 1
    fi
    # esp-disk-part prints "DISK PARTNO" for efibootmgr -d/-p
    set -- $(/usr/lib/efibootmgr/esp-disk-part "$ESP")
    ESPDISK=$1
    PNUM=$2
    if [ -z "$ESPDISK" ] || [ -z "$PNUM" ]; then
        echo "Could not determine the ESP disk and partition number." >&2
        return 1
    fi
    # drop stale entries with the same label; efibootmgr prints
    # "Boot0001* Label<TAB>loader-path", so cut the label field at the tab
    efibootmgr 2>/dev/null | cut -f1 | while IFS= read -r LINE; do
        case "$LINE" in
            Boot[0-9A-F][0-9A-F][0-9A-F][0-9A-F]*) ;;
            *) continue ;;
        esac
        NUM=${LINE#Boot}
        NUM=${NUM%%[!0-9A-F]*}
        REST=${LINE#Boot????}
        REST=${REST#\*}
        REST=${REST# }
        [ "$REST" = "$LIMINE_LABEL" ] && efibootmgr -Bq -b "$NUM"
    done
    efibootmgr -qc -d "$ESPDISK" -p "$PNUM" \
        -L "$LIMINE_LABEL" -l "\\EFI\\limine\\$EFI_NAME"
}

install_efi() {
    [ -n "$EFI_NAME" ] && [ -r "/usr/share/limine/$EFI_NAME" ] || return 1

    ESP="$LIMINE_ESP_PATH"
    if [ -z "$ESP" ]; then
        if /usr/lib/base-kernel/esp-validate /boot/efi; then
            ESP=/boot/efi
        elif /usr/lib/base-kernel/esp-validate /boot; then
            ESP=/boot
        fi
    fi
    # no ESP: skip EFI install (e.g. BIOS-only system) and let BIOS handle it
    [ -z "$ESP" ] && return 1

    echo "Installing Limine EFI payload to $ESP..."
    # the vendor directory doubles as the marker the kernel hook looks for
    mkdir -p "$ESP/EFI/limine"
    cp "/usr/share/limine/$EFI_NAME" "$ESP/EFI/limine/$EFI_NAME"

    # register a firmware entry unless removable-only was requested, falling back
    # to the removable EFI/BOOT path if the firmware entry could not be written
    if [ -z "$LIMINE_REMOVABLE" ]; then
        register_nvram || LIMINE_REMOVABLE=1
    fi
    if [ -n "$LIMINE_REMOVABLE" ]; then
        mkdir -p "$ESP/EFI/BOOT"
        cp "/usr/share/limine/$EFI_NAME" "$ESP/EFI/BOOT/$EFI_NAME"
    fi
    return 0
}

install_bios() {
    [ -n "$DISK" ] || return 1
    if [ ! -r /usr/share/limine/limine-bios.sys ] \
        || ! command -v limine >/dev/null 2>&1; then
        echo "ERROR: limine BIOS support is not available on this system." >&2
        exit 1
    fi
    if [ ! -b "$DISK" ]; then
        echo "ERROR: '$DISK' is not a block device (pass the whole disk)." >&2
        exit 1
    fi
    echo "Installing Limine BIOS stage to $DISK..."
    # limine-bios.sys is read from the boot volume next to limine.conf
    cp /usr/share/limine/limine-bios.sys /boot/
    limine bios-install "$DISK"
}

DID=
install_efi && DID=1
install_bios && DID=1

if [ -z "$DID" ]; then
    echo "ERROR: nothing to install." >&2
    echo "On EFI, ensure the ESP is mounted; on x86 BIOS, pass the disk." >&2
    exit 1
fi

echo "Limine installed. Reconfigure your kernel to generate the config," \
     "e.g. 'apk fix linux-lts' (or install/update a kernel)."

exit 0
