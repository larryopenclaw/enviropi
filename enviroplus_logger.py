#!/usr/bin/env python3
"""
Enviro+ Data Logger
Logs temp, pressure, humidity, light, and noise to JSON every 5 minutes
"""

import json
import time
from datetime import datetime
from pathlib import Path

# Data directory
DATA_DIR = Path("/home/enviropi/enviro_data")
DATA_DIR.mkdir(exist_ok=True)

def read_sensors():
    """Read all Enviro+ sensors"""
    data = {
        "timestamp": datetime.now().isoformat()
    }
    
    # BME280: Temperature, Pressure, Humidity
    try:
        from bme280 import BME280
        from smbus2 import SMBus
        import time
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)
        
        # Discard first reading (sensor warm-up)
        _ = bme280.get_temperature()
        _ = bme280.get_humidity()
        _ = bme280.get_pressure()
        time.sleep(0.5)
        
        # Take actual readings
        data["temperature_c"] = round(bme280.get_temperature(), 2)
        data["pressure_hpa"] = round(bme280.get_pressure(), 2)
        data["humidity_pct"] = round(bme280.get_humidity(), 2)
    except Exception as e:
        print(f"BME280 error: {e}")
        data["temperature_c"] = None
        data["pressure_hpa"] = None
        data["humidity_pct"] = None
    
    # LTR-559: Light
    try:
        from ltr559 import LTR559
        ltr = LTR559()
        data["light_lux"] = round(ltr.get_lux(), 2)
    except Exception as e:
        print(f"LTR-559 error: {e}")
        data["light_lux"] = None
    
    # Microphone: Noise level (skipped - requires kernel driver setup)
    # TODO: Enable adau7002 audio device tree overlay
    data["noise_low"] = None
    data["noise_mid"] = None
    data["noise_high"] = None
    data["noise_amp"] = None
    
    return data

def log_reading():
    """Log current sensor readings"""
    try:
        # Read sensors
        reading = read_sensors()
        
        # Today's log file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = DATA_DIR / f"enviro_{today}.json"
        
        # Load existing data
        if log_file.exists():
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"date": today, "readings": []}
        
        # Append reading
        log_data["readings"].append(reading)
        
        # Write back
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Print summary
        print(f"[{reading['timestamp']}] {reading['temperature_c']}°C, {reading['humidity_pct']}% RH, {reading['pressure_hpa']} hPa, {reading['light_lux']} lux")
        if reading['noise_amp'] is not None:
            print(f"  Noise: {reading['noise_amp']:.1f} amplitude")
        
        return reading
        
    except Exception as e:
        print(f"Error logging data: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    log_reading()
