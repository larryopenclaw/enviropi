#!/usr/bin/env python3
"""
EnviroPi Sensor Test Script
Tests all Enviro pHAT sensors and reports status
"""

import sys

def test_light():
    """Test light sensor"""
    try:
        from envirophat import light
        lux = light.light()
        print(f"✅ Light sensor: {lux} lux")
        return True
    except Exception as e:
        print(f"❌ Light sensor failed: {e}")
        return False

def test_weather():
    """Test temperature and pressure sensors"""
    try:
        from envirophat import weather
        temp = weather.temperature()
        pressure = weather.pressure()
        print(f"✅ Temperature: {temp:.1f}°C")
        print(f"✅ Pressure: {pressure:.1f} hPa")
        return True
    except Exception as e:
        print(f"❌ Weather sensor failed: {e}")
        return False

def test_motion():
    """Test motion/accelerometer"""
    try:
        from envirophat import motion
        accel = motion.accelerometer()
        print(f"✅ Accelerometer: x={accel.x:.2f}, y={accel.y:.2f}, z={accel.z:.2f}")
        return True
    except Exception as e:
        print(f"❌ Motion sensor failed: {e}")
        return False

def test_leds():
    """Test LEDs"""
    try:
        from envirophat import leds
        leds.off()
        print(f"✅ LEDs working")
        return True
    except Exception as e:
        print(f"❌ LEDs failed: {e}")
        return False

if __name__ == "__main__":
    print("=== EnviroPi Sensor Test ===\n")
    
    results = []
    results.append(test_light())
    results.append(test_weather())
    results.append(test_motion())
    results.append(test_leds())
    
    print(f"\n=== Results: {sum(results)}/4 sensors working ===")
    sys.exit(0 if all(results) else 1)
