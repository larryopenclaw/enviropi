# EnviroPi TODO

## Immediate (2026-02-04)
- [x] Scan I2C for additional sensors
- [x] Update email recipient to chris.remboldt@gmail.com
- [ ] **Wait until 17:55** - Let cron collect more data points
- [ ] **Test email report** - Run `./send_daily_report.sh`
- [ ] Verify email arrives and looks good

## Next Session
- [ ] Schedule daily email automation (macOS cron or OpenClaw cron)
- [ ] Create comprehensive README.md for GitHub
- [ ] Add hardware photos/diagrams
- [ ] Push to GitHub as public repo: larryopenclaw/enviropi
- [ ] Add LICENSE file (MIT?)
- [ ] Consider adding setup script for easy deployment

## Future Enhancements
- [ ] Add graphing to email report (matplotlib?)
- [ ] Web dashboard (optional)
- [ ] Alert if temperature/pressure out of normal range
- [ ] Compare outdoor weather API data with indoor readings
- [ ] Multiple Pi setup (different rooms)

## Notes
- Current setup: Pi Zero 2 W + BMP280 (temp/pressure) + BH1750 (light)
- Missing sensors from some Enviro pHAT docs: LSM303D, ADS1015 (not present on this board)
- Data logging: Every 5 minutes via cron
- Data retention: 7 days of JSON logs
