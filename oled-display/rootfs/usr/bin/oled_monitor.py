#!/usr/bin/env python3
import time
import subprocess
import psutil
import json
import os
import socket
from datetime import timedelta
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106, ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import glob

# Get configuration from options
with open('/data/options.json') as f:
    config = json.load(f)

# Support both new flat options and legacy nested options
display_config = config.get('display', {})
system_config = config.get('system', {})
custom_text_config = config.get('custom_text', {})
network_config = config.get('network', {})

# Display configuration (flat first, then legacy fallback)
display_type = config.get('display_type', display_config.get('type', 'sh1106'))
i2c_address_str = config.get('i2c_address', display_config.get('i2c_address', '0x3C'))
i2c_address = int(i2c_address_str, 16) if isinstance(i2c_address_str, str) else int(i2c_address_str)
i2c_port = config.get('i2c_port', display_config.get('i2c_port', 'auto'))
width = config.get('width', display_config.get('width', 128))
height = config.get('height', display_config.get('height', 64))
rotate = config.get('rotate', display_config.get('rotate', 0))
contrast = config.get('contrast', display_config.get('contrast', 255))

# System configuration
update_interval = config.get('update_interval', system_config.get('update_interval', 1))
title = config.get('title', system_config.get('title', 'home assistant'))
show_title = config.get('show_title', system_config.get('show_title', True))
show_temperature = config.get('show_temperature', system_config.get('show_temperature', True))
debug_mode = config.get('debug_mode', system_config.get('debug_mode', False))

# Build metrics from either legacy list or new toggles
metrics_config = config.get('metrics', [])
if metrics_config:
    metrics = sorted(metrics_config, key=lambda x: x.get('position', 99))
else:
    show_cpu_metric = config.get('show_cpu', True)
    show_memory_metric = config.get('show_memory', True)
    show_disk_metric = config.get('show_disk', True)
    show_temperature_metric = config.get('show_temperature_metric', False)
    show_uptime_metric = config.get('show_uptime', False)
    disk_mount_point = config.get('disk_mount_point', '/')

    metrics = []
    position_counter = 1
    if show_cpu_metric:
        metrics.append({"type": "cpu", "position": position_counter, "show_bar": True, "label": "CPU"})
        position_counter += 1
    if show_memory_metric:
        metrics.append({"type": "memory", "position": position_counter, "show_bar": True, "label": "RAM"})
        position_counter += 1
    if show_disk_metric:
        metrics.append({"type": "disk", "position": position_counter, "show_bar": True, "label": "DISK", "mount_point": disk_mount_point})
        position_counter += 1
    if show_temperature_metric:
        metrics.append({"type": "temperature", "position": position_counter, "show_bar": False, "label": "TEMP"})
        position_counter += 1
    if show_uptime_metric:
        metrics.append({"type": "uptime", "position": position_counter, "show_bar": False, "label": "UPTIME"})

# Custom text configuration
custom_text_enabled = config.get('custom_text_enabled', custom_text_config.get('enabled', False))
custom_text_position = config.get('custom_text_position', custom_text_config.get('position', 4))
custom_text = config.get('custom_text', custom_text_config.get('text', 'Home Assistant'))

# Network configuration
show_ip = config.get('show_ip', network_config.get('show_ip', False))
network_position = config.get('network_position', network_config.get('position', 5))
network_interface = config.get('network_interface', network_config.get('interface', 'eth0'))
network_label = config.get('network_label', network_config.get('label', 'IP'))

def find_i2c_device():
    """Find available I2C devices"""
    i2c_devices = glob.glob('/dev/i2c-*')
    if not i2c_devices:
        # Try alternative paths
        i2c_devices = glob.glob('/dev/i2c*')
    
    if i2c_devices:
        # Sort to prefer i2c-1, then i2c-0, etc.
        i2c_devices.sort()
        return i2c_devices[0].split('-')[-1]  # Extract port number
    return None

def initialize_display():
    """Initialize the OLED display with error handling"""
    # Use configured port or auto-detect
    if i2c_port == 'auto':
        port_num = find_i2c_device()
    else:
        port_num = i2c_port
    
    if port_num is None:
        print("ERROR: No I2C devices found. Please enable I2C in your system.")
        print("Available devices:")
        try:
            result = subprocess.run(['ls', '-la', '/dev/'], capture_output=True, text=True)
            print(result.stdout)
        except:
            pass
        return None
    
    try:
        print(f"Using I2C device: /dev/i2c-{port_num}")
        serial = i2c(port=int(port_num), address=i2c_address)
        
        if display_type == 'sh1106':
            device = sh1106(serial, width=width, height=height, rotate=rotate)
        else:
            device = ssd1306(serial, width=width, height=height, rotate=rotate)
        
        # Set contrast
        device.contrast(contrast)
        print(f"Successfully initialized {display_type} display")
        return device
        
    except Exception as e:
        print(f"ERROR: Failed to initialize display: {e}")
        print(f"Tried I2C port: {port_num}, address: 0x{i2c_address:02X}")
        return None

