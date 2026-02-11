# EnviroPi Deployment Log

## Current Status (2026-02-10)

### ✅ Deployed Services

#### 1. LCD Display Service
- **Status:** Active and running
- **Uptime:** Since Feb 9, 2026 11:32 CST
- **Service:** `enviropi-display.service` (systemd)
- **Auto-start:** Enabled (starts on boot)
- **Update frequency:** Every 5 seconds

#### 2. Data Logger
- **Status:** Active and logging
- **Deployed:** Feb 10, 2026 20:25 CST
- **Schedule:** Every 5 minutes (cron)
- **Log location:** `~/enviro_data/enviro_YYYY-MM-DD.json`
- **Cron job:**
  ```bash
  */5 * * * * /usr/bin/python3 /home/enviropi/enviroplus_logger.py >> /home/enviropi/enviro.log 2>&1
  ```

### 📊 Current Sensor Readings

**As of 2026-02-10 20:25 CST:**
- Temperature: 71.6°F (22.0°C)
- Humidity: 43.0% RH
- Pressure: 29.39 inHg (995 hPa)
- Light: 4 lux

### 📁 Data Format

Daily JSON files stored in `~/enviro_data/`:

```json
{
  "date": "2026-02-10",
  "readings": [
    {
      "timestamp": "2026-02-10T20:25:30.099105",
      "temperature_c": 21.99,
      "pressure_hpa": 995.38,
      "humidity_pct": 42.99,
      "light_lux": 0,
      "noise_low": null,
      "noise_mid": null,
      "noise_high": null,
      "noise_amp": null
    }
  ]
}
```

### 🔧 Deployment Commands Used

```bash
# Copy logger to Pi
scp enviroplus_logger.py enviropi@enviropi.local:~/

# Test logger
ssh enviropi@enviropi.local "python3 ~/enviroplus_logger.py"

# Install cron job
ssh enviropi@enviropi.local "echo '*/5 * * * * /usr/bin/python3 /home/enviropi/enviroplus_logger.py >> /home/enviropi/enviro.log 2>&1' | crontab -"

# Verify cron
ssh enviropi@enviropi.local "crontab -l"
```

### 🎯 Next Steps

- [ ] Set up daily email reports (`send_daily_report.sh`)
- [ ] Add noise monitoring (requires MEMS mic driver setup)
- [ ] Create data visualization dashboard
- [ ] Set up automated backups of JSON data files

### 📝 Connection Info

- **Hostname:** enviropi.local
- **IP:** 192.168.2.15
- **User:** enviropi
- **SSH:** Port 22

### 🔍 Monitoring Commands

```bash
# Check display service status
ssh enviropi@enviropi.local "sudo systemctl status enviropi-display.service"

# View recent sensor readings
ssh enviropi@enviropi.local "tail -20 ~/enviro.log"

# View today's data
ssh enviropi@enviropi.local "cat ~/enviro_data/enviro_$(date +%Y-%m-%d).json"

# Live sensor check
ssh enviropi@enviropi.local "python3 -c 'from bme280 import BME280; from smbus2 import SMBus; from ltr559 import LTR559; import time; bus = SMBus(1); bme = BME280(i2c_dev=bus); ltr = LTR559(); _ = bme.get_temperature(); time.sleep(0.5); print(f\"Temp: {bme.get_temperature():.1f}°C, Humidity: {bme.get_humidity():.1f}%, Pressure: {bme.get_pressure():.0f}hPa, Light: {ltr.get_lux():.0f}lux\")'"
```

### 🛠️ Troubleshooting

**If data stops logging:**
```bash
# Check cron is running
ssh enviropi@enviropi.local "systemctl status cron"

# Check for errors in log
ssh enviropi@enviropi.local "tail -50 ~/enviro.log"

# Manually trigger logger
ssh enviropi@enviropi.local "python3 ~/enviroplus_logger.py"
```

**If display stops updating:**
```bash
# Check service status
ssh enviropi@enviropi.local "sudo systemctl status enviropi-display.service"

# Restart service
ssh enviropi@enviropi.local "sudo systemctl restart enviropi-display.service"

# View service logs
ssh enviropi@enviropi.local "sudo journalctl -u enviropi-display.service -n 50"
```
