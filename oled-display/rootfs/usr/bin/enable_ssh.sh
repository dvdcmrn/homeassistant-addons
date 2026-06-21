#!/usr/bin/with-contenv bashio

# HAOS debug SSH (port 22222) enablement
# Based on HassOSConfigurator HassOsEnableSSH by adamoutler:
# https://github.com/adamoutler/HassOSConfigurator/tree/main/HassOsEnableSSH

set +e

if ! bashio::config.true 'system.enable_ssh'; then
  bashio::log.info "system.enable_ssh=false, skipping debug SSH configurator"
  exit 0
fi

key="$(bashio::config 'system.ssh_public_key')"
if [ -z "${key}" ] || [ "${key}" = "null" ]; then
  bashio::log.warning "system.enable_ssh=true but ssh_public_key is empty; skipping"
  exit 0
fi

bashio::log.info "Starting HAOS debug SSH configurator (port 22222)"

mountAttempts=0
mountFailures=0

copyKeyToDevicePartition() {
  local partition="/dev/${1}"
  local tmp_path="/tmp/${1}"
  local config_dir="${tmp_path}/CONFIG"
  local authorized_keys_file="${config_dir}/authorized_keys"

  if [ ! -e "${partition}" ]; then
    bashio::log.debug "[skip] ${partition} does not exist"
    return 0
  fi

  mkdir -p "${tmp_path}" 2>/dev/null
  mountAttempts=$((mountAttempts + 1))
  mount "${partition}" "${tmp_path}" 2>/dev/null

  if [ $? -ne 0 ]; then
    mountFailures=$((mountFailures + 1))
    bashio::log.warning "Failed to mount ${partition}"
    return 1
  fi

  if [ ! -e "${tmp_path}/cmdline.txt" ]; then
    bashio::log.debug "[skip] No HAOS boot marker in ${partition}"
    umount "${tmp_path}" 2>/dev/null || true
    return 0
  fi

  if [ -e "${config_dir}/" ] && grep -Fq "${key}" "${authorized_keys_file}" 2>/dev/null; then
    bashio::log.info "[skip] SSH key already present on ${partition}"
    umount "${tmp_path}" 2>/dev/null || true
    return 0
  fi

  bashio::log.info "Writing authorized_keys on ${partition}"
  mkdir -p "${config_dir}"
  echo "${key}" >> "${authorized_keys_file}"
  umount "${tmp_path}" 2>/dev/null || true
  bashio::log.info "[success] SSH key written to ${partition}"
  return 0
}

partitions=(
  vda1
  sda1
  sdb1
  mmcblk0p1
  mmcblk0p2
  mmcblk1p1
  nvme0n1p1
  xvda8
)

for partition in "${partitions[@]}"; do
  copyKeyToDevicePartition "${partition}"
done

if [ "${mountAttempts}" -gt 0 ] && [ "${mountAttempts}" -eq "${mountFailures}" ]; then
  bashio::log.error "Failed to mount any boot partition for SSH setup"
  bashio::log.error "If this add-on shows Protection mode ON on the Info tab, turn it OFF, then restart"
  bashio::log.error "With full_access this add-on should install unprotected (like HassOS I2C Configurator)"
  exit 1
fi

bashio::log.warning "SSH configurator finished. Hard power-off reboot required before ssh root@host -p 22222 works"
exit 0
