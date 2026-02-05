# EnviroPi - Environmental Monitoring with Pimoroni Enviro Hat

## Hardware
- **Device:** Raspberry Pi Zero 2 W
- **Sensor:** Pimoroni Enviro HAT
- **Credentials:** enviropi / enviropipw

## Sensors (Enviro HAT)
The Pimoroni Enviro HAT includes:
- **BMP280** - Temperature & Barometric Pressure
- **TCS3472** - RGB Color & Light sensor
- **LSM303D** - Magnetometer & Accelerometer
- **ADS1015** - Analog inputs (for additional sensors)
- **2x LEDs** - Programmable RGB LEDs

## Project Plan

### Phase 1: Connection & Discovery
- [x] Project setup
- [x] Found Pi on network (192.168.2.15 / enviropi.local)
- [x] Enable SSH on Pi
- [x] Connect to Pi via SSH
- [x] Install required Python libraries
- [x] I2C enabled & sensors detected
- [ ] Fix physical HAT connection (I/O errors)
- [ ] Test sensor readings

### Phase 2: Data Collection Script
- [ ] Python script to read all sensors
- [ ] Format data as JSON
- [ ] Store daily logs locally on Pi
- [ ] Rotate logs (keep last 7 days)

### Phase 3: Email Reports
- [ ] SSH into Pi from macOS
- [ ] Pull latest sensor logs
- [ ] Generate formatted email with charts/graphs
- [ ] Send via Gmail (larryopenclaw@gmail.com)
- [ ] Schedule daily via cron

### Phase 4: GitHub Publishing
- [ ] Clean up code
- [ ] Add documentation
- [ ] Create public repo: larry-openclaw/enviropi
- [ ] Push to GitHub
- [ ] Add README with setup instructions

## Tech Stack
- **Pi:** Python 3 + Pimoroni libraries
- **macOS:** Shell scripts + Python for email formatting
- **Email:** gog CLI (Google Workspace)
- **Repository:** GitHub (public)

## Cool Ideas
- Temperature/humidity trends over time
- Barometric pressure weather prediction
- Light level detection (daylight tracking)
- Color sensor for ambient light temperature
- Motion detection via accelerometer
- Historical data visualization
- Alerts for extreme conditions
