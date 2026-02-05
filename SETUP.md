# EnviroPi Setup Log

## 2026-02-04 17:05 CST - Initial Connection

### Connection Established ✅
- **IP:** 192.168.2.15
- **Hostname:** enviropi
- **OS:** Debian Linux 6.12.47+rpt-rpi-v8 (aarch64)
- **Python:** 3.13.5
- **Authentication:** SSH key-based (password: enviropipw)

### Setup Steps

1. **Enabled SSH**
   - Created empty `/boot/ssh` file on SD card
   - Pi auto-enabled SSH on first boot

2. **SSH Key Setup**
   - Generated RSA key on macOS
   - Copied to Pi using sshpass
   - Password-less authentication now working

3. **Installing Base Packages** (in progress)
   ```bash
   sudo apt update
   sudo apt install -y i2c-tools python3-pip python3-numpy python3-smbus
   ```

### Setup Progress (2026-02-04 17:10 CST)

4. **Enabled I2C Interface** ✅
   - I2C was disabled by default
   - Enabled via `raspi-config nonint do_i2c 0`
   - Rebooting to apply changes

5. **Found Pimoroni Documentation** ✅
   - Official installer: `curl -sS https://get.pimoroni.com/envirophat | bash`
   - GitHub repo: https://github.com/pimoroni/enviroplus-python
   - Pinout reference: https://pinout.xyz/pinout/enviro_phat

### Next Steps
- [ ] Scan I2C bus after reboot (should see devices now)
- [ ] Install Pimoroni Enviro pHAT library
- [ ] Test sensor readings
- [ ] Build data collection script
- [ ] Set up daily email reports

### Hardware Detection
- I2C bus detected: `/sys/bus/i2c/devices/i2c-2`
- Need to scan for connected sensors once i2c-tools installed

### Enviro HAT Expected Sensors
- BMP280: Temperature & Pressure (I2C address 0x76 or 0x77)
- TCS3472: Light/Color sensor (I2C address 0x29)
- LSM303D: Magnetometer/Accelerometer (I2C address 0x1d or 0x1e)
- ADS1015: Analog-to-Digital Converter (I2C address 0x48)
