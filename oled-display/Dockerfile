ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-pillow \
    i2c-tools \
    gcc \
    python3-dev \
    musl-dev

# Install Python packages
RUN pip3 install --no-cache-dir \
    luma.oled \
    luma.core \
    psutil

# Copy data
COPY rootfs /

# Make scripts executable
RUN chmod a+x /etc/services.d/oled/run

# Labels
LABEL \
  io.hass.name="OLED System Monitor" \
  io.hass.description="Displays system stats on an OLED display" \
  io.hass.version="${BUILD_VERSION}" \
  io.hass.type="addon" \
  io.hass.arch="armhf|aarch64|i386|amd64"
