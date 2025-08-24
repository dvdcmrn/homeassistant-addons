ARG BUILD_FROM
FROM ${BUILD_FROM}

# Install required dependencies including development headers
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-pillow \
    py3-psutil \
    i2c-tools \
    linux-headers \
    zlib-dev \
    jpeg-dev \
    gcc \
    python3-dev \
    musl-dev

# Install Python packages with pre-built wheels
RUN pip3 install --no-cache-dir \
    luma.oled \
    luma.core

# Copy data
COPY rootfs /

# Make scripts executable
RUN chmod a+x /etc/services.d/oled/run

# Labels
LABEL \
  io.hass.name="OLED System Monitor" \
  io.hass.description="Displays system stats on an OLED display" \
  io.hass.arch="armhf|aarch64|i386|amd64"