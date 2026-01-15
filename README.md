# MójDomek Home Assistant Integration

Home Assistant custom integration for monitoring MójDomek.eu septic tank level sensors.

## Features

This integration provides real-time monitoring of your septic tank through the following sensors:

- **Tank Level (%)** - Current fill level as percentage
- **Tank Level (cm)** - Current fill level in centimeters
- **Temperature** - Current temperature reading
- **Battery Voltage** - Sensor battery voltage
- **Battery Level (%)** - Sensor battery percentage
- **Signal Strength** - RSSI signal strength
- **Predicted Full Date** - Estimated date when tank will be full
- **Last Emptied** - Timestamp of last tank emptying
- **Last Update** - Timestamp of last sensor reading

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL and select "Integration" as the category
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/mojdomek` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

### Finding Your API ID

Your API ID is the unique identifier in your MójDomek API URL. For example:
```
https://mojdomek.eu/api/api2.php?id=YOUR_ID
```
In this case, your API ID is `YOUR_ID`.

### Setup via UI

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "MójDomek"
4. Enter your API ID
5. Click Submit

The integration will automatically discover all locations associated with your account and create sensors for each.

## Sensors Created

For each location (tank sensor), the integration creates the following entities:

| Sensor | Unit | Device Class | Description |
|--------|------|--------------|-------------|
| Tank Level | % | Battery | Current fill percentage |
| Tank Level (cm) | cm | Distance | Current fill level in centimeters |
| Temperature | °C | Temperature | Ambient temperature |
| Battery Voltage | V | Voltage | Sensor battery voltage |
| Battery Level | % | Battery | Sensor battery percentage |
| Signal Strength | % | - | RSSI signal quality |
| Predicted Full Date | - | Timestamp | When tank is predicted to be full |
| Last Emptied | - | Timestamp | Last emptying date |
| Last Update | - | Timestamp | Last sensor update time |

## Device Information

Each sensor device includes:
- Location name
- Manufacturer: MójDomek.eu
- Model: Hardware board version (e.g., SZ04-002)
- Software version
- Location address

## Additional Attributes

Each sensor provides extra attributes:
- `location_id` - Unique location identifier
- `max_capacity` - Maximum tank capacity in cm
- `alarm_level` - Alarm threshold level
- `direction` - Fill direction (growth/reduction)
- `tank_type` - Type of tank
- `address` - Physical address
- `town` - Town/city

## Automation Examples

### Alert When Tank Is Nearly Full

```yaml
automation:
  - alias: "Septic Tank Nearly Full Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.czujnik_rzeszotary_tank_level
        above: 80
    action:
      - service: notify.mobile_app
        data:
          title: "Septic Tank Alert"
          message: "Tank is {{ states('sensor.czujnik_rzeszotary_tank_level') }}% full"
```

### Low Battery Warning

```yaml
automation:
  - alias: "Tank Sensor Low Battery"
    trigger:
      - platform: numeric_state
        entity_id: sensor.czujnik_rzeszotary_battery_level
        below: 20
    action:
      - service: notify.mobile_app
        data:
          title: "Sensor Battery Low"
          message: "Tank sensor battery at {{ states('sensor.czujnik_rzeszotary_battery_level') }}%"
```

## API Details

This integration polls the MójDomek API every 5 minutes (300 seconds) by default. The API endpoint used is:

```
https://mojdomek.eu/api/api2.php?id=YOUR_API_ID
```

No authentication beyond the API ID is required.

## Support

For issues, feature requests, or contributions, please visit the [GitHub repository](https://github.com/yourusername/mojdomek-homeassistant).

## License

This integration is provided as-is without any warranty. Use at your own risk.
