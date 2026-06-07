#!/bin/sh

[ -r /etc/os-release ] && . /etc/os-release

LIMINE_SYSTEM_CFG=/usr/lib/limine/limine
LIMINE_CFG=/etc/default/limine
# overridable defaults
LIMINE_SYSTEM_CMDLINE_FILE=/usr/lib/limine/cmdline
LIMINE_SYSTEM_DEVICETREE_FILE=/usr/lib/limine/devicetree
LIMINE_CMDLINE_FILE=/etc/default/limine-cmdline
LIMINE_DEVICETREE_FILE=/etc/default/limine-devicetree
LIMINE_OS_TITLE="$PRETTY_NAME"
LIMINE_TIMEOUT=5
LIMINE_SERIAL=
LIMINE_CONFIG_PATH=
LIMINE_ESP_PATH=
LIMINE_CMDLINE=
LIMINE_CMDLINE_DEFAULT="quiet splash"
LIMINE_DEVICETREE=
LIMINE_DISABLE_DEVICETREE=
LIMINE_DISABLE_RECOVERY=

[ -z "$LIMINE_OS_TITLE" ] && LIMINE_OS_TITLE="Chimera Linux"

# source global config, then user override
[ -r "$LIMINE_SYSTEM_CFG" ] && . "$LIMINE_SYSTEM_CFG"
[ -r "$LIMINE_CFG" ] && . "$LIMINE_CFG"

# disabled?
[ -z "$1" ] && [ -n "$LIMINE_DISABLE_KERNEL_HOOK" ] && exit 0

# where limine reads its config; detect the ESP unless told otherwise
if [ -z "$LIMINE_CONFIG_PATH" ]; then
    if [ -z "$LIMINE_ESP_PATH" ]; then
        if /usr/lib/base-kernel/esp-validate /boot/efi; then
            LIMINE_ESP_PATH=/boot/efi
        elif /usr/lib/base-kernel/esp-validate /boot; then
            LIMINE_ESP_PATH=/boot
        fi
    fi
    # not installed?
    if [ -z "$1" ]; then
        if [ -n "$LIMINE_ESP_PATH" ]; then
            [ -d "${LIMINE_ESP_PATH}/EFI/limine" ] || exit 0
        else
            [ -f /boot/limine-bios.sys ] || exit 0
        fi
    fi
    if [ -n "$LIMINE_ESP_PATH" ]; then
        LIMINE_CONFIG_PATH="${LIMINE_ESP_PATH}/limine.conf"
    else
        # no ESP (e.g. BIOS): config lives on the boot volume
        LIMINE_CONFIG_PATH="/boot/limine.conf"
    fi
fi

# address the kernel volume by GPT PARTUUID, boot() for non-GPT disks
KMP=$(findmnt -no TARGET --target /boot 2>/dev/null)
KMP=${KMP:-/}
KPARTUUID=$(findmnt -no PARTUUID --target /boot 2>/dev/null)
if [ -n "$KPARTUUID" ]; then
    KVOL="uuid(${KPARTUUID})"
else
    KVOL="boot()"
fi

# first argument overrides the output ("-" means stdout)
[ -n "$1" ] && LIMINE_CONFIG_PATH="$1"

# strip the mountpoint prefix to get a path relative to that volume
vol_path() {
    case "$KMP" in
        /) echo "$1" ;;
        *) echo "${1#"$KMP"}" ;;
    esac
}

DEV_CMDLINE=$LIMINE_CMDLINE
DEV_CMDLINE_DEFAULT=$LIMINE_CMDLINE_DEFAULT
DEV_EXTRA_CMDLINE=
DEV_DEVICETREE=$LIMINE_DEVICETREE
export DEV_CMDLINE DEV_CMDLINE_DEFAULT DEV_EXTRA_CMDLINE

if [ -r "$LIMINE_CMDLINE_FILE" ]; then
    DEV_EXTRA_CMDLINE=$(cat "$LIMINE_CMDLINE_FILE")
elif [ -r "$LIMINE_SYSTEM_CMDLINE_FILE" ]; then
    DEV_EXTRA_CMDLINE=$(cat "$LIMINE_SYSTEM_CMDLINE_FILE")
fi

if [ -z "$DEV_DEVICETREE" ]; then
    if [ -r "$LIMINE_DEVICETREE_FILE" ]; then
        DEV_DEVICETREE=$(cat "$LIMINE_DEVICETREE_FILE")
    elif [ -r "$LIMINE_SYSTEM_DEVICETREE_FILE" ]; then
        DEV_DEVICETREE=$(cat "$LIMINE_SYSTEM_DEVICETREE_FILE")
    fi
fi

COUT=$(mktemp)

write_cfg() {
    echo "$@" >> "$COUT"
}

write_dtb() {
    [ -n "$LIMINE_DISABLE_DEVICETREE" ] && return 0
    case "$2" in
        '') ;;
        /*) write_cfg "    dtb_path: ${KVOL}:$(vol_path "$2")" ;;
        *)  write_cfg "    dtb_path: ${KVOL}:$(vol_path "/boot/dtbs/dtbs-$1/$2")" ;;
    esac
}

CMDLINE_MULTI=$(/usr/lib/base-kernel/kernel-cmdline 1)
CMDLINE_SINGLE=$(/usr/lib/base-kernel/kernel-cmdline)

write_entry() {
    write_cfg ""
    write_cfg "/${LIMINE_OS_TITLE} (${1})"
    write_cfg "    protocol: linux"
    write_cfg "    kernel_path: ${KVOL}:$(vol_path "/boot/${3}")"
    if [ -f "/boot/initrd.img-${2}" ]; then
        write_cfg "    module_path: ${KVOL}:$(vol_path "/boot/initrd.img-${2}")"
    fi
    write_dtb "$2" "$DEV_DEVICETREE"
    write_cfg "    cmdline: ${4}"
}

write_cfg "timeout: ${LIMINE_TIMEOUT}"
[ -n "$LIMINE_SERIAL" ] && write_cfg "serial: yes"

for KVER in $(linux-version list | linux-version sort --reverse); do
    # get the actual kernel name
    for KPATH in /boot/vmlinu[xz]-${KVER}; do
        KPATH=$(basename "$KPATH")
        break
    done
    write_entry "$KVER" "$KVER" "$KPATH" "$CMDLINE_MULTI"
    if [ -z "$LIMINE_DISABLE_RECOVERY" ]; then
        write_entry "$KVER, recovery" "$KVER" "$KPATH" "$CMDLINE_SINGLE"
    fi
done

if [ "$LIMINE_CONFIG_PATH" = "-" ]; then
    cat "$COUT"
    rm -f "$COUT"
else
    DIRN=$(dirname "$LIMINE_CONFIG_PATH")
    mkdir -p "$DIRN"
    echo "Generating Limine config at ${LIMINE_CONFIG_PATH}..."
    mv "$COUT" "$LIMINE_CONFIG_PATH"
fi

exit 0
