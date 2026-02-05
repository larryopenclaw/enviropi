# EnviroPi Connection Notes

## Network Discovery - 2026-02-04 16:41 CST

### Status
- ✅ Pi is on the network
- ✅ Hostname resolving correctly
- ❌ SSH not enabled/running yet

### Network Details
- **Hostname:** enviropi.local
- **IPv4:** 192.168.2.15
- **IPv6:** fe80:c::da3a:ddff:fee0:4c8a
- **SSH Port:** 22 (connection refused)

### Hardware
- Raspberry Pi Zero 2 W
- Pimoroni Enviro HAT
- Connected via USB hub
- Fresh 64-bit Raspberry Pi OS flash

### Credentials
- **Username:** enviropi
- **Password:** enviropipw

## Next Steps
1. Enable SSH on the Pi (see options in WhatsApp message)
2. Once SSH is up, connect and explore
3. Install Pimoroni libraries
4. Start sensor testing

## Commands to Try Once SSH is Up
```bash
# Test connection
ssh enviropi@enviropi.local

# Check OS version
cat /etc/os-release

# Check Python version
python3 --version

# Install Pimoroni libraries
sudo apt update
sudo apt install -y python3-pip python3-numpy
sudo pip3 install pimoroni-bme280
sudo pip3 install envirophat

# Test sensors
python3 -c "from envirophat import light; print(light.light())"
```
