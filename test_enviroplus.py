#!/usr/bin/env python3
"""
Test all Enviro+ sensors
"""

import time

print("=== Testing Enviro+ Sensors ===\n")

# Test BME280 (temp, pressure, humidity)
try:
    from bme280 import BME280
    from smbus2 import SMBus
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)
    temp = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    print(f"✅ BME280:")
    print(f"   Temperature: {temp:.1f}°C")
    print(f"   Pressure: {pressure:.1f} hPa")
    print(f"   Humidity: {humidity:.1f}%")
except Exception as e:
    print(f"❌ BME280 failed: {e}")

print()

# Test LTR-559 (light + proximity)
try:
    from ltr559 import LTR559
    ltr = LTR559()
    light = ltr.get_lux()
    prox = ltr.get_proximity()
    print(f"✅ LTR-559:")
    print(f"   Light: {light:.1f} lux")
    print(f"   Proximity: {prox}")
except Exception as e:
    print(f"❌ LTR-559 failed: {e}")

print()

# Test microphone (noise level)
try:
    from enviroplus import noise
    low, mid, high, amp = noise.get_noise_profile()
    print(f"✅ Microphone:")
    print(f"   Low: {low:.1f}, Mid: {mid:.1f}, High: {high:.1f}")
    print(f"   Amplitude: {amp:.1f}")
except Exception as e:
    print(f"❌ Microphone failed: {e}")

print()

# Test LCD display
try:
    from ST7735 import ST7735
    from PIL import Image, ImageDraw, ImageFont
    
    disp = ST7735(
        port=0,
        cs=1,
        dc=9,
        backlight=12,
        rotation=270,
        spi_speed_hz=10000000
    )
    
    disp.begin()
    
    # Create test image
    img = Image.new('RGB', (disp.width, disp.height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), "EnviroPi", fill=(255, 255, 255))
    draw.text((10, 30), "Working!", fill=(0, 255, 0))
    
    disp.display(img)
    print(f"✅ LCD Display: {disp.width}x{disp.height}")
except Exception as e:
    print(f"❌ LCD Display failed: {e}")

print()

# Test PMS5003 particulate sensor (if connected)
try:
    from pms5003 import PMS5003
    pms = PMS5003()
    readings = pms.read()
    print(f"✅ PMS5003 Particulate Sensor:")
    print(f"   PM1.0: {readings.pm_ug_per_m3(1.0)}")
    print(f"   PM2.5: {readings.pm_ug_per_m3(2.5)}")
    print(f"   PM10: {readings.pm_ug_per_m3(10)}")
except Exception as e:
    print(f"ℹ️  PMS5003: {e} (may not be connected)")

print()
print("=== Test Complete ===")
