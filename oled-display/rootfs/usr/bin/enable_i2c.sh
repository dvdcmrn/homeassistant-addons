#!/usr/bin/with-contenv bash

set -euo pipefail

log_info() {
    echo "[I2C] $*"
}

log_warn() {
    echo "[I2C][WARN] $*"
}

BOOT_CFG="/mnt/boot/config.txt"
BACKUP_SUFFIX="$(date +%Y%m%d-%H%M%S)"

log_info "Attempting to enable I2C using HassOSConfigurator-like steps"

if [ ! -e "$BOOT_CFG" ]; then
    log_warn "Boot config not found at $BOOT_CFG. This may not be Home Assistant OS or the path is unavailable. Skipping boot config changes."
else
    if [ ! -w "$BOOT_CFG" ]; then
        log_warn "Boot config at $BOOT_CFG is not writable from this add-on. Try enabling I2C via Settings → System → Hardware, or run steps manually."
    else
        cp "$BOOT_CFG" "${BOOT_CFG}.bak-${BACKUP_SUFFIX}" || true
        grep -qE '^dtparam=i2c_arm=on$' "$BOOT_CFG" || echo 'dtparam=i2c_arm=on' >> "$BOOT_CFG"
        grep -qE '^dtparam=i2c1=on$' "$BOOT_CFG" || echo 'dtparam=i2c1=on' >> "$BOOT_CFG"
        log_info "Ensured dtparam entries for i2c_arm and i2c1 in $BOOT_CFG"
    fi
fi

# Try to load kernel modules in the running system (may fail on HA OS sandbox)
if command -v modprobe >/dev/null 2>&1; then
    modprobe i2c-dev 2>/dev/null || log_warn "Could not load i2c-dev (may require reboot or elevated privileges)"
    modprobe i2c-bcm2835 2>/dev/null || log_warn "Could not load i2c-bcm2835 (may require reboot or elevated privileges)"
else
    log_warn "modprobe not available in container"
fi

# Show available I2C devices for visibility
if ls /dev/i2c-* >/dev/null 2>&1; then
    log_info "Available I2C devices: $(ls /dev/i2c-* | xargs)"
else
    log_warn "No /dev/i2c-* devices visible yet. A system reboot may be required."
fi

log_info "I2C enablement routine completed"

