# MójDomek Septic Tank Monitor

Monitor your septic tank levels with MójDomek.eu sensors directly in Home Assistant.

## Features

- Real-time tank level monitoring (percentage and centimeters)
- Temperature tracking
- Battery level and voltage monitoring
- Signal strength (RSSI)
- Predicted tank full date
- Last emptied date tracking
- Automatic device discovery for all your locations

## Configuration

You'll need your MójDomek API ID, which you can find in your API URL:
`https://mojdomek.eu/api/api2.php?id=YOUR_ID`

Simply enter this ID during setup, and the integration will automatically discover all your tank sensors.

## What You'll Get

For each tank location, you'll receive 9 sensors providing comprehensive monitoring:
- Tank fill level (% and cm)
- Temperature
- Battery status (voltage and %)
- Signal strength
- Predictive analytics (when will the tank be full)
- Historical data (last emptied)

Perfect for peace of mind and proactive maintenance!
