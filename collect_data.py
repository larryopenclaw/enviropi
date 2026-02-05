#!/usr/bin/env python3
"""
EnviroPi Data Collection Script
Logs sensor data to JSON file every 5 minutes
"""

import json
import time
from datetime import datetime
from pathlib import Path

# Data directory
DATA_DIR = Path("/home/enviropi/enviro_data")
DATA_DIR.mkdir(exist_ok=True)

def read_sensors():
    """Read all sensor values"""
    from envirophat import light, weather, motion
    
    return {
        "timestamp": datetime.now().isoformat(),
        "temperature_c": round(weather.temperature(), 2),
        "pressure_hpa": round(weather.pressure(), 2),
        "light_lux": round(light.light(), 2),
        "accelerometer": {
            "x": round(motion.accelerometer().x, 3),
            "y": round(motion.accelerometer().y, 3),
            "z": round(motion.accelerometer().z, 3)
        }
    }

def log_data():
    """Log current sensor readings to today's JSON file"""
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = DATA_DIR / f"enviro_{today}.json"
    
    try:
        # Read sensors
        data = read_sensors()
        
        # Load existing data
        if log_file.exists():
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {"date": today, "readings": []}
        
        # Append new reading
        log_data["readings"].append(data)
        
        # Write back
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"[{data['timestamp']}] Logged: {data['temperature_c']}°C, {data['pressure_hpa']} hPa, {data['light_lux']} lux")
        
        # Keep only last 7 days of data
        cleanup_old_logs()
        
    except Exception as e:
        print(f"Error logging data: {e}")

def cleanup_old_logs():
    """Remove log files older than 7 days"""
    import os
    from datetime import timedelta
    
    cutoff = datetime.now() - timedelta(days=7)
    
    for log_file in DATA_DIR.glob("enviro_*.json"):
        file_date = log_file.stem.replace("enviro_", "")
        try:
            file_datetime = datetime.strptime(file_date, "%Y-%m-%d")
            if file_datetime < cutoff:
                os.remove(log_file)
                print(f"Cleaned up old log: {log_file.name}")
        except ValueError:
            pass  # Skip malformed filenames

if __name__ == "__main__":
    # For cron: run once and exit
    log_data()
