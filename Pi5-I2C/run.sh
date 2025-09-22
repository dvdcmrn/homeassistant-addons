#!/usr/bin/with-contenv bash

# Pi5-I2C - Enhanced I2C enablement for Raspberry Pi (Pi 4/5) on Home Assistant OS
# Based on HassOSConfigurator by adamoutler: https://github.com/adamoutler/HassOSConfigurator/tree/main/Pi4EnableI2C
# Integrated into OLED System Monitor add-on

set -euo pipefail

log_info() {
    echo "[Pi5-I2C] $*"
}

log_warn() {
    echo "[Pi5-I2C][WARN] $*"
}

log_error() {
    echo "[Pi5-I2C][ERROR] $*"
}

# I2C configuration parameters
I2C_VC_CONFIG='dtparam=i2c_vc=on'
I2C_ARM_CONFIG='dtparam=i2c_arm=on'

log_info "Starting enhanced I2C enablement process for Raspberry Pi (Pi 4/5)"
log_info "Based on HassOSConfigurator implementation by adamoutler"
log_info "This process may require up to 3 reboots for full I2C enablement"

# Check if I2C is already available
if ls /dev/i2c-* >/dev/null 2>&1; then
    log_info "I2C devices already available: $(ls /dev/i2c-* | xargs)"
    log_info "I2C is already enabled! You can disable this add-on if no longer needed."
    exit 0
fi

log_info "I2C not detected, attempting to enable..."

# Function to perform I2C configuration on a partition
performWork() {
    local partition=$1
    local mount_point="/tmp/$partition"
    
    if [ ! -e "/dev/$partition" ]; then
        log_warn "Partition /dev/$partition not available"
        return 0
    fi
    
    log_info "Processing partition: $partition"
    
    # Unmount and remount the partition
    umount "$mount_point" 2>/dev/null || true
    mkdir -p "$mount_point" 2>/dev/null || true
    
    local mount_result
    mount_result=$(mount "/dev/$partition" "$mount_point" 2>&1) || {
        if [[ "$mount_result" == *"root"* ]]; then
            log_error "Detected Protection Mode is enabled. Disable Protection Mode in Info Screen."
        fi
        log_warn "Failed to mount /dev/$partition: $mount_result"
        return 1
    }
    
    if [ -e "$mount_point/config.txt" ]; then
        log_info "Found config.txt on $partition"
        
        # Create modules directory for HASSOS
        mkdir -p "$mount_point/CONFIG/modules" 2>/dev/null || true
        echo "i2c-dev" > "$mount_point/CONFIG/modules/rpi-i2c.conf" 2>/dev/null || true
        
        # Check for Raspbian support (i2c-bcm2708)
        if ls "$mount_point" | grep -q vmlinuz; then
            log_info "Detected Raspbian, not HASSOS - enabling additional modules"
            local p2="${partition::-1}2"
            local p2_mount="/tmp/${p2}"
            
            mkdir -p "$p2_mount" 2>/dev/null || true
            if mount "/dev/${p2}" "$p2_mount" 2>/dev/null; then
                # Add i2c modules to /etc/modules for Raspbian
                if ! grep -q "bcm" "$p2_mount/etc/modules" 2>/dev/null; then
                    echo "i2c-bcm2708" >> "$p2_mount/etc/modules" 2>/dev/null || true
                fi
                if ! grep -q "i2c-dev" "$p2_mount/etc/modules" 2>/dev/null; then
                    echo "i2c-dev" >> "$p2_mount/etc/modules" 2>/dev/null || true
                fi
                umount "$p2_mount" 2>/dev/null || true
            fi
        fi
        
        # Add I2C VC configuration
        if grep -q "$I2C_VC_CONFIG" "$mount_point/config.txt" 2>/dev/null && ! grep -q "^#" "$mount_point/config.txt" | grep -q "$I2C_VC_CONFIG"; then
            log_info "I2C VC already configured on $partition"
        else
            log_info "Adding $I2C_VC_CONFIG to $partition/config.txt"
            echo "$I2C_VC_CONFIG" >> "$mount_point/config.txt"
        fi
        
        # Add I2C ARM configuration  
        if grep -q "$I2C_ARM_CONFIG" "$mount_point/config.txt" 2>/dev/null && ! grep -q "^#" "$mount_point/config.txt" | grep -q "$I2C_ARM_CONFIG"; then
            log_info "I2C ARM already configured on $partition"
        else
            log_info "Adding $I2C_ARM_CONFIG to $partition/config.txt"
            echo "$I2C_ARM_CONFIG" >> "$mount_point/config.txt"
        fi
        
        # Unmount the partition
        umount "$mount_point" 2>/dev/null || true
        log_info "Successfully configured I2C on $partition"
        
    else
        log_warn "No config.txt found on $partition"
        umount "$mount_point" 2>/dev/null || true
    fi
}

# Try to mount /tmp if not available
mkdir -p /tmp 2>/dev/null || true

# Check available partitions and attempt I2C configuration
log_info "Scanning for boot partitions..."

# Try common partition names
for partition in sda1 sdb1 mmcblk0p1 nvme0n1p1; do
    if [ -e "/dev/$partition" ]; then
        log_info "Found partition: $partition"
        performWork "$partition"
    fi
done

# Check if any partitions were found
if [ ! -e "/dev/sda1" ] && [ ! -e "/dev/sdb1" ] && [ ! -e "/dev/mmcblk0p1" ] && [ ! -e "/dev/nvme0n1p1" ]; then
    log_error "No boot partitions found. Protection mode may be enabled?"
    log_error "You cannot run this without disabling protection mode"
    exit 1
fi

log_info "I2C configuration completed"
log_warn "IMPORTANT: You need to perform a hard power-off reboot now"
log_warn "You may need to reboot up to 3 times total:"
log_warn "  1. First reboot: Places configuration files in boot partition"
log_warn "  2. Second reboot: Activates I2C hardware and loads kernel modules"
log_warn "  3. Third reboot (if needed): Ensures all I2C devices are properly initialized"
log_warn "After final reboot, I2C devices should be available at /dev/i2c-*"
log_warn "Check add-on logs after each reboot to see progress"

exit 0
