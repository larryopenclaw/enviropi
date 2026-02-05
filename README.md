# 🥧 EnviroPi

Environmental monitoring system for Raspberry Pi Zero 2 W + Pimoroni Enviro+

Monitor temperature, humidity, pressure, and light levels with automatic data logging and beautiful daily email reports!

![Raspberry Pi Zero 2 W with Pimoroni Enviro+](https://shop.pimoroni.com/cdn/shop/products/PIM486-01-Angle_1024x1024.jpg?v=1586260914)

## Features

- 🌡️ **Temperature** monitoring (°F and °C)
- 💧 **Humidity** tracking (% RH)
- 🌍 **Barometric pressure** (inHg and hPa - pilot-friendly!)
- 💡 **Light level** measurement (lux)
- 📺 **Live LCD display** updating every 5 seconds
- 📊 **Automated data logging** every 5 minutes
- 📧 **Daily HTML email reports** with statistics
- 🔄 **Auto-start on boot** (systemd services)

## Hardware

- **Raspberry Pi Zero 2 W** (or any Pi with 40-pin GPIO)
- **Pimoroni Enviro+** HAT
  - BME280 sensor (temp/pressure/humidity)
  - LTR-559 sensor (light)
  - 0.96" color LCD display (160x80)
  - [Buy it here](https://shop.pimoroni.com/products/enviro)

## Quick Start

### 1. Set up your Pi

```bash
# Enable I2C and SPI
sudo raspi-config nonint do_i2c 0
sudo raspi-config nonint do_spi 0

# Install dependencies
sudo apt update
sudo apt install -y i2c-tools python3-pip python3-numpy python3-smbus

# Install Pimoroni Enviro+ library
sudo pip3 install envirophat --break-system-packages
```

### 2. Deploy the data logger

```bash
# Copy the logger script to your Pi
scp enviroplus_logger.py pi@your-pi.local:/home/pi/

# Set up cron job for 5-minute logging
crontab -e
# Add this line:
*/5 * * * * /usr/bin/python3 /home/pi/enviroplus_logger.py >> /home/pi/enviro.log 2>&1
```

### 3. Set up the LCD display

```bash
# Copy display script and service file
scp display_readings.py pi@your-pi.local:/home/pi/
scp enviropi-display.service pi@your-pi.local:/tmp/

# Install and enable the display service
sudo mv /tmp/enviropi-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable enviropi-display.service
sudo systemctl start enviropi-display.service
```

### 4. (Optional) Set up email reports

Edit `send_daily_report.sh` to configure your email settings, then run it daily via cron or manually.

## Data Format

Sensor readings are stored as JSON in `~/enviro_data/enviro_YYYY-MM-DD.json`:

```json
{
  "date": "2026-02-04",
  "readings": [
    {
      "timestamp": "2026-02-04T19:20:24.264895",
      "temperature_c": 26.89,
      "pressure_hpa": 1003.1,
      "humidity_pct": 19.47,
      "light_lux": 0,
      "noise_low": null,
      "noise_mid": null,
      "noise_high": null,
      "noise_amp": null
    }
  ]
}
```

## LCD Display

The color LCD shows:

- **Top row:** "EnviroPi" title + current time
- **Temperature:** Large °F display with °C in parentheses (red)
- **Humidity:** % RH (blue)
- **Pressure:** inHg with hPa in parentheses (green) - aviation-friendly!
- **Light:** lux value (yellow)

Updates every 5 seconds with current sensor data.

## Email Reports

Daily HTML email reports include:

- Total number of readings collected
- Temperature statistics (avg/min/max)
- Humidity statistics (avg/min/max)
- Pressure statistics (avg/min/max)
- Light level statistics (avg/peak)
- Professional formatting with color-coded sections

## Files

- `enviroplus_logger.py` - Main data collection script
- `display_readings.py` - LCD display service
- `send_daily_report.sh` - Email report generator
- `test_enviroplus.py` - Sensor diagnostic script
- `enviropi-display.service` - systemd service file

## Troubleshooting

### BME280 sensor returns wrong humidity (78% or similar)

The BME280 needs a "warm-up" reading. The logger discards the first reading and uses the second one. If you see consistently wrong data, check that the HAT is firmly seated on all GPIO pins.

### LCD display not working

1. Verify SPI is enabled: `ls /dev/spi*`
2. Check service status: `sudo systemctl status enviropi-display.service`
3. View logs: `tail -f ~/display.log`

### No I2C devices detected

1. Verify I2C is enabled: `ls /dev/i2c-*`
2. Scan for devices: `sudo i2cdetect -y 1`
3. Check physical HAT connection

## Project Timeline

Built in **~3 hours** from scratch:

- Pi setup and SSH access: 10 min
- Sensor discovery and testing: 30 min
- Data logger development: 20 min
- LCD display implementation: 30 min
- Email reporting system: 20 min
- Bug fixes and polish: 70 min

## License

MIT License - feel free to use, modify, and share!

## Acknowledgments

- [Pimoroni](https://pimoroni.com/) for the excellent Enviro+ HAT
- Built with Python 3.13 on Raspberry Pi OS

## Author

Created by Larry Openclaw 🤖

---

**Want to see it in action?** Check out the [STATUS.md](STATUS.md) file for detailed project notes and current readings!
