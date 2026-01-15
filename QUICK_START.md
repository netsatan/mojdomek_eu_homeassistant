# Quick Start Guide

## Installation (5 minutes)

### Step 1: Copy Files
```bash
# Copy the integration to your Home Assistant
cp -r custom_components/mojdomek /config/custom_components/
```

### Step 2: Restart Home Assistant
- Settings → System → Restart

### Step 3: Add Integration
1. Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "MójDomek"
4. Enter your API ID (e.g., `YOUR_ID`)
5. Click Submit

## Your API ID

Find it in your MójDomek API URL:
```
https://mojdomek.eu/api/api2.php?id=YOUR_ID
                                    ^^^^^^^^
                                    This is your API ID
```

## What You Get

**9 sensors per tank location:**
- 📊 Tank Level (%) - with alarm thresholds
- 📏 Tank Level (cm) - actual measurement
- 🌡️ Temperature
- 🔋 Battery Voltage
- 🔋 Battery Level (%)
- 📶 Signal Strength (RSSI)
- 📅 Predicted Full Date
- 🗓️ Last Emptied Date
- 🕐 Last Update Time

## Quick Dashboard

Add this to your dashboard for instant monitoring:

```yaml
type: gauge
entity: sensor.YOUR_LOCATION_tank_level
name: Septic Tank
min: 0
max: 100
severity:
  green: 0
  yellow: 70
  red: 85
```

Replace `YOUR_LOCATION` with your actual sensor name.

## Sample Automation

Alert when tank is 80% full:

```yaml
automation:
  - alias: "Tank Almost Full"
    trigger:
      platform: numeric_state
      entity_id: sensor.YOUR_LOCATION_tank_level
      above: 80
    action:
      service: notify.mobile_app
      data:
        message: "Septic tank is {{ states('sensor.YOUR_LOCATION_tank_level') }}% full!"
```

## Troubleshooting

**Integration not found?**
- Verify folder: `/config/custom_components/mojdomek/`
- Check manifest.json exists
- Full restart required (not reload)

**Invalid API ID?**
- Test it: `curl "https://mojdomek.eu/api/api2.php?id=YOUR_ID"`
- Should return `"active": true`

**No sensors?**
- Check logs: Settings → System → Logs
- Filter for "mojdomek"

## Support

- 📖 Full docs: See README.md
- 🐛 Issues: Check home-assistant.log
- 📝 Examples: See DASHBOARD_EXAMPLE.yaml