# Load a font
font = ImageFont.load_default()

def get_cpu_temperature():
    try:
        # For Raspberry Pi
        temp = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp']).decode()
        return float(int(temp.strip()) / 1000)
    except:
        # Fallback
        try:
            return psutil.sensors_temperatures()['cpu_thermal'][0].current
        except:
            return 0

def get_ip_address(interface):
    try:
        cmd = f"ip addr show {interface} | grep 'inet ' | awk '{{print $2}}' | cut -d/ -f1"
        ip = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
        return ip
    except:
        try:
            # Fallback to hostname -I
            return subprocess.check_output('hostname -I', shell=True).decode('utf-8').split()[0]
        except:
            return "No IP"

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        return str(timedelta(seconds=int(uptime_seconds)))
    except:
        return "Unknown"

def draw_metric(draw, metric, y_position):
    metric_type = metric.get('type')
    label = metric.get('label', metric_type.upper())
    show_bar = metric.get('show_bar', True)
    
    if metric_type == 'cpu':
        value = psutil.cpu_percent()
        text = f"{label}: {value}%"
    elif metric_type == 'memory':
        memory = psutil.virtual_memory()
        value = memory.percent
        text = f"{label}: {value}%"
    elif metric_type == 'disk':
        mount_point = metric.get('mount_point', '/')
        disk = psutil.disk_usage(mount_point)
        value = disk.percent
        text = f"{label}: {value}%"
    elif metric_type == 'temperature':
        value = get_cpu_temperature()
        text = f"{label}: {value:.1f}°C"
    elif metric_type == 'uptime':
        value = get_uptime()
        text = f"{label}: {value}"
        show_bar = False  # No bar for uptime
    else:
        return y_position  # Skip unknown metric types
    
    # Draw text
    draw.text((5, y_position), text, font=font, fill="white")
    
    # Draw bar if needed
    if show_bar and metric_type in ['cpu', 'memory', 'disk']:
        draw.rectangle((70, y_position, 123, y_position + 8), outline="white", fill="black")
        draw.rectangle((70, y_position, 70 + int(53 * value / 100), y_position + 8), outline="white", fill="white")
    
    return y_position + 15  # Return next position

# Main loop
try:
    if debug_mode:
        print("DEBUG MODE: Running without OLED display")
        device = None
    else:
        device = initialize_display()
        if device is None:
            print("WARNING: OLED initialization failed or no I2C device. Falling back to debug mode.")
            debug_mode = True
            print("DEBUG MODE: Running without OLED display")
            device = None

    while True:
        # Get temperature for title
        cpu_temp = get_cpu_temperature() if show_temperature else None
        
        if debug_mode:
            # Debug mode: print to console
            print(f"\n=== {title} ===")
            if show_temperature and cpu_temp:
                print(f"Temperature: {cpu_temp:.1f}°C")
            
            # Print metrics
            for metric in metrics:
                metric_type = metric.get('type')
                label = metric.get('label', metric_type.upper())
                
                if metric_type == 'cpu':
                    value = psutil.cpu_percent()
                    print(f"{label}: {value}%")
                elif metric_type == 'memory':
                    memory = psutil.virtual_memory()
                    value = memory.percent
                    print(f"{label}: {value}%")
                elif metric_type == 'disk':
                    mount_point = metric.get('mount_point', '/')
                    disk = psutil.disk_usage(mount_point)
                    value = disk.percent
                    print(f"{label}: {value}%")
                elif metric_type == 'temperature':
                    value = get_cpu_temperature()
                    print(f"{label}: {value:.1f}°C")
                elif metric_type == 'uptime':
                    value = get_uptime()
                    print(f"{label}: {value}")
            
            if custom_text_enabled:
                print(f"Custom: {custom_text}")
            
            if show_ip:
                ip = get_ip_address(network_interface)
                print(f"{network_label}: {ip}")
        else:
            # Normal mode: draw on OLED display
            with canvas(device) as draw:
                y_position = 5
                
                # Draw title
                if show_title:
                    draw.text((5, y_position), title, font=font, fill="white")
                    if show_temperature:
                        draw.text((70, y_position), f"{cpu_temp:.1f}°C", font=font, fill="white")
                    y_position += 15
                
                # Draw metrics
                for metric in metrics:
                    y_position = draw_metric(draw, metric, y_position)
                
                # Draw custom text if enabled
                if custom_text_enabled:
                    draw.text((5, y_position), custom_text, font=font, fill="white")
                    y_position += 15
                
                # Draw IP address if enabled
                if show_ip:
                    ip = get_ip_address(network_interface)
                    draw.text((5, y_position), f"{network_label}: {ip}", font=font, fill="white")
        
        # Wait before next update
        time.sleep(update_interval)
        
except KeyboardInterrupt:
    # Clear the display on exit
    if device:
        device.clear()
