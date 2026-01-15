# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-01-15

### Added
- Initial release of MójDomek Home Assistant integration
- Support for multiple tank locations per account
- Real-time monitoring of tank levels (percentage and centimeters)
- Temperature sensor
- Battery monitoring (voltage and percentage)
- Signal strength (RSSI) monitoring
- Predicted tank full date
- Last emptied timestamp tracking
- Configuration flow for easy setup via UI
- English and Polish translations
- Comprehensive device information
- Extra state attributes for enhanced automation
- HACS compatibility

### Features
- 9 sensors per location:
  - Tank Level (%)
  - Tank Level (cm)
  - Temperature
  - Battery Voltage
  - Battery Level (%)
  - Signal Strength
  - Predicted Full Date
  - Last Emptied
  - Last Update
- Auto-discovery of all account locations
- 5-minute polling interval
- Device grouping by location
- Rich metadata attributes
