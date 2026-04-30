#!/usr/bin/env python3
import time
import subprocess
import psutil
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont
# Initialize the device
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, width=128, height=64)
# Load a font
font = ImageFont.load_default()
def get_cpu_temperature():
    try:
        # For Raspberry Pi
        temp = subprocess.check_output(['vcgencmd', 'measure_temp']).decode()
        return float(temp.replace('temp=', '').replace('\'C', ''))
    except:
        # Fallback
        try:
            return psutil.sensors_temperatures()['cpu_thermal'][0].current
        except:
            return 0
# Main loop
try:
    while True:
        # Get stats
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        cpu_temp = get_cpu_temperature()
        
        # Draw on the display
        with canvas(device) as draw:
            # Title with temperature
            draw.text((5, 5), "thor", font=font, fill="white")
            draw.text((70, 5), f"{cpu_temp:.1f}°C", font=font, fill="white")
            
            # CPU usage with bar graph
            draw.text((5, 20), f"CPU: {cpu_usage}%", font=font, fill="white")
            draw.rectangle((70, 20, 123, 28), outline="white", fill="black")
            draw.rectangle((70, 20, 70 + int(53 * cpu_usage / 100), 28), outline="white", fill="white")
            
            # RAM usage with bar graph
            draw.text((5, 35), f"RAM: {memory.percent}%", font=font, fill="white")
            draw.rectangle((70, 35, 123, 43), outline="white", fill="black")
            draw.rectangle((70, 35, 70 + int(53 * memory.percent / 100), 43), outline="white", fill="white")
            
            # Disk usage with bar graph
            draw.text((5, 50), f"DISK: {disk.percent}%", font=font, fill="white")
            draw.rectangle((70, 50, 123, 58), outline="white", fill="black")
            draw.rectangle((70, 50, 70 + int(53 * disk.percent / 100), 58), outline="white", fill="white")
        
        # Wait before next update
        time.sleep(1)
        
except KeyboardInterrupt:
    # Clear the display on exit
    device.clear()
