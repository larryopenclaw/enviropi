#!/usr/bin/env python3
"""
EnviroPi Data Logger
Reads BMP280 (temp/pressure) and TCS3472 (light) sensors
Logs to JSON every 5 minutes via cron
"""

import smbus
import time
import json
from datetime import datetime
from pathlib import Path

# I2C bus
bus = smbus.SMBus(1)

# BMP280 Temperature & Pressure Sensor
BMP280_ADDR = 0x76
REG_DIG_T1 = 0x88
REG_CHIPID = 0xD0
REG_CONTROL = 0xF4
REG_CONFIG = 0xF5
REG_PRESS_MSB = 0xF7
REG_TEMP_MSB = 0xFA

# BH1750 Light Sensor
BH1750_ADDR = 0x23

# Data directory
DATA_DIR = Path("/home/enviropi/enviro_data")
DATA_DIR.mkdir(exist_ok=True)

def read_bmp280_cal():
    """Read BMP280 calibration data"""
    cal = []
    for i in range(0x88, 0x88 + 24):
        cal.append(bus.read_byte_data(BMP280_ADDR, i))
    
    dig_T1 = cal[1] * 256 + cal[0]
    dig_T2 = cal[3] * 256 + cal[2]
    if dig_T2 > 32767: dig_T2 -= 65536
    dig_T3 = cal[5] * 256 + cal[4]
    if dig_T3 > 32767: dig_T3 -= 65536
    
    dig_P1 = cal[7] * 256 + cal[6]
    dig_P2 = cal[9] * 256 + cal[8]
    if dig_P2 > 32767: dig_P2 -= 65536
    dig_P3 = cal[11] * 256 + cal[10]
    if dig_P3 > 32767: dig_P3 -= 65536
    dig_P4 = cal[13] * 256 + cal[12]
    if dig_P4 > 32767: dig_P4 -= 65536
    dig_P5 = cal[15] * 256 + cal[14]
    if dig_P5 > 32767: dig_P5 -= 65536
    dig_P6 = cal[17] * 256 + cal[16]
    if dig_P6 > 32767: dig_P6 -= 65536
    dig_P7 = cal[19] * 256 + cal[18]
    if dig_P7 > 32767: dig_P7 -= 65536
    dig_P8 = cal[21] * 256 + cal[20]
    if dig_P8 > 32767: dig_P8 -= 65536
    dig_P9 = cal[23] * 256 + cal[22]
    if dig_P9 > 32767: dig_P9 -= 65536
    
    return (dig_T1, dig_T2, dig_T3, dig_P1, dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9)

def read_bmp280():
    """Read temperature and pressure from BMP280"""
    # Configure sensor
    bus.write_byte_data(BMP280_ADDR, REG_CONTROL, 0x6F)
    bus.write_byte_data(BMP280_ADDR, REG_CONFIG, 0xA0)
    time.sleep(0.1)
    
    # Read calibration
    cal = read_bmp280_cal()
    
    # Read raw data
    data = bus.read_i2c_block_data(BMP280_ADDR, REG_PRESS_MSB, 6)
    adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    
    # Compensate temperature
    dig_T1, dig_T2, dig_T3 = cal[0], cal[1], cal[2]
    var1 = ((adc_t / 16384.0) - (dig_T1 / 1024.0)) * dig_T2
    var2 = (((adc_t / 131072.0) - (dig_T1 / 8192.0)) ** 2) * dig_T3
    t_fine = int(var1 + var2)
    temp = (var1 + var2) / 5120.0
    
    # Compensate pressure
    dig_P1, dig_P2, dig_P3, dig_P4, dig_P5, dig_P6, dig_P7, dig_P8, dig_P9 = cal[3:12]
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1
    
    if var1 == 0:
        pressure = 0
    else:
        pressure = 1048576.0 - adc_p
        pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
        var1 = dig_P9 * pressure * pressure / 2147483648.0
        var2 = pressure * dig_P8 / 32768.0
        pressure = pressure + (var1 + var2 + dig_P7) / 16.0
        pressure = pressure / 100.0  # Convert to hPa
    
    return {"temperature_c": round(temp, 2), "pressure_hpa": round(pressure, 2)}

def read_bh1750():
    """Read light level from BH1750"""
    try:
        # Power on
        bus.write_byte(BH1750_ADDR, 0x01)
        time.sleep(0.01)
        
        # Continuous high res mode
        bus.write_byte(BH1750_ADDR, 0x10)
        time.sleep(0.2)
        
        # Read 2 bytes
        data = bus.read_i2c_block_data(BH1750_ADDR, 0x00, 2)
        lux = round((data[0] * 256 + data[1]) / 1.2, 2)
        
        return {"light_lux": lux}
    except Exception as e:
        return {"light_lux": None}

def log_reading():
    """Log current sensor readings"""
    try:
        # Read sensors
        weather_data = read_bmp280()
        light_data = read_bh1750()
        
        # Combine data
        reading = {
            "timestamp": datetime.now().isoformat(),
            **weather_data,
            **light_data
        }
        
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
        
        print(f"[{reading['timestamp']}] {reading['temperature_c']}°C, {reading['pressure_hpa']} hPa, {reading['light_lux']} lux")
        
        return reading
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    log_reading()
