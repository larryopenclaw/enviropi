#!/usr/bin/env python3
"""
EnviroPi Display - Show live sensor readings on LCD
Runs continuously, updates every 5 seconds
"""

import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from st7735 import ST7735
from bme280 import BME280
from smbus2 import SMBus
from ltr559 import LTR559

# Initialize display
disp = ST7735(
    port=0,
    cs=1,
    dc=9,
    backlight=12,
    rotation=270,
    spi_speed_hz=10000000
)
disp.begin()

# Initialize sensors
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
ltr = LTR559()

# Colors
COLOR_BG = (0, 0, 0)
COLOR_TEXT = (255, 255, 255)
COLOR_TEMP = (255, 100, 100)
COLOR_HUM = (100, 150, 255)
COLOR_PRESS = (150, 255, 150)
COLOR_LIGHT = (255, 255, 100)

def read_sensors():
    """Read all sensors with warm-up"""
    # Discard first reading
    _ = bme280.get_temperature()
    _ = bme280.get_humidity()
    _ = bme280.get_pressure()
    time.sleep(0.5)
    
    # Get actual readings
    temp_c = bme280.get_temperature()
    temp_f = temp_c * 9/5 + 32
    humidity = bme280.get_humidity()
    pressure_hpa = bme280.get_pressure()
    pressure_inhg = pressure_hpa * 0.02953  # Convert hPa to inHg
    light = ltr.get_lux()
    
    return temp_c, temp_f, humidity, pressure_hpa, pressure_inhg, light

def update_display():
    """Update display with current readings"""
    temp_c, temp_f, humidity, pressure_hpa, pressure_inhg, light = read_sensors()
    
    # Create image
    img = Image.new('RGB', (disp.width, disp.height), color=COLOR_BG)
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fall back to default if not available
    try:
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except:
        font_small = ImageFont.load_default()
        font_large = ImageFont.load_default()
    
    # Draw title
    draw.text((5, 2), "EnviroPi", font=font_small, fill=COLOR_TEXT)
    draw.text((120, 2), datetime.now().strftime("%H:%M"), font=font_small, fill=COLOR_TEXT)
    
    # Draw sensor readings (compact layout for 160x80)
    y = 16
    
    # Temperature
    draw.text((5, y), f"{temp_f:.1f}°F", font=font_large, fill=COLOR_TEMP)
    draw.text((5, y+14), f"({temp_c:.1f}°C)", font=font_small, fill=COLOR_TEMP)
    
    # Humidity
    draw.text((85, y), f"{humidity:.1f}%", font=font_large, fill=COLOR_HUM)
    draw.text((85, y+14), "RH", font=font_small, fill=COLOR_HUM)
    
    # Pressure (both hPa and inHg)
    y += 32
    draw.text((5, y), f"{pressure_inhg:.2f}", font=font_large, fill=COLOR_PRESS)
    draw.text((5, y+14), f"inHg ({pressure_hpa:.0f}hPa)", font=font_small, fill=COLOR_PRESS)
    
    # Light
    draw.text((85, y), f"{light:.0f}", font=font_large, fill=COLOR_LIGHT)
    draw.text((85, y+14), "lux", font=font_small, fill=COLOR_LIGHT)
    
    # Display
    disp.display(img)

if __name__ == "__main__":
    print("EnviroPi Display - Starting...")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            try:
                update_display()
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                print(f"Display error: {e}")
                time.sleep(5)
    except KeyboardInterrupt:
        # Clear display
        img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
        disp.display(img)
        print("\nDisplay stopped.")
